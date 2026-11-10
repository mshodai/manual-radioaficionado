"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 08.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos08.py

Límites de las emisiones no esenciales: apartado 4.1 del anexo I de la Orden
IET/1311/2013 (texto del BOE comprobado en noviembre de 2026). Se interpretan
como «el valor más restrictivo de los dos»: x dB por debajo de la potencia media
y, a la vez, nunca por encima del valor absoluto que fija cada apartado.
"""
import math

fallos = 0


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


def db(x):
    return 10 * math.log10(x)


def limite_espuria(f_mhz, p_media):
    """Potencia máxima (W) de cada componente no esencial según el anexo I, 4.1."""
    if f_mhz < 30:
        return min(p_media * 1e-4, 50e-3)
    if f_mhz < 235:
        return min(p_media * 1e-6, 1e-3) if p_media > 25 else min(p_media * 1e-4, 25e-6)
    if f_mhz < 960:
        return min(p_media * 1e-6, 20e-3) if p_media > 25 else min(p_media * 1e-4, 25e-6)
    if f_mhz < 17_700:
        return min(p_media * 1e-5, 100e-3) if p_media > 10 else min(p_media * 1e-5, 100e-6)
    raise ValueError("fuera de la tabla")


# ---------- Armónicos ----------
comprueba("2.º armónico de 50,2 MHz", 2 * 50.2, 100.4)
comprueba("3.º armónico de 50,2 MHz", 3 * 50.2, 150.6)
comprueba("4.º armónico de 50,2 MHz", 4 * 50.2, 200.8)
cierto("100,4 MHz cae en la radio FM (87,5 a 108 MHz, CNAF, nota UN-17)", 87.5 <= 100.4 <= 108)
comprueba("3.er armónico de 145,2 MHz", 3 * 145.2, 435.6)
cierto("435,6 MHz cae en la banda de 70 cm (430 a 440 MHz)", 430 <= 435.6 <= 440)
comprueba("2.º armónico de 145,2 MHz", 2 * 145.2, 290.4)
# Figura 8.1: atenuación del filtro ilustrativo en el 2.º armónico
at2 = min(60, 160 * math.log10(100.4 / 56))
comprueba("figura 8.1: el filtro baja el 2.º armónico unos 40 dB", at2, 40, tol=0.02)
comprueba("figura 8.1: el 3.º armónico queda en −98 dBc", -38 - min(60, 160 * math.log10(150.6 / 56)), -98)

# ---------- dBc ----------
comprueba("−55 dBc de 100 W, en µW", 100 * 10 ** (-5.5) * 1e6, 316, tol=0.003)
comprueba("−60 dB de 100 W, en µW", 100 * 1e-6 * 1e6, 100)
cierto("316 µW supera el límite de 100 µW (30-235 MHz, P > 25 W)", 316e-6 > limite_espuria(100, 100))

# ---------- Límites del anexo I ----------
comprueba("HF, 400 W: límite (mW)", limite_espuria(14, 400) * 1e3, 40)
comprueba("HF, 1000 W: límite (mW)", limite_espuria(14, 1000) * 1e3, 50)
comprueba("HF, 1000 W: equivale a dB por debajo", db(1000 / 50e-3), 43, tol=0.002)
comprueba("VHF, 50 W: límite (µW)", limite_espuria(145, 50) * 1e6, 50)
comprueba("VHF, 5 W: límite (µW)", limite_espuria(145, 5) * 1e6, 25)
comprueba("VHF, 5 W: −40 dB serían (µW)", 5 * 1e-4 * 1e6, 500)
comprueba("VHF, 5 W: 25 µW equivale a dB por debajo", db(5 / 25e-6), 53, tol=0.002)
comprueba("UHF, 50 W: límite (µW)", limite_espuria(435, 50) * 1e6, 50)
# Pregunta: 10 W en 14 MHz
comprueba("HF, 10 W: límite (mW)", limite_espuria(14, 10) * 1e3, 1)

# ---------- Intermodulación (figura 8.2) ----------
f1, f2 = 145.35, 145.60
comprueba("2f1 − f2", 2 * f1 - f2, 145.10)
comprueba("2f2 − f1", 2 * f2 - f1, 145.85)
comprueba("3f1 − 2f2", 3 * f1 - 2 * f2, 144.85)
comprueba("3f2 − 2f1", 3 * f2 - 2 * f1, 146.10)
comprueba("f1 + f2 (2.º orden)", f1 + f2, 290.95)
comprueba("f2 − f1 (2.º orden)", f2 - f1, 0.25)
# Pregunta de autoevaluación: 432,8 y 433,4 MHz
a, b = 432.8, 433.4
comprueba("2a − b", 2 * a - b, 432.2)
comprueba("2b − a", 2 * b - a, 434.0)
# Ejemplo HF de 2.º orden: dos emisoras de onda corta
comprueba("suma de 5,95 y 9,62 MHz (2.º orden)", 5.95 + 9.62, 15.57)
comprueba("diferencia 9,62 − 5,95 (2.º orden)", 9.62 - 5.95, 3.67)

# ---------- Fuente conmutada a 70 kHz (figura 8.4) ----------
fsw = 70  # kHz
en_40 = [n * fsw for n in range(1, 1000) if 7000 <= n * fsw <= 7200]
cierto("armónicos de 70 kHz en 7000-7200 kHz: 7000, 7070, 7140", en_40 == [7000, 7070, 7140])
comprueba("101 × 70 kHz", 101 * fsw, 7070)
comprueba("102 × 70 kHz", 102 * fsw, 7140)
en_20 = [n * fsw for n in range(1, 1000) if 14000 <= n * fsw <= 14350]
comprueba("armónicos de 70 kHz en 14 000-14 350 kHz (número)", len(en_20), 6)
# Pregunta: peine cada 45 kHz → frecuencia de conmutación
comprueba("separación del peine = frecuencia de conmutación (kHz)", 7135 - 7090, 45)

# ---------- Unidades S ----------
comprueba("de S8 a S3: dB", (8 - 3) * 6, 30)
comprueba("30 dB en veces de potencia", 10 ** 3, 1000)
comprueba("de S9 + 10 a S5: dB", 10 + (9 - 5) * 6, 34)

# ---------- Ruido de líneas eléctricas ----------
comprueba("zumbido de las descargas: 2 × 50 Hz", 2 * 50, 100)

# ---------- Campo en el aparato del vecino ----------
pire = 100 * 1.64
comprueba("PIRE de 100 W en un dipolo (W)", pire, 164)
comprueba("E a 12 m (V/m)", math.sqrt(30 * pire) / 12, 5.8, tol=0.01)
comprueba("E a 24 m (V/m)", math.sqrt(30 * pire) / 24, 2.9, tol=0.01)
comprueba("doblar la distancia: −6 dB de campo", 20 * math.log10(0.5), -6.0, tol=0.01)
comprueba("portátil de 5 W a 1 m (V/m)", math.sqrt(30 * 5) / 1, 12.2, tol=0.005)
comprueba("bajar de 100 W a 25 W: dB", db(25 / 100), -6.0, tol=0.01)
comprueba("bajar de 100 W a 25 W: el campo se reduce a la mitad", math.sqrt(25 / 100), 0.5)

# ---------- Choque de modo común ----------
z_camino, z_choque = 150, 1500
r = z_camino / (z_camino + z_choque)
comprueba("I con choque / I sin choque", r, 0.091, tol=0.01)
comprueba("…en dB", 20 * math.log10(r), -20.8, tol=0.005)
comprueba("Z ∝ N²: 1 espira de 80 Ω → 5 espiras (Ω)", 80 * 5 ** 2, 2000)
# Pregunta: choque de 600 Ω con camino de 200 Ω
comprueba("pregunta: reducción con 600 Ω sobre 200 Ω (dB)", 20 * math.log10(200 / 800), -12.0, tol=0.01)

# ---------- Cable de tierra largo ----------
comprueba("λ/4 a 7,1 MHz (m): 75/f", 75 / 7.1, 10.6, tol=0.005)
comprueba("λ/2 a 14,2 MHz (m): 150/f", 150 / 14.2, 10.6, tol=0.005)
comprueba("λ/4 a 3,65 MHz (m)", 75 / 3.65, 20.5, tol=0.005)
# Pregunta: cable de tierra de 5 m, ¿en qué frecuencia es λ/4?
comprueba("frecuencia con λ/4 = 5 m (MHz)", 75 / 5, 15)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
