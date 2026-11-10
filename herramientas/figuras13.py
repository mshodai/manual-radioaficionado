"""Genera las figuras SVG del capítulo 13 (dibujo propio).

Uso, desde la raíz del repositorio:
    python3 herramientas/figuras13.py docs/assets/figuras

Figuras:
- 13-orbitas.svg: órbita baja y geoestacionaria a escala, y detalle del tramo de
  órbita baja que ve una estación durante un pase cenital.
- 13-doppler.svg: desplazamiento Doppler en 437 MHz durante un pase cenital y un
  pase bajo de un satélite a 800 km (órbita circular, sin el giro de la Tierra).
- 13-qo100-plan.svg: plan de banda del transpondedor estrecho del QO-100 según
  AMSAT-DL (https://amsat-dl.org/en/p4-a-nb-transponder-bandplan-and-operating-guidelines/,
  comprobado en noviembre de 2026).

Reglas de legibilidad de ESTILO.md: letra de 12 px como mínimo y viewBox de
700 px de ancho como máximo.
"""
import math
import os
import sys

OUT = sys.argv[1]
INK = "#1a1a1a"
ACC = "#1565c0"   # azul
ALT = "#c62828"   # rojo
VERDE = "#2e7d32"
GRIS = "#9e9e9e"
GRIS_T = "#555555"
CLARO = "#eeeeee"
NARANJA = "#fff3e0"
AZUL_CLARO = "#e3f2fd"
VERDE_CLARO = "#e8f5e9"
ROJO_CLARO = "#ffebee"
TIERRA = "#cfe3f5"

MU = 398600.4418     # km³/s²
R = 6371.0           # km
C = 299792.458       # km/s


def svg(w, h, body, title, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{title}</title>
<defs>
  <marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
  </marker>
{defs}
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


def circ(cx, cy, r, extra=""):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {extra}/>'


def flecha(x1, y1, x2, y2, extra=""):
    return L(x1, y1, x2, y2, f'marker-end="url(#flecha)" {extra}')


def guarda(nombre, w, h, cuerpo, titulo, defs=""):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(svg(w, h, cuerpo, titulo, defs))
    print("escrito", nombre)


# ---------------------------------------------------------------------------
# 13-orbitas.svg
# ---------------------------------------------------------------------------
def orbitas():
    W, H = 700, 440
    c = []
    # Panel izquierdo, a escala: radio GEO = 42 164 km
    cx, cy, rg = 185, 225, 160
    k = rg / 42164.0
    rt = R * k
    rl = (R + 800) * k
    c.append(T(cx, 30, "A escala", 14, extra='font-weight="600"'))
    c.append(circ(cx, cy, rg, f'stroke="{ACC}" stroke-dasharray="6 5"'))
    c.append(circ(cx, cy, rl, f'stroke="{ALT}" stroke-width="1.5"'))
    c.append(circ(cx, cy, rt, f'fill="{TIERRA}" stroke="{INK}" stroke-width="1.5"'))
    # Satélite geoestacionario y su huella (tangentes a la Tierra)
    sx, sy = cx + rg, cy
    c.append(circ(sx, sy, 6, f'fill="{ACC}" stroke="none"'))
    ang = math.asin(rt / rg)
    for sgn in (-1, 1):
        a = math.pi + sgn * ang
        # punto de tangencia
        d = math.sqrt(rg * rg - rt * rt)
        tx, ty = sx + d * math.cos(a), sy + d * math.sin(a)
        c.append(L(sx, sy, tx, ty, f'stroke="{ACC}" stroke-width="1" opacity="0.7"'))
    c.append(T(sx - 4, sy - 16, "QO-100", 13, "end", fill=ACC))
    c.append(T(cx, cy + rg + 26, "Órbita geoestacionaria: 35 786 km", 13, fill=ACC))
    c.append(flecha(cx - 70, cy - 72, cx - rl * 0.62, cy - rl * 0.80, f'stroke="{ALT}" stroke-width="1.5"'))
    c.append(T(cx - 72, cy - 78, "Órbita baja", 13, "end", fill=ALT))
    c.append(T(cx - 72, cy - 62, "(800 km)", 12, "end", fill=ALT))

    # Separador
    c.append(L(372, 50, 372, 400, f'stroke="{GRIS}" stroke-width="1" stroke-dasharray="3 4"'))

    # Panel derecho, detalle de un pase cenital
    c.append(T(535, 30, "Detalle de un pase", 14, extra='font-weight="600"'))
    ex, ey, re = 535, 500, 230
    ro = re * (R + 800) / R
    c.append(f'<g clip-path="url(#recorte)">')
    c.append(circ(ex, ey, ro, f'stroke="{ALT}" stroke-width="1.5"'))
    c.append(circ(ex, ey, re, f'fill="{TIERRA}" stroke="{INK}" stroke-width="1.5"'))
    c.append('</g>')
    stx, sty = ex, ey - re
    # Horizonte de la estación
    dx = math.sqrt(ro * ro - re * re)
    c.append(L(stx - dx - 20, sty, stx + dx + 20, sty, f'stroke="{GRIS_T}" stroke-width="1.2" stroke-dasharray="5 4"'))
    c.append(T(stx - dx + 8, sty + 17, "Horizonte", 12, "start", fill=GRIS_T))
    # Arco visible
    a0 = math.atan2(-(sty - ey), -dx)
    a1 = math.atan2(-(sty - ey), dx)
    x0, y0 = ex - dx, sty
    x1, y1 = ex + dx, sty
    c.append(f'<path d="M{x0:.1f},{y0:.1f} A{ro:.1f},{ro:.1f} 0 0 1 {x1:.1f},{y1:.1f}" stroke="{ALT}" stroke-width="4"/>')
    c.append(circ(x0, y0, 5, f'fill="{ALT}" stroke="none"'))
    c.append(circ(x1, y1, 5, f'fill="{ALT}" stroke="none"'))
    c.append(T(x0, y0 - 14, "AOS", 13, fill=ALT))
    c.append(T(x1, y1 - 14, "LOS", 13, fill=ALT))
    c.append(flecha(ex - 20, ey - ro - 12, ex + 20, ey - ro - 12, f'stroke="{ALT}" stroke-width="1.5"'))
    c.append(T(ex, ey - ro - 20, "Tramo visible", 13, fill=ALT))
    # Estación
    c.append(circ(stx, sty, 5, f'fill="{INK}" stroke="none"'))
    c.append(T(stx, sty + 22, "Estación", 13))
    c.append(T(535, 360, "Tierra", 13, fill=GRIS_T))
    defs = '  <clipPath id="recorte"><rect x="380" y="50" width="310" height="370"/></clipPath>'
    guarda("13-orbitas.svg", W, H, "\n".join(c),
           "Órbita baja y geoestacionaria a escala, y tramo de órbita baja visible desde una estación entre la adquisición y la pérdida de señal",
           defs)


# ---------------------------------------------------------------------------
# 13-doppler.svg
# ---------------------------------------------------------------------------
def doppler_pase(h, f_mhz, delta_deg, paso=1.0):
    """Doppler (kHz) frente al tiempo (min) para una órbita circular de altura h,
    con la estación a delta_deg grados (ángulo central) del plano orbital.
    Sin el giro de la Tierra. Devuelve [(t_min, df_khz, elev_deg)] con elev > 0."""
    r = R + h
    w = math.sqrt(MU / r ** 3)          # rad/s
    d = math.radians(delta_deg)
    est = (R * math.cos(d), 0.0, R * math.sin(d))
    pts = []
    t = -1200.0
    while t <= 1200.0:
        th = w * t
        sat = (r * math.cos(th), r * math.sin(th), 0.0)
        vel = (-r * w * math.sin(th), r * w * math.cos(th), 0.0)
        rho = tuple(s - e for s, e in zip(sat, est))
        dist = math.sqrt(sum(x * x for x in rho))
        vr = sum(a * b for a, b in zip(rho, vel)) / dist      # >0 si se aleja
        sen_el = sum(a * b for a, b in zip(rho, est)) / (dist * R)
        el = math.degrees(math.asin(sen_el))
        if el > 0:
            pts.append((t / 60, -f_mhz * 1e3 * vr / C, el))
        t += paso
    return pts


def doppler():
    W, H = 700, 380
    x0, x1 = 90, 670
    y0, y1 = 50, 310
    tmin, tmax = -8.0, 8.0
    fmin, fmax = -12.0, 12.0

    def X(t):
        return x0 + (t - tmin) / (tmax - tmin) * (x1 - x0)

    def Y(f):
        return y1 - (f - fmin) / (fmax - fmin) * (y1 - y0)

    c = []
    # Rejilla y ejes
    for f in range(-12, 13, 4):
        c.append(L(x0, Y(f), x1, Y(f), f'stroke="{CLARO}" stroke-width="1"'))
        c.append(T(x0 - 8, Y(f) + 4, f"{f:+d}".replace("+0", "0").replace("-", "−"), 12, "end"))
    for t in range(-8, 9, 2):
        c.append(L(X(t), y0, X(t), y1, f'stroke="{CLARO}" stroke-width="1"'))
        c.append(T(X(t), y1 + 18, f"{t:d}".replace("-", "−"), 12))
    c.append(L(x0, Y(0), x1, Y(0), f'stroke="{GRIS}" stroke-width="1.2"'))
    c.append(L(x0, y0, x0, y1))
    c.append(L(x0, y1, x1, y1))
    c.append(T(x1, y1 + 38, "Minutos desde el punto más cercano del pase", 12, "end", fill=GRIS_T))
    c.append(T(24, (y0 + y1) / 2, "Desplazamiento (kHz)", 12, extra=f'transform="rotate(-90 24 {(y0 + y1) / 2:.1f})"', fill=GRIS_T))

    # Curvas
    cen = doppler_pase(800, 437.0, 0.0)
    baj = doppler_pase(800, 437.0, 19.0)
    for pts, col in ((cen, ALT), (baj, ACC)):
        d = " ".join(f"{'M' if i == 0 else 'L'}{X(t):.1f},{Y(f):.1f}" for i, (t, f, _) in enumerate(pts))
        c.append(f'<path d="{d}" stroke="{col}" stroke-width="2.5"/>')
    el_baj = max(e for _, _, e in baj)

    # Leyenda
    c.append(L(X(1.2), Y(9.5), X(2.0), Y(9.5), f'stroke="{ALT}" stroke-width="2.5"'))
    c.append(T(X(2.2), Y(9.5) + 4, "Pase cenital (elevación máx. 90°)", 13, "start"))
    c.append(L(X(1.2), Y(7.3), X(2.0), Y(7.3), f'stroke="{ACC}" stroke-width="2.5"'))
    c.append(T(X(2.2), Y(7.3) + 4, f"Pase bajo (elevación máx. {el_baj:.0f}°)", 13, "start"))
    c.append(T(X(-7.6), Y(-7.5), "Se acerca: frecuencia más alta", 12, "start", fill=GRIS_T))
    c.append(T(X(7.6), Y(-2.5), "Se aleja: frecuencia más baja", 12, "end", fill=GRIS_T))
    c.append(T(x0, 30, "Satélite a 800 km, señal emitida en 437 MHz", 14, "start", 'font-weight="600"'))
    guarda("13-doppler.svg", W, H, "\n".join(c),
           "Desplazamiento Doppler frente al tiempo durante un pase cenital y un pase bajo de un satélite a 800 km en 437 MHz")
    return el_baj, cen, baj


# ---------------------------------------------------------------------------
# 13-qo100-plan.svg
# ---------------------------------------------------------------------------
def qo100():
    W, H = 700, 380
    x0, x1 = 40, 660
    f0, f1 = 500.0, 1000.0           # kHz por encima de 10 489 MHz

    def X(f):
        return x0 + (f - f0) / (f1 - f0) * (x1 - x0)

    yb, hb = 150, 56
    c = []
    tramos = [
        (505, 540, CLARO, "CW"),
        (540, 580, AZUL_CLARO, "Dig."),
        (580, 650, VERDE_CLARO, "Digital"),
        (650, 745, NARANJA, "BLU"),
        (755, 850, NARANJA, "BLU"),
        (850, 857.5, ROJO_CLARO, ""),
        (857.5, 865, "#ffcdd2", ""),
        (865, 990, "#f3e5f5", "Mixto y concursos"),
    ]
    for a, b, col, nom in tramos:
        c.append(rect(X(a), yb, X(b) - X(a), hb, col, f'stroke="{GRIS}" stroke-width="1"'))
        if nom:
            c.append(T((X(a) + X(b)) / 2, yb + hb / 2 + 5, nom, 13))
    # Balizas
    for f, nom, yt in ((500, "Baliza inferior (CW)", 92), (750, "Baliza central (BPSK)", 92),
                       (993.5, "Baliza multimedia", 112), (1000, "Baliza superior (CW)", 92)):
        c.append(L(X(f), yb - 6, X(f), yb + hb + 6, f'stroke="{ALT}" stroke-width="3"'))
    c.append(flecha(X(500) + 2, 100, X(500), yb - 8, f'stroke="{ALT}" stroke-width="1.2"'))
    c.append(T(X(500) - 4, 94, "Baliza inferior (CW)", 12, "start", fill=ALT))
    c.append(flecha(X(750), 100, X(750), yb - 8, f'stroke="{ALT}" stroke-width="1.2"'))
    c.append(T(X(750), 94, "Baliza central (BPSK)", 12, fill=ALT))
    c.append(flecha(X(1000) - 2, 80, X(1000), yb - 8, f'stroke="{ALT}" stroke-width="1.2"'))
    c.append(T(X(1000) + 4, 74, "Baliza superior (CW)", 12, "end", fill=ALT))
    c.append(flecha(X(993.5) - 2, 122, X(993.5), yb - 8, f'stroke="{ALT}" stroke-width="1.2"'))
    c.append(T(X(993.5) - 6, 118, "Baliza multimedia", 12, "end", fill=ALT))
    # Difusión y emergencia
    c.append(flecha(X(830), yb + hb + 46, X(853.75), yb + hb + 4, 'stroke-width="1.2"'))
    c.append(T(X(828), yb + hb + 60, "Difusión", 12, "end"))
    c.append(flecha(X(880), yb + hb + 46, X(861.25), yb + hb + 4, f'stroke="{ALT}" stroke-width="1.2"'))
    c.append(T(X(882), yb + hb + 60, "Emergencia (10 489,860)", 12, "start", fill=ALT))

    # Ejes de bajada y subida
    ya = yb + hb + 96
    c.append(L(x0, ya, x1, ya))
    for f in range(500, 1001, 100):
        c.append(L(X(f), ya, X(f), ya + 6))
        c.append(T(X(f), ya + 22, "10 490,000" if f == 1000 else f"10 489,{f:03d}", 12))
    c.append(T(x0, ya - 10, "Bajada (MHz)", 12, "start", fill=GRIS_T))
    ys = ya + 50
    c.append(L(x0, ys, x1, ys, f'stroke="{GRIS_T}"'))
    for f in range(500, 1001, 100):
        c.append(L(X(f), ys, X(f), ys + 6, f'stroke="{GRIS_T}"'))
        c.append(T(X(f), ys + 22, f"2400,{f - 500:03d}", 12, fill=GRIS_T))
    c.append(T(x0, ys - 10, "Subida (MHz)", 12, "start", fill=GRIS_T))
    c.append(T(x0, 36, "QO-100, transpondedor de banda estrecha", 14, "start", 'font-weight="600"'))
    guarda("13-qo100-plan.svg", W, H, "\n".join(c),
           "Plan de banda del transpondedor estrecho del QO-100 con sus balizas, tramos y frecuencias de subida y bajada")


orbitas()
el_baj, _, _ = doppler()
print(f"elevación máxima del pase bajo: {el_baj:.1f}°")
qo100()
