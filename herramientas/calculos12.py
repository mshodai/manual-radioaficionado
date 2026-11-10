"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 12.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos12.py

Datos de partida (todos comprobados en noviembre de 2026):
- FT8 y FT4: guía de usuario de WSJT-X (https://wsjtx.github.io/wsjtx/guide-full.html,
  apartado 20, «Protocol Specifications», y tabla de parámetros) y artículo de QEX
  de julio/agosto de 2020 «The FT4 and FT8 Communication Protocols».
- Frecuencias de dial por defecto: models/FrequencyList.cpp del repositorio oficial
  https://github.com/WSJTX/wsjtx.
- Tramos de HF: plan de HF de la IARU Región 1, en vigor desde el 16-10-2020.
- PSK31: especificación publicada por la ARRL (https://www.arrl.org/psk31-spec).
- RTTY: ayuda de fldigi (https://www.w1hkj.org/FldigiHelp/rtty_page.html).
- APRS: 1200 bit/s AFSK según el README de Dire Wolf.
- DMR: ETSI TS 102 361-1 V2.6.1 (2023-05): 4800 símbolos/s de 2 bits, ranuras de
  30 ms, trama de 60 ms, canal de 12,5 kHz.
- D-STAR: norma de la JARL (STD6_0_E): 4,8 kbit/s como máximo; voz AMBE de
  2,4 kbit/s, 3,6 kbit/s con la corrección de errores.
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


def emitida(dial_khz, audio_hz):
    """Frecuencia emitida en USB: dial más la frecuencia del tono de audio."""
    return dial_khz + audio_hz / 1000


# ---------- FT8 y FT4: parámetros ----------
ft8_baudios = 12000 / 1920
comprueba("FT8: velocidad de símbolo (baudios)", ft8_baudios, 6.25)
comprueba("FT8: duración de símbolo (s)", 1 / ft8_baudios, 0.16)
comprueba("FT8: símbolos (174/3 + 21)", 174 / 3 + 21, 79)
comprueba("FT8: duración de la emisión (s)", 79 / ft8_baudios, 12.64)
comprueba("FT8: margen hasta el final del periodo de 15 s", 15 - 79 / ft8_baudios, 2.36)
comprueba("FT8: ancho ocupado (Hz)", 8 * ft8_baudios, 50)
ft4_baudios = 12000 / 576
comprueba("FT4: velocidad de símbolo (baudios)", ft4_baudios, 20.83, tol=0.001)
comprueba("FT4: símbolos (174/2 + 16 + 2)", 174 / 2 + 16 + 2, 105)
comprueba("FT4: duración de la emisión (s)", 105 / ft4_baudios, 5.04)
comprueba("FT4: ancho ocupado (Hz)", 4 * ft4_baudios, 83.3)
comprueba("FT8: bits por símbolo con 8 tonos", math.log2(8), 3)

# ---------- Ejemplo: frecuencia emitida y plan de bandas ----------
comprueba("Dial 14 074 kHz + 1200 Hz", emitida(14074, 1200), 14075.2)
comprueba("Dial 14 074 kHz + 200 Hz", emitida(14074, 200), 14074.2)
comprueba("Dial 14 074 kHz + 3000 Hz", emitida(14074, 3000), 14077.0)
cierto("14 074,2 a 14 077,0 kHz en 14 070-14 089 kHz, la parte solo de digimodes del tramo de 500 Hz 14 070-14 099",
       14070 <= emitida(14074, 200) and emitida(14074, 3000) <= 14089)
comprueba("Dial 7074 kHz + 200 Hz", emitida(7074, 200), 7074.2)
comprueba("Dial 7074 kHz + 3000 Hz", emitida(7074, 3000), 7077.0)
cierto("7074,2 a 7077,0 kHz dentro del tramo de todos los modos 7060-7100 kHz",
       7060 <= emitida(7074, 200) and emitida(7074, 3000) <= 7100)
cierto("7074 kHz queda fuera del tramo de 500 Hz 7040-7050 kHz", emitida(7074, 200) > 7050)

# ---------- Ejemplo: relación señal/ruido en 2500 Hz y en 50 Hz ----------
comprueba("10·log(2500/50) (dB)", 10 * math.log10(2500 / 50), 17.0)
comprueba("-21 dB en 2500 Hz equivalen en 50 Hz a", -21 + 10 * math.log10(2500 / 50), -4.0, tol=0.01)

# ---------- Ejemplo: deriva del reloj ----------
deriva_dia = 20e-6 * 86400
comprueba("Reloj con 20 ppm de error: deriva diaria (s)", deriva_dia, 1.7, tol=0.02)
comprueba("Horas hasta desviarse 1 s con 20 ppm", 1 / 20e-6 / 3600, 13.9, tol=0.005)

# ---------- Ejemplo: armónicos del audio ----------
comprueba("Tono de 700 Hz con dial en 14 074 kHz", emitida(14074, 700), 14074.7)
comprueba("2.º armónico del tono de 700 Hz (kHz emitidos)", emitida(14074, 2 * 700), 14075.4)
comprueba("3.er armónico del tono de 700 Hz (kHz emitidos)", emitida(14074, 3 * 700), 14076.1)
cierto("1400 y 2100 Hz caben en un filtro de BLU de unos 3 kHz", 2 * 700 < 3000 and 3 * 700 < 3000)
comprueba("2.º armónico de un tono de 1600 Hz", 2 * 1600, 3200)
cierto("3200 Hz queda fuera de un filtro de BLU de unos 3 kHz", 2 * 1600 > 3000)

# ---------- PSK31 y RTTY ----------
comprueba("PSK31: duración de símbolo (ms)", 1000 / 31.25, 32)
comprueba("RTTY: duración de bit a 45,45 baudios (ms)", 1000 / 45.45, 22.0)

# ---------- APRS: ocupación del canal ----------
t_paquete = 75 * 8 / 1200
comprueba("Paquete APRS de 75 bytes a 1200 bit/s (s)", t_paquete, 0.5)
comprueba("40 estaciones, un paquete por minuto: s ocupados", 40 * t_paquete, 20)
comprueba("... en porcentaje del minuto", 40 * t_paquete / 60 * 100, 33, tol=0.02)
comprueba("Con un salto de digipeater cada paquete suena dos veces: s", 2 * 40 * t_paquete, 40)
comprueba("... en porcentaje del minuto", 2 * 40 * t_paquete / 60 * 100, 67, tol=0.01)

# ---------- DMR ----------
comprueba("DMR: velocidad bruta (bit/s)", 4800 * 2, 9600)
comprueba("DMR: trama de dos ranuras de 30 ms (ms)", 2 * 30, 60)
comprueba("DMR: ancho equivalente por conversación (kHz)", 12.5 / 2, 6.25)
comprueba("DMR: fracción del tiempo que transmite un portátil", 30 / 60, 0.5)

# ---------- D-STAR ----------
comprueba("D-STAR: voz con corrección de errores (kbit/s)", 2.4 + 1.2, 3.6)
comprueba("D-STAR: lo que queda para datos y sincronismo (kbit/s)", 4.8 - 3.6, 1.2)

# ---------- Autoevaluación ----------
comprueba("P1: dial 14 074 kHz, tono 2000 Hz", emitida(14074, 2000), 14076.0)
cierto("P1: 14 076 kHz dentro del tramo 14 070-14 089 kHz", 14070 <= 14076 <= 14089)
comprueba("P5: -21 dB en 2500 Hz, en 50 Hz", -21 + 10 * math.log10(2500 / 50), -4.0, tol=0.01)
comprueba("P5: ancho de FT8", 8 * 6.25, 50)
comprueba("P6: DMR, 4800 símbolos/s de 2 bits", 4800 * 2, 9600)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
