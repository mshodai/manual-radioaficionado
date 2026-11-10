"""Comprueba las cifras de las preguntas de cálculo del simulacro (capítulo 16).

Cada pregunta del banco (herramientas/simulacro.yml) que lleva «calculo: true»
tiene aquí una función, registrada con @calculo("id"), que rehace la cuenta y
devuelve el texto que tiene que aparecer en la respuesta correcta («24 Ω»,
«3,3 kΩ»). La comprobación falla si ese texto no está en la respuesta correcta,
si aparece en alguna incorrecta, si una pregunta de cálculo no tiene función o
si una función no tiene pregunta. Si cambia una cifra del banco, hay que
cambiarla también aquí.

Uso, desde la raíz del repositorio:
    python3 herramientas/calculos16.py

simulacro.py hace la misma comprobación antes de generar la página.
"""
import math
import re
import sys
from pathlib import Path

CALCULOS = {}

C = 299_792_458  # m/s, velocidad de la luz


def calculo(ident):
    """Registra la función que comprueba la pregunta «ident»."""
    def registrar(f):
        if ident in CALCULOS:
            raise ValueError(f"cálculo duplicado: {ident}")
        CALCULOS[ident] = f
        return f
    return registrar


def es(x, dec=0):
    """Número con coma decimal y espacio de millares a partir de cinco cifras."""
    texto = f"{round(x, dec):.{dec}f}"
    entero, _, decimales = texto.partition(".")
    signo = "-" if entero.startswith("-") else ""
    entero = entero.lstrip("-")
    if len(entero) >= 5:
        grupos = []
        while entero:
            grupos.insert(0, entero[-3:])
            entero = entero[:-3]
        entero = " ".join(grupos)
    return signo + entero + ("," + decimales if decimales else "")


def aparece(valor, texto):
    """¿Está «valor» en «texto» como cifra completa (no dentro de otra)?"""
    patron = r"(?<![\d,])(?<!\d )" + re.escape(valor) + r"(?![\d])(?!,\d)"
    return re.search(patron, texto) is not None


def comprobar(banco):
    """Devuelve (líneas de informe, número de fallos) para la lista de preguntas."""
    informe, fallos = [], 0
    ids = {p["id"] for p in banco if p.get("calculo")}
    for p in banco:
        if not p.get("calculo"):
            continue
        f = CALCULOS.get(p["id"])
        if f is None:
            informe.append(f"MAL {p['id']}: pregunta de cálculo sin función en calculos16.py")
            fallos += 1
            continue
        valor = f()
        ok = aparece(valor, p["correcta"])
        malas = [i for i in p["incorrectas"] if aparece(valor, i)]
        if ok and not malas:
            informe.append(f"OK  {p['id']}: {valor}")
        else:
            fallos += 1
            motivo = "no está en la correcta" if not ok else f"aparece también en «{malas[0]}»"
            informe.append(f"MAL {p['id']}: {valor} {motivo}")
    for ident in sorted(set(CALCULOS) - ids):
        informe.append(f"MAL {ident}: función sin pregunta de cálculo en el banco")
        fallos += 1
    return informe, fallos


# --- Cálculos de las preguntas ----------------------------------------------
# Una función por pregunta, en el orden del banco. El comentario dice de dónde
# sale la cuenta.


@calculo("c02-002")
def _():
    # R = V / I = 13,8 V / 1,5 A
    return es(13.8 / 1.5, 1) + " Ω"


@calculo("c02-004")
def _():
    # P = V² / R = 24² / 120
    return es(24 ** 2 / 120, 1) + " W"


@calculo("c02-005")
def _():
    # t = capacidad / consumo = 18 Ah / 2 A
    return es(18 / 2, 0) + " h"


@calculo("c02-006")
def _():
    # R = R1·R2 / (R1 + R2)
    return es(330 * 220 / (330 + 220), 0) + " Ω"


@calculo("c02-007")
def _():
    # Vs = Ve · R2 / (R1 + R2)
    return es(13.8 * 10 / (22 + 10), 2) + " V"


@calculo("c02-008")
def _():
    # Vp = Vpp / 2; Ve = Vp / √2; P = Ve² / R
    ve = 40 / 2 / math.sqrt(2)
    return es(ve ** 2 / 50, 0) + " W"


@calculo("c02-009")
def _():
    # P = 100 W · 10^(−6/10) ≈ 100 / 4
    return es(100 * 10 ** (-6 / 10), 0) + " W"


@calculo("c02-010")
def _():
    # P = 1 mW · 10^(37/10), en vatios
    return es(1e-3 * 10 ** (37 / 10), 0) + " W"


@calculo("c02-012")
def _():
    # X_L = 2π f L
    return es(2 * math.pi * 14e6 * 2e-6, 0) + " Ω"


@calculo("c02-021")
def _():
    # X_C = 1 / (2π f C) = 1 / (2π · 3,6 MHz · 220 pF)
    return es(1 / (2 * math.pi * 3.6e6 * 220e-12), 0) + " Ω"


@calculo("c02-022")
def _():
    # R = (V − V_LED) / I = (13,8 − 2) / 0,015
    return es((13.8 - 2) / 0.015, 0) + " Ω"


@calculo("c02-026")
def _():
    # I = V / R = 0,12 V / 0,005 Ω
    return es(0.12 / 0.005, 0) + " A"


@calculo("c03-002")
def _():
    # Potencia media = 100 W · 0,2 (BLU sin procesador) · 0,5 (mitad del tiempo)
    return es(100 * 0.2 * 0.5, 0) + " W"


@calculo("c03-003")
def _():
    # E = 87 / √f, f = 3,6 MHz
    return es(87 / math.sqrt(3.6), 1) + " V/m"


@calculo("c04-001")
def _():
    # λ ≈ 300 / f (MHz)
    return es(300 / 430, 2) + " m"


@calculo("c04-002")
def _():
    # P = Pc · (1 + m² / 2)
    return es(50 * (1 + 0.8 ** 2 / 2), 0) + " W"


@calculo("c04-003")
def _():
    # OL por debajo: imagen = señal − 2 · FI
    return es(50.2 - 2 * 10.7, 1) + " MHz"


@calculo("c04-004")
def _():
    # I/Q: ancho visible = fs, centrado en el OL
    ol, fs = 433.5, 3.2
    return es(ol - fs / 2, 1) + " y " + es(ol + fs / 2, 1) + " MHz"


@calculo("c04-005")
def _():
    # 10 · log (B1 / B2)
    return es(10 * math.log10(2400 / 250), 1) + " dB"


@calculo("c04-006")
def _():
    # bit/s = baudios · log2 M
    return es(100 * math.log2(8), 0) + " bit/s"


@calculo("c04-023")
def _():
    # P consumida = 13,8 V · 18 A; calor = consumida − 100 W de RF
    return es(13.8 * 18 - 100, 1) + " W"


@calculo("c04-026")
def _():
    # unos 6 dB por bit: 12 · 6
    return es(12 * 6) + " dB"


@calculo("c04-028")
def _():
    # 6 dB por unidad S, de S5 a S9
    return es((9 - 5) * 6, 0) + " dB"


@calculo("c05-001")
def _():
    # L = 32,44 + 20 log d (km) + 20 log f (MHz)
    return es(32.44 + 20 * math.log10(20) + 20 * math.log10(435), 1) + " dB"


@calculo("c05-003")
def _():
    # MUF = foF2 / cos θ; FOT = 0,85 · MUF
    muf = 8 / math.cos(math.radians(75))
    return es(0.85 * muf, 1) + " MHz"


@calculo("c05-010")
def _():
    # d = 4,12 · √h
    return es(4.12 * math.sqrt(64), 0) + " km"


@calculo("c05-012")
def _():
    # 50 % de 1000 W p. i. r. e.
    return es(0.5 * 1000, 0) + " W p. i. r. e."


@calculo("c06-001")
def _():
    # L = 143 / f = 143 / 28,5 MHz
    return es(143 / 28.5, 2) + " m"


@calculo("c06-004")
def _():
    # p. i. r. e. = 20 W · 10^((10 + 2,15) / 10)
    return es(20 * 10 ** ((10 + 2.15) / 10), 0) + " W"


@calculo("c06-008")
def _():
    # L = 71,5 / 435 MHz, en centímetros
    return es(71.5 / 435 * 100, 1) + " cm"


@calculo("c06-011")
def _():
    # ROE = Z0 / ZL = 50 / 30 (carga resistiva menor que Z0)
    return "ROE " + es(50 / 30, 2)


@calculo("c06-012")
def _():
    # |Γ| = √(Pref / Pdir); ROE = (1 + |Γ|) / (1 − |Γ|)
    g = math.sqrt(20 / 80)
    return "ROE " + es((1 + g) / (1 - g), 0)


@calculo("c06-017")
def _():
    # |Γ| = 10^(−RL/20); ROE = (1 + |Γ|) / (1 − |Γ|)
    g = 10 ** (-20 / 20)
    return "ROE " + es((1 + g) / (1 - g), 2)


@calculo("c06-019")
def _():
    # P carga = P directa − P reflejada
    return es(75 - 3, 0) + " W"


@calculo("c08-001")
def _():
    # f3 = 3 · 29,5 MHz
    return es(3 * 29.5, 1) + " MHz"


@calculo("c08-004")
def _():
    # 60 dB por debajo de 100 W, sin superar 20 mW; manda el menor (en µW)
    return es(min(100 * 10 ** (-60 / 10), 20e-3) * 1e6, 0) + " µW"


@calculo("c08-005")
def _():
    # Z ≈ Z1 · N² = 50 Ω · 4²
    return es(50 * 4 ** 2, 0) + " Ω"


@calculo("c09-011")
def _():
    # Entrada = salida − desplazamiento = 438,725 MHz − 7,6 MHz (en kHz para evitar redondeos)
    return es((438725 - 7600) / 1000, 3) + " MHz"


@calculo("c12-002")
def _():
    # Tiempo libre = 15 s − 79 símbolos / 6,25 baudios
    return es(15 - 79 / 6.25, 2) + " s"


@calculo("c12-003")
def _():
    # 4800 símbolos/s · 2 bits por símbolo (4FSK)
    return es(4800 * 2, 0) + " bit/s"


@calculo("c12-004")
def _():
    # Dial + 2 · tono: 14 074 kHz + 2 · 0,8 kHz
    return es(14074 + 2 * 0.8, 1) + " kHz"


@calculo("c13-003")
def _():
    # Δf = f · v / c = 435 MHz · 6 km/s / c; se aleja: por debajo
    return es(435e6 * 6000 / C / 1000, 1) + " kHz por debajo"


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import simulacro
    informe, fallos = comprobar(simulacro.cargar_banco())
    print("\n".join(informe))
    print(f"{len(informe) - fallos} correctas, {fallos} con fallos")
    print("Todo correcto." if not fallos else f"{fallos} fallos.")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
