"""Genera el capítulo 17 (Glosario) a partir de herramientas/glosario-entradas.txt.

Uso, desde la raíz del repositorio, con una copia del sitio ya compilada
(ver ESTILO.md, §9 y §12):

    python3 herramientas/glosario.py /tmp/manual-build/site

Lee las anclas reales del sitio compilado, comprueba que todas las entradas
apuntan a un apartado que existe, que no hay términos duplicados y que cada
«Véase **X**» remite a una entrada existente, y escribe docs/17-glosario.md.
Si algo falla, no escribe nada y termina con error.

Formato de cada línea de glosario-entradas.txt (las que empiezan por # y las
vacías se ignoran):

    Término @ página#ancla @ Definición breve.

donde «página» es la ruta de la página sin extensión, relativa a docs/
(04-teoria-radio, 09-reglamentacion/espanol, 15-emergencias para su index.md).
"""

import html
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADAS = RAIZ / "herramientas" / "glosario-entradas.txt"
SALIDA = RAIZ / "docs" / "17-glosario.md"
INDICES = ("09-reglamentacion", "15-emergencias")  # secciones con index.md

INTRO = (
    "Este glosario reúne los términos, las siglas y las abreviaturas que aparecen en el manual, "
    "incluidos los grupos del código Q y las abreviaturas de telegrafía más habituales. Cada entrada "
    "da una definición breve y te lleva al apartado del capítulo donde se explica con detalle: úsalo "
    "para repasar antes del examen o cuando encuentres en la banda una palabra que no recuerdas.\n\n"
    "Las siglas llevan su desarrollo y, si son inglesas, su significado en español. Las expresiones "
    "que tienen sinónimo remiten a la entrada principal con «Véase»."
)


def anclas(sitio: Path) -> dict:
    """Devuelve {'página#ancla': texto del encabezado} de los h1-h3 del sitio compilado."""
    res = {}
    for f in sitio.rglob("index.html"):
        pagina = f.parent.relative_to(sitio).as_posix()
        if pagina == ".":
            continue
        s = f.read_text(encoding="utf-8")
        m = re.search(r"<article.*?</article>", s, re.S)
        for _, ident, texto in re.findall(r'<h([1-3]) id="([^"]+)"[^>]*>(.*?)</h\1>', m.group(0) if m else s, re.S):
            texto = html.unescape(re.sub(r"<[^>]+>", "", texto)).replace("¶", "").strip()
            res[f"{pagina}#{ident}"] = texto
    return res


def clave(s: str) -> str:
    """Clave de orden: minúsculas, sin tildes ni signos."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum() and unicodedata.category(c) != "Mn")


def ruta_md(pagina: str) -> str:
    return pagina + ("/index.md" if pagina in INDICES else ".md")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    sitio = Path(sys.argv[1])
    mapa = anclas(sitio)
    if not mapa:
        print(f"No hay páginas compiladas en {sitio}")
        return 1

    entradas, errores = [], []
    for n, linea in enumerate(ENTRADAS.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip() or linea.startswith("#"):
            continue
        partes = [p.strip() for p in linea.split(" @ ", 2)]
        if len(partes) != 3:
            errores.append(f"línea {n}: formato incorrecto")
            continue
        termino, ancla, definicion = partes
        if ancla not in mapa:
            errores.append(f"línea {n}: ancla inexistente {ancla} ({termino})")
        entradas.append((termino, ancla, definicion))

    claves = [clave(t) for t, _, _ in entradas]
    for k in sorted({k for k in claves if claves.count(k) > 1}):
        errores.append(f"término duplicado: {k}")
    nombres = {t for t, _, _ in entradas}
    for t, _, d in entradas:
        for v in re.findall(r"Véase \*\*(.+?)\*\*", d):
            if v not in nombres:
                errores.append(f"remisión rota: {t} → {v}")
    if errores:
        print("\n".join(errores))
        return 1

    grupos = {}
    for e in sorted(entradas, key=lambda e: clave(e[0])):
        inicial = clave(e[0])[0]
        grupos.setdefault(inicial.upper() if inicial.isalpha() else "0-9", []).append(e)
    orden = sorted(grupos, key=lambda g: (g != "0-9", g))

    def ident(g):
        return "cifras-y-simbolos" if g == "0-9" else g.lower()

    def titulo(g):
        return "Cifras y símbolos" if g == "0-9" else g

    out = ["# Glosario", "", INTRO, ""]
    out.append(" · ".join(f"[{'0–9' if g == '0-9' else g}](#{ident(g)})" for g in orden))
    out.append("")
    for g in orden:
        out += [f"## {titulo(g)}", ""]
        for termino, ancla, definicion in grupos[g]:
            pagina, frag = ancla.split("#")
            cap = int(pagina[:2])
            enlace = f"[Cap. {cap}, «{mapa[ancla]}»]({ruta_md(pagina)}#{frag})"
            out += [f"**{termino}**", f":   {definicion} {enlace}.", ""]
    SALIDA.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")
    print(f"{len(entradas)} entradas en {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
