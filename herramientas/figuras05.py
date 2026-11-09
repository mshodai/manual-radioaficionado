"""Genera las figuras SVG del capítulo 05 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras05.py docs/assets/figuras

Datos externos que usa la figura 5.3 (ciclo solar): número de manchas mensual
suavizado (13 meses) de SILSO, Real Observatorio de Bélgica, fichero
https://www.sidc.be/SILSO/DATA/SN_ms_tot_V2.0.txt, descargado el 9 de noviembre
de 2026. Se toma un valor cada tres meses más los mínimos y máximos. Los valores
de 2026 están marcados como provisionales en el fichero.

Datos de la figura 5.5 (balizas del IBP): orden de turnos de la tabla de
https://www.ncdxf.org/beacon/beaconlocations.html, horario imprimible
https://www.ncdxf.org/beacon/ibp.pdf y regla de rotación del reloj oficial
https://www.ncdxf.org/beacon/BeaconClock.js (comprobados el 9 de noviembre
de 2026).
"""
import math, sys, os

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul: lo principal
ALT = "#c62828"   # rojo: lo que se pierde o se resalta
VERDE = "#2e7d32"
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


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>'


def flecha(x1, y1, x2, y2, color=INK, doble=False):
    m = "flecha-acc" if color == ACC else "flecha"
    ini = f'marker-start="url(#{m})" ' if doble else ""
    return L(x1, y1, x2, y2, f'stroke="{color}" {ini}marker-end="url(#{m})"')


def guarda(nombre, w, h, cuerpo, titulo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, "\n".join(cuerpo), titulo))


# ---------- Figura 5.1: capas de la ionosfera de día y de noche ----------
b = []
x_eje, y_suelo, esc = 70, 330, 0.65   # 0,65 px por km
def yk(km):
    return y_suelo - km * esc
# eje de altitud
b.append(flecha(x_eje, y_suelo, x_eje, yk(470)))
b.append(T(x_eje - 8, yk(470) + 4, "km", 13, "end"))
for km in (0, 100, 200, 300, 400):
    b.append(L(x_eje - 5, yk(km), x_eje, yk(km)))
    b.append(T(x_eje - 9, yk(km) + 5, str(km), 12, "end"))
b.append(L(x_eje, y_suelo, 640, y_suelo, f'stroke="{INK}"'))
capas_dia = [("D", 60, 90, "#fff3e0"), ("E", 90, 130, "#ffe0b2"),
             ("F1", 150, 220, "#bbdefb"), ("F2", 250, 400, "#90caf9")]
capas_noche = [("E (débil)", 95, 125, "#fff3e0"), ("F", 250, 400, "#bbdefb")]
for x0, titulo, capas in ((110, "De día", capas_dia), (390, "De noche", capas_noche)):
    w = 230
    b.append(T(x0 + w / 2, 22, titulo, 16, extra='font-weight="600"'))
    for nombre, a, c, color in capas:
        b.append(rect(x0, yk(c), w, yk(a) - yk(c), color, f'stroke="{GRIS}" stroke-width="1"'))
        b.append(T(x0 + w / 2, (yk(a) + yk(c)) / 2 + 5, nombre, 14))
# notas
b.append(T(225, y_suelo + 24, "la D absorbe las frecuencias bajas", 12, fill=ALT))
b.append(T(505, y_suelo + 24, "sin D: las bandas bajas llegan lejos", 12, fill=VERDE))
guarda("05-ionosfera.svg", 660, 370, b,
       "Capas de la ionosfera. De día hay cuatro: D entre 60 y 90 km, E entre 90 y 130 km, F1 entre 150 y 220 km y F2 entre 250 y 400 km. De noche desaparece la D, la E se debilita y F1 y F2 se funden en una sola capa F.")

# ---------- Figura 5.2: salto y zona de silencio ----------
b = []
cx, R, H = 360, 1400, 110       # centro horizontal, radio de la Tierra y altura de la capa (px, exagerada)
cy = 200 + R                    # el punto de emisión queda en y = 200
def tierra(phi, r=R):
    return cx + r * math.sin(phi), cy - r * math.cos(phi)
phi0 = -0.2                     # el emisor está a la izquierda
# superficie y capa
b.append(poly([tierra(phi0 + k * 0.005) for k in range(-10, 100)], f'stroke="{INK}" stroke-width="2.5"'))
b.append(poly([tierra(phi0 + k * 0.005, R + H) for k in range(-10, 100)], f'stroke="#90caf9" stroke-width="16" opacity="0.7"'))
xl, yl = tierra(phi0 - 0.03, R + H + 16)
b.append(T(xl, yl, "capa F", 13, "start"))
# antena emisora
xe, ye = tierra(phi0)
b.append(L(xe, ye, xe, ye - 26, f'stroke="{INK}" stroke-width="3"'))
b.append(T(xe - 8, ye - 12, "emisor", 13, "end"))
# onda de superficie
b.append(poly([tierra(phi0 + k * 0.002, R + 6) for k in range(0, 31)], f'stroke="{VERDE}" stroke-width="3"'))
xg, yg = tierra(phi0, R - 22)
b.append(T(xg - 30, yg + 4, "onda de superficie", 12, "start", fill=VERDE))
# rayos: semiángulo central de cada salto
def rayo(semi, color, ancho=2.2, sigue=False):
    p1 = tierra(phi0 + semi, R + H)
    p2 = tierra(phi0 + 2 * semi)
    out = [L(xe, ye - 26, *p1, f'stroke="{color}" stroke-width="{ancho}"')]
    if sigue:
        dx, dy = p1[0] - xe, p1[1] - (ye - 26)
        out.append(L(*p1, p1[0] + dx * 0.35, p1[1] + dy * 0.35, f'stroke="{color}" stroke-width="{ancho}" stroke-dasharray="6 5"'))
    else:
        out.append(L(*p1, *p2, f'stroke="{color}" stroke-width="{ancho}"'))
    return out
b += rayo(0.045, ALT, sigue=True)     # muy empinado: atraviesa
b += rayo(0.09, ACC)                  # primer rayo que vuelve: distancia de salto
b += rayo(0.16, ACC)                  # más rasante: llega más lejos
xt, yt = tierra(phi0 + 0.045, R + H + 60)
b.append(T(xt + 10, yt - 4, "ángulo demasiado alto: se escapa", 12, "start", fill=ALT))
# zona de silencio entre el fin de la onda de superficie y el primer retorno
a1, a2 = phi0 + 0.062, phi0 + 0.18
b.append(poly([tierra(a1 + k * (a2 - a1) / 40, R - 14) for k in range(41)], f'stroke="{ALT}" stroke-width="1.5" stroke-dasharray="4 4"'))
xs, ys = tierra((a1 + a2) / 2 + 0.03, R - 44)
b.append(T(xs, ys + 4, "zona de silencio", 13, fill=ALT))
# distancia de salto
d1 = [tierra(phi0 + k * 0.18 / 40, R - 72) for k in range(41)]
b.append(poly(d1, f'stroke="{INK}" stroke-width="1.2"'))
b.append(L(*tierra(phi0, R - 65), *tierra(phi0, R - 79), 'stroke-width="1.2"'))
b.append(L(*tierra(phi0 + 0.18, R - 65), *tierra(phi0 + 0.18, R - 79), 'stroke-width="1.2"'))
xd, yd = tierra(phi0 + 0.09, R - 94)
b.append(T(xd, yd + 4, "distancia de salto", 13))
xr, yr = tierra(phi0 + 0.32, R - 22)
b.append(T(xr, yr + 4, "un salto más largo", 12, fill=ACC))
guarda("05-salto.svg", 700, 330, b,
       "Un emisor lanza rayos hacia la capa F. El más empinado la atraviesa y se pierde en el espacio. Los menos inclinados vuelven a la Tierra: el primero que vuelve marca la distancia de salto, y entre el final de la onda de superficie y ese punto queda la zona de silencio.")

# ---------- Figura 5.3: ciclo solar ----------
# (año, mes, número de manchas suavizado) — SILSO, descargado el 9-11-2026
SSN = [(2008, 1, 6.6), (2008, 4, 5.1), (2008, 7, 4.0), (2008, 10, 2.4), (2008, 12, 2.2), (2009, 1, 2.5), (2009, 4, 3.3), (2009, 7, 5.5), (2009, 10, 10.9), (2010, 1, 14.0), (2010, 4, 20.8), (2010, 7, 25.2), (2010, 10, 34.5), (2011, 1, 45.7), (2011, 4, 61.1), (2011, 7, 83.6), (2011, 10, 87.4), (2012, 1, 95.5), (2012, 4, 95.1), (2012, 7, 84.5), (2012, 10, 85.8), (2013, 1, 86.8), (2013, 4, 84.3), (2013, 7, 94.6), (2013, 10, 107.0), (2014, 1, 109.3), (2014, 4, 116.4), (2014, 7, 112.6), (2014, 10, 97.3), (2015, 1, 89.3), (2015, 4, 78.9), (2015, 7, 68.3), (2015, 10, 64.3), (2016, 1, 54.4), (2016, 4, 47.8), (2016, 7, 38.5), (2016, 10, 31.5), (2017, 1, 27.8), (2017, 4, 24.8), (2017, 7, 21.0), (2017, 10, 16.7), (2018, 1, 14.2), (2018, 4, 7.8), (2018, 7, 7.0), (2018, 10, 6.8), (2019, 1, 5.4), (2019, 4, 4.3), (2019, 7, 3.5), (2019, 10, 2.6), (2019, 12, 1.8), (2020, 1, 2.2), (2020, 4, 3.6), (2020, 7, 9.0), (2020, 10, 11.9), (2021, 1, 17.3), (2021, 4, 24.8), (2021, 7, 31.4), (2021, 10, 45.2), (2022, 1, 60.1), (2022, 4, 73.0), (2022, 7, 86.7), (2022, 10, 98.9), (2023, 1, 113.3), (2023, 4, 122.9), (2023, 7, 124.6), (2023, 10, 124.8), (2024, 1, 131.2), (2024, 4, 144.4), (2024, 7, 155.0), (2024, 10, 160.9), (2025, 1, 146.2), (2025, 4, 133.3), (2025, 7, 122.5), (2025, 10, 108.5), (2026, 1, 104.1), (2026, 4, 88.6)]
b = []
gx0, gx1, gy0, gy1 = 70, 640, 300, 40       # caja del gráfico
a0, a1, smax = 2008, 2027, 180
def px(anio, mes):
    return gx0 + (anio + (mes - 0.5) / 12 - a0) / (a1 - a0) * (gx1 - gx0)
def py(v):
    return gy0 - v / smax * (gy0 - gy1)
for v in range(0, 181, 40):
    b.append(L(gx0, py(v), gx1, py(v), f'stroke="#e0e0e0" stroke-width="1"'))
    b.append(T(gx0 - 8, py(v) + 4, str(v), 12, "end"))
for anio in range(2008, 2028, 2):
    x = px(anio, 0.5)
    b.append(L(x, gy0, x, gy0 + 5))
    b.append(T(x, gy0 + 20, str(anio), 12))
b.append(L(gx0, gy0, gx1, gy0))
b.append(L(gx0, gy0, gx0, gy1))
b.append(T(gx0, gy1 - 14, "número de manchas suavizado (13 meses)", 13, "start"))
b.append(poly([(px(a, m), py(v)) for a, m, v in SSN], f'stroke="{ACC}" stroke-width="2.5"'))
hitos = [((2008, 12, 2.2), "mínimo", 8, -10), ((2014, 4, 116.4), "máximo del ciclo 24", 0, -12),
         ((2019, 12, 1.8), "mínimo", 8, -10), ((2024, 10, 160.9), "máximo del ciclo 25: 160,9", -6, -12),
         ((2026, 4, 88.6), "abril de 2026: 88,6", -8, 22)]
for (a, m, v), txt, dx, dy in hitos:
    b.append(f'<circle cx="{px(a, m):.1f}" cy="{py(v):.1f}" r="4" fill="{ALT}" stroke="none"/>')
    anc = "end" if dx < 0 else ("start" if dx > 0 else "middle")
    b.append(T(px(a, m) + dx, py(v) + dy, txt, 12, anc))
b.append(T(px(2011, 6), gy0 - 140, "ciclo 24", 14, fill=ACC, extra='font-weight="600"'))
b.append(T(px(2021, 9), gy0 - 140, "ciclo 25", 14, fill=ACC, extra='font-weight="600"'))
guarda("05-ciclo-solar.svg", 680, 340, b,
       "Número de manchas solares suavizado de 2008 a abril de 2026, según SILSO. Mínimo en diciembre de 2008, máximo del ciclo 24 en abril de 2014 con 116,4, mínimo en diciembre de 2019 con 1,8, máximo del ciclo 25 en octubre de 2024 con 160,9 y descenso hasta 88,6 en abril de 2026.")

# ---------- Figura 5.4: horizonte radioeléctrico ----------
b = []
cx, R = 350, 600
cy = 250 + R
def sup(phi, r=R):
    return cx + r * math.sin(phi), cy - r * math.cos(phi)
b.append(poly([sup(-0.55 + k * 0.01) for k in range(111)], f'stroke="{INK}" stroke-width="2.5"'))
# antenas exageradas
h1, h2 = 80, 50
pA, pB = -0.42, 0.38
xA, yA = sup(pA); xA2, yA2 = sup(pA, R + h1)
xB, yB = sup(pB); xB2, yB2 = sup(pB, R + h2)
b.append(L(xA, yA, xA2, yA2, 'stroke-width="3"'))
b.append(L(xB, yB, xB2, yB2, 'stroke-width="3"'))
b.append(T(xA2 - 8, yA2 - 6, "h₁", 15, "end"))
b.append(T(xB2 + 8, yB2 - 6, "h₂", 15, "start"))
# punto de tangencia de cada antena
t1 = pA + math.acos(R / (R + h1))
t2 = pB - math.acos(R / (R + h2))
xT1, yT1 = sup(t1); xT2, yT2 = sup(t2)
b.append(L(xA2, yA2, xT1, yT1, f'stroke="{ACC}" stroke-width="2.2"'))
b.append(L(xB2, yB2, xT2, yT2, f'stroke="{ACC}" stroke-width="2.2"'))
b.append(f'<circle cx="{xT1:.1f}" cy="{yT1:.1f}" r="4" fill="{ALT}" stroke="none"/>')
b.append(f'<circle cx="{xT2:.1f}" cy="{yT2:.1f}" r="4" fill="{ALT}" stroke="none"/>')
b.append(T((xA2 + xT1) / 2, (yA2 + yT1) / 2 - 12, "d₁", 15, fill=ACC))
b.append(T((xB2 + xT2) / 2, (yB2 + yT2) / 2 - 12, "d₂", 15, fill=ACC))
b.append(T(350, 40, "alcance en visión directa: d = d₁ + d₂", 15))
b.append(T(350, 62, "d (km) ≈ 4,12 · (√h₁ + √h₂), con h en metros", 14))
b.append(T(350, 330, "la curvatura y las alturas están exageradas", 12, fill=GRIS))
guarda("05-horizonte.svg", 700, 350, b,
       "Dos antenas de alturas h1 y h2 sobre una Tierra curva. Desde cada una, una línea tangente a la superficie marca su horizonte; el alcance en visión directa es la suma de las dos distancias.")

# ---------- Figura 5.5: turnos de las balizas del IBP ----------
BALIZAS = ["4U1UN", "VE8AT", "W6WX", "KH6RS", "ZL6B", "VK6RBP", "JA2IGY", "RR9O", "VR2B",
           "4S7B", "ZS6DN", "5Z4B", "4X6TU", "OH2B", "CS3B", "LU4AA", "OA4B", "YV5B"]
BANDAS = ["14 100", "18 110", "21 150", "24 930", "28 200"]
b = []
x0, y0, cw, ch, colt = 20, 58, 104, 21, 120
b.append(T(x0, 22, "Segundos desde el inicio del ciclo y baliza que suena en cada frecuencia (kHz)", 13, "start"))
b.append(T(x0 + colt / 2, y0 - 10, "segundos", 13, extra='font-weight="600"'))
for j, f in enumerate(BANDAS):
    b.append(T(x0 + colt + j * cw + cw / 2, y0 - 10, f, 13, extra='font-weight="600"'))
for n in range(18):
    y = y0 + n * ch
    fondo = "#f5f5f5" if n % 2 else "#ffffff"
    b.append(rect(x0, y, colt + 5 * cw, ch, fondo, 'stroke="none"'))
    b.append(T(x0 + colt / 2, y + 15, f"{n * 10}–{n * 10 + 10}", 12))
    for j in range(5):
        baliza = BALIZAS[(n - j) % 18]
        cx = x0 + colt + j * cw
        if baliza == "CS3B":
            b.append(rect(cx + 2, y + 2, cw - 4, ch - 4, "#ffcdd2", 'stroke="none" rx="3"'))
        b.append(T(cx + cw / 2, y + 15, baliza, 12, fill=ALT if baliza == "CS3B" else INK))
b.append(L(x0, y0, x0 + colt + 5 * cw, y0, 'stroke-width="1"'))
b.append(L(x0, y0 + 18 * ch, x0 + colt + 5 * cw, y0 + 18 * ch, 'stroke-width="1"'))
b.append(T(x0, y0 + 18 * ch + 22, "El ciclo dura 3 minutos y vuelve a empezar en el segundo 0 de cada minuto múltiplo de 3 (UTC).", 12, "start"))
guarda("05-ibp.svg", 660, 470, b,
       "Tabla de turnos del IBP: 18 franjas de 10 segundos en filas y las cinco frecuencias en columnas. Cada baliza sube de frecuencia en cada franja; CS3B, en Madeira, está resaltada: suena de 140 a 180 segundos en las cuatro primeras frecuencias y en 28 200 kHz durante los 10 primeros segundos del ciclo.")

print("Figuras del capítulo 05 generadas en", OUT)
