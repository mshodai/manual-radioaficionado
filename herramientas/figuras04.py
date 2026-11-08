"""Genera las figuras SVG del capítulo 04 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras04.py docs/assets/figuras
"""
import math, sys, os

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul: señal útil
ALT = "#c62828"   # rojo: lo que molesta (imagen, sobremodulación)
GRIS = "#9e9e9e"


def svg(w, h, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{title}</title>
<defs>
  <marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
  </marker>
  <marker id="flecha-acc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/>
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


def T(x, y, s, size=14, anchor="middle", extra="", fill=INK):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" stroke="none" {extra}>{s}</text>'


def poly(pts, extra=""):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{d}" {extra}/>'


def flecha(x1, y1, x2, y2, color=INK, doble=False):
    m = "flecha-acc" if color == ACC else "flecha"
    ini = f'marker-start="url(#{m})" ' if doble else ""
    return L(x1, y1, x2, y2, f'stroke="{color}" {ini}marker-end="url(#{m})"')


def guarda(nombre, w, h, cuerpo, titulo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, "\n".join(cuerpo), titulo))


# ---------- Figura 4.1: longitud de onda ----------
b = []
x0, x1, y0, A = 50, 560, 120, 60
b.append(flecha(x0, y0, x1 + 15, y0) + T(x1 + 10, y0 + 22, "distancia", 13, "end"))
b.append(flecha(x0, y0 + A + 25, x0, y0 - A - 25) + T(x0 + 8, y0 - A - 28, "campo", 13, "start"))
lam = 220  # píxeles por longitud de onda
pts = [(x, y0 - A * math.sin(2 * math.pi * (x - x0) / lam)) for x in range(x0, x1 + 1, 2)]
b.append(poly(pts, f'stroke="{ACC}" stroke-width="2.5"'))
# λ entre dos crestas
c1 = x0 + lam / 4
c2 = c1 + lam
for c in (c1, c2):
    b.append(L(c, y0 - A, c, y0 - A - 22, f'stroke="{GRIS}" stroke-dasharray="4 4"'))
b.append(flecha(c1, y0 - A - 15, c2, y0 - A - 15, doble=True))
b.append(T((c1 + c2) / 2, y0 - A - 22, "λ (longitud de onda)", 14))
# amplitud
xa = c2 + lam  # tercera cresta
b.append(L(xa, y0 - A, xa + 40, y0 - A, f'stroke="{GRIS}" stroke-dasharray="4 4"'))
b.append(flecha(xa + 34, y0, xa + 34, y0 - A, doble=True) + T(xa + 42, y0 - A / 2 + 5, "amplitud", 13, "start"))
b.append(T(200, 238, "λ = c / f", 15) + T(440, 238, "λ (m) ≈ 300 / f (MHz)", 15))
guarda("04-longitud-onda.svg", 670, 260, b,
       "Onda senoidal dibujada a lo largo de la distancia. La longitud de onda es la distancia entre dos crestas consecutivas y la amplitud es el valor máximo del campo.")

# ---------- Figura 4.2: bandas de la UIT ----------
b = []
bandas = [
    ("LF", "30–300 kHz", "kilométricas", "onda larga"),
    ("MF", "300–3000 kHz", "hectométricas", "onda media, 160 m"),
    ("HF", "3–30 MHz", "decamétricas", "bandas de 80 a 10 m"),
    ("VHF", "30–300 MHz", "métricas", "radio FM, 6 m y 2 m"),
    ("UHF", "300–3000 MHz", "decimétricas", "70 cm, TDT, móviles"),
    ("SHF", "3–30 GHz", "centimétricas", "satélite, 3 cm"),
]
w0, bw, yb = 30, 100, 60
tonos = ["#e3f2fd", "#bbdefb", "#90caf9", "#64b5f6", "#42a5f5", "#1e88e5"]
for i, (sim, rango, onda, ej) in enumerate(bandas):
    x = w0 + i * bw
    b.append(f'<rect x="{x}" y="{yb}" width="{bw}" height="60" fill="{tonos[i]}" stroke="{INK}"/>')
    b.append(T(x + bw / 2, yb + 27, sim, 18, extra='font-weight="600"'))
    b.append(T(x + bw / 2, yb + 48, rango, 11.5))
    b.append(T(x + bw / 2, yb + 85, "ondas", 12))
    b.append(T(x + bw / 2, yb + 101, onda, 12))
    b.append(T(x + bw / 2, yb + 130, ej.split(", ")[0], 11.5, fill=ACC))
    if ", " in ej:
        b.append(T(x + bw / 2, yb + 146, ", ".join(ej.split(", ")[1:]), 11.5, fill=ACC))
b.append(flecha(w0, 35, w0 + 6 * bw, 35) + T(w0, 28, "frecuencia (escala logarítmica: cada casilla, ×10)", 13, "start"))
b.append(flecha(w0 + 6 * bw, 228, w0, 228) + T(w0 + 6 * bw, 248, "longitud de onda", 13, "end"))
guarda("04-bandas-uit.svg", 660, 262, b,
       "Seis bandas de la nomenclatura de la UIT, de LF a SHF, cada una diez veces más alta en frecuencia que la anterior, con su nombre métrico y ejemplos de uso.")

# ---------- Figura 4.3: envolvente de AM ----------
b = []


def panel_am(ox, titulo, m, recorta):
    out = []
    w, y0 = 270, 120
    A = 63 / (1 + m)  # el pico de la envolvente siempre a 63 px del eje
    out.append(T(ox + w / 2, 28, titulo, 15, extra='font-weight="600"'))
    out.append(L(ox, y0, ox + w, y0, f'stroke="{GRIS}"'))
    pts, env_s, env_i = [], [], []
    for k in range(0, 1081):
        t = k / 1080
        mod = 1 + m * math.sin(2 * math.pi * 2 * t)
        if recorta:
            mod = max(mod, 0)
        x = ox + t * w
        pts.append((x, y0 - A * mod * math.sin(2 * math.pi * 40 * t)))
        env_s.append((x, y0 - A * mod))
        env_i.append((x, y0 + A * mod))
    out.append(poly(pts, f'stroke="{ACC}" stroke-width="1.2"'))
    col = ALT if recorta else INK
    out.append(poly(env_s, f'stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"'))
    out.append(poly(env_i, f'stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"'))
    return out


b += panel_am(25, "m = 0,5", 0.5, False)
b += panel_am(335, "m > 1: sobremodulación", 1.6, True)
b.append(T(160, 222, "La envolvente reproduce el audio.", 13))
b.append(T(470, 222, "La portadora se corta: distorsión", 13, fill=ALT))
b.append(T(470, 239, "y bandas laterales de sobra.", 13, fill=ALT))
guarda("04-am-envolvente.svg", 630, 255, b,
       "Dos señales de AM. A la izquierda, con índice de modulación 0,5, la envolvente sigue suavemente al audio. A la derecha, sobremodulada, la portadora llega a anularse durante parte del ciclo y la envolvente se deforma.")

# ---------- Figura 4.4: espectros de AM, BLU y FM ----------
b = []


def bessel_j(n, x, terminos=30):
    return sum((-1) ** k / (math.factorial(k) * math.factorial(k + n)) * (x / 2) ** (2 * k + n)
               for k in range(terminos))


def eje(ox, w, y, etiqueta):
    return [flecha(ox, y, ox + w, y), T(ox + w, y + 20, etiqueta, 12, "end")]


ybase, H = 190, 120
# AM
ox = 30
b.append(T(ox + 85, 30, "AM (A3E)", 15, extra='font-weight="600"'))
b += eje(ox, 180, ybase, "f")
fc = ox + 90
b.append(L(fc, ybase, fc, ybase - H, 'stroke-width="3"') + T(fc, ybase + 18, "fc", 12))
for s in (-1, 1):
    x1, x2 = fc + s * 12, fc + s * 62
    b.append(f'<polygon points="{x1},{ybase} {x1},{ybase-45} {x2},{ybase-20} {x2},{ybase}" fill="{ACC}" fill-opacity="0.35" stroke="{ACC}"/>')
b.append(T(fc - 40, ybase - 55, "BLI", 12) + T(fc + 40, ybase - 55, "BLS", 12))
b.append(flecha(fc - 62, ybase + 34, fc + 62, ybase + 34, doble=True) + T(fc, ybase + 52, "2 · fmáx", 12))
# BLU
ox = 240
b.append(T(ox + 85, 30, "BLU superior (J3E)", 15, extra='font-weight="600"'))
b += eje(ox, 180, ybase, "f")
fc = ox + 90
b.append(L(fc, ybase, fc, ybase - H, f'stroke="{GRIS}" stroke-dasharray="4 4"') + T(fc, ybase + 18, "fc", 12))
b.append(T(fc, ybase - H - 6, "suprimida", 11, fill=GRIS))
b.append(f'<polygon points="{fc+12},{ybase} {fc+12},{ybase-90} {fc+62},{ybase-60} {fc+62},{ybase}" fill="{ACC}" fill-opacity="0.35" stroke="{ACC}"/>')
b.append(T(fc + 40, ybase - 98, "BLS", 12))
b.append(flecha(fc + 12, ybase + 34, fc + 62, ybase + 34, doble=True) + T(fc + 37, ybase + 52, "≈ fmáx", 12))
# FM con β = 2,5: rayas separadas fm, alturas |Jn(β)|
ox = 450
beta = 2.5
b.append(T(ox + 95, 30, "FM (F3E), β = 2,5", 15, extra='font-weight="600"'))
b += eje(ox, 200, ybase, "f")
fc = ox + 100
paso = 13
for n in range(-6, 7):
    a = abs(bessel_j(abs(n), beta))
    x = fc + n * paso
    col = INK if n == 0 else ACC
    b.append(L(x, ybase, x, ybase - H * a / 0.6, f'stroke="{col}" stroke-width="3"'))
b.append(T(fc, ybase + 18, "fc", 12))
b.append(flecha(fc - 4.5 * paso, ybase + 34, fc + 4.5 * paso, ybase + 34, doble=True) + T(fc, ybase + 52, "2 · (Δf + fm)", 12))
guarda("04-espectros.svg", 680, 262, b,
       "Espectros de tres emisiones. La AM tiene una portadora y dos bandas laterales simétricas. La BLU superior conserva solo la banda lateral superior, sin portadora. La FM muestra una portadora y muchas rayas laterales separadas por la frecuencia del audio.")

# ---------- Figura 4.5: frecuencia imagen ----------
b = []
y = 150
f2x = lambda f: 40 + (f - 5) * 17  # MHz -> píxel
b.append(flecha(30, y, 680, y) + T(680, y + 22, "f (MHz)", 13, "end"))
for f in range(10, 40, 5):
    b.append(L(f2x(f), y - 4, f2x(f), y + 4) + T(f2x(f), y + 22, str(f), 12, fill=GRIS))


def raya(f, alto, color, etq, sub):
    x = f2x(f)
    return (L(x, y, x, y - alto, f'stroke="{color}" stroke-width="4"')
            + T(x, y - alto - 24, etq, 14, extra='font-weight="600"', fill=color)
            + T(x, y - alto - 8, sub, 12, fill=color))


b.append(raya(14.2, 70, ACC, "señal", "14,2"))
b.append(raya(23.2, 95, INK, "OL", "23,2"))
b.append(raya(32.2, 70, ALT, "imagen", "32,2"))
b.append(flecha(f2x(14.2), y + 45, f2x(23.2), y + 45, doble=True) + T(f2x(18.7), y + 63, "9 MHz = FI", 13))
b.append(L(f2x(23.2), y + 45, f2x(32.2), y + 45, f'stroke="{ALT}" marker-start="url(#flecha)" marker-end="url(#flecha)"')
         + T(f2x(27.7), y + 63, "9 MHz = FI", 13, fill=ALT))
b.append(flecha(f2x(14.2), y + 88, f2x(32.2), y + 88, doble=True) + T(f2x(23.2), y + 106, "2 · FI = 18 MHz", 13))
guarda("04-imagen.svg", 720, 270, b,
       "Eje de frecuencias con la señal deseada en 14,2 MHz, el oscilador local en 23,2 MHz y la frecuencia imagen en 32,2 MHz. Señal e imagen están a 9 MHz del oscilador, una por cada lado, y separadas entre sí 18 MHz.")

print("Figuras del capítulo 04 generadas en", OUT)
