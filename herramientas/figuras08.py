"""Genera las figuras SVG del capítulo 08 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras08.py docs/assets/figuras

Figuras:
- 08-armonicos.svg: espectro de una emisión en 50,2 MHz con sus armónicos y la
  banda de radiodifusión en FM; respuesta de un filtro paso bajo ideal dibujada
  a mano (forma, no un diseño real).
- 08-intermodulacion.svg: dos señales y sus productos de tercer y quinto orden.
- 08-modo-comun.svg: corrientes diferenciales y en modo común en un coaxial, y
  el efecto de un choque.
- 08-fuente-conmutada.svg: «peine» de armónicos de una fuente conmutada de
  70 kHz alrededor de la banda de 40 m.
"""
import math
import os
import sys

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul: lo deseado
ALT = "#c62828"   # rojo: lo no deseado
VERDE = "#2e7d32"
GRIS = "#9e9e9e"
CLARO = "#e0e0e0"
FONDO_BANDA = "#fff3e0"


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
  <marker id="flecha-alt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{ALT}"/>
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


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>'


def circ(x, y, r, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" {extra}/>'


def flecha(x1, y1, x2, y2, color=INK, doble=False, extra=""):
    m = {ACC: "flecha-acc", ALT: "flecha-alt"}.get(color, "flecha")
    ini = f'marker-start="url(#{m})" ' if doble else ""
    return L(x1, y1, x2, y2, f'stroke="{color}" {ini}marker-end="url(#{m})" {extra}')


def guarda(nombre, w, h, cuerpo, titulo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, "\n".join(cuerpo), titulo))


def ejes_db(x0, y0, x1, y_top, db_min, db_max, paso, rotulo_y):
    """Eje vertical en dBc con rejilla; devuelve la función que pasa dB a y."""
    out = []

    def y_de(db):
        return y0 - (db - db_min) / (db_max - db_min) * (y0 - y_top)

    for db in range(db_min, db_max + 1, paso):
        y = y_de(db)
        out.append(L(x0, y, x1, y, f'stroke="{CLARO}" stroke-width="1"'))
        out.append(T(x0 - 8, y + 4, f"{db}".replace("-", "−"), 12, "end"))
    out.append(L(x0, y0, x1, y0))
    out.append(L(x0, y0, x0, y_top))
    out.append(T(x0 - 44, (y0 + y_top) / 2, rotulo_y, 13, extra=f'transform="rotate(-90 {x0 - 44:.1f} {(y0 + y_top) / 2:.1f})"'))
    return out, y_de


# ---------- Figura 8.1: armónicos de una emisión en 6 m ----------
b = []
X0, X1, Y0, YT = 90, 760, 330, 70
FMIN, FMAX = 0, 230            # MHz


def x_de(f):
    return X0 + (f - FMIN) / (FMAX - FMIN) * (X1 - X0)


# banda de FM sombreada (87,5 a 108 MHz)
b.append(rect(x_de(87.5), YT, x_de(108) - x_de(87.5), Y0 - YT, FONDO_BANDA, 'stroke="none"'))
b.append(T(x_de(87.5) - 4, Y0 - 8, "radio FM", 12, "end", fill="#e65100"))
ejes, y_de = ejes_db(X0, Y0, X1, YT, -100, 0, 20, "nivel respecto a la portadora (dBc)")
b += ejes
for f in range(0, 231, 50):
    b.append(L(x_de(f), Y0, x_de(f), Y0 + 5))
    b.append(T(x_de(f), Y0 + 20, f"{f}", 12))
b.append(T((X0 + X1) / 2, Y0 + 42, "frecuencia (MHz)", 13))
F0 = 50.2
# niveles sin filtro (ilustrativos) y con filtro
sin_filtro = {1: 0, 2: -30, 3: -38, 4: -50}


def atenuacion(f):
    """Paso bajo ilustrativo: plano hasta 56 MHz y luego cae deprisa, con tope de 60 dB."""
    return 0 if f <= 56 else min(60, 160 * math.log10(f / 56))


for n, db in sin_filtro.items():
    f = n * F0
    x = x_de(f)
    color = ACC if n == 1 else ALT
    b.append(L(x, Y0, x, y_de(db), f'stroke="{color}" stroke-width="5"'))
    etiqueta = "portadora" if n == 1 else f"{n}.º armónico"
    lado = (x - 8, "end") if n == 4 else (x + 8, "start")
    b.append(T(lado[0], y_de(db) - 6, f"{etiqueta}: {f:.1f}".replace(".", ","), 12, lado[1], fill=color))
    filtrado = db - atenuacion(f)
    if n > 1 and filtrado >= -100:
        b.append(circ(x, y_de(filtrado), 5, f'fill="#ffffff" stroke="{VERDE}" stroke-width="2"'))
# respuesta de un paso bajo (forma ilustrativa) sobre la misma escala
pts = []
for k in range(0, 201):
    f = 1 + k * (FMAX - 1) / 200
    pts.append((x_de(f), y_de(-atenuacion(f))))
b.append(poly(pts, f'stroke="{VERDE}" stroke-width="2" stroke-dasharray="7 5"'))
b.append(T(x_de(175), y_de(-62) + 18, "respuesta del filtro paso bajo", 12, "start", fill=VERDE))
b.append(T(x_de(175), y_de(-62) + 34, "○ armónico tras el filtro", 12, "start", fill=VERDE))
b.append(T((X0 + X1) / 2, 30, "Emisión en 50,2 MHz y sus armónicos", 15, extra='font-weight="600"'))
guarda("08-armonicos.svg", 800, 400, b,
       "Espectro de una emisión en 50,2 megahercios. La portadora está a 0 dBc; los armónicos aparecen en 100,4, 150,6 y 200,8 megahercios con niveles decrecientes. El segundo armónico cae dentro de la banda de radiodifusión en FM, de 87,5 a 108 megahercios. Una curva discontinua verde muestra la respuesta de un filtro paso bajo, que deja pasar la portadora; tras el filtro, el segundo armónico baja unos 40 dB más y el tercero queda por debajo de −90 dBc. Los niveles son ilustrativos.")


# ---------- Figura 8.2: intermodulación ----------
b = []
X0, X1, Y0, YT = 90, 760, 310, 70
F1, F2 = 145.35, 145.60
D = F2 - F1
FMIN, FMAX = F1 - 3 * D, F2 + 3 * D


def x_de(f):
    return X0 + (f - FMIN) / (FMAX - FMIN) * (X1 - X0)


ejes, y_de = ejes_db(X0, Y0, X1, YT, -80, 0, 20, "nivel relativo (dB)")
b += ejes
rayas = [(F1, 0, ACC, "f₁"), (F2, 0, ACC, "f₂"),
         (2 * F1 - F2, -45, ALT, "2f₁ − f₂"), (2 * F2 - F1, -45, ALT, "2f₂ − f₁"),
         (3 * F1 - 2 * F2, -68, ALT, "3f₁ − 2f₂"), (3 * F2 - 2 * F1, -68, ALT, "3f₂ − 2f₁")]
for f, db, color, nombre in rayas:
    x = x_de(f)
    b.append(L(x, Y0, x, y_de(db), f'stroke="{color}" stroke-width="5"'))
    b.append(T(x, y_de(db) - 24, nombre, 13, fill=color))
    b.append(T(x, y_de(db) - 8, f"{f:.3f}".replace(".", ","), 12, fill=color))
b.append(T((X0 + X1) / 2, Y0 + 24, "frecuencia (MHz)", 13))
# cotas de la separación Δ
yc = Y0 - 18
for a, c in ((2 * F1 - F2, F1), (F1, F2), (F2, 2 * F2 - F1)):
    b.append(flecha(x_de(a) + 4, yc, x_de(c) - 4, yc, doble=True, extra='stroke-width="1.2"'))
    b.append(T((x_de(a) + x_de(c)) / 2, yc - 6, "Δ", 13))
b.append(T((X0 + X1) / 2, 30, "Productos de intermodulación de dos señales separadas Δ = 250 kHz", 15, extra='font-weight="600"'))
guarda("08-intermodulacion.svg", 800, 350, b,
       "Dos señales fuertes en 145,350 y 145,600 megahercios, separadas 250 kilohercios, generan en un elemento no lineal productos de tercer orden en 145,100 y 145,850 megahercios, a la misma separación por fuera de cada una, y productos de quinto orden más débiles en 144,850 y 146,100 megahercios. Los niveles son ilustrativos.")


# ---------- Figura 8.3: modo diferencial y modo común en un coaxial ----------
b = []
# coaxial dibujado en sección longitudinal: malla arriba y abajo, vivo en el centro
xa, xb = 150, 690
yc = 150
b.append(rect(xa, yc - 40, xb - xa, 80, "#f5f5f5", f'stroke="{INK}" stroke-width="2"'))
b.append(L(xa, yc - 40, xb, yc - 40, 'stroke-width="5"'))
b.append(L(xa, yc + 40, xb, yc + 40, 'stroke-width="5"'))
b.append(L(xa, yc, xb, yc, f'stroke="{INK}" stroke-width="3"'))
b.append(T(xa - 10, yc + 5, "equipo", 13, "end"))
b.append(T(xb + 10, yc + 5, "antena", 13, "start"))
# corriente por el vivo hacia la antena
b.append(flecha(260, yc - 10, 420, yc - 10, ACC, extra='stroke-width="2.5"'))
b.append(T(340, yc - 16, "I₁ por el vivo", 13, fill=ACC))
# corriente de vuelta por la cara interior de la malla
b.append(flecha(420, yc + 12, 260, yc + 12, ACC, extra='stroke-width="2.5"'))
b.append(T(340, yc + 32, "I₂ por dentro de la malla", 13, fill=ACC))
# corriente en modo común por fuera
b.append(flecha(600, yc + 58, 440, yc + 58, ALT, extra='stroke-width="2.5"'))
b.append(T(520, yc + 78, "I₃ por fuera de la malla: modo común", 13, fill=ALT))
b.append(T(420, yc - 62, "Modo diferencial: I₁ = I₂, opuestas; sus campos se anulan fuera del cable", 13, fill=ACC))
b.append(T(420, 30, "Corrientes en un coaxial", 15, extra='font-weight="600"'))
# segundo dibujo: choque de modo común
y2 = 350
b.append(L(150, y2, 330, y2, 'stroke-width="6"'))
b.append(L(510, y2, 690, y2, 'stroke-width="6"'))
for k in range(5):
    cx = 360 + k * 30
    b.append(f'<ellipse cx="{cx:.1f}" cy="{y2:.1f}" rx="16" ry="34" stroke="{INK}" stroke-width="5"/>')
b.append(rect(345, y2 - 46, 150, 92, "none", f'stroke="{GRIS}" stroke-width="1.5" stroke-dasharray="5 4"'))
b.append(T(420, y2 - 54, "varias espiras de coaxial sobre un toroide de ferrita", 13))
b.append(flecha(250, y2 - 24, 320, y2 - 24, ACC, extra='stroke-width="2.5"'))
b.append(T(240, y2 - 32, "la señal útil pasa", 13, "end", fill=ACC))
b.append(flecha(640, y2 + 24, 520, y2 + 24, ALT, extra='stroke-width="2.5"'))
b.append(L(512, y2 + 12, 528, y2 + 36, f'stroke="{ALT}" stroke-width="3"'))
b.append(L(512, y2 + 36, 528, y2 + 12, f'stroke="{ALT}" stroke-width="3"'))
b.append(T(600, y2 + 58, "el modo común encuentra una impedancia alta", 13, fill=ALT))
b.append(T(420, y2 - 84, "Choque de modo común (balun de corriente)", 14, extra='font-weight="600"'))
guarda("08-modo-comun.svg", 840, 440, b,
       "Arriba, un coaxial en corte longitudinal. La corriente útil va por el vivo y vuelve por la cara interior de la malla con el mismo valor y sentido opuesto, así que sus campos se anulan fuera del cable: es el modo diferencial. Una tercera corriente, en modo común, circula por la cara exterior de la malla y hace que el cable radie y capte. Abajo, un choque formado por varias espiras de coaxial sobre un toroide de ferrita: la señal útil pasa sin notarlo y la corriente en modo común encuentra una impedancia alta.")


# ---------- Figura 8.4: peine de una fuente conmutada ----------
b = []
X0, X1, Y0, YT = 90, 760, 300, 70
FMIN, FMAX = 6.7, 7.5        # MHz
FSW = 0.070                  # 70 kHz


def x_de(f):
    return X0 + (f - FMIN) / (FMAX - FMIN) * (X1 - X0)


b.append(rect(x_de(7.0), YT, x_de(7.2) - x_de(7.0), Y0 - YT, FONDO_BANDA, 'stroke="none"'))
b.append(T((x_de(7.0) + x_de(7.2)) / 2, YT - 8, "banda de 40 m (7,0 a 7,2 MHz)", 12, fill="#e65100"))
ejes, y_de = ejes_db(X0, Y0, X1, YT, 0, 40, 10, "nivel sobre el ruido (dB)")
b += ejes
for k in range(0, 9):
    f = 6.7 + k * 0.1
    b.append(L(x_de(f), Y0, x_de(f), Y0 + 5))
    b.append(T(x_de(f), Y0 + 20, f"{f:.1f}".replace(".", ","), 12))
b.append(T((X0 + X1) / 2, Y0 + 42, "frecuencia (MHz)", 13))
n0 = math.ceil(FMIN / FSW)
n1 = math.floor(FMAX / FSW)
for n in range(n0, n1 + 1):
    f = n * FSW
    nivel = 30 - 6 * abs(f - 7.1)  # forma suave, ilustrativa
    x = x_de(f)
    # cada raya ensanchada: la frecuencia de conmutación deriva con la carga
    b.append(rect(x - 3, y_de(nivel), 6, Y0 - y_de(nivel), ALT, 'stroke="none" fill-opacity="0.85"'))
    if n == 101:
        b.append(T(x - 6, y_de(nivel) - 8, "101 × 70 kHz", 12, "end", fill=ALT))
    if n == 102:
        b.append(T(x + 6, y_de(nivel) - 8, "102 × 70 kHz", 12, "start", fill=ALT))
b.append(flecha(x_de(101 * FSW), y_de(36), x_de(102 * FSW), y_de(36), doble=True, extra='stroke-width="1.2"'))
b.append(T((x_de(101 * FSW) + x_de(102 * FSW)) / 2, y_de(36) - 6, "70 kHz", 12))
b.append(T((X0 + X1) / 2, 30, "Armónicos de una fuente conmutada de 70 kHz", 15, extra='font-weight="600"'))
guarda("08-fuente-conmutada.svg", 800, 370, b,
       "Espectro entre 6,7 y 7,5 megahercios con la banda de 40 metros sombreada. Aparece una fila de rayas separadas 70 kilohercios, los armónicos de una fuente conmutada que trabaja a esa frecuencia; los armónicos 101 y 102 caen en 7,070 y 7,140 megahercios, dentro de la banda. Las rayas son anchas porque la frecuencia de conmutación varía con la carga. Los niveles son ilustrativos.")

print("Figuras del capítulo 08 generadas en", OUT)
