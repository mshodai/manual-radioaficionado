"""Comprueba los ejemplos numéricos y las soluciones de la autoevaluación del capítulo 11.

Cada bloque calcula un resultado y lo compara con el valor redondeado que aparece
en el texto. Si alguna cifra del capítulo cambia, hay que cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos11.py

Fuentes de los datos fijos (comprobadas en noviembre de 2026):
- Código y temporización: Recomendación UIT-R M.1677-1 (10/2009), anexo 1.
- Segmentos de CW: plan de bandas de HF de la IARU Región 1 de 2020 (en vigor
  desde el 16 de octubre de 2020; no se ha podido confirmar si hay cambios posteriores), y planes de VHF y UHF de diciembre de 2020.
- Velocidad de identificación de los repetidores: artículo 25.d) de la Orden
  IET/1311/2013 (BOE-A-2013-7624).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from morse11 import CODIGO, LETRAS, PROSIGNOS, SIGNOS, farnsworth, t_punto, unidades, unidades_caracter  # noqa: E402

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


def segundos(texto, ppm):
    """Duración de un texto sin el espacio de palabra final."""
    c, e = unidades(texto)
    return (c + e - 7) * t_punto(ppm)


# ---------- Tabla del código ----------
cierto("26 letras + É en la tabla", len(LETRAS) == 27)
cierto("prosigno AR = signo + de la recomendación", PROSIGNOS["AR"] == SIGNOS["+"])
cierto("prosigno KN = paréntesis de apertura", PROSIGNOS["KN"] == SIGNOS["("])
cierto("prosigno BT = doble guion (=)", PROSIGNOS["BT"] == SIGNOS["="])
cierto("K = invitación a transmitir", CODIGO["K"] == "-.-")
cierto("letras de un solo elemento: E y T", sorted(k for k, v in LETRAS.items() if len(v) == 1) == ["E", "T"])
# Ejemplo del texto: las cifras tienen siempre cinco elementos
cierto("todas las cifras tienen 5 elementos", all(len(CODIGO[str(n)]) == 5 for n in range(10)))
# Ejemplo: el 0 es la cifra más larga: 5 rayas = 15 + 4 = 19 unidades
comprueba("cifra 0: unidades", unidades_caracter(CODIGO["0"]), 19)
comprueba("letra E: unidades", unidades_caracter(CODIGO["E"]), 1)

# ---------- PARIS ----------
c, e = unidades("PARIS")
comprueba("PARIS: unidades dentro de los caracteres", c, 31)
comprueba("PARIS: unidades de espacio (4 entre letras + 1 de palabra)", e, 19)
comprueba("PARIS: total", c + e, 50)
for letra, u in {"P": 11, "A": 5, "R": 7, "I": 3, "S": 5}.items():
    comprueba(f"PARIS: letra {letra}", unidades_caracter(CODIGO[letra]), u)
c, e = unidades("CODEX")
comprueba("CODEX: total", c + e, 60)

# ---------- Fórmula del punto ----------
comprueba("20 ppm: punto (ms)", t_punto(20) * 1e3, 60)
comprueba("20 ppm: raya (ms)", 3 * t_punto(20) * 1e3, 180)
comprueba("20 ppm: espacio entre palabras (ms)", 7 * t_punto(20) * 1e3, 420)
comprueba("12 ppm: punto (ms)", t_punto(12) * 1e3, 100)
comprueba("20 ppm: una PARIS dura 3 s", 50 * t_punto(20), 3)
comprueba("baudios a 20 ppm (unidades por segundo)", 1 / t_punto(20), 16.7, tol=0.01)

# ---------- Llamada CQ de ejemplo ----------
comprueba("CQ CQ CQ DE EA0ZZZ EA0ZZZ K: unidades sin el espacio final", sum(unidades("CQ CQ CQ DE EA0ZZZ EA0ZZZ K")) - 7, 289)
comprueba("CQ de ejemplo a 18 ppm (s)", segundos("CQ CQ CQ DE EA0ZZZ EA0ZZZ K", 18), 19.3, tol=0.01)

# ---------- Repetidor (artículo 25.d) ----------
comprueba("10 ppm: punto (ms)", t_punto(10) * 1e3, 120)
comprueba("ED0ZZZ a 10 ppm (s)", segundos("ED0ZZZ", 10), 9.0)

# ---------- Farnsworth ----------
u = farnsworth(20, 10)
comprueba("Farnsworth 20/10: unidad de espacio (ms)", u * 1e3, 218, tol=0.01)
comprueba("Farnsworth 20/10: espacio entre letras (ms)", 3 * u * 1e3, 654, tol=0.01)
comprueba("Farnsworth 20/10: espacio entre palabras (s)", 7 * u, 1.53, tol=0.01)
comprueba("10 ppm normal: espacio entre letras (ms)", 3 * t_punto(10) * 1e3, 360)
comprueba("10 ppm normal: espacio entre palabras (ms)", 7 * t_punto(10) * 1e3, 840)
comprueba("Farnsworth 20/10: caracteres de PARIS (s)", 31 * t_punto(20), 1.86)
comprueba("Farnsworth 20/10: total de PARIS = 6 s", 31 * t_punto(20) + 19 * u, 6)
comprueba("Farnsworth 18/6: espacio entre letras (ms)", 3 * farnsworth(18, 6) * 1e3, 1253, tol=0.01)

# ---------- Clics de manipulación ----------
# Modelo: un elemento de duración T con flancos de coseno alzado de duración tr.
# Equivale a un rectángulo de T - tr convolucionado con medio seno de tr; la
# envolvente de su espectro, respecto a la frecuencia cero, es:
#     1 / (π f (T - tr)) · 1 / |1 - (2 f tr)^2|   (con tr = 0, solo el primer factor)
# La fórmula solo vale como envolvente lejos de f = 1 / (2 tr); aquí se usa a
# partir de 1 kHz, muy por encima de los 100 Hz de ese punto para tr = 5 ms.


def envolvente_db(f, T, tr):
    a = 1 / (math.pi * f * (T - tr))
    if tr > 0:
        a /= abs(1 - (2 * f * tr) ** 2)
    return 20 * math.log10(a)


T = t_punto(20)  # un punto a 20 ppm: 60 ms
comprueba("clics, flancos instantáneos, 1 kHz (dB)", envolvente_db(1000, T, 0), -45.5, tol=0.01)
comprueba("clics, flancos instantáneos, 3 kHz (dB)", envolvente_db(3000, T, 0), -55, tol=0.01)
comprueba("clics, flancos de 5 ms, 1 kHz (dB)", envolvente_db(1000, T, 0.005), -84.5, tol=0.01)
comprueba("clics, mejora a 1 kHz con 5 ms (dB)", envolvente_db(1000, T, 0) - envolvente_db(1000, T, 0.005), 39, tol=0.02)


def corte(nivel):
    """Con flancos instantáneos, frecuencia a partir de la cual la envolvente queda por debajo de nivel (dB)."""
    f = 10.0
    while envolvente_db(f, T, 0) > nivel:
        f += 1
    return f


comprueba("flancos instantáneos: −60 dB a partir de (kHz)", corte(-60) / 1e3, 5.3, tol=0.01)

# ---------- Segmentos de la IARU Región 1 (HF, 16 de octubre de 2020) ----------
cw_hf = {  # banda: (inicio, fin) del tramo con 200 Hz como máximo (kHz)
    "160 m": (1810, 1838), "80 m": (3500, 3570), "40 m": (7000, 7040),
    "30 m": (10100, 10130), "20 m": (14000, 14070), "17 m": (18068, 18095),
    "15 m": (21000, 21070), "12 m": (24890, 24915), "10 m": (28000, 28070),
}
comprueba("ancho del segmento de CW de 40 m (kHz)", cw_hf["40 m"][1] - cw_hf["40 m"][0], 40)
comprueba("ancho del segmento de CW de 20 m (kHz)", cw_hf["20 m"][1] - cw_hf["20 m"][0], 70)
cierto("160 m: el tramo de CW (1810-1838) cabe en lo autorizado en España (1810-1850)",
       1810 <= cw_hf["160 m"][0] and cw_hf["160 m"][1] <= 1850)
qrp = {"80 m": 3560, "40 m": 7030, "30 m": 10116, "20 m": 14060, "17 m": 18086,
       "15 m": 21060, "12 m": 24906, "10 m": 28060, "160 m": 1836}
cierto("todas las frecuencias QRP de CW caen dentro de su tramo de CW",
       all(cw_hf[b][0] <= f <= cw_hf[b][1] for b, f in qrp.items()))

# ---------- Autoevaluación ----------
comprueba("P1: punto a 25 ppm (ms)", t_punto(25) * 1e3, 48)
comprueba("P1: distractor, raya a 25 ppm (ms)", 3 * t_punto(25) * 1e3, 144)
comprueba("P2: PARIS en 2,4 s → ppm", 60 / 2.4, 25)
comprueba("P2: distractor 50/2,4", 50 / 2.4, 20.8, tol=0.01)
cierto("P3: −.−. es la C", CODIGO["C"] == "-.-.")
cierto("P3: distractores: K = −.−, Y = −.−−, Q = −−.−",
       (CODIGO["K"], CODIGO["Y"], CODIGO["Q"]) == ("-.-", "-.--", "--.-"))
u = farnsworth(15, 6)
comprueba("P5: Farnsworth 15/6, espacio entre letras (s)", 3 * u, 1.19, tol=0.01)
comprueba("P5: distractor, espacio entre letras a 6 ppm normal (s)", 3 * t_punto(6), 0.6)
comprueba("P5: distractor, espacio entre letras a 15 ppm normal (s)", 3 * t_punto(15), 0.24)
comprueba("P5: unidad de espacio (s)", u, 0.396, tol=0.01)
comprueba("P5: distractor d), espacio entre palabras (s)", 7 * u, 2.77, tol=0.01)
comprueba("P1: distractor a), 500/25 (ms)", 500 / 25, 20)
cierto("P9: ·− es la A y ·−· la R", CODIGO["A"] == ".-" and CODIGO["R"] == ".-.")
cierto("figura 11.3: −· es la N y −·− la K", CODIGO["N"] == "-." and CODIGO["K"] == "-.-")
cierto("4 m en España (70,150-70,250) contiene la llamada de 70,200", 70.150 <= 70.200 <= 70.250)

print()
print("Todo correcto." if fallos == 0 else f"{fallos} comprobaciones fallidas.")
sys.exit(1 if fallos else 0)
