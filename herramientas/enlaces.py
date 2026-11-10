"""Comprueba los enlaces del sitio compilado: internos, anclas y externos.

Uso, desde la raíz del repositorio, con una copia del sitio ya compilada
(ver ESTILO.md, §9 y §14):

    python3 herramientas/enlaces.py /tmp/manual-build/site
    python3 herramientas/enlaces.py /tmp/manual-build/site --sin-externos

Recorre todas las páginas HTML del sitio y comprueba:

- Enlaces internos (href y src): que el archivo de destino existe y, si llevan
  ancla (#…), que la página de destino tiene un elemento con ese id.
- Enlaces externos (http y https): una petición HEAD con un tiempo de espera
  corto; si el servidor no admite HEAD, un GET que solo pide el primer byte.
  Las redirecciones no se siguen solas: se anotan y se sigue la cadena a mano
  para dar el destino final. Las anclas de las páginas externas no se
  comprueban, porque obligaría a descargarlas enteras.

Los resultados externos se clasifican así:

- Rotos: el servidor responde 4xx (también al final de una redirección) o el
  nombre no se resuelve o rechaza la conexión.
- Dudosos: tiempo agotado, error de certificado o 5xx que persiste tras un
  reintento. Suelen ser problemas pasajeros del servidor o del almacén de
  certificados de este Python; ábrelos en el navegador antes de tocarlos.
- Redirigidos: responden, pero en otra dirección; conviene actualizar el enlace.
- Excepciones conocidas: los de la lista EXCEPCIONES, que fallan aquí por un
  motivo ya revisado pero funcionan en el navegador. Se informan aparte, con su
  motivo y el resultado de esta pasada, y no cuentan como error.

No corrige nada: imprime cada grupo con las páginas del manual en que aparece
cada enlace, y termina con código 1 si hay algún enlace interno o externo roto.
Solo usa la biblioteca estándar de Python.
"""

import argparse
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

SITE_URL = "https://mshodai.github.io/manual-radioaficionado/"
AGENTE = "manual-radioaficionado-enlaces/1.0 (comprobador de enlaces)"
IGNORAR = ("mailto:", "tel:", "javascript:", "data:")
MAX_SALTOS = 5
POR_SERVIDOR = 2  # peticiones simultáneas como máximo a un mismo servidor

# Enlaces externos revisados a mano que fallan con este script pero funcionan en
# el navegador: {prefijo de la URL: motivo}. Revísala de vez en cuando y quita
# las que ya respondan bien.
EXCEPCIONES = {
    "https://giro.uml.edu/": "su certificado depende de la raíz emSign Root TLS CA - G1, "
    "que no está en el almacén de certificados de Python; los navegadores y curl en macOS la aceptan",
    "https://www.sidc.be/SILSO/": "responde, pero tarda unos 30 s, más que el tiempo de espera",
}


class Analizador(HTMLParser):
    """Recoge los id/name de los elementos y los href/src de la página."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.enlaces = []

    def handle_starttag(self, etiqueta, atributos):
        a = dict(atributos)
        for clave in ("id", "name"):
            if a.get(clave) and (clave == "id" or etiqueta == "a"):
                self.ids.add(a[clave])
        if etiqueta == "link" and a.get("rel") in ("preconnect", "dns-prefetch"):
            return  # indicaciones al navegador, no enlaces
        if etiqueta in ("a", "link") and a.get("href"):
            self.enlaces.append(a["href"])
        elif etiqueta in ("img", "script", "source", "iframe") and a.get("src"):
            self.enlaces.append(a["src"])


def leer_sitio(sitio: Path):
    """Devuelve ({ruta html: ids}, {ruta html: [enlaces]})."""
    ids, enlaces = {}, {}
    for f in sorted(sitio.rglob("*.html")):
        p = Analizador()
        p.feed(f.read_text(encoding="utf-8"))
        ids[f] = p.ids
        enlaces[f] = p.enlaces
    return ids, enlaces


def url_de(sitio: Path, f: Path) -> str:
    """URL ficticia de la página, para resolver los enlaces relativos."""
    rel = f.relative_to(sitio).as_posix()
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "http://sitio.local/" + rel


def destino_local(sitio: Path, url: str):
    """Archivo del sitio al que apunta una URL interna, o None si no existe."""
    ruta = unquote(urlsplit(url).path).lstrip("/")
    candidato = sitio / ruta
    if ruta == "" or ruta.endswith("/"):
        candidato = candidato / "index.html"
    if candidato.is_file():
        return candidato
    if (candidato / "index.html").is_file():
        return candidato / "index.html"
    return None


def nombre(sitio: Path, f: Path) -> str:
    rel = f.relative_to(sitio).as_posix()
    return rel[: -len("/index.html")] if rel.endswith("/index.html") else rel


def comprobar_internos(sitio, ids, enlaces):
    """Devuelve {(página, enlace): motivo} de los enlaces internos rotos y {url externa: {páginas}}."""
    rotos, externos = {}, defaultdict(set)
    for f, lista in enlaces.items():
        base = url_de(sitio, f)
        for href in lista:
            if href.startswith(IGNORAR):
                continue
            # Absolutas al sitio publicado, o con su prefijo (la página 404 las usa así).
            for prefijo in (SITE_URL, urlsplit(SITE_URL).path):
                if href.startswith(prefijo):
                    href = "/" + href[len(prefijo):]
                    break
            absoluta = urljoin(base, href)
            partes = urlsplit(absoluta)
            if partes.netloc != "sitio.local":
                if partes.scheme in ("http", "https"):
                    externos[absoluta].add(nombre(sitio, f))
                continue
            dest = destino_local(sitio, absoluta)
            if dest is None:
                rotos[(nombre(sitio, f), href)] = "no existe el destino"
            elif partes.fragment and unquote(partes.fragment) not in ids.get(dest, set()):
                rotos[(nombre(sitio, f), href)] = f"no existe el ancla en {nombre(sitio, dest)}"
    return rotos, externos


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


ABRIDOR = urllib.request.build_opener(SinRedireccion)
SEMAFOROS = defaultdict(lambda: threading.Semaphore(POR_SERVIDOR))
CERROJO = threading.Lock()


def peticion(url: str, metodo: str, espera: float):
    """Devuelve (código, Location) sin seguir redirecciones."""
    cabeceras = {"User-Agent": AGENTE, "Accept": "*/*"}
    if metodo == "GET":
        cabeceras["Range"] = "bytes=0-0"
    req = urllib.request.Request(url, method=metodo, headers=cabeceras)
    try:
        with ABRIDOR.open(req, timeout=espera) as r:
            return r.status, None
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location")


def comprobar_externo(url: str, espera: float):
    """Devuelve (estado, detalle): 'ok', 'redirigido', 'dudoso' o 'roto'."""
    partes = urlsplit(url)
    actual = urlunsplit(partes._replace(fragment=""))
    cadena = []
    for _ in range(MAX_SALTOS + 1):
        servidor = urlsplit(actual).netloc
        with CERROJO:
            sem = SEMAFOROS[servidor]
        try:
            with sem:
                try:
                    codigo, destino = peticion(actual, "HEAD", espera)
                except TimeoutError:  # algunos servidores tardan solo con HEAD
                    codigo, destino = peticion(actual, "GET", 2 * espera)
                if codigo in (400, 403, 404, 405, 429, 501) or codigo >= 500:
                    codigo, destino = peticion(actual, "GET", espera)
                if codigo >= 500:  # a menudo pasajero: un reintento tras una pausa
                    time.sleep(3)
                    codigo, destino = peticion(actual, "GET", espera)
        except Exception as e:  # tiempo agotado, DNS, TLS…
            motivo = getattr(e, "reason", e)
            pasajero = isinstance(e, TimeoutError) or isinstance(motivo, (TimeoutError, ssl.SSLError))
            detalle = f"{actual}: {type(motivo).__name__}: {motivo}"
            return ("dudoso" if pasajero else "roto"), " → ".join(cadena + [detalle])
        if codigo in (301, 302, 303, 307, 308) and destino:
            cadena.append(f"{codigo} {actual}")
            actual = urljoin(actual, destino)
            continue
        estado = "dudoso" if codigo >= 500 else "roto" if codigo >= 400 else None
        if cadena:
            return estado or "redirigido", " → ".join(cadena + [f"{actual} ({codigo})"])
        return estado or "ok", f"HTTP {codigo}"
    return "roto", " → ".join(cadena + ["demasiadas redirecciones"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sitio", type=Path, help="carpeta del sitio compilado")
    ap.add_argument("--sin-externos", action="store_true", help="comprueba solo los enlaces internos")
    ap.add_argument("--espera", type=float, default=8.0, help="tiempo de espera por petición, en s (8)")
    ap.add_argument("--hilos", type=int, default=8, help="peticiones externas simultáneas (8)")
    args = ap.parse_args()

    if not (args.sitio / "index.html").is_file():
        sys.exit(f"{args.sitio} no parece un sitio compilado (falta index.html)")

    ids, enlaces = leer_sitio(args.sitio)
    rotos, externos = comprobar_internos(args.sitio, ids, enlaces)
    total = sum(len(v) for v in enlaces.values())
    print(f"{len(enlaces)} páginas, {total} enlaces, {len(externos)} URL externas distintas.\n")

    print(f"== Internos rotos: {len(rotos)}")
    for (pagina, href), motivo in sorted(rotos.items()):
        print(f"  {pagina}: {href}  ({motivo})")

    hay_rotos = bool(rotos)
    if not args.sin_externos:
        urls = sorted(externos)
        with ThreadPoolExecutor(args.hilos) as ex:
            resultados = dict(zip(urls, ex.map(lambda u: comprobar_externo(u, args.espera), urls)))
        conocidos = {u: (resultados.pop(u), m) for u in urls for p, m in EXCEPCIONES.items() if u.startswith(p)}
        grupos = (
            ("roto", "Externos rotos"),
            ("dudoso", "Externos dudosos (compruébalos en el navegador)"),
            ("redirigido", "Externos redirigidos"),
        )
        for estado, titulo in grupos:
            lista = [(u, d) for u, (e, d) in resultados.items() if e == estado]
            print(f"\n== {titulo}: {len(lista)}")
            for u, detalle in lista:
                print(f"  {u}\n      {detalle}\n      en: {', '.join(sorted(externos[u]))}")
            hay_rotos |= estado == "roto" and bool(lista)
        ok = sum(1 for e, _ in resultados.values() if e == "ok")
        print(f"\n== Externos correctos: {ok}")
        print(f"\n== Excepciones conocidas (no cuentan como error): {len(conocidos)}")
        for u, ((estado, detalle), motivo) in conocidos.items():
            print(f"  {u}\n      motivo: {motivo}\n      esta vez: {estado} ({detalle})")

    sys.exit(1 if hay_rotos else 0)


if __name__ == "__main__":
    main()
