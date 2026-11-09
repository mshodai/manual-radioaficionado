"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 06.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos06.py

Atenuaciones de cables: hojas de datos de los fabricantes, consultadas el 9 de
noviembre de 2026 (las URL están en el capítulo, junto a la tabla). Las de Belden
vienen en dB/100 ft y aquí se pasan a dB/100 m multiplicando por 100/30,48.
"""
import cmath
import math

C = 3e8          # velocidad de la luz redondeada, como en el texto (m/s)
FT = 0.3048      # metros por pie (exacto)
fallos = 0


def comprueba(nombre, calculado, en_texto, tol=0.006):
    """Compara con tolerancia relativa (0,6 % por defecto, por los redondeos)."""
    global fallos
    ok = abs(calculado - en_texto) <= tol * max(abs(en_texto), 1e-12)
    print(f"{'OK ' if ok else 'MAL'} {nombre}: calculado {calculado:.6g}, en el texto {en_texto}")
    if not ok:
        fallos += 1


def db(x):
    return 10 * math.log10(x)


def gamma(zl, z0=50):
    return (zl - z0) / (zl + z0)


def roe(g):
    g = abs(g)
    return (1 + g) / (1 - g)


def g_de_roe(s):
    return (s - 1) / (s + 1)


def z0_coax(D, d, er):
    """Impedancia característica de un coaxial (Ω): 138/√εr · log10(D/d)."""
    return 138 / math.sqrt(er) * math.log10(D / d)


def z0_paralela(S, d, er=1.0):
    """Línea paralela con S >> d (Ω): 276/√εr · log10(2S/d)."""
    return 276 / math.sqrt(er) * math.log10(2 * S / d)


def z0_exacta_coax(D, d, er):
    """Fórmula exacta: (η0 / 2π√εr) · ln(D/d), con η0 = 376,73 Ω."""
    return 376.73 / (2 * math.pi * math.sqrt(er)) * math.log(D / d)


def z0_exacta_paralela(S, d, er=1.0):
    """Fórmula exacta: (η0 / π√εr) · arccosh(S/d)."""
    return 376.73 / (math.pi * math.sqrt(er)) * math.acosh(S / d)


# ---------- Constantes del texto, ya en metros ----------
comprueba("λ/2 = 150/f", C / 2 / 1e6, 150)
comprueba("dipolo real: 0,95·150 ≈ 143", 0.953 * 150, 143, tol=0.002)
comprueba("vertical λ/4: 143/2 = 71,5", 143 / 2, 71.5)
comprueba("bucle de onda completa: 1,02·300 ≈ 306", 1.02 * 300, 306)
# Las constantes clásicas en pies, convertidas, dan lo mismo (comprobación de la conversión)
comprueba("468/f pies en metros", 468 * FT, 143, tol=0.003)
comprueba("234/f pies en metros", 234 * FT, 71.5, tol=0.003)
comprueba("1005/f pies en metros", 1005 * FT, 306, tol=0.002)
comprueba("dBd → dBi: 10 log 1,64", db(1.64), 2.15, tol=0.003)
comprueba("constante del coaxial 138 = 60·ln10", 60 * math.log(10), 138, tol=0.002)
comprueba("constante de la paralela 276 = 120·ln10", 120 * math.log(10), 276, tol=0.002)

# ---------- Antenas ----------
comprueba("dipolo para 7,1 MHz (m)", 143 / 7.1, 20.14, tol=0.002)
comprueba("cada brazo del dipolo de 7,1 MHz (m)", 143 / 7.1 / 2, 10.07, tol=0.002)
comprueba("dipolo para 14,2 MHz (m)", 143 / 14.2, 10.07, tol=0.002)
comprueba("vertical λ/4 para 145 MHz (cm)", 71.5 / 145 * 100, 49, tol=0.01)
comprueba("bucle para 14,2 MHz, perímetro (m)", 306 / 14.2, 21.5, tol=0.005)
comprueba("bucle para 14,2 MHz, lado de un cuadro (m)", 306 / 14.2 / 4, 5.4, tol=0.005)

# Corrección por exceso de longitud: dipolo de 20,14 m resuena en 7,1; recortar para 7,15
comprueba("subir de 7,1 a 7,15 MHz: nueva longitud (m)", 20.14 * 7.1 / 7.15, 20.0, tol=0.002)
comprueba("subir de 7,1 a 7,15 MHz: recorte total (cm)", (20.14 - 20.14 * 7.1 / 7.15) * 100, 14, tol=0.03)

# Dipolo plegado: 4 × 73 Ω
comprueba("dipolo plegado 4·73 (Ω)", 4 * 73, 292)

# Media onda alimentada en un extremo con transformador 49:1 (espiras 7:1)
comprueba("EFHW: 2 450 Ω / 49 (Ω)", 2450 / 49, 50)
comprueba("relación de espiras para 49:1", math.sqrt(49), 7)

# Ganancia y PRA/PIRE
comprueba("7 dBi en dBd", 7 - 2.15, 4.85)
comprueba("100 W y 6 dBd: PRA (W)", 100 * 10 ** (6 / 10), 398, tol=0.003)
comprueba("100 W y 6 dBd: PIRE (W)", 100 * 10 ** (8.15 / 10), 653, tol=0.003)

# Relación delante/detrás
comprueba("D/A con S9+10 delante y S7 detrás (dB, 6 dB por punto S)", 10 + 2 * 6, 22)

# Apertura efectiva
lam = C / 145e6
comprueba("λ a 145 MHz (m)", lam, 2.07, tol=0.003)
comprueba("apertura efectiva del dipolo a 145 MHz (m²)", 1.64 * lam ** 2 / (4 * math.pi), 0.56, tol=0.01)
comprueba("apertura efectiva de una Yagi de 13 dBi a 145 MHz (m²)", 10 ** 1.3 * lam ** 2 / (4 * math.pi), 6.8, tol=0.01)

# Parabólica para QO-100 (10 489,5 MHz, bajada del transpondedor de banda estrecha)
lam10 = C / 10_489.5e6
g_par = 0.6 * (math.pi * 0.8 / lam10) ** 2
comprueba("λ a 10,49 GHz (cm)", lam10 * 100, 2.86, tol=0.003)
comprueba("parabólica 80 cm, η 0,6 (dBi)", db(g_par), 36.7, tol=0.003)
comprueba("parabólica 1,2 m: ganancia extra (dB)", 20 * math.log10(1.2 / 0.8), 3.5, tol=0.01)

# Eficiencia de una vertical acortada
comprueba("eficiencia con Rr = 12 Ω y pérdidas 18 Ω (%)", 12 / (12 + 18) * 100, 40)
comprueba("40 % en dB", db(0.4), -4.0, tol=0.01)
comprueba("100 W entregados, 40 W radiados", 100 * 0.4, 40)

# ---------- Líneas ----------
comprueba("Z0 coaxial, d = 1,0 mm, D = 3,5 mm, PE (Ω)", z0_coax(3.5, 1.0, 2.25), 50, tol=0.01)
comprueba("…con la fórmula exacta (Ω)", z0_exacta_coax(3.5, 1.0, 2.25), 50, tol=0.01)
comprueba("factor de velocidad con εr = 2,25", 1 / math.sqrt(2.25), 0.67, tol=0.01)
comprueba("εr del PE espumado si FV = 0,85", 1 / 0.85 ** 2, 1.38, tol=0.005)
comprueba("Z0 coaxial, mismo D/d en aire (Ω)", z0_coax(3.5, 1.0, 1.0), 75, tol=0.01)
comprueba("Z0 línea paralela, d = 2 mm, S = 30 mm (Ω)", z0_paralela(30, 2), 408, tol=0.005)
comprueba("…con la fórmula exacta (Ω)", z0_exacta_paralela(30, 2), 408, tol=0.005)

# Longitud eléctrica de un cuarto de onda de coaxial
lam145 = C / 145e6
comprueba("λ/4 en el aire a 145 MHz (cm)", lam145 / 4 * 100, 51.7, tol=0.003)
comprueba("λ/4 en coaxial FV 0,66 a 145 MHz (cm)", lam145 / 4 * 0.66 * 100, 34.1, tol=0.003)
comprueba("λ/4 en coaxial FV 0,85 a 145 MHz (cm)", lam145 / 4 * 0.85 * 100, 44.0, tol=0.003)

# ---------- Tabla de cables (dB/100 m) ----------
belden = {  # dB/100 ft en la hoja → dB/100 m en la tabla
    "8240 10": (1.1, 3.6), "8240 50": (2.5, 8.2), "8240 100": (3.8, 12.5), "8240 400": (8.4, 27.6), "8240 1000": (14.5, 47.6),
    "9258 10": (0.9, 3.0), "9258 50": (2.1, 6.9), "9258 100": (3.1, 10.2), "9258 400": (6.6, 21.7), "9258 1000": (11.2, 36.7),
    "8267 10": (0.55, 1.8), "8267 50": (1.3, 4.3), "8267 100": (1.9, 6.2), "8267 400": (4.1, 13.5), "8267 1000": (8.0, 26.2),
}
for k, (pie, m) in belden.items():
    # la tabla da un decimal: se compara el valor redondeado
    comprueba(f"Belden {k} MHz: {pie} dB/100 ft → dB/100 m", round(pie / FT + 1e-9, 1), m, tol=1e-9)
comprueba("diámetro RG-58 Belden: 0,193 in (mm)", 0.193 * 25.4, 4.9, tol=0.005)
comprueba("diámetro RG-8X Belden: 0,242 in (mm)", 0.242 * 25.4, 6.15, tol=0.002)
comprueba("diámetro RG-213 Belden: 0,405 in (mm)", 0.405 * 25.4, 10.3, tol=0.002)

# Ejemplos con datos de la tabla
comprueba("25 m de H155 a 144 MHz (dB)", 10.55 * 0.25, 2.6, tol=0.02)
comprueba("…de 50 W llegan (W)", 50 * 10 ** (-10.55 * 0.25 / 10), 27, tol=0.02)
comprueba("25 m de Ecoflex 10 a 144 MHz (dB)", 4.66 * 0.25, 1.2, tol=0.03)
comprueba("…de 50 W llegan (W)", 50 * 10 ** (-4.66 * 0.25 / 10), 38, tol=0.01)
comprueba("30 m de RG-58 a 10 MHz (dB)", 1.1 / FT * 0.30, 1.1, tol=0.02)
comprueba("…de 100 W llegan (W)", 100 * 10 ** (-1.1 / FT * 0.30 / 10), 78, tol=0.01)
comprueba("30 m de RG-58 a 400 MHz (dB)", 8.4 / FT * 0.30, 8.3, tol=0.01)
comprueba("…de 100 W llegan (W)", 100 * 10 ** (-8.4 / FT * 0.30 / 10), 15, tol=0.03)

# ---------- ROE ----------
g = gamma(100)
comprueba("Γ con 100 Ω sobre 50 Ω", g, 1 / 3)
comprueba("ROE con 100 Ω", roe(g), 2.0)
comprueba("potencia reflejada con ROE 2 (%)", g ** 2 * 100, 11.1, tol=0.003)
comprueba("ROE con 25 Ω", roe(gamma(25)), 2.0)
for s, pct, rl in ((1.5, 4.0, 14.0), (2, 11.1, 9.5), (3, 25.0, 6.0), (5, 44.4, 3.5)):
    gg = g_de_roe(s)
    comprueba(f"ROE {s}: potencia reflejada (%)", gg ** 2 * 100, pct, tol=0.01)
    comprueba(f"ROE {s}: pérdida de retorno (dB)", -20 * math.log10(gg), rl, tol=0.01)
# Ejemplo del vatímetro: 100 W directa, 4 W reflejada
gg = math.sqrt(4 / 100)
comprueba("100 W directa y 4 W reflejada: ROE", roe(gg), 1.5)
comprueba("…potencia entregada a la carga (W)", 100 - 4, 96)
comprueba("ROE 1,5: pérdida por desadaptación (dB)", -db(1 - g_de_roe(1.5) ** 2), 0.18, tol=0.03)

# Una línea con pérdidas enmascara la ROE
for a_db, roe_texto in ((3, 3.0), (1, 8.7)):
    gin = 10 ** (-2 * a_db / 20)
    comprueba(f"extremo abierto tras {a_db} dB de línea: ROE en el equipo", roe(gin), roe_texto, tol=0.01)
# ROE 3 en la antena con 2 dB de línea → en el equipo
gin = g_de_roe(3) * 10 ** (-2 * 2 / 20)
comprueba("ROE 3 en la antena tras 2 dB de línea: ROE en el equipo", roe(gin), 1.9, tol=0.02)

# Transformador de cuarto de onda
comprueba("adaptar 100 Ω a 50 Ω: Z0 del tramo (Ω)", math.sqrt(100 * 50), 70.7, tol=0.002)
comprueba("con coaxial de 75 Ω, la carga que se ve (Ω)", 75 ** 2 / 100, 56.3, tol=0.003)
comprueba("ROE resultante con 75 Ω", roe(gamma(75 ** 2 / 100)), 1.13, tol=0.01)


# Transformación de impedancias por una línea sin pérdidas (comprueba las reglas del texto)
def zin(zl, z0, bl):
    t = math.tan(bl)
    return z0 * (zl + 1j * z0 * t) / (z0 + 1j * zl * t)


assert abs(zin(100, 70.7107, math.pi / 2 - 1e-9) - 50) < 0.01
assert abs(zin(1e-9, 50, math.pi / 2 - 1e-6)) > 1e6, "λ/4 en corto: muy alta"
assert abs(zin(1e12, 50, math.pi / 2 - 1e-6)) < 1e-3, "λ/4 abierto: muy baja"
assert abs(zin(33 - 12j, 50, math.pi - 1e-9) - (33 - 12j)) < 1e-3, "λ/2 repite"

# Stub en cortocircuito de λ/4 en 145 MHz contra el segundo armónico (ejemplo 19)
bl145 = math.pi / 2 - 1e-6                 # λ/4 a la fundamental
assert abs(zin(1e-9, 50, bl145)) > 1e5, "invisible en 145 MHz"
assert abs(zin(1e-9, 50, 2 * bl145)) < 1e-3, "corto en 290 MHz (media onda)"
assert abs(zin(1e-9, 50, 4 * bl145)) < 1e-3, "corto en 580 MHz (cuarto armónico)"
# Por qué no vale un stub abierto de λ/4 a 290 MHz: en 145 MHz es λ/8 abierto, −j50 Ω en paralelo
y = 1 / 50 + 1 / zin(1e12, 50, math.pi / 4)
assert roe(gamma(1 / y)) > 2.5

# ---------- Autoevaluación ----------
comprueba("P1: dipolo para 3,65 MHz (m)", 143 / 3.65, 39.2, tol=0.002)
comprueba("P1 distractor: 150/f (m)", 150 / 3.65, 41.1, tol=0.002)
comprueba("P1 distractor: 71,5/f (m)", 71.5 / 3.65, 19.6, tol=0.002)
comprueba("P2: 9 dBi en dBd", 9 - 2.15, 6.85)
comprueba("P3: ROE con 150 Ω sobre 50 Ω", roe(gamma(150)), 3.0)
comprueba("P3: potencia reflejada (%)", gamma(150) ** 2 * 100, 25)
comprueba("P4: λ/4 a 50,1 MHz con FV 0,82 (m)", C / 50.1e6 / 4 * 0.82, 1.23, tol=0.003)
comprueba("P4 distractor: sin FV (m)", C / 50.1e6 / 4, 1.50, tol=0.003)
comprueba("P4 distractor: dividiendo por el FV (m)", C / 50.1e6 / 4 / 0.82, 1.83, tol=0.003)
comprueba("P5 distractor: media aritmética (Ω)", (12.5 + 50) / 2, 31.25)
comprueba("P1 distractor: el doble (m)", 2 * 143 / 3.65, 78.4, tol=0.002)
comprueba("P3: Γ con 150 Ω", gamma(150), 0.5)
comprueba("P5: adaptar 12,5 Ω a 50 Ω (Ω)", math.sqrt(12.5 * 50), 25)
comprueba("P6: 40 m de Aircell 7 a 432 MHz (dB)", 12.92 * 0.40, 5.2, tol=0.01)
comprueba("P6: de 50 W llegan (W)", 50 * 10 ** (-12.92 * 0.40 / 10), 15, tol=0.02)
comprueba("P6 distractor: Ecoflex 15 a 432 MHz (W)", 50 * 10 ** (-6.10 * 0.40 / 10), 28.5, tol=0.01)
comprueba("P10: 100 W directa, 11 W reflejada: ROE", roe(math.sqrt(11 / 100)), 2.0, tol=0.01)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
