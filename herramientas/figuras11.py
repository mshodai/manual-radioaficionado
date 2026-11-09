"""Genera las figuras SVG del capítulo 11 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras11.py docs/assets/figuras

Figuras:
- 11-paris.svg: temporización de la palabra PARIS, unidad a unidad (50 en total).
- 11-farnsworth.svg: PARIS a 10 ppm normal y a 10 ppm con caracteres a 20 ppm
  (Farnsworth); las dos ocupan los mismos 6 s.
- 11-yambico.svg: manipulador yámbico con las dos palas apretadas; salida en
  modo A y en modo B.
- 11-clics.svg: envolvente de un punto con flancos instantáneos y con flancos
  de 5 ms, y la envolvente de su espectro (modelo de calculos11.py).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from morse11 import eventos, farnsworth, t_punto  # noqa: E402

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul: señal / lo deseado
ALT = "#c62828"   # rojo: lo no deseado
VERDE = "#2e7d32"
GRIS = "#9e9e9e"
CLARO = "#e0e0e0"
NARANJA = "#e65100"
FONDO = "#fff3e0"


def svg(w, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{title}</title>
<rect width="100%" height="100%" rx="8" fill="#ffffff"/>
<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif">
{body}
</g>
</svg>
'''


def L(x1, y1, x2, y2, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {extra}/>'


def T(x, y, s, size=14, anchor="middle", extra="", fill=INK):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" stroke="none" {extra}>{s}</text>'


def poly(pts, extra=""):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{d}" {extra}/>'


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>'


def guarda(nombre, w, h, cuerpo, titulo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, "\n".join(cuerpo), titulo))


def coma(x, dec=0):
    return f"{x:.{dec}f}".replace(".", ",")


def llave(x1, x2, y, texto, color=INK, size=12, xt=None, anchor="middle"):
    """Corchete horizontal bajo un tramo, con su rótulo."""
    return [
        L(x1, y, x1, y + 6, f'stroke="{color}" stroke-width="1.5"'),
        L(x2, y, x2, y + 6, f'stroke="{color}" stroke-width="1.5"'),
        L(x1, y + 6, x2, y + 6, f'stroke="{color}" stroke-width="1.5"'),
        T((x1 + x2) / 2 if xt is None else xt, y + 22, texto, size, anchor, fill=color),
    ]


# ---------- Figura 11.1: temporización de PARIS ----------
b = []
X0, U = 40, 14.4           # 50 unidades → 720 px
YB, H = 110, 34            # base y altura de la señal
ev = eventos("PARIS")
# rejilla de unidades
for k in range(51):
    grueso = k % 5 == 0
    b.append(L(X0 + k * U, YB + 2, X0 + k * U, YB + (10 if grueso else 6), f'stroke="{GRIS}" stroke-width="1"'))
    if k % 10 == 0:
        b.append(T(X0 + k * U, YB + 24, f"{k}", 11, fill=GRIS))
b.append(L(X0, YB, X0 + 50 * U, YB, f'stroke="{CLARO}" stroke-width="1"'))
# señal y espacios
x = X0
pts = [(x, YB)]
letras = "PARIS"
inicio_letra = [X0]
for on, u, tipo in ev:
    if on:
        pts += [(x, YB), (x, YB - H), (x + u * U, YB - H), (x + u * U, YB)]
    else:
        if tipo == "e":
            b.append(rect(x, YB - H, u * U, H, FONDO, 'stroke="none"'))
            inicio_letra.append(x + u * U)
    x += u * U
pts.append((x, YB))
b.append(poly(pts, f'stroke="{ACC}" stroke-width="2.5"'))
# rótulos de letras y espacios
xs = X0
li = 0
cur = X0
for on, u, tipo in ev:
    if tipo == "e":
        b.append(T((xs + cur) / 2, YB - H - 12, letras[li], 16, extra='font-weight="600"'))
        b.append(T(cur + u * U / 2, YB - H / 2 + 4, f"{u}", 12, fill=NARANJA))
        li += 1
        xs = cur + u * U
    cur += u * U
b += llave(X0, X0 + U, YB + 32, "punto: 1 unidad", ACC, xt=X0, anchor="start")
xr = X0 + 16 * U         # raya de la A
b += llave(xr, xr + 3 * U, YB + 32, "raya: 3 unidades", ACC, xt=xr, anchor="start")
b.append(T(X0, YB + 82, "Espacios: 1 unidad dentro de una letra · 3 entre letras · 7 entre palabras.", 12, "start"))
b.append(T(X0, YB + 100, "PARIS ocupa 31 unidades de señal y espacios internos + 19 de espacios entre letras y palabra = 50.", 12, "start"))
b.append(T(400, 28, "Temporización de la palabra PARIS (cada marca es una unidad)", 15, extra='font-weight="600"'))
guarda("11-paris.svg", 800, 230, b,
       "Temporización de la palabra PARIS en Morse: puntos de una unidad, rayas de tres, espacios de una, tres y siete unidades; cincuenta unidades en total")

# ---------- Figura 11.2: Farnsworth ----------
b = []
X0, ANCHO = 40, 720
SEG = 6.0                   # PARIS a 10 ppm dura 6 s
esc = ANCHO / SEG


def tira(y, unidad_car, unidad_esp, color, titulo):
    out = [T(X0, y - 44, titulo, 13, "start", extra='font-weight="600"')]
    x = X0
    pts = [(x, y)]
    for on, u, tipo in eventos("PARIS"):
        d = u * (unidad_car if tipo == "c" else unidad_esp) * esc
        if on:
            pts += [(x, y), (x, y - 26), (x + d, y - 26), (x + d, y)]
        elif tipo == "e":
            out.append(rect(x, y - 26, d, 26, FONDO, 'stroke="none"'))
        x += d
    pts.append((x, y))
    out.append(poly(pts, f'stroke="{color}" stroke-width="2"'))
    return out


b += tira(100, t_punto(10), t_punto(10), ACC, "10 ppm normales: punto de 120 ms y espacio entre letras de 360 ms")
b += tira(200, t_punto(20), farnsworth(20, 10), VERDE,
          f"Farnsworth 20/10: punto de 60 ms y espacio entre letras de {coma(3 * farnsworth(20, 10) * 1000)} ms")
for s in range(7):
    xx = X0 + s * esc
    b.append(L(xx, 222, xx, 228, f'stroke="{GRIS}" stroke-width="1"'))
    b.append(T(xx, 244, f"{s} s", 11, fill=GRIS))
b.append(L(X0, 225, X0 + ANCHO, 225, f'stroke="{GRIS}" stroke-width="1"'))
b.append(T(400, 28, "La misma palabra, la misma velocidad media: cambia dónde está el tiempo", 15, extra='font-weight="600"'))
guarda("11-farnsworth.svg", 800, 262, b,
       "Comparación de PARIS a 10 palabras por minuto con temporización normal y con caracteres a 20 palabras por minuto y espacios alargados; ambas duran seis segundos")

# ---------- Figura 11.3: modos yámbicos A y B ----------
b = []
X0, U = 150, 40           # unidad = 40 px
filas = {"pala de raya": 80, "pala de punto": 140, "salida en modo A": 220, "salida en modo B": 290}
for nombre, y in filas.items():
    b.append(T(X0 - 12, y - 8, nombre, 13, "end"))
    b.append(L(X0, y, X0 + 15 * U, y, f'stroke="{CLARO}" stroke-width="1"'))


def nivel(y, tramos, color, alto=24):
    pts = [(X0, y)]
    for a, z in tramos:
        pts += [(X0 + a * U, y), (X0 + a * U, y - alto), (X0 + z * U, y - alto), (X0 + z * U, y)]
    pts.append((X0 + 15 * U, y))
    return poly(pts, f'stroke="{color}" stroke-width="2.5"')


# palas: raya pulsada en 0, punto en 1; se sueltan las dos en 4,6 (durante el punto)
SUELTA = 4.6
b.append(nivel(filas["pala de raya"], [(0, SUELTA)], GRIS))
b.append(nivel(filas["pala de punto"], [(1, SUELTA)], GRIS))
b.append(L(X0 + SUELTA * U, 50, X0 + SUELTA * U, 300, f'stroke="{ALT}" stroke-width="1.5" stroke-dasharray="5 4"'))
b.append(T(X0 + SUELTA * U + 6, 52, "sueltas las dos palas", 12, "start", fill=ALT))
# modo A: raya (0-3), espacio, punto (4-5) → N
b.append(nivel(filas["salida en modo A"], [(0, 3), (4, 5)], ACC))
b.append(T(X0 + 6 * U, filas["salida en modo A"] - 8, "− ·  = N", 14, "start", fill=ACC, extra='font-weight="600"'))
# modo B: añade una raya más (6-9) → K
b.append(nivel(filas["salida en modo B"], [(0, 3), (4, 5), (6, 9)], VERDE))
b.append(T(X0 + 10 * U, filas["salida en modo B"] - 8, "− · −  = K", 14, "start", fill=VERDE, extra='font-weight="600"'))
b.append(T(X0 + 7.5 * U, filas["salida en modo B"] + 26, "el modo B termina el elemento en curso y añade el contrario", 12, fill=VERDE))
b.append(T(400, 28, "Manipulador yámbico con las dos palas apretadas", 15, extra='font-weight="600"'))
guarda("11-yambico.svg", 800, 340, b,
       "Cronograma de un manipulador yámbico: al soltar las dos palas durante un punto, el modo A acaba en ese punto y el modo B añade una raya más")

# ---------- Figura 11.4: clics de manipulación ----------
b = []
TP = t_punto(20)          # 60 ms


def envolvente(t, tr):
    if t < 0 or t > TP:
        return 0.0
    if tr == 0:
        return 1.0
    if t < tr:
        return 0.5 - 0.5 * math.cos(math.pi * t / tr)
    if t > TP - tr:
        return 0.5 - 0.5 * math.cos(math.pi * (TP - t) / tr)
    return 1.0


def espectro_db(f, tr):
    a = 1 / (math.pi * f * (TP - tr))
    if tr > 0:
        a /= abs(1 - (2 * f * tr) ** 2)
    return max(-120, 20 * math.log10(a))


# panel izquierdo: envolventes en el tiempo (−10 a 70 ms)
PX0, PX1, PY0 = 60, 330, 150
tx = lambda t: PX0 + (t + 0.01) / 0.08 * (PX1 - PX0)  # noqa: E731
for tr, color, dy, nombre in [(0, ALT, 0, "flancos instantáneos"), (0.005, VERDE, 110, "flancos de 5 ms")]:
    y0 = PY0 + dy
    pts = [(tx(-0.01 + k * 0.08 / 400), y0 - 70 * envolvente(-0.01 + k * 0.08 / 400, tr)) for k in range(401)]
    b.append(L(PX0, y0, PX1, y0, f'stroke="{CLARO}" stroke-width="1"'))
    b.append(poly(pts, f'stroke="{color}" stroke-width="2.5"'))
    b.append(T(PX0, y0 - 80, nombre, 13, "start", fill=color, extra='font-weight="600"'))
for t in (0, 0.03, 0.06):
    b.append(T(tx(t), PY0 + 128, f"{int(t * 1000)} ms", 11, fill=GRIS))
b.append(T((PX0 + PX1) / 2, 50, "Envolvente de un punto a 20 ppm", 14, extra='font-weight="600"'))
# panel derecho: espectro (0 a 3 kHz a cada lado, solo el lado superior)
SX0, SX1, SY0, SYT = 430, 770, 280, 80
fx = lambda f: SX0 + f / 3000 * (SX1 - SX0)  # noqa: E731
dy_ = lambda d: SYT + (-d) / 120 * (SY0 - SYT)  # noqa: E731
for d in range(0, -121, -20):
    b.append(L(SX0, dy_(d), SX1, dy_(d), f'stroke="{CLARO}" stroke-width="1"'))
    b.append(T(SX0 - 6, dy_(d) + 4, f"{d}".replace("-", "−"), 11, "end"))
for f in range(0, 3001, 1000):
    b.append(T(fx(f), SY0 + 18, f"{f // 1000}", 11))
b.append(T((SX0 + SX1) / 2, SY0 + 36, "separación respecto a la portadora (kHz)", 12))
b.append(T(SX0 - 40, (SY0 + SYT) / 2, "dB", 12, extra=f'transform="rotate(-90 {SX0 - 40} {(SY0 + SYT) / 2})"'))
for tr, color in [(0, ALT), (0.005, VERDE)]:
    f_ini = 50 if tr == 0 else 400   # la fórmula de la envolvente solo vale lejos de 1/(2·tr)
    pts = [(fx(f), dy_(espectro_db(f, tr))) for f in range(f_ini, 3001, 10)]
    b.append(poly(pts, f'stroke="{color}" stroke-width="2.5"'))
b.append(T(fx(1500), dy_(-44), "flancos instantáneos", 12, fill=ALT))
b.append(T(fx(1500), dy_(-100), "flancos de 5 ms", 12, fill=VERDE))
b.append(T((SX0 + SX1) / 2, 50, "Envolvente del espectro (modelo)", 14, extra='font-weight="600"'))
b.append(L(380, 60, 380, 300, f'stroke="{CLARO}" stroke-width="1"'))
guarda("11-clics.svg", 800, 330, b,
       "Un punto de CW con flancos instantáneos y con flancos suavizados de 5 ms, y la envolvente de su espectro: con flancos suaves la energía cae mucho más deprisa al alejarse de la portadora")
print("Figuras del capítulo 11 generadas en", OUT)
