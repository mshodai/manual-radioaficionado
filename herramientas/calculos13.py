"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 13.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos13.py

Modelo: órbitas circulares, Tierra esférica de 6 371 km de radio (6 378,137 km,
el ecuatorial, para la órbita geoestacionaria y el apuntado al QO-100), sin el
giro de la Tierra en los pases de órbita baja. Las alturas de 400 y 800 km son
supuestos de los ejemplos, no datos de ningún satélite concreto.

Datos de partida (todos comprobados en noviembre de 2026):
- Frecuencias de SO-50, AO-123, RS-44, FO-29, AO-7, JO-97, AO-73 e ISS: listas de
  satélites FM y lineales de AMSAT (actualizadas el 31-10-2026).
- QO-100: posición 25,9° E (web del receptor del BATC); transpondedor estrecho,
  subida 2 400,000-2 400,500 MHz y bajada 10 489,500-10 490,000 MHz, sin invertir
  (plan de banda de AMSAT-DL).
- Régimen general de 13 cm: 1 000 W p. i. r. e. en el apartado 3.1 del anexo I
  de la Orden IET/1311/2013, al 50 % por ser banda secundaria (apartado 3.2).
- Autorización para el QO-100: resolución de la Secretaría de Estado de
  Telecomunicaciones e Infraestructuras Digitales de 4-12-2025, vigente hasta el
  26-12-2026 (página de autorizaciones de uso temporal del Ministerio):
  2 400-2 410 MHz, 1 500 W p. i. r. e. y antenas directivas de 21,5 dBi o más.
- Fórmula de la pérdida en el espacio libre con la constante 32,44 del capítulo 5.
"""
import math

fallos = 0

MU = 398600.4418      # km³/s², constante gravitatoria terrestre
R = 6371.0            # km, radio medio
RE = 6378.137         # km, radio ecuatorial
C = 299792.458        # km/s
DIA_SIDEREO = 86164.0905  # s


def comprueba(nombre, calculado, en_texto, tol=0.006):
    """Compara con tolerancia relativa (0,6 % por defecto, por los redondeos)."""
    global fallos
    ok = abs(calculado - en_texto) <= tol * max(abs(en_texto), 1e-12)
    print(f"{'OK ' if ok else 'MAL'} {nombre}: calculado {calculado:.6g}, en el texto {en_texto}")
    if not ok:
        fallos += 1


def cierto(nombre, condicion):
    global fallos
    print(f"{'OK ' if condicion else 'MAL'} {nombre}")
    if not condicion:
        fallos += 1


def velocidad(r):
    return math.sqrt(MU / r)


def periodo(r):
    return 2 * math.pi * math.sqrt(r ** 3 / MU)


def doppler_khz(f_mhz, v_kms):
    return f_mhz * 1e3 * v_kms / C


def l_el(d_km, f_mhz):
    """Pérdida en el espacio libre (dB), como en el capítulo 5."""
    return 32.44 + 20 * math.log10(d_km) + 20 * math.log10(f_mhz)


def distancia(h, elev_deg):
    """Distancia a un satélite a h km de altura visto con una elevación dada."""
    r = R + h
    e = math.radians(elev_deg)
    return math.sqrt(r * r - (R * math.cos(e)) ** 2) - R * math.sin(e)


def ganancia_plato(d_m, f_mhz, eta=0.6):
    lam = C * 1e3 / (f_mhz * 1e6)
    return eta * (math.pi * d_m / lam) ** 2


def apuntado(lat, lon, lon_sat=25.9):
    """Azimut, elevación (grados) y distancia (km) a un geoestacionario."""
    rg = (MU * DIA_SIDEREO ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
    phi = math.radians(lat)
    dl = math.radians(lon_sat - lon)
    cg = math.cos(phi) * math.cos(dl)
    g = math.acos(cg)
    el = math.degrees(math.atan((cg - RE / rg) / math.sin(g)))
    az = 180 - math.degrees(math.atan2(math.tan(dl), math.sin(phi)))
    d = math.sqrt(RE ** 2 + rg ** 2 - 2 * RE * rg * cg)
    return az, el, d


# ---------- Órbita baja: satélite a 800 km ----------
r800 = R + 800
comprueba("800 km: radio de la órbita (km)", r800, 7171)
comprueba("800 km: velocidad (km/s)", velocidad(r800), 7.46)
comprueba("800 km: periodo (s)", periodo(r800), 6040, tol=0.002)
comprueba("800 km: periodo (min)", periodo(r800) / 60, 101, tol=0.005)
comprueba("800 km: vueltas al día", 86400 / periodo(r800), 14, tol=0.04)
a800 = math.degrees(math.acos(R / r800))
comprueba("800 km: arccos(R/r) (°)", a800, 27.3)
comprueba("800 km: radio de la huella (km)", R * math.radians(a800), 3040)
comprueba("800 km: pase cenital (min)", 2 * a800 / 360 * periodo(r800) / 60, 15, tol=0.03)

# ---------- Órbita de 400 km ----------
r400 = R + 400
a400 = math.degrees(math.acos(R / r400))
comprueba("400 km: pase cenital (min)", 2 * a400 / 360 * periodo(r400) / 60, 10, tol=0.03)
comprueba("400 km: huella (km)", R * math.radians(a400), 2200, tol=0.01)
comprueba("400 km: velocidad radial máxima (km/s)", velocidad(r400) * R / r400, 7.2, tol=0.01)
comprueba("ISS: Doppler en 437,800 MHz a 7,2 km/s (kHz)", doppler_khz(437.8, velocidad(r400) * R / r400), 10.5, tol=0.01)
comprueba("ISS: Doppler en 145,990 MHz a 7,2 km/s (kHz)", doppler_khz(145.99, velocidad(r400) * R / r400), 3.5, tol=0.01)

# ---------- Órbita geoestacionaria ----------
rg = (MU * DIA_SIDEREO ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
comprueba("GEO: radio (km)", rg, 42164, tol=0.0005)
comprueba("GEO: altura sobre el ecuador (km)", rg - RE, 35786, tol=0.0005)
comprueba("GEO: unas 45 veces más lejos que una órbita de 800 km", (rg - RE) / 800, 45, tol=0.01)
comprueba("Periodo rozando la superficie (min)", periodo(R) / 60, 84, tol=0.01)

# ---------- Doppler ----------
vr800 = velocidad(r800) * R / r800
comprueba("800 km: velocidad radial máxima (km/s)", vr800, 6.6, tol=0.01)
comprueba("Doppler en 436,795 MHz (kHz)", doppler_khz(436.795, 6.62), 9.6, tol=0.01)
comprueba("Doppler en 145,850 MHz (kHz)", doppler_khz(145.85, 6.62), 3.2, tol=0.01)
comprueba("Inversor: subida 145,965 y bajada 435,640 (kHz)", 6.62 / C * (435.640 - 145.965) * 1e3, 6.4, tol=0.01)
comprueba("No inversor: mismas frecuencias (kHz)", 6.62 / C * (435.640 + 145.965) * 1e3, 12.8, tol=0.01)

# ---------- RS-44 ----------
comprueba("RS-44: constante con un extremo (MHz)", 145.935 + 435.670, 581.605, tol=1e-9)
comprueba("RS-44: constante con el otro (MHz)", 145.995 + 435.610, 581.605, tol=1e-9)
comprueba("RS-44: centro de la bajada (MHz)", (435.610 + 435.670) / 2, 435.640, tol=1e-9)
comprueba("RS-44: subida para bajar en 435,640 (MHz)", 581.605 - 435.640, 145.965, tol=1e-9)

# ---------- Enlace con un satélite FM a 800 km ----------
comprueba("Distancia en el horizonte (km)", distancia(800, 0), 3290, tol=0.002)
comprueba("Distancia en la vertical (km)", distancia(800, 90), 800, tol=1e-9)
comprueba("Pérdida en 145,85 MHz a 800 km (dB)", l_el(800, 145.85), 133.8, tol=0.001)
comprueba("Pérdida en 145,85 MHz a 3 290 km (dB)", l_el(distancia(800, 0), 145.85), 146.1, tol=0.001)
comprueba("Diferencia (dB)", 20 * math.log10(distancia(800, 0) / 800), 12.3, tol=0.005)
comprueba("5 W con 12,3 dB menos (W)", 5 / 10 ** 1.23, 0.3, tol=0.05)

# ---------- QO-100 ----------
comprueba("NB: bajada menos subida (MHz)", 10489.500 - 2400.000, 8089.5, tol=1e-9)
comprueba("NB: lo mismo en el otro extremo (MHz)", 10490.000 - 2400.500, 8089.5, tol=1e-9)
comprueba("NB: subida 2 400,200 se oye en (MHz)", 2400.200 + 8089.5, 10489.700, tol=1e-9)
comprueba("Baliza inferior en frecuencia intermedia (MHz)", 10489.5 - 9750, 739.5, tol=1e-9)
comprueba("Error de 25 ppm en 9 750 MHz (kHz)", 9750e3 * 25e-6, 244, tol=0.002)

lugares = {
    "A Coruña": (43.37, -8.40, 135, 29, 38670),
    "Madrid": (40.42, -3.70, 139, 34, 38240),
    "Sevilla": (37.39, -5.98, 134, 35, 38150),
    "Barcelona": (41.39, 2.17, 146, 36, 38070),
    "Las Palmas de Gran Canaria": (28.10, -15.41, 118, 34, 38240),
}
for nombre, (la, lo, az_t, el_t, d_t) in lugares.items():
    az, el, d = apuntado(la, lo)
    comprueba(f"{nombre}: azimut (°)", az, az_t, tol=0.005)
    comprueba(f"{nombre}: elevación (°)", el, el_t, tol=0.02)
    comprueba(f"{nombre}: distancia (km)", d, d_t, tol=0.0005)
    cierto(f"{nombre}: elevación entre 29 y 40°", 29 <= el <= 40)
    cierto(f"{nombre}: hacia el sureste (90-180°)", 90 < az < 180)

_, _, d_mad = apuntado(40.42, -3.70)
comprueba("Madrid: recorrido de ida y vuelta (km)", 2 * 38240, 76480, tol=1e-9)
comprueba("Madrid: retardo (s)", 2 * d_mad / C, 0.26, tol=0.02)
comprueba("Madrid: pérdida en 10 489,75 MHz (dB)", l_el(38240, 10489.75), 204.5, tol=0.001)

# Ganancias de plato (rendimiento 0,6)
comprueba("Longitud de onda en 2 400 MHz (cm)", C * 1e5 / 2400e6, 12.5, tol=0.002)
g75 = ganancia_plato(0.75, 2400)
comprueba("Plato de 75 cm en 2 400 MHz (veces)", g75, 213, tol=0.005)
comprueba("... en dBi", 10 * math.log10(g75), 23.3, tol=0.003)
comprueba("p. i. r. e. con 2 W (W)", 2 * g75, 427, tol=0.005)
g120 = ganancia_plato(1.2, 2400)
comprueba("Plato de 1,2 m en 2 400 MHz (dBi)", 10 * math.log10(g120), 27.4, tol=0.003)
comprueba("p. i. r. e. con 10 W (W)", 10 * g120, 5470, tol=0.005)
general = 0.5 * 1000
comprueba("Régimen general de 13 cm, banda secundaria (W p. i. r. e.)", general, 500)
limite = 1500           # autorización para el QO-100
G_MIN = 21.5            # dBi, ganancia mínima de la autorización
cierto("Plato de 75 cm: 23,3 dBi, por encima de 21,5 dBi", 10 * math.log10(g75) >= G_MIN)
cierto("Plato de 1,2 m: 27,4 dBi, por encima de 21,5 dBi", 10 * math.log10(g120) >= G_MIN)
cierto("427 W con el plato de 75 cm, dentro de 1 500 W", 2 * g75 <= limite)
comprueba("... veces el límite de 1 500 W ('más de tres veces y media')", 10 * g120 / limite, 3.6, tol=0.02)
cierto("... entre 3,5 y 4 veces", 3.5 < 10 * g120 / limite < 4)
comprueba("27,4 dBi en veces", 10 ** 2.74, 549, tol=0.002)
comprueba("Potencia máxima con el plato de 1,2 m (W)", limite / 10 ** 2.74, 2.7, tol=0.02)
g60 = ganancia_plato(0.6, 2400)
comprueba("Plato de 60 cm en 2 400 MHz (veces)", g60, 137, tol=0.005)
comprueba("... en dBi ('unos 21,4 dBi')", 10 * math.log10(g60), 21.4, tol=0.003)
cierto("... por debajo de 21,5 dBi, a menos de dos décimas",
       0 < G_MIN - 10 * math.log10(g60) < 0.2)
cierto("... también en 2 410 MHz, el borde superior de la autorización",
       10 * math.log10(ganancia_plato(0.6, 2410)) < G_MIN)
eta_min = 10 ** (G_MIN / 10) / (math.pi * 0.6 / (C * 1e5 / 2400e6 / 100)) ** 2
comprueba("Rendimiento mínimo del plato de 60 cm para 21,5 dBi", eta_min, 0.62, tol=0.01)
cierto("Capítulo 6: plato de 80 cm en 10 489,5 MHz, unos 36,7 dBi",
       abs(10 * math.log10(ganancia_plato(0.8, 10489.5)) - 36.7) < 0.1)

# ---------- Autorización especial en 13 cm ----------
cierto("La subida de 2 400 MHz cae en 2 300-2 450 MHz y fuera de 2 316-2 332 MHz",
       2300 <= 2400.0 <= 2450 and not (2316 <= 2400.0 <= 2332))
cierto("El transpondedor estrecho (2 400,0-2 400,5 MHz) cabe en 2 400-2 410 MHz",
       2400 <= 2400.0 and 2400.5 <= 2410)

# ---------- Autoevaluación ----------
comprueba("P1: periodo a 800 km (min)", periodo(r800) / 60, 101, tol=0.005)
comprueba("P2: Doppler en 437,8 MHz a 7 km/s (kHz)", doppler_khz(437.8, 7), 10.2, tol=0.005)
comprueba("P2: lo mismo en 145,99 MHz (kHz)", doppler_khz(145.99, 7), 3.4, tol=0.01)
comprueba("P4: subida para bajar en 435,655 (MHz)", 581.605 - 435.655, 145.950, tol=1e-9)
comprueba("P5: 20 log(3 290/800) (dB)", 20 * math.log10(3290 / 800), 12.3, tol=0.005)
az, el, _ = apuntado(40.42, -3.70)
comprueba("P7: Madrid, azimut (°)", az, 139, tol=0.005)
comprueba("P7: Madrid, elevación (°)", el, 34, tol=0.02)
comprueba("P8: potencia máxima (W)", 1500 / 10 ** 2.74, 2.7, tol=0.02)
comprueba("P8, distractor b): 500 W del régimen general (W)", 500 / 10 ** 2.74, 0.9, tol=0.02)
comprueba("P8, distractor d): 1 500 / 27,4 (W)", 1500 / 27.4, 55, tol=0.01)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
