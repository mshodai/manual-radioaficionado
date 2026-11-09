"""Código Morse internacional y temporización, compartidos por los scripts del capítulo 11.

Tabla tomada de la Recomendación UIT-R M.1677-1 (10/2009), anexo 1, parte I,
apartados 1.1.1 a 1.1.3 (comprobada en la fuente oficial en noviembre de 2026):
https://www.itu.int/rec/R-REC-M.1677-1-200910-I/es

La Ñ no figura en la recomendación; se añade aparte, marcada como uso
tradicional en español, y no se usa en los cálculos de la recomendación.

No se ejecuta por sí solo: lo importan calculos11.py, figuras11.py y audio11.py.
"""

LETRAS = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "É": "..-..",
}
CIFRAS = {
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",
}
SIGNOS = {
    ".": ".-.-.-", ",": "--..--", ":": "---...", "?": "..--..", "'": ".----.",
    "-": "-....-", "/": "-..-.", "(": "-.--.", ")": "-.--.-", '"': ".-..-.",
    "=": "-...-", "+": ".-.-.", "@": ".--.-.",
}
# Señales de servicio de la recomendación (sin carácter escrito asociado)
SERVICIO = {
    "comprendido": "...-.",
    "error": "........",
    "invitación a transmitir": "-.-",
    "espera": ".-...",
    "fin de trabajo": "...-.-",
    "señal de comienzo": "-.-.-",
}
# Uso tradicional en español, fuera de la recomendación
EXTRA_ES = {"Ñ": "--.--"}

CODIGO = {**LETRAS, **CIFRAS, **SIGNOS}

# Prosignos: secuencias que se transmiten sin espacio entre las letras.
# Se escriben entre < >: <AR>, <SK>, <KN>, <BT>...
PROSIGNOS = {
    "AR": ".-.-.", "SK": "...-.-", "KN": "-.--.", "BT": "-...-",
    "AS": ".-...", "SN": "...-.", "HH": "........", "KA": "-.-.-",
}


def unidades_caracter(seq):
    """Duración de un carácter en unidades (puntos), sin el espacio que le sigue."""
    elementos = sum(1 if s == "." else 3 for s in seq)
    return elementos + (len(seq) - 1)


def eventos(texto, codigo=None):
    """Convierte un texto en una lista de (encendido, unidades).

    Los prosignos van entre < >. Espacio entre letras: 3 unidades; entre
    palabras: 7. Devuelve también el desglose (unidades de carácter, de espacio).
    """
    codigo = codigo or {**CODIGO, **EXTRA_ES}
    out = []
    palabras = texto.upper().split()
    for np_, palabra in enumerate(palabras):
        simbolos = []
        i = 0
        while i < len(palabra):
            if palabra[i] == "<":
                j = palabra.index(">", i)
                simbolos.append(PROSIGNOS[palabra[i + 1:j]])
                i = j + 1
            else:
                simbolos.append(codigo[palabra[i]])
                i += 1
        for ns, seq in enumerate(simbolos):
            for ne, s in enumerate(seq):
                out.append((True, 1 if s == "." else 3, "c"))
                if ne < len(seq) - 1:
                    out.append((False, 1, "c"))
            if ns < len(simbolos) - 1:
                out.append((False, 3, "e"))
        out.append((False, 7, "e"))  # tras la última palabra, para encadenar
    return out


def unidades(texto):
    """(unidades de carácter, unidades de espacio) de un texto, contando el espacio final de palabra."""
    ev = eventos(texto)
    c = sum(u for _, u, k in ev if k == "c")
    e = sum(u for _, u, k in ev if k == "e")
    return c, e


def t_punto(ppm):
    """Duración del punto en segundos para una velocidad en palabras por minuto (palabra PARIS)."""
    return 1.2 / ppm


def farnsworth(c_ppm, s_ppm):
    """Unidad de espacio (s) cuando los caracteres van a c_ppm y la velocidad media es s_ppm.

    En PARIS hay 31 unidades dentro de los caracteres y 19 en los espacios. Los
    caracteres duran 31 · 1,2 / c; el resto del minuto se reparte entre las 19
    unidades de espacio.
    """
    t_total = 60 / s_ppm
    t_car = 31 * 1.2 / c_ppm
    return (t_total - t_car) / 19
