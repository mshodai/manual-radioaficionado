"""Genera las figuras SVG del capítulo 03 (dibujo propio).

Datos: niveles de referencia de campo eléctrico del anexo II del
Real Decreto 1066/2001 (BOE-A-2001-18256), cuadro 2.

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras03.py docs/assets/figuras
"""
import math, sys, os

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"
GRID = "#d0d0d0"
BAND = "#c62828"


def svg(w, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{title}</title>
<rect width="100%" height="100%" rx="8" fill="#ffffff"/>
<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif">
{body}
</g>
</svg>
'''


def T(x, y, s, size=13, anchor="middle", color=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{color}" stroke="none" {extra}>{s}</text>')


def e_ref(f_mhz):
    """Nivel de referencia de E (V/m) para el público, f en MHz."""
    if f_mhz < 1:
        return 87.0
    if f_mhz < 10:
        return 87.0 / math.sqrt(f_mhz)
    if f_mhz < 400:
        return 28.0
    if f_mhz < 2000:
        return 1.375 * math.sqrt(f_mhz)
    return 61.0


def niveles():
    W, H = 640, 340
    x0, x1, y0, y1 = 70, 610, 290, 40          # área del gráfico
    fmin, fmax = 0.15, 10000.0                  # MHz
    emin, emax = 0.0, 100.0                     # V/m

    def X(f):
        return x0 + (math.log10(f) - math.log10(fmin)) / (math.log10(fmax) - math.log10(fmin)) * (x1 - x0)

    def Y(e):
        return y0 - (e - emin) / (emax - emin) * (y0 - y1)

    b = []
    # rejilla y ejes
    for e in range(0, 101, 20):
        b.append(f'<line x1="{x0}" y1="{Y(e):.1f}" x2="{x1}" y2="{Y(e):.1f}" stroke="{GRID}" stroke-width="1"/>')
        b.append(T(x0 - 8, Y(e) + 4, str(e), 12, "end"))
    for f, lab in [(1, "1 MHz"), (10, "10 MHz"), (100, "100 MHz"), (1000, "1 GHz"), (10000, "10 GHz")]:
        b.append(f'<line x1="{X(f):.1f}" y1="{y0}" x2="{X(f):.1f}" y2="{y1}" stroke="{GRID}" stroke-width="1"/>')
        b.append(T(X(f), y0 + 18, lab, 12))
    b.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}"/>')
    b.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}"/>')
    b.append(T(22, (y0 + y1) / 2, "E (V/m)", 13, "middle", INK, f'transform="rotate(-90 22 {(y0 + y1) / 2})"'))
    b.append(T((x0 + x1) / 2, y0 + 40, "Frecuencia (escala logarítmica)", 13))

    # curva
    pts = []
    n = 400
    for i in range(n + 1):
        f = 10 ** (math.log10(fmin) + i / n * (math.log10(fmax) - math.log10(fmin)))
        pts.append(f"{X(f):.1f},{Y(e_ref(f)):.1f}")
    b.append(f'<polyline points="{" ".join(pts)}" stroke="{ACC}" stroke-width="3"/>')

    # tramo de 28 V/m
    b.append(T(X(63), Y(28) - 10, "28 V/m (10–400 MHz)", 12, "middle", ACC, 'font-weight="600"'))
    b.append(T(X(4500), Y(61) - 10, "61 V/m", 12, "middle", ACC, 'font-weight="600"'))
    b.append(T(X(0.4), Y(87) - 10, "87 V/m", 12, "middle", ACC, 'font-weight="600"'))

    # algunas bandas de aficionado
    for f, lab in [(3.6, "80 m"), (7.1, "40 m"), (14.2, "20 m"), (50, "6 m"), (145, "2 m"), (435, "70 cm"), (1296, "23 cm")]:
        e = e_ref(f)
        b.append(f'<circle cx="{X(f):.1f}" cy="{Y(e):.1f}" r="4.5" fill="{BAND}" stroke="none"/>')
        if f < 10:      # en el tramo descendente, la etiqueta a la izquierda
            b.append(T(X(f) - 9, Y(e) + 4, lab, 11, "end", BAND))
        else:
            b.append(T(X(f), Y(e) + 18, lab, 11, "middle", BAND))

    title = ("Niveles de referencia del campo eléctrico para el público según el anexo II del "
             "Real Decreto 1066/2001, entre 150 kHz y 10 GHz: 87 V/m hasta 1 MHz, bajan hasta 28 V/m "
             "entre 10 y 400 MHz, suben de nuevo y quedan en 61 V/m por encima de 2 GHz. "
             "Se marcan las bandas de 80 m, 40 m, 20 m, 6 m, 2 m, 70 cm y 23 cm.")
    return svg(W, H, "\n".join(b), title)


os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "03-niveles-referencia.svg"), "w", encoding="utf-8") as fh:
    fh.write(niveles())
print("Figuras del capítulo 03 generadas en", OUT)
