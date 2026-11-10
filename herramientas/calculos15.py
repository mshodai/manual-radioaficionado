"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 15.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos15.py

Los consumos, capacidades y horas de sol son supuestos de los ejemplos, no datos
de ningún equipo concreto. Las cifras de Meshtastic (velocidad del preajuste
LONG_FAST) y del ciclo de trabajo de 868 MHz están en el docstring del bloque
correspondiente (comprobadas en noviembre de 2026).
"""

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


def corriente_media(i_tx, i_rx, fraccion_tx):
    """Corriente media de un equipo que transmite una fracción del tiempo."""
    return fraccion_tx * i_tx + (1 - fraccion_tx) * i_rx


def autonomia(capacidad_ah, profundidad, i_media):
    """Horas de funcionamiento con la capacidad útil de la batería."""
    return capacidad_ah * profundidad / i_media


# ---------- Ejemplo 1: transceptor móvil de VHF/UHF ----------
# Supuestos: 10 A transmitiendo, 0,8 A recibiendo, 10 % del tiempo en transmisión.
i_movil = corriente_media(10, 0.8, 0.10)
comprueba("Móvil: corriente media (A)", i_movil, 1.72)
comprueba("LiFePO4 40 Ah al 80 %: capacidad útil (Ah)", 40 * 0.8, 32)
comprueba("LiFePO4 40 Ah al 80 %: autonomía (h)", autonomia(40, 0.8, i_movil), 18.6)
comprueba("Plomo 40 Ah al 50 %: capacidad útil (Ah)", 40 * 0.5, 20)
comprueba("Plomo 40 Ah al 50 %: autonomía (h)", autonomia(40, 0.5, i_movil), 11.6)
comprueba("Consumo en 24 h (Ah)", i_movil * 24, 41.3)
comprueba("Energía diaria a 12,8 V (Wh)", i_movil * 24 * 12.8, 528)

# ---------- Ejemplo 1 bis: transmitiendo el 25 % del tiempo ----------
i_movil_25 = corriente_media(10, 0.8, 0.25)
comprueba("Móvil al 25 %: corriente media (A)", i_movil_25, 3.1)
comprueba("Móvil al 25 %: autonomía con LiFePO4 40 Ah (h)", autonomia(40, 0.8, i_movil_25), 10.3)

# ---------- Ejemplo 2: panel solar ----------
# Supuestos: panel de 100 W, 3 horas solares pico, rendimiento global 0,75.
e_panel = 100 * 3 * 0.75
comprueba("Panel 100 W: energía diaria (Wh)", e_panel, 225)
comprueba("Panel 100 W: carga diaria a 12,8 V (Ah)", e_panel / 12.8, 17.6)
p_necesaria = i_movil * 24 * 12.8 / (3 * 0.75)
comprueba("Potencia de panel para 528 Wh/día (W)", p_necesaria, 235)

# ---------- Ejemplo 3: portátil de mano con pilas ----------
# Supuestos: batería de 7,4 V y 2 000 mAh; 1,5 A transmitiendo, 0,15 A recibiendo; 10 %.
i_port = corriente_media(1.5, 0.15, 0.10)
comprueba("Portátil: corriente media (A)", i_port, 0.285)
comprueba("Portátil: autonomía con 2 Ah al 90 % (h)", autonomia(2, 0.9, i_port), 6.3)
comprueba("Portátil: energía de la batería (Wh)", 7.4 * 2, 14.8)

# ---------- Autoevaluación del índice ----------
i_q4 = corriente_media(8, 0.5, 0.20)
comprueba("P4: corriente media (A)", i_q4, 2)
comprueba("P4: autonomía (h)", autonomia(30, 0.8, i_q4), 12)
comprueba("P4: distractor a) 24/8 (h)", 30 * 0.8 / 8, 3.0)
comprueba("P4: distractor c) sin profundidad (h)", 30 / i_q4, 15)
comprueba("P5: energía del panel de 60 W (Wh)", 60 * 4 * 0.75, 180)
comprueba("P5: sin pérdidas (Wh)", 60 * 4, 240)
comprueba("P5: carga diaria a 12,8 V (Ah)", 60 * 4 * 0.75 / 12.8, 14, tol=0.03)

# ---------- Radiogramas: control (número de palabras) ----------
# Procedimiento de emergencia en HF de la IARU (emerg-ww.pdf): el control es el
# número de palabras del texto; en su ejemplo, 26 palabras con «stop» incluido.
ejemplo_iaru = ("please send us information about following persons stop walter smith "
                "harbour street 4 stop adam brown and family water avenue 16 stop "
                "eva black rain-way 28")
comprueba("Ejemplo de la IARU: palabras", len(ejemplo_iaru.split()), 26)
texto_15 = ("NECESITAMOS DOS GRUPOS ELECTROGENOS Y AGUA POTABLE PARA CIEN PERSONAS "
            "EN EL POLIDEPORTIVO MUNICIPAL")
comprueba("Ejemplo del capítulo: control", len(texto_15.split()), 14)
cierto("Ejemplo del capítulo: 25 palabras o menos", len(texto_15.split()) <= 25)
texto_p7 = "EVACUADAS TREINTA PERSONAS AL COLEGIO PUBLICO SIN HERIDOS"
comprueba("P7: control", len(texto_p7.split()), 8)

# ---------- Meshtastic (subpágina) ----------
# Documentación oficial (meshtastic.org, noviembre de 2026): EU_868 a +27 dBm,
# ciclo del 10 % en una hora; LONG_FAST a 1,07 kbit/s teóricos; mensajes de unos
# 200 bytes como máximo en las aplicaciones.
comprueba("+27 dBm en mW", 10 ** (27 / 10), 500, tol=0.01)
comprueba("200 bytes en bits", 200 * 8, 1600)
t200 = 200 * 8 / 1070
comprueba("200 bytes a 1,07 kbit/s (s)", t200, 1.5, tol=0.01)
comprueba("10 % de una hora (s)", 0.10 * 3600, 360)
comprueba("Mensajes de 1,5 s en 360 s", 360 / 1.5, 240)
comprueba("P3: 100 bytes a 1,07 kbit/s (s)", 100 * 8 / 1070, 0.75)
comprueba("P2: 20 dBm en mW", 10 ** (20 / 10), 100)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
raise SystemExit(1 if fallos else 0)
