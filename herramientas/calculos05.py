"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 05.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos05.py
"""
import math

C = 3e8          # velocidad de la luz redondeada, como en el texto (m/s)
R_T = 6371       # radio medio de la Tierra (km)
K = 4 / 3        # factor del radio efectivo (Recomendación UIT-R P.834)
fallos = 0


def comprueba(nombre, calculado, en_texto, tol=0.006):
    """Compara con tolerancia relativa (0,6 % por defecto, por los redondeos)."""
    global fallos
    ok = abs(calculado - en_texto) <= tol * max(abs(en_texto), 1e-12)
    print(f"{'OK ' if ok else 'MAL'} {nombre}: calculado {calculado:.6g}, en el texto {en_texto}")
    if not ok:
        fallos += 1


def pel(d_km, f_mhz):
    """Pérdida de trayecto en espacio libre (dB), con d en km y f en MHz."""
    return 32.44 + 20 * math.log10(d_km) + 20 * math.log10(f_mhz)


def salto_maximo(h_km):
    """Distancia máxima de un salto con el rayo saliendo rasante (elevación 0)."""
    return 2 * R_T * math.acos(R_T / (R_T + h_km))


def incidencia(d_km, h_km):
    """Ángulo de incidencia en la capa (respecto a la vertical) para un salto de d km
    con reflexión equivalente a h km de altura, sobre Tierra esférica."""
    phi = d_km / (2 * R_T)
    elev = math.atan((math.cos(phi) - R_T / (R_T + h_km)) / math.sin(phi))
    return math.degrees(math.asin(R_T * math.cos(elev) / (R_T + h_km))), math.degrees(elev)


def horizonte(h_m, k=K):
    """Distancia al horizonte (km) desde una altura de h metros."""
    return math.sqrt(2 * k * R_T * 1e3 * h_m) / 1e3


# Tabla de conversión de K a ak (glosario de NOAA SWPC, comprobado en noviembre de 2026)
AK = {0: 0, 1: 3, 2: 7, 3: 15, 4: 27, 5: 48, 6: 80, 7: 140, 8: 240, 9: 400}

# Balizas del IBP en orden de turno (ncdxf.org, comprobado en noviembre de 2026)
IBP = ["4U1UN", "VE8AT", "W6WX", "KH6RS", "ZL6B", "VK6RBP", "JA2IGY", "RR9O", "VR2B",
       "4S7B", "ZS6DN", "5Z4B", "4X6TU", "OH2B", "CS3B", "LU4AA", "OA4B", "YV5B"]
FREC_IBP = [14100, 18110, 21150, 24930, 28200]


def baliza(hh, mm, ss, banda):
    """Baliza que suena en la banda indicada (índice 0-4) a la hora UTC dada.
    Coincide con el horario imprimible https://www.ncdxf.org/beacon/ibp.pdf (4U1UN en
    14 100 kHz a las mm:00 de cada minuto múltiplo de 3; CS3B a las 02:20, 05:20...)
    y con el reloj oficial BeaconClock.js: turno n = (segundos desde la época / 10) mod 18,
    y en la banda b suena la baliza (n - b) mod 18. Como un día tiene 86 400 s,
    múltiplo de 180, basta con contar desde las 00:00:00 UTC."""
    n = ((hh * 3600 + mm * 60 + ss) // 10) % 18
    return IBP[(n - banda) % 18]


# ---------- Ejemplos del texto ----------

# Pérdida en espacio libre
comprueba("PEL 145 MHz, 50 km (dB)", pel(50, 145), 109.6)
comprueba("PEL 145 MHz, 100 km (dB)", pel(100, 145), 115.7)
comprueba("duplicar la distancia añade (dB)", pel(100, 145) - pel(50, 145), 6.0, tol=0.01)
comprueba("constante 32,44 = 20 log(4π·10⁹/c)", 20 * math.log10(4 * math.pi * 1e3 * 1e6 / 299_792_458), 32.44, tol=0.001)

# Alcance máximo de un salto
comprueba("salto máximo por la capa E, 110 km (km)", salto_maximo(110), 2350, tol=0.01)
comprueba("salto máximo por la capa F2, 300 km (km)", salto_maximo(300), 3800, tol=0.02)

# Ley de la secante: foF2 = 6 MHz, salto de 2 000 km, capa a 300 km
i, elev = incidencia(2000, 300)
comprueba("incidencia para 2 000 km y 300 km (grados)", i, 69, tol=0.01)
comprueba("elevación de salida para 2 000 km (grados)", elev, 12, tol=0.02)
muf = 6 / math.cos(math.radians(i))
comprueba("MUF con foF2 = 6 MHz (MHz)", muf, 16.9)
comprueba("MUF con el ángulo redondeado a 69° (MHz)", 6 / math.cos(math.radians(69)), 16.7, tol=0.01)
comprueba("FOT = 85 % de la MUF (MHz)", 0.85 * muf, 14.4)
assert 14.35 < muf and muf < 21.0, "20 m debe funcionar y 15 m no"

# NVIS: frecuencias por debajo de foF2
assert 3.6 < 6 < 7.1

# Horizonte
comprueba("horizonte óptico: constante 3,57", horizonte(1, k=1), 3.57)
comprueba("horizonte radioeléctrico: constante 4,12", horizonte(1), 4.12)
comprueba("radio efectivo k·R (km)", K * R_T, 8500, tol=0.01)
comprueba("portátil a 1,5 m y repetidor a 900 m (km)", 4.12 * (math.sqrt(1.5) + math.sqrt(900)), 129, tol=0.01)
comprueba("dos móviles a 1,5 m (km)", 4.12 * 2 * math.sqrt(1.5), 10, tol=0.02)

# Doppler en un satélite de órbita baja
comprueba("Doppler máximo en 437 MHz a 7 km/s (kHz)", 437e6 * 7e3 / C / 1e3, 10.2)
comprueba("Doppler máximo en 145,8 MHz a 7 km/s (kHz)", 145.8e6 * 7e3 / C / 1e3, 3.4)

# Rebote lunar
comprueba("retardo de ida y vuelta a la Luna (s)", 2 * 384_400e3 / C, 2.56)

# Eco por trayecto largo: una vuelta a la Tierra
comprueba("vuelta completa a la Tierra (s)", 40_000e3 / C, 0.13, tol=0.03)

# Balizas del IBP
assert baliza(0, 0, 0, 0) == "4U1UN"
assert [baliza(10, 2, 25 + 10 * b, b) for b in range(4)] == ["CS3B"] * 4
assert baliza(10, 3, 5, 4) == "CS3B", "CS3B en 28 200 kHz en los primeros 10 s del ciclo siguiente"
comprueba("CS3B en 14 100: segundo del ciclo", IBP.index("CS3B") * 10, 140)
comprueba("100 W a 0,1 W (dB)", 10 * math.log10(100 / 0.1), 30)
comprueba("cada raya, 10 dB menos", 10 * math.log10(10), 10)
comprueba("ciclo completo (s)", 18 * 10, 180)

# Índice A a partir de K
ks = [2, 2, 3, 4, 3, 3, 2, 1]
comprueba("A diario del ejemplo", sum(AK[k] for k in ks) / 8, 12)

# Regla del 50 % en bandas secundarias (apartado 3.2 del anexo I de la Orden IET/1311/2013)
comprueba("30 m: 50 % de 1 000 W p.c.e.", 0.5 * 1000, 500)
comprueba("6 m: 50 % de 600 W p.c.e.", 0.5 * 600, 300)
comprueba("4 m: 50 % de 600 W p.c.e.", 0.5 * 600, 300)
comprueba("160 m (1 810-1 830 kHz): 50 % de 1 000 W p.c.e.", 0.5 * 1000, 500)
comprueba("23, 13, 6, 3 cm y 24,05-24,25 GHz: 50 % de 1 000 W p.i.r.e.", 0.5 * 1000, 500)
comprueba("longitud de onda en 24 GHz (cm)", C / 24e9 * 100, 1.25)

# Ciclo solar (SILSO)
comprueba("caída del suavizado de oct-2024 a abr-2026 (%)", (160.9 - 88.6) / 160.9 * 100, 45, tol=0.01)

# ---------- Autoevaluación ----------
comprueba("P1: MUF con foF2 = 5 MHz y 60° (MHz)", 5 / math.cos(math.radians(60)), 10)
comprueba("P1 distractor: 5·cos 60°", 5 * math.cos(math.radians(60)), 2.5)
comprueba("P1 distractor: 5/sen 60°", 5 / math.sin(math.radians(60)), 5.8, tol=0.01)
comprueba("P2: horizonte con 16 m y 25 m (km)", 4.12 * (math.sqrt(16) + math.sqrt(25)), 37, tol=0.01)
comprueba("P2 distractor: horizonte óptico (km)", 3.57 * 9, 32, tol=0.01)
assert baliza(14, 5, 25, 0) == "CS3B", "P5"
assert {baliza(14, 5, 25, 0), baliza(14, 5, 15, 0), baliza(14, 5, 35, 0), baliza(14, 5, 5, 0)} == {"CS3B", "OH2B", "LU4AA", "4X6TU"}
comprueba("P6: de 100 W a 0,1 W (dB)", 10 * math.log10(100 / 0.1), 30)
ks7 = [3, 4, 5, 6, 6, 5, 4, 3]
comprueba("P7: índice A del día", sum(AK[k] for k in ks7) / 8, 42.5)
comprueba("P7 distractor: suma sin dividir", sum(AK[k] for k in ks7), 340)
comprueba("P7 distractor: media de los K", sum(ks7) / 8, 4.5)
comprueba("P10: Doppler en 435 MHz a 6 km/s (kHz)", 435e6 * 6e3 / C / 1e3, 8.7)
comprueba("P10 distractor: en 145 MHz (kHz)", 145e6 * 6e3 / C / 1e3, 2.9)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
