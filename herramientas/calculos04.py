"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 04.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos04.py
"""
import math

C = 3e8  # velocidad de la luz redondeada, como en el texto (m/s)
fallos = 0


def comprueba(nombre, calculado, en_texto, tol=0.006):
    """Compara con tolerancia relativa (0,6 % por defecto, por los redondeos)."""
    global fallos
    ok = abs(calculado - en_texto) <= tol * max(abs(en_texto), 1e-12)
    print(f"{'OK ' if ok else 'MAL'} {nombre}: calculado {calculado:.6g}, en el texto {en_texto}")
    if not ok:
        fallos += 1


def db(p):
    return 10 * math.log10(p)


# ---------- Ejemplos del texto ----------

# Longitud de onda y frecuencia
comprueba("λ de 50,2 MHz (m)", C / 50.2e6, 5.98)
comprueba("λ de 50,2 MHz con c exacta (m)", 299_792_458 / 50.2e6, 5.97)
comprueba("f para λ = 2,05 m (MHz)", C / 2.05 / 1e6, 146.3)
comprueba("periodo de 10 MHz (ns)", 1 / 10e6 * 1e9, 100)

# AM
fc, fm = 7120, 3.4  # kHz
comprueba("AM: ancho de banda con audio de 3,4 kHz (kHz)", 2 * fm, 6.8)
comprueba("AM: banda lateral inferior (kHz)", fc - fm, 7116.6)
comprueba("AM: banda lateral superior (kHz)", fc + fm, 7123.4)
Pc = 40
comprueba("AM m=1: potencia total (W)", Pc * (1 + 1**2 / 2), 60)
comprueba("AM m=1: cada banda lateral (W)", Pc * 1**2 / 4, 10)
comprueba("AM m=0,6: dos bandas laterales (W)", Pc * 0.6**2 / 2, 7.2)
comprueba("AM m=0,6: potencia total (W)", Pc * (1 + 0.6**2 / 2), 47.2)
comprueba("AM: 6K00A3E con audio hasta 3 kHz (kHz)", 2 * 3, 6.0)

# BLU
comprueba("USB 14 250 kHz, borde inferior (kHz)", 14250 + 0.3, 14250.3)
comprueba("USB 14 250 kHz, borde superior (kHz)", 14250 + 2.8, 14252.8)
comprueba("LSB 3 690 kHz, borde inferior (kHz)", 3690 - 2.8, 3687.2)
comprueba("LSB 3 690 kHz, borde superior (kHz)", 3690 - 0.3, 3689.7)
comprueba("BLU: ancho ocupado 300-2 800 Hz (kHz)", 2.8 - 0.3, 2.5)

# FM
df, fmod = 2.5, 3.0
comprueba("FM: índice de modulación 2,5/3", df / fmod, 0.83, tol=0.01)
comprueba("FM: Carson 2(2,5+3) (kHz)", 2 * (df + fmod), 11)

# Multiplicador de frecuencia en un transmisor de FM
comprueba("multiplicador ×12: frecuencia de salida (MHz)", 12.15 * 12, 145.8)
comprueba("multiplicador ×12: desviación de salida (kHz)", 0.25 * 12, 3)

# Mezclador y frecuencia imagen
comprueba("mezcla 14 200 − 5 200 kHz", 14200 - 5200, 9000)
comprueba("mezcla 14 200 + 5 200 kHz", 14200 + 5200, 19400)
comprueba("OL por encima: 14 200 + 9 000 kHz", 14200 + 9000, 23200)
comprueba("OL por encima: suma 14 200 + 23 200 kHz", 14200 + 23200, 37400)
comprueba("imagen con OL 23,2 MHz y FI 9 MHz (MHz)", 23.2 + 9, 32.2)
comprueba("imagen = f + 2·FI (MHz)", 14.2 + 2 * 9, 32.2)
comprueba("VHF: OL por debajo 145,6 − 10,7 (MHz)", 145.6 - 10.7, 134.9)
comprueba("VHF: imagen 145,6 − 2·10,7 (MHz)", 145.6 - 2 * 10.7, 124.2)
assert 117.975 < 124.2 <= 137, "la imagen debería caer en la banda aeronáutica"

# Armónicos
comprueba("2.º armónico de 7 050 kHz", 2 * 7050, 14100)
comprueba("3.er armónico de 7 050 kHz", 3 * 7050, 21150)
assert 14000 <= 14100 <= 14350 and 21000 <= 21150 <= 21450

# Rendimiento de un amplificador
Pdc = 13.8 * 9
comprueba("potencia consumida 13,8 V × 9 A (W)", Pdc, 124.2)
comprueba("rendimiento con 50 W de salida (%)", 50 / Pdc * 100, 40.3)
comprueba("calor disipado (W)", Pdc - 50, 74.2)

comprueba("clase A, rendimiento teórico máximo (%)", 50, 50)
comprueba("clase B, rendimiento teórico máximo π/4 (%)", math.pi / 4 * 100, 78.5)

# Relación señal/ruido y filtros
comprueba("S/R con 2 µV y 0,5 µV (dB)", 20 * math.log10(2 / 0.5), 12.0)
comprueba("mejora al pasar de 2,4 kHz a 500 Hz (dB)", db(2400 / 500), 6.8)
comprueba("S9 frente a S7: 2 unidades × 6 dB", 2 * 6, 12)
comprueba("12 dB en potencia (veces)", 10 ** (12 / 10), 16, tol=0.02)

# Modulación digital
comprueba("4 estados: bits por símbolo", math.log2(4), 2)
comprueba("50 baudios × 2 bit (bit/s)", 50 * 2, 100)

# SDR
comprueba("muestreo directo hasta 30 MHz: mínimo (MS/s)", 2 * 30, 60)
comprueba("Nyquist con 122,88 MS/s (MHz)", 122.88 / 2, 61.44)
comprueba("ADC de 8 bits ≈ 6 dB/bit (dB)", 6 * 8, 48)
comprueba("ADC de 14 bits ≈ 6 dB/bit (dB)", 6 * 14, 84)
comprueba("ADC de 8 bits, 6,02N + 1,76 (dB)", 6.02 * 8 + 1.76, 49.9, tol=0.01)
comprueba("ADC de 14 bits, 6,02N + 1,76 (dB)", 6.02 * 14 + 1.76, 86.0, tol=0.01)
comprueba("flujo I/Q 2,4 MS/s × 2 × 8 bit (Mbit/s)", 2.4e6 * 2 * 8 / 1e6, 38.4)
comprueba("SDR I/Q: banda visible centrada en 145,5 MHz, borde inferior", 145.5 - 2.4 / 2, 144.3)
comprueba("SDR I/Q: banda visible centrada en 145,5 MHz, borde superior", 145.5 + 2.4 / 2, 146.7)

# ---------- Autoevaluación ----------
comprueba("P1: λ de 28,5 MHz (m)", C / 28.5e6, 10.5)
comprueba("P2: AM con audio hasta 4 kHz (kHz)", 2 * 4, 8)
comprueba("P4: Carson 2(4+3) (kHz)", 2 * (4 + 3), 14)
comprueba("P5: OL por encima 21,3 + 10,7 (MHz)", 21.3 + 10.7, 32.0)
comprueba("P5: imagen 21,3 + 2·10,7 (MHz)", 21.3 + 2 * 10.7, 42.7)
comprueba("P6: 50,1 − 39,4 (MHz)", 50.1 - 39.4, 10.7)
comprueba("P6: 50,1 + 39,4 (MHz)", 50.1 + 39.4, 89.5)
comprueba("P8: máxima frecuencia con 20 MS/s (MHz)", 20 / 2, 10)
comprueba("P10: desviación tras ×9 (kHz)", 0.5 * 9, 4.5)
# Distractores de la P1 y la P4, para que no coincidan por casualidad con la respuesta
assert abs(C / 28.5e6 - 1.05) > 1 and abs(C / 28.5e6 - 105) > 1
assert 2 * 4 != 2 * (4 + 3) and 4 + 3 != 14

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
