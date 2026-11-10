"""Genera las figuras SVG del capítulo 06 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras06.py docs/assets/figuras

Los diagramas de radiación de la figura 6.2 se calculan aquí mismo:
- Dipolo de media onda en espacio libre: E(θ) = cos(π/2 · cos θ) / sen θ.
- «Yagi» de tres elementos: modelo simplificado, tres fuentes con un reparto de
  corrientes elegido a mano multiplicadas por el diagrama del dipolo. Sirve para
  enseñar la forma (lóbulo principal, lóbulo trasero, relación delante/detrás),
  no para diseñar una antena real. Al ejecutarlo, el script imprime el ancho de
  haz y la relación delante/detrás del modelo, que son las cifras del pie.
"""
import cmath
import math
import os
import sys

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul: lo principal
ALT = "#c62828"   # rojo: lo que se pierde o se resalta
VERDE = "#2e7d32"
GRIS = "#9e9e9e"
CLARO = "#e0e0e0"


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


def polygon(pts, extra=""):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" {extra}/>'


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>'


def circ(x, y, r, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" {extra}/>'


def flecha(x1, y1, x2, y2, color=INK, doble=False, extra=""):
    m = "flecha-acc" if color == ACC else "flecha"
    ini = f'marker-start="url(#{m})" ' if doble else ""
    trazo = "" if "stroke=" in extra else f'stroke="{color}" '
    return L(x1, y1, x2, y2, f'{trazo}{ini}marker-end="url(#{m})" {extra}')


def cota(x1, x2, y, texto, size=13):
    """Cota horizontal con flechas en los dos extremos y el texto encima."""
    return [flecha(x1, y, x2, y, doble=True, extra='stroke-width="1.2"'),
            T((x1 + x2) / 2, y - 7, texto, size)]


def guarda(nombre, w, h, cuerpo, titulo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, "\n".join(cuerpo), titulo))


# ---------- Figura 6.1: tensión y corriente en un dipolo de media onda ----------
b = []
x0, x1, ya = 90, 610, 170          # extremos del dipolo y altura del hilo
xm = (x0 + x1) / 2
amp = 85
# hilo y punto de alimentación
b.append(L(x0, ya, xm - 8, ya, 'stroke-width="4"'))
b.append(L(xm + 8, ya, x1, ya, 'stroke-width="4"'))
b.append(circ(xm - 8, ya, 3, f'fill="{INK}"'))
b.append(circ(xm + 8, ya, 3, f'fill="{INK}"'))
b.append(L(xm - 8, ya, xm - 8, ya + 70, 'stroke-width="1.5"'))
b.append(L(xm + 8, ya, xm + 8, ya + 70, 'stroke-width="1.5"'))
b.append(T(xm, ya + 88, "a la línea", 12))
# corriente: máxima en el centro, nula en los extremos
pts = []
for k in range(101):
    x = x0 + (x1 - x0) * k / 100
    pts.append((x, ya - amp * math.sin(math.pi * k / 100)))
b.append(poly(pts, f'stroke="{ACC}" stroke-width="2.5"'))
# tensión: máxima en los extremos (y de signo opuesto), mínima en el centro
pts = []
for k in range(101):
    x = x0 + (x1 - x0) * k / 100
    pts.append((x, ya - amp * math.cos(math.pi * k / 100)))
b.append(poly(pts, f'stroke="{ALT}" stroke-width="2.5" stroke-dasharray="8 6"'))
b.append(T(xm + 60, ya - amp - 12, "corriente I: máxima en el centro", 13, "start", fill=ACC))
b.append(T(x0, ya - amp - 12, "tensión V: máxima en las puntas", 13, "start", fill=ALT))
b.append(T(x1, ya + amp + 22, "(con signo opuesto en cada punta)", 12, "end", fill=ALT))
b += cota(x0, x1, 305, "λ/2 (algo menos en la práctica)")
b.append(T(xm, 30, "Dipolo de media onda alimentado en el centro", 15, extra='font-weight="600"'))
guarda("06-dipolo.svg", 700, 325, b,
       "Dipolo de media onda alimentado en el centro. La corriente es máxima en el centro y nula en las puntas; la tensión es mínima en el centro y máxima en las puntas, con signo opuesto en cada una. Por eso la impedancia es baja en el centro, unos 73 ohmios, y muy alta en los extremos.")


# ---------- Figura 6.2: diagramas de radiación ----------
def e_dipolo(theta):
    """Campo normalizado de un dipolo de media onda; theta medido desde el eje del hilo."""
    s = math.sin(theta)
    if abs(s) < 1e-9:
        return 0.0
    return abs(math.cos(math.pi / 2 * math.cos(theta)) / s)


# Modelo de Yagi de 3 elementos: posiciones a lo largo del boom (en λ) y corrientes
# complejas elegidas a mano para dar un lóbulo hacia +x.
YAGI = [(-0.20, 0.60 * cmath.exp(1j * math.radians(120))),   # reflector
        (0.00, 1.00),                                         # excitado
        (0.15, 0.50 * cmath.exp(-1j * math.radians(130)))]    # director


def e_yagi(phi):
    """Campo en el plano de los elementos; phi medido desde el boom (0 = hacia delante)."""
    af = sum(i * cmath.exp(1j * 2 * math.pi * x * math.cos(phi)) for x, i in YAGI)
    # los elementos son perpendiculares al boom: el ángulo respecto al hilo es 90° − phi
    return abs(af) * e_dipolo(math.pi / 2 - phi)


N = 720
angs = [2 * math.pi * k / N for k in range(N)]
ey = [e_yagi(a) for a in angs]
emax = max(ey)
ey = [v / emax for v in ey]
fb_db = 20 * math.log10(ey[0] / ey[N // 2])
# ancho de haz a −3 dB del modelo
k = 0
while ey[k] >= 1 / math.sqrt(2):
    k += 1
haz_yagi = 2 * math.degrees(angs[k])
# ancho de haz del dipolo, desde su máximo (theta = 90°)
th = math.pi / 2
while e_dipolo(th) >= 1 / math.sqrt(2):
    th += 0.0005
haz_dip = 2 * math.degrees(th - math.pi / 2)
print(f"Dipolo: ancho de haz a −3 dB = {haz_dip:.1f}°")
print(f"Modelo de Yagi: relación delante/detrás = {fb_db:.1f} dB, ancho de haz = {haz_yagi:.1f}°")


def polar(cx, cy, r, valores, color, titulo, nota):
    out = []
    for f, estilo in ((1.0, f'stroke="{GRIS}" stroke-width="1"'),
                      (1 / math.sqrt(2), f'stroke="{GRIS}" stroke-width="1" stroke-dasharray="4 4"'),
                      (0.5, f'stroke="{CLARO}" stroke-width="1"')):
        out.append(circ(cx, cy, r * f, estilo))
    for a in range(0, 180, 30):
        ra = math.radians(a)
        out.append(L(cx - r * math.cos(ra), cy - r * math.sin(ra), cx + r * math.cos(ra), cy + r * math.sin(ra),
                     f'stroke="{CLARO}" stroke-width="1"'))
    pts = [(cx + r * v * math.cos(a), cy - r * v * math.sin(a)) for a, v in valores]
    out.append(polygon(pts, f'stroke="{color}" stroke-width="2.5" fill="{color}" fill-opacity="0.12"'))
    out.append(T(cx, cy - r - 34, titulo, 15, extra='font-weight="600"'))
    out.append(T(cx, cy + r + 30, nota, 12))
    out.append(T(cx + r * 0.5 + 4, cy + r * 0.5 + 14, "−3 dB", 12, "start", fill=GRIS))
    return out


b = []
r = 140
# dipolo visto desde arriba, con el hilo en vertical en el dibujo (eje y)
vals_d = [(a, e_dipolo(a - math.pi / 2)) for a in angs]
b += polar(200, 230, r, vals_d, ACC, "Dipolo (visto desde arriba)", "dos lóbulos, nulos en la dirección del hilo")
b.append(L(200, 230 - 40, 200, 230 + 40, 'stroke-width="4"'))
b.append(T(212, 230 - 30, "hilo", 12, "start"))
# yagi, lóbulo hacia la derecha
vals_y = list(zip(angs, ey))
b += polar(560, 230, r, vals_y, ALT, "Yagi de 3 elementos (modelo)", f"lóbulo principal; detrás, {fb_db:.0f} dB menos")
b.append(flecha(560, 230, 560 + r + 40, 230, extra='stroke-width="1.5"'))
b.append(T(560 + r + 30, 250, "delante", 12, "end"))
guarda("06-diagramas.svg", 760, 430, b,
       f"Diagramas de radiación en el plano horizontal. A la izquierda, un dipolo de media onda horizontal visto desde arriba: dos lóbulos perpendiculares al hilo y nulos en su dirección, con un ancho de haz de unos {haz_dip:.0f} grados. A la derecha, una Yagi de tres elementos: un lóbulo principal hacia delante y un lóbulo trasero {fb_db:.0f} dB más débil. El círculo discontinuo marca la mitad de la potencia, −3 dB.")


# ---------- Figura 6.4: Yagi de tres elementos ----------
b = []
yb = 215                              # altura del boom
xs = {"Reflector": 170, "Excitado": 330, "Director": 450}
largos = {"Reflector": 270, "Excitado": 250, "Director": 228}
b.append(L(110, yb, 540, yb, 'stroke-width="5" stroke="#616161"'))
b.append(T(560, yb + 5, "boom", 12, "start"))
for nombre, x in xs.items():
    h = largos[nombre] / 2
    color = ACC if nombre == "Excitado" else INK
    if nombre == "Excitado":
        b.append(L(x, yb - h, x, yb - 7, f'stroke="{color}" stroke-width="4"'))
        b.append(L(x, yb + 7, x, yb + h, f'stroke="{color}" stroke-width="4"'))
        b.append(L(x, yb + 7, x + 40, yb + 60, 'stroke-width="1.3"'))
        b.append(T(x + 44, yb + 74, "línea", 12, "start"))
    else:
        b.append(L(x, yb - h, x, yb + h, f'stroke="{color}" stroke-width="4"'))
    b.append(T(x, yb - h - 14, nombre, 14, fill=color))
b.append(T(170, yb + largos["Reflector"] / 2 + 22, "un 5 % más largo", 12))
b.append(T(330, yb + largos["Excitado"] / 2 + 22, "≈ λ/2, resonante", 12, fill=ACC))
b.append(T(450, yb + largos["Director"] / 2 + 22, "un 5 % más corto", 12))
b.append(flecha(560, 135, 660, 135, ACC, extra='stroke-width="3"'))
b.append(T(610, 121, "máxima radiación", 13, fill=ACC))
b.append(T(350, 30, "Yagi de tres elementos vista desde arriba", 15, extra='font-weight="600"'))
guarda("06-yagi.svg", 700, 400, b,
       "Yagi de tres elementos vista desde arriba. Sobre un boom hay tres elementos paralelos: detrás el reflector, algo más largo; en medio el elemento excitado, de media onda, que es el único conectado a la línea; delante el director, algo más corto. La antena radia sobre todo hacia el lado del director.")


# ---------- Figura 6.3: plano de tierra ----------
b = []
for cx, titulo, caida, imp in ((190, "Radiales horizontales", 0, "≈ 36 Ω"), (520, "Radiales a 45° hacia abajo", 45, "≈ 50 Ω")):
    yb_ = 230
    largo_v, largo_r = 150, 150
    b.append(L(cx, yb_ - 8, cx, yb_ - 8 - largo_v, f'stroke="{ACC}" stroke-width="4"'))
    b.append(rect(cx - 12, yb_ - 8, 24, 16, "#eeeeee", 'stroke-width="1.5"'))
    for lado in (-1, 1):
        dx = lado * largo_r * math.cos(math.radians(caida))
        dy = largo_r * math.sin(math.radians(caida))
        b.append(L(cx + lado * 12, yb_, cx + dx, yb_ + dy, 'stroke-width="3"'))
    # radiales hacia y desde el observador, en perspectiva
    for lado in (-1, 1):
        dx = lado * 0.45 * largo_r * math.cos(math.radians(caida))
        dy = 0.45 * largo_r * math.sin(math.radians(caida)) + 26
        b.append(L(cx, yb_ + 8, cx + dx, yb_ + dy, f'stroke="{GRIS}" stroke-width="2.5"'))
    b.append(L(cx, yb_ + 8, cx, yb_ + 110, 'stroke-width="1.3" stroke-dasharray="5 4"'))
    b.append(T(cx + 6, yb_ + 126, "coaxial", 12))
    b.append(T(cx + 10, yb_ - 8 - largo_v / 2, "λ/4", 14, "start", fill=ACC))
    b.append(T(cx, 36, titulo, 15, extra='font-weight="600"'))
    b.append(T(cx, 60, f"impedancia {imp}", 14))
b.append(T(355, 380, "Los radiales, también de λ/4, hacen de «suelo» artificial para la vertical.", 13))
guarda("06-plano-tierra.svg", 710, 400, b,
       "Dos antenas verticales de cuarto de onda con cuatro radiales de cuarto de onda. Con los radiales horizontales, la impedancia es de unos 36 ohmios. Si se inclinan unos 45 grados hacia abajo, sube hasta unos 50 ohmios y se puede alimentar directamente con coaxial de 50 ohmios.")


# ---------- Figura 6.5: sección de un coaxial y de una línea paralela ----------
b = []
cx, cy = 190, 200
capas = [(110, "#424242", "cubierta"), (96, "#bdbdbd", "malla"), (88, "#fff8e1", "dieléctrico"), (26, "#ef6c00", "vivo")]
for rr, color, _ in capas:
    b.append(circ(cx, cy, rr, f'fill="{color}" stroke="{INK}" stroke-width="1.2"'))
b += [flecha(cx - 88, cy + 150, cx + 88, cy + 150, doble=True, extra='stroke-width="1.2"'),
      T(cx, cy + 172, "D: diámetro interior de la malla", 13),
      L(cx - 88, cy + 10, cx - 88, cy + 155, f'stroke="{GRIS}" stroke-width="1" stroke-dasharray="3 3"'),
      L(cx + 88, cy + 10, cx + 88, cy + 155, f'stroke="{GRIS}" stroke-width="1" stroke-dasharray="3 3"')]
b.append(flecha(cx - 26, cy, cx + 26, cy, doble=True, extra='stroke-width="1.2" stroke="#ffffff"'))
b.append(T(cx, cy - 8, "d", 13, fill="#ffffff"))
b.append(T(cx + 130, cy - 95, "cubierta", 12, "start"))
b.append(L(cx + 127, cy - 99, cx + 70, cy - 80, 'stroke-width="1"'))
b.append(T(cx + 130, cy - 60, "malla", 12, "start"))
b.append(L(cx + 127, cy - 64, cx + 66, cy - 63, 'stroke-width="1"'))
b.append(T(cx + 130, cy - 25, "dieléctrico", 12, "start"))
b.append(L(cx + 127, cy - 29, cx + 55, cy - 30, 'stroke-width="1"'))
b.append(T(cx, 50, "Cable coaxial", 15, extra='font-weight="600"'))
# línea paralela
cx2 = 540
for dx in (-75, 75):
    b.append(circ(cx2 + dx, cy, 14, f'fill="#ef6c00" stroke="{INK}" stroke-width="1.2"'))
b.append(rect(cx2 - 61, cy - 6, 122, 12, "#eeeeee", f'stroke="{GRIS}" stroke-width="1"'))
b.append(T(cx2, cy + 30, "separadores de plástico (o aire)", 12, fill="#616161"))
b += cota(cx2 - 75, cx2 + 75, cy - 40, "S: separación entre centros")
b.append(flecha(cx2 + 61, cy + 60, cx2 + 89, cy + 60, doble=True, extra='stroke-width="1.2"'))
b.append(T(cx2 + 75, cy + 82, "d", 13))
b.append(T(cx2, 50, "Línea paralela", 15, extra='font-weight="600"'))
guarda("06-secciones.svg", 720, 400, b,
       "Sección de un cable coaxial y de una línea paralela. El coaxial tiene un conductor central de diámetro d, un dieléctrico, una malla de diámetro interior D y una cubierta. La línea paralela tiene dos conductores de diámetro d separados una distancia S entre centros.")


# ---------- Figura 6.6: ondas estacionarias ----------
b = []
gx0, gx1, gy0 = 90, 650, 330
alto = 120                    # píxeles por unidad de |V| normalizada a la tensión incidente
b.append(flecha(gx0, gy0, gx1 + 20, gy0))
b.append(flecha(gx0, gy0, gx0, gy0 - 2.2 * alto))
b.append(T(gx0 - 10, gy0 - 2.2 * alto + 4, "|V|", 13, "end"))
b.append(T(gx1 + 20, gy0 + 22, "posición en la línea", 12, "end"))
b.append(T(gx1, gy0 + 40, "carga →", 12, "end"))
for v in (1, 2):
    b.append(L(gx0, gy0 - v * alto, gx1, gy0 - v * alto, f'stroke="{CLARO}" stroke-width="1"'))
    b.append(T(gx0 - 8, gy0 - v * alto + 4, str(v), 12, "end"))
# longitud dibujada: 1,25 λ
for gamma, color, nombre, guion in ((0.0, VERDE, "ROE 1 (adaptada)", ""),
                                     (0.5, ACC, "ROE 3", ""),
                                     (1.0, ALT, "ROE infinita (extremo abierto)", 'stroke-dasharray="7 5"')):
    pts = []
    for k in range(301):
        z = 1.25 * (1 - k / 300)          # distancia a la carga en λ
        v = abs(1 + gamma * cmath.exp(-1j * 4 * math.pi * z))
        pts.append((gx0 + (gx1 - gx0) * k / 300, gy0 - v * alto))
    b.append(poly(pts, f'stroke="{color}" stroke-width="2.5" {guion}'))
b.append(T(560, gy0 - 1.0 * alto - 8, "ROE 1", 12, fill=VERDE))
b.append(T(gx0 + 10, 30, "ROE 3: máximos de 1,5 y mínimos de 0,5", 13, "start", fill=ACC))
b.append(T(gx0 + 10, 50, "ROE infinita: máximos de 2 y nulos", 13, "start", fill=ALT))
# media longitud de onda entre máximos
xa = gx0 + (gx1 - gx0) * (1.25 - 1.0) / 1.25
xb = gx0 + (gx1 - gx0) * (1.25 - 0.5) / 1.25
b += cota(xa, xb, gy0 + 22, "λ/2 entre dos máximos")
guarda("06-estacionarias.svg", 700, 380, b,
       "Amplitud de la tensión a lo largo de una línea de transmisión, normalizada a la onda incidente. Con la carga adaptada, ROE 1, la tensión es la misma en toda la línea. Con ROE 3 oscila entre 1,5 y 0,5. Con el extremo abierto, ROE infinita, oscila entre 2 y 0. Los máximos se repiten cada media longitud de onda.")


# ---------- Figura 6.7: líneas de cuarto de onda en cortocircuito y abiertas ----------
b = []
for fila, (y, extremo, ve, nota) in enumerate(((95, "cortocircuito", "un circuito abierto", "impedancia muy alta"),
                                               (245, "abierta", "un cortocircuito", "impedancia muy baja"))):
    xa, xb = 110, 430
    b.append(L(xa, y - 20, xb, y - 20, 'stroke-width="2.5"'))
    b.append(L(xa, y + 20, xb, y + 20, 'stroke-width="2.5"'))
    b.append(circ(xa, y - 20, 4, f'fill="#ffffff" stroke="{INK}"'))
    b.append(circ(xa, y + 20, 4, f'fill="#ffffff" stroke="{INK}"'))
    if extremo == "cortocircuito":
        b.append(L(xb, y - 20, xb, y + 20, f'stroke="{ALT}" stroke-width="4"'))
        b.append(T(xb + 10, y + 5, "en corto", 13, "start", fill=ALT))
    else:
        b.append(T(xb + 10, y + 5, "abierta", 13, "start", fill=ALT))
    b += cota(xa, xb, y - 34, "λ/4 eléctrico")
    b.append(T(xa - 12, y + 5, "entrada", 12, "end"))
    b.append(flecha(500, y, 560, y, ACC, extra='stroke-width="2"'))
    b.append(T(575, y - 4, f"equivale a {ve}", 13, "start", fill=ACC))
    b.append(T(575, y + 16, f"({nota})", 12, "start", fill=ACC))
b.append(T(400, 330, "Media longitud de onda repite en la entrada lo que hay en el extremo.", 13))
guarda("06-lineas-resonantes.svg", 820, 350, b,
       "Dos tramos de línea de un cuarto de longitud de onda eléctrica. Si el extremo está en cortocircuito, en la entrada se ve un circuito abierto, de impedancia muy alta, como un circuito resonante paralelo. Si el extremo está abierto, en la entrada se ve un cortocircuito, como un circuito resonante serie. Un tramo de media onda repite en la entrada lo que hay en el extremo.")
print("Figuras escritas en", OUT)
