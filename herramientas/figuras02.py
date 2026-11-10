"""Genera las figuras SVG del capítulo 02 (dibujo propio, simbología IEC 60617).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras02.py docs/assets/figuras
"""
import math, sys, os

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"

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
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {extra}/>'

def T(x, y, s, size=14, anchor="middle", extra="", fill=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" stroke="none" {extra}>{s}</text>'

def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="{INK}"/>'

def res_v(x, y1, y2):  # resistencia vertical entre y1 e y2
    m = (y1 + y2) / 2
    return L(x, y1, x, m - 25) + f'<rect x="{x-10}" y="{m-25}" width="20" height="50"/>' + L(x, m + 25, x, y2)

def res_h(x1, x2, y):
    m = (x1 + x2) / 2
    return L(x1, y, m - 25, y) + f'<rect x="{m-25}" y="{y-10}" width="50" height="20"/>' + L(m + 25, y, x2, y)

def meter(cx, cy, letter):
    return f'<circle cx="{cx}" cy="{cy}" r="17"/>' + T(cx, cy + 6, letter, 17, extra='font-weight="600"')

# ---------- Figura 2.1: medida de tensión y corriente ----------
b = []
b.append(L(60, 50, 60, 108) + L(60, 124, 60, 190))
b.append(L(38, 108, 82, 108) + f'<line x1="50" y1="124" x2="70" y2="124" stroke-width="5"/>')
b.append(T(30, 104, "+", 16) + T(30, 150, "12 V", 14))
b.append(L(60, 50, 163, 50) + meter(180, 50, "A") + L(197, 50, 300, 50))
b.append(res_v(300, 50, 190) + T(275, 125, "R", 15))
b.append(L(60, 190, 300, 190))
b.append(L(300, 85, 380, 85) + L(380, 85, 380, 103) + meter(380, 120, "V") + L(380, 137, 380, 155) + L(380, 155, 300, 155))
b.append(dot(300, 85) + dot(300, 155))
b.append(f'<line x1="95" y1="34" x2="140" y2="34" stroke="{ACC}" marker-end="url(#flecha-acc)"/>' + T(118, 26, "I", 15, extra='font-style="italic"', fill=ACC))
b.append(T(180, 90, "en serie", 12) + T(380, 176, "en paralelo", 12))
open(os.path.join(OUT, "02-medida.svg"), "w").write(svg(440, 230, "\n".join(b),
    "Pila de 12 V que alimenta una resistencia R. El amperímetro A está en serie en el hilo superior y el voltímetro V, en paralelo con la resistencia."))

# ---------- Figura 2.2: serie y paralelo ----------
b = []
term = lambda x, y: f'<circle cx="{x}" cy="{y}" r="4" fill="#ffffff"/>'
b.append(T(140, 30, "En serie", 16, extra='font-weight="600"'))
b.append(term(30, 110) + L(34, 110, 50, 110) + res_h(50, 140, 110) + res_h(140, 230, 110) + L(230, 110, 246, 110) + term(250, 110))
b.append(T(95, 90, "R₁") + T(185, 90, "R₂"))
b.append(T(140, 200, "R = R₁ + R₂", 15))
b.append(T(420, 30, "En paralelo", 16, extra='font-weight="600"'))
b.append(term(300, 110) + L(304, 110, 340, 110) + L(340, 78, 340, 150) + L(500, 78, 500, 150) + L(500, 110, 536, 110) + term(540, 110))
b.append(res_h(340, 500, 78) + res_h(340, 500, 150))
b.append(dot(340, 110) + dot(500, 110))
b.append(T(420, 60, "R₁") + T(420, 180, "R₂"))
b.append(T(420, 210, "1/R = 1/R₁ + 1/R₂", 15))
open(os.path.join(OUT, "02-serie-paralelo.svg"), "w").write(svg(570, 230, "\n".join(b),
    "Dos resistencias en serie, una a continuación de la otra, y dos resistencias en paralelo, conectadas entre los mismos dos puntos."))

# ---------- Figura 2.3: onda senoidal ----------
b = []
x0, y0, per, amp = 60, 140, 320, 95
b.append(L(x0, y0, 455, y0, 'marker-end="url(#flecha)"') + L(x0, 250, x0, 25, 'marker-end="url(#flecha)"'))
b.append(T(452, y0 + 24, "t", 14, extra='font-style="italic"'))
pts = []
for i in range(0, 381):
    x = x0 + i * 1.0
    y = y0 - amp * math.sin(2 * math.pi * (x - x0) / per)
    pts.append(f"{x:.1f},{y:.1f}")
b.append(f'<polyline points="{" ".join(pts)}" stroke="{ACC}" stroke-width="2.5"/>')
yp, yef = y0 - amp, y0 - amp / math.sqrt(2)
dash = 'stroke-dasharray="5 4" stroke-width="1.2"'
b.append(L(x0, yp, 440, yp, dash) + L(x0, yef, 440, yef, dash) + L(x0, y0 + amp, 440, y0 + amp, dash))
b.append(T(x0 - 8, yp + 5, "Vₚ", 14, "end") + T(x0 - 8, yef + 5, "Vₑ", 14, "end") + T(x0 - 8, y0 + amp + 5, "−Vₚ", 14, "end"))
b.append(T(300, yef - 7, "Vₑ ≈ 0,707 · Vₚ", 13))
b.append(L(480, yp, 480, y0 + amp, 'marker-start="url(#flecha)" marker-end="url(#flecha)" stroke-width="1.5"') + T(488, y0 + 5, "Vₚₚ", 14, "start"))
b.append(L(x0, 262, x0 + per, 262, 'marker-start="url(#flecha)" marker-end="url(#flecha)" stroke-width="1.5"') + L(x0 + per, y0, x0 + per, 268, dash))
b.append(T(x0 + per / 2, 282, "periodo T = 1/f", 14))
open(os.path.join(OUT, "02-senoide.svg"), "w").write(svg(530, 295, "\n".join(b),
    "Onda senoidal de tensión con su valor de pico, su valor eficaz (unas siete décimas del pico), su valor pico a pico y su periodo."))

# ---------- Figura 2.4: símbolos IEC ----------
CW, CH, COLS = 170, 120, 4
def cell(i, draw, label):
    cx = (i % COLS) * CW + CW / 2
    top = (i // COLS) * CH
    cy = top + 50
    return draw(cx, cy) + T(cx, top + 108, label, 13)

def s_res(cx, cy):
    return res_h(cx - 50, cx + 50, cy)
def s_cap(cx, cy):
    return L(cx - 50, cy, cx - 6, cy) + L(cx + 6, cy, cx + 50, cy) + f'<g stroke-width="3">{L(cx-6, cy-18, cx-6, cy+18)}{L(cx+6, cy-18, cx+6, cy+18)}</g>'
def s_elec(cx, cy):
    return (L(cx - 50, cy, cx - 11, cy) + f'<rect x="{cx-11}" y="{cy-18}" width="6" height="36"/>'
            + f'<line x1="{cx+6}" y1="{cy-18}" x2="{cx+6}" y2="{cy+18}" stroke-width="3"/>' + L(cx + 6, cy, cx + 50, cy) + T(cx - 22, cy - 14, "+", 15))
def s_coil(cx, cy):
    arcs = "".join(" a7.5,7.5 0 0 1 15,0" for _ in range(4))
    return L(cx - 50, cy, cx - 30, cy) + f'<path d="M{cx-30},{cy}{arcs}"/>' + L(cx + 30, cy, cx + 50, cy)
def diode(cx, cy, bar=None):
    tri = f'<path d="M{cx-12},{cy-13} L{cx-12},{cy+13} L{cx+10},{cy} z" fill="{INK}"/>'
    bar = bar or L(cx + 10, cy - 13, cx + 10, cy + 13)
    return L(cx - 50, cy, cx - 12, cy) + tri + bar + L(cx + 10, cy, cx + 50, cy)
def s_diode(cx, cy):
    return diode(cx, cy)
def s_led(cx, cy):
    a = 'marker-end="url(#flecha)" stroke-width="1.5"'
    return diode(cx, cy) + L(cx, cy - 16, cx + 12, cy - 30, a) + L(cx + 9, cy - 13, cx + 21, cy - 27, a)
def s_zener(cx, cy):
    return diode(cx, cy, f'<path d="M{cx+4},{cy-17} L{cx+10},{cy-13} L{cx+10},{cy+13} L{cx+16},{cy+17}"/>')
def s_bat(cx, cy):
    return (L(cx - 50, cy, cx - 5, cy) + L(cx - 5, cy - 20, cx - 5, cy + 20) + f'<line x1="{cx+5}" y1="{cy-10}" x2="{cx+5}" y2="{cy+10}" stroke-width="5"/>'
            + L(cx + 5, cy, cx + 50, cy) + T(cx - 16, cy - 18, "+", 15))
def s_gnd(cx, cy):
    return L(cx, cy - 32, cx, cy + 4) + L(cx - 20, cy + 4, cx + 20, cy + 4) + L(cx - 13, cy + 11, cx + 13, cy + 11) + L(cx - 6, cy + 18, cx + 6, cy + 18)
def s_fuse(cx, cy):
    return L(cx - 50, cy, cx + 50, cy) + f'<rect x="{cx-22}" y="{cy-9}" width="44" height="18"/>'
def s_npn(cx, cy):
    return (f'<circle cx="{cx+2}" cy="{cy}" r="24"/>' + L(cx - 50, cy, cx - 8, cy)
            + f'<line x1="{cx-8}" y1="{cy-14}" x2="{cx-8}" y2="{cy+14}" stroke-width="3"/>'
            + L(cx - 8, cy - 6, cx + 12, cy - 20) + L(cx + 12, cy - 20, cx + 12, cy - 38)
            + L(cx - 8, cy + 6, cx + 11, cy + 19, 'marker-end="url(#flecha)"') + L(cx + 12, cy + 20, cx + 12, cy + 38)
            + T(cx - 44, cy - 6, "B", 12) + T(cx + 24, cy - 28, "C", 12) + T(cx + 24, cy + 34, "E", 12))
def s_ant(cx, cy):
    return L(cx, cy + 32, cx, cy - 30) + f'<path d="M{cx-16},{cy-30} L{cx},{cy-8} L{cx+16},{cy-30}"/>'

items = [(s_res, "Resistencia"), (s_cap, "Condensador"), (s_elec, "Condensador electrolítico"), (s_coil, "Bobina"),
         (s_diode, "Diodo"), (s_led, "LED"), (s_zener, "Diodo Zener"), (s_npn, "Transistor NPN"),
         (s_bat, "Pila o batería"), (s_fuse, "Fusible"), (s_gnd, "Toma de tierra"), (s_ant, "Antena")]
b = [cell(i, f, l) for i, (f, l) in enumerate(items)]
open(os.path.join(OUT, "02-simbolos.svg"), "w").write(svg(CW * COLS, CH * 3, "\n".join(b),
    "Símbolos IEC de resistencia, condensador, condensador electrolítico, bobina, diodo, LED, diodo Zener, transistor NPN, pila, fusible, toma de tierra y antena."))
print("ok")
