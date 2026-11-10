"""Genera las figuras SVG del capítulo 12 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras12.py docs/assets/figuras

Figuras:
- 12-dial-audio.svg: frecuencia del dial, tonos de audio y frecuencias emitidas
  en 20 m, sobre los tramos del plan de HF de la IARU Región 1.
- 12-ft8-ciclo.svg: periodos de 15 s de FT8, emisión de 12,64 s y efecto de un
  reloj adelantado.
- 12-dmr-ranuras.svg: dos conversaciones que comparten un canal DMR en ranuras de
  30 ms dentro de tramas de 60 ms (ETSI TS 102 361-1).

Reglas de legibilidad de ESTILO.md: letra de 12 px como mínimo y viewBox de
700 px de ancho como máximo.
"""
import os
import sys

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul
ALT = "#c62828"   # rojo
VERDE = "#2e7d32"
GRIS = "#9e9e9e"
CLARO = "#eeeeee"
NARANJA = "#fff3e0"
AZUL_CLARO = "#e3f2fd"
VERDE_CLARO = "#e8f5e9"


def svg(w, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{title}</title>
<defs>
  <marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
  </marker>
</defs>
<rect width="100%" height="100%" rx="8" fill="#ffffff"/>
<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif">
{body}
</g>
</svg>
'''


def L(x1, y1, x2, y2, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {extra}/>'


def T(x, y, s, size=13, anchor="middle", extra="", fill=INK):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" stroke="none" {extra}>{s}</text>'


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>'


def flecha(x1, y1, x2, y2, extra=""):
    return L(x1, y1, x2, y2, f'marker-end="url(#flecha)" {extra}')


def guarda(nombre, w, h, cuerpo, titulo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, cuerpo, titulo))
    print("escrito", nombre)


# ---------------------------------------------------------------------------
# 12-dial-audio.svg
# ---------------------------------------------------------------------------
def dial_audio():
    W, H = 700, 300
    x0, x1 = 40, 660            # 14 066 a 14 099 kHz
    f0, f1 = 14066.0, 14099.0

    def X(f):
        return x0 + (f - f0) / (f1 - f0) * (x1 - x0)

    c = []
    # Tramos del plan de HF (IARU R1)
    yb, hb = 60, 40
    tramos = [
        (14066, 14070, CLARO, "CW", "200 Hz"),
        (14070, 14089, AZUL_CLARO, "Solo modos digitales", "14 070–14 089 · 500 Hz"),
        (14089, 14099, NARANJA, "Digitales y automáticas", "14 089–14 099 · 500 Hz"),
    ]
    for a, b, col, nom, anc in tramos:
        c.append(rect(X(a), yb, X(b) - X(a), hb, col, f'stroke="{GRIS}" stroke-width="1"'))
        c.append(T((X(a) + X(b)) / 2, yb + 18, nom, 13))
        c.append(T((X(a) + X(b)) / 2, yb + 34, anc, 12, fill="#555555"))
    c.append(T(x0, 40, "Plan de HF de la IARU Región 1 (20 m)", 14, "start", 'font-weight="600"'))

    # Eje de frecuencias
    ye = 230
    c.append(L(x0, ye, x1, ye))
    for f in range(14066, 14100, 2):
        c.append(L(X(f), ye, X(f), ye + 6))
    for f in (14068, 14072, 14076, 14080, 14084, 14088, 14092, 14096):
        c.append(T(X(f), ye + 22, f"{f // 1000} {f % 1000:03d}", 12))
    c.append(T(x1, ye + 44, "kHz emitidos", 12, "end", fill="#555555"))

    # Dial y paso de audio (200 a 3000 Hz)
    xd = X(14074)
    c.append(L(xd, 120, xd, ye, f'stroke="{ALT}" stroke-dasharray="5 4"'))
    c.append(T(xd - 6, 136, "Dial: 14 074 kHz", 13, "end", fill=ALT))
    c.append(rect(X(14074.2), 150, X(14077.0) - X(14074.2), ye - 150, "#bbdefb", 'stroke="none" opacity="0.7"'))
    c.append(T(X(14077.0) + 8, 160, "Paso de audio del receptor:", 12, "start", fill=ACC))
    c.append(T(X(14077.0) + 8, 175, "de 200 a 3000 Hz sobre el dial", 12, "start", fill=ACC))

    # Señales de FT8 (50 Hz de ancho, dibujadas algo más anchas para que se vean)
    for f, h in ((14074.6, 30), (14075.2, 38), (14075.9, 22), (14076.5, 34)):
        c.append(rect(X(f) - 3, ye - h, 6, h, ACC, 'stroke="none"'))
    c.append(flecha(X(14078.5), 205, X(14076.65), 205, f'stroke="{INK}" stroke-width="1.5"'))
    c.append(T(X(14078.7), 209, "Señales de FT8 de 50 Hz:", 13, "start"))
    c.append(T(X(14078.7), 225, "dial + tono de audio", 13, "start"))

    guarda("12-dial-audio.svg", W, H, "\n".join(c),
           "Dial en 14 074 kHz, paso de audio de 200 a 3000 Hz y señales de FT8 en la parte del tramo de banda estrecha de 14 070 a 14 099 kHz que es solo para modos digitales, de 14 070 a 14 089 kHz")


# ---------------------------------------------------------------------------
# 12-ft8-ciclo.svg
# ---------------------------------------------------------------------------
def ft8_ciclo():
    W, H = 700, 300
    x0, x1 = 110, 670          # 0 a 60 s
    def X(t):
        return x0 + t / 60 * (x1 - x0)

    c = []
    # Eje de tiempo
    ye = 250
    c.append(L(x0, ye, x1, ye))
    for t in range(0, 61, 15):
        c.append(L(X(t), 40, X(t), ye + 6, f'stroke="{GRIS}" stroke-width="1" stroke-dasharray="3 4"'))
        c.append(T(X(t), ye + 22, f"{t} s", 12))
    c.append(T(x1, ye + 42, "Segundos de cada minuto UTC", 12, "end", fill="#555555"))
    for i, nom in enumerate(("Par", "Impar", "Par", "Impar")):
        c.append(T(X(15 * i + 7.5), 34, nom, 13, fill="#555555"))

    def fila(y, etiqueta, inicios, color, nota=None):
        c.append(T(x0 - 10, y + 20, etiqueta[0], 13, "end"))
        c.append(T(x0 - 10, y + 36, etiqueta[1], 13, "end"))
        for t in inicios:
            c.append(rect(X(t), y + 8, X(t + 12.64) - X(t), 30, color, 'stroke="none"'))
        if nota:
            c.append(T(*nota))

    fila(50, ("Estación", "A"), (0, 30), ACC)
    c.append(T(X(6.3), 79, "TX 12,64 s", 12, fill="#ffffff"))
    fila(100, ("Estación", "B"), (15, 45), VERDE)
    c.append(T(X(21.3), 129, "TX 12,64 s", 12, fill="#ffffff"))
    # Reloj adelantado 3 s: empieza 3 s antes
    fila(160, ("Reloj", "+3 s"), (12, 42), ALT)
    c.append(T(X(27.6), 220, "Quiere emitir en los impares, pero empieza 3 s antes:", 12, fill=ALT))
    c.append(T(X(27.6), 236, "fuera del margen de ±1 s que pide WSJT-X", 12, fill=ALT))
    guarda("12-ft8-ciclo.svg", W, H, "\n".join(c),
           "Periodos de 15 s de FT8: la estación A emite en los pares y la B en los impares, 12,64 s cada vez; una estación que quiere emitir en los impares con el reloj adelantado 3 s empieza 3 s antes de tiempo")


# ---------------------------------------------------------------------------
# 12-dmr-ranuras.svg
# ---------------------------------------------------------------------------
def dmr_ranuras():
    W, H = 700, 250
    x0, x1 = 60, 660            # 0 a 240 ms
    def X(t):
        return x0 + t / 240 * (x1 - x0)

    c = []
    y = 70
    for k in range(8):
        t = 30 * k
        ranura = 1 if k % 2 == 0 else 2
        col = ACC if ranura == 1 else VERDE
        c.append(rect(X(t) + 1, y, X(t + 30) - X(t) - 2, 50, col, 'stroke="none"'))
        c.append(T(X(t + 15), y + 30, f"R{ranura}", 14, fill="#ffffff", extra='font-weight="600"'))
    # tramas de 60 ms
    for k in range(5):
        c.append(L(X(60 * k), y - 14, X(60 * k), y + 64, f'stroke="{INK}" stroke-width="1.5"'))
    c.append(L(X(0), y - 22, X(60), y - 22, 'stroke-width="1.5" marker-start="url(#flecha)" marker-end="url(#flecha)"'))
    c.append(T(X(30), y - 30, "Trama: 60 ms", 13))
    c.append(L(X(90), y - 22, X(120), y - 22, 'stroke-width="1.5" marker-start="url(#flecha)" marker-end="url(#flecha)"'))
    c.append(T(X(105), y - 30, "Ranura: 30 ms", 13))
    # Eje
    ye = 150
    c.append(L(x0, ye, x1, ye))
    for t in range(0, 241, 60):
        c.append(L(X(t), ye, X(t), ye + 6))
        c.append(T(X(t), ye + 22, f"{t} ms", 12))
    # Leyenda
    c.append(rect(x0, 200, 18, 18, ACC, 'stroke="none"'))
    c.append(T(x0 + 26, 214, "Ranura 1: una conversación", 13, "start"))
    c.append(rect(x0 + 300, 200, 18, 18, VERDE, 'stroke="none"'))
    c.append(T(x0 + 326, 214, "Ranura 2: otra distinta", 13, "start"))
    guarda("12-dmr-ranuras.svg", W, H, "\n".join(c),
           "Un canal DMR de 12,5 kHz dividido en tramas de 60 ms con dos ranuras de 30 ms que se alternan, cada una con una conversación")


if __name__ == "__main__":
    dial_audio()
    ft8_ciclo()
    dmr_ranuras()
