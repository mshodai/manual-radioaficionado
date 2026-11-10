"""Valida el banco del simulacro y genera el capítulo 16 (Autoevaluación).

Uso, desde la raíz del repositorio, con una copia del sitio ya compilada
(ver ESTILO.md, §9 y §13):

    python3 herramientas/simulacro.py /tmp/manual-build/site

Lee herramientas/simulacro.yml y comprueba que:
- cada pregunta tiene los campos que tocan, con una respuesta correcta y tres
  incorrectas, las cuatro distintas;
- las materias existen en el anexo II de la Orden IET/1311/2013 para su parte;
- el enlace apunta a un apartado (h1-h3) que existe en el sitio compilado;
- no hay identificadores repetidos ni preguntas duplicadas o casi iguales;
- las cifras de las preguntas de cálculo coinciden con calculos16.py;
- cada parte tiene al menos MINIMO preguntas y cada materia al menos una, porque
  simulacro.js pone en cada simulacro una pregunta de cada materia.

Si todo está bien, escribe docs/16-autoevaluacion.md con el banco incrustado
como JSON; la página la monta docs/javascripts/simulacro.js. Si algo falla, no
escribe nada y termina con error.

Para comprobar un fragmento suelto del banco sin generar la página:

    python3 herramientas/simulacro.py --fragmento preguntas.yml [--calculos calc.py] SITIO

Formato de cada pregunta en simulacro.yml:

    - id: c02-001                 # cNN-NNN, NN = capítulo del enlace
      parte: 1                    # 1 (técnica) o 2 (normativa)
      materia: 1                  # apartado del anexo II dentro de su parte
      pregunta: "Enunciado…"
      correcta: "Respuesta correcta"
      incorrectas:
        - "Error típico 1"
        - "Error típico 2"
        - "Error típico 3"
      explicacion: "Por qué es la correcta y dónde está el error típico."
      enlace: 02-electricidad-electronica#ley-de-ohm
      calculo: true               # opcional: cifras comprobadas en calculos16.py
"""

import difflib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from glosario import anclas  # noqa: E402
import calculos16  # noqa: E402

BANCO = RAIZ / "herramientas" / "simulacro.yml"
SALIDA = RAIZ / "docs" / "16-autoevaluacion.md"
MINIMO = 60          # preguntas por parte en el banco
POR_PARTE = 30       # preguntas por parte en cada simulacro
APTO = 15            # aciertos para ser apto en una parte
MINUTOS = 45         # tiempo por parte
PARECIDO = 0.85      # a partir de aquí, dos enunciados se consideran duplicados

# Apartados del anexo II de la Orden IET/1311/2013 (resumidos como en el cap. 1).
MATERIAS = {
    1: {
        1: "Teoría de la electricidad, electromagnetismo y radio",
        2: "Componentes",
        3: "Circuitos",
        4: "Receptores",
        5: "Transmisores",
        6: "Antenas y líneas de transmisión",
        7: "Propagación",
        8: "Medidas",
        9: "Interferencia e inmunidad",
        10: "Seguridad",
    },
    2: {
        1: "Alfabeto fonético internacional",
        2: "Código Q",
        3: "Abreviaturas",
        4: "Socorro, urgencia, seguridad y catástrofes",
        5: "Distintivos de llamada",
        6: "Planes de bandas de la IARU",
        7: "Responsabilidad social y procedimientos operativos",
        8: "Reglamentación nacional e internacional",
        9: "Inspección y régimen sancionador",
    },
}
CAMPOS = {"id", "parte", "materia", "pregunta", "correcta", "incorrectas", "explicacion", "enlace"}
OPCIONALES = {"calculo"}
PROHIBIDO = re.compile(r"anteriores|\b[a-d]\) y [a-d]\)", re.I)
# Las opciones van sin punto final, salvo el de una abreviatura (p. i. r. e.).
ABREVIATURA = re.compile(r"\b(p\. c\. e|p\. i\. r\. e|p\. r\. a|etc)\.$")


def normal(s: str) -> str:
    """Minúsculas, sin tildes, signos ni espacios repetidos (para comparar textos)."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join(re.sub(r"[^\w]+", " ", s).split())


def cargar_banco(ruta: Path = BANCO) -> list:
    datos = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    return datos or []


def validar(banco: list, mapa: dict, completo: bool) -> list:
    errores = []
    ids = {}
    for n, p in enumerate(banco, 1):
        ident = p.get("id", f"#{n}") if isinstance(p, dict) else f"#{n}"
        if not isinstance(p, dict):
            errores.append(f"{ident}: no es un diccionario")
            continue
        faltan = CAMPOS - p.keys()
        sobran = p.keys() - CAMPOS - OPCIONALES
        if faltan:
            errores.append(f"{ident}: faltan campos {sorted(faltan)}")
            continue
        if sobran:
            errores.append(f"{ident}: campos desconocidos {sorted(sobran)}")
        if not re.fullmatch(r"c\d\d-\d{3}", str(ident)):
            errores.append(f"{ident}: el id debe ser cNN-NNN")
        if ident in ids:
            errores.append(f"{ident}: id repetido")
        ids[ident] = p
        if p["parte"] not in MATERIAS:
            errores.append(f"{ident}: parte {p['parte']} inexistente")
        elif p["materia"] not in MATERIAS[p["parte"]]:
            errores.append(f"{ident}: la parte {p['parte']} no tiene materia {p['materia']}")
        textos = [p["pregunta"], p["correcta"], *p["incorrectas"], p["explicacion"]]
        if not all(isinstance(t, str) and t.strip() for t in textos):
            errores.append(f"{ident}: hay textos vacíos o que no son cadenas")
            continue
        if len(p["incorrectas"]) != 3:
            errores.append(f"{ident}: tiene {len(p['incorrectas'])} incorrectas en lugar de 3")
        opciones = [p["correcta"], *p["incorrectas"]]
        if len({normal(o) for o in opciones}) != len(opciones):
            errores.append(f"{ident}: hay opciones repetidas")
        for o in opciones:
            if PROHIBIDO.search(o):
                errores.append(f"{ident}: opción que depende de las demás o de su orden: «{o}»")
            if o.endswith(".") and not ABREVIATURA.search(o):
                errores.append(f"{ident}: opción con punto final: «{o}»")
        for t in textos:
            if re.search(r"[$`*_\\]|\]\(|<[a-z/]", t):
                errores.append(f"{ident}: texto con LaTeX, Markdown o HTML: «{t[:50]}…»")
                break
        if str(p["enlace"]).endswith(".md") or ".md#" in str(p["enlace"]):
            errores.append(f"{ident}: el enlace va sin .md (página#ancla)")
        elif p["enlace"] not in mapa:
            errores.append(f"{ident}: ancla inexistente {p['enlace']}")
        else:
            cap = p["enlace"][:2]
            if str(ident)[1:3] != cap:
                errores.append(f"{ident}: el id no coincide con el capítulo del enlace ({cap})")
        if "calculo" in p and p["calculo"] is not True:
            errores.append(f"{ident}: «calculo» solo puede valer true")

    # Duplicados y casi duplicados (mismo enunciado o enunciado muy parecido).
    validas = [p for p in banco if isinstance(p, dict) and isinstance(p.get("pregunta"), str)]
    norm = [normal(p["pregunta"]) for p in validas]
    for i in range(len(validas)):
        for j in range(i + 1, len(validas)):
            sm = difflib.SequenceMatcher(None, norm[i], norm[j])
            if sm.real_quick_ratio() >= PARECIDO and sm.quick_ratio() >= PARECIDO and sm.ratio() >= PARECIDO:
                errores.append(f"{validas[i].get('id')} y {validas[j].get('id')}: enunciados casi iguales")

    informe, fallos = calculos16.comprobar(validas)
    # Con un fragmento suelto, calculos16.py tiene también las funciones del
    # resto del banco: solo se comprueba que las preguntas tengan su función.
    errores += [linea for linea in informe if linea.startswith("MAL")
                and (completo or "función sin pregunta" not in linea)]

    if completo:
        for parte in MATERIAS:
            n = sum(1 for p in validas if p.get("parte") == parte)
            if n < MINIMO:
                errores.append(f"la parte {parte} tiene {n} preguntas; hacen falta al menos {MINIMO}")
            for m, nombre in MATERIAS[parte].items():
                if not any(p.get("parte") == parte and p.get("materia") == m for p in validas):
                    errores.append(f"parte {parte}, materia {m} ({nombre}): no tiene ninguna pregunta")
    return errores


def avisos(banco: list) -> list:
    """Sesgos que no impiden generar la página, pero conviene vigilar."""
    res = []
    larga = [p["id"] for p in banco if len(p["correcta"]) > 1.3 * max(len(i) for i in p["incorrectas"])]
    if len(larga) > len(banco) // 5:
        res.append(f"la correcta es claramente la más larga en {len(larga)} de {len(banco)} preguntas")
    for parte, materias in MATERIAS.items():
        for m, nombre in materias.items():
            n = sum(1 for p in banco if p["parte"] == parte and p["materia"] == m)
            if n < 3:
                res.append(f"parte {parte}, materia {m} ({nombre}): solo {n} preguntas")
    return res


def url(enlace: str) -> str:
    """Enlace relativo a la página del capítulo 16 (URL de directorio)."""
    pagina, frag = enlace.split("#")
    return f"../{pagina}/#{frag}"


def tabla_materias(banco: list) -> str:
    filas = []
    for parte, materias in MATERIAS.items():
        nombre_parte = "Primera" if parte == 1 else "Segunda"
        for m, nombre in materias.items():
            n = sum(1 for p in banco if p["parte"] == parte and p["materia"] == m)
            filas.append(f"| {nombre_parte} | {m}. {nombre} | {n} |")
    return "\n".join(["| Parte | Apartado del anexo II | Preguntas |", "|---|---|---|", *filas])


def generar(banco: list, mapa: dict) -> str:
    datos = {
        "porParte": POR_PARTE,
        "apto": APTO,
        "minutos": MINUTOS,
        "materias": {str(k): {str(m): n for m, n in v.items()} for k, v in MATERIAS.items()},
        "preguntas": [
            {
                "id": p["id"],
                "parte": p["parte"],
                "materia": p["materia"],
                "pregunta": p["pregunta"],
                "opciones": [p["correcta"], *p["incorrectas"]],
                "explicacion": p["explicacion"],
                "url": url(p["enlace"]),
                "apartado": f"Cap. {int(p['enlace'][:2])}, «{mapa[p['enlace']]}»",
            }
            for p in banco
        ],
    }
    # «<» escapado para que ningún texto pueda cerrar la etiqueta <script>.
    json_banco = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    n1 = sum(1 for p in banco if p["parte"] == 1)
    n2 = sum(1 for p in banco if p["parte"] == 2)
    return PLANTILLA.format(
        n=len(banco), n1=n1, n2=n2, por_parte=POR_PARTE, apto=APTO, minutos=MINUTOS,
        tabla=tabla_materias(banco), json=json_banco,
    )


PLANTILLA = """\
# Autoevaluación

<!-- Página generada por herramientas/simulacro.py a partir de herramientas/simulacro.yml. No la edites a mano. -->

Este capítulo es un **simulacro del examen**. Cada vez que lo empiezas saca al azar {por_parte} preguntas de cada parte de un banco de {n} preguntas escritas para este manual, y te las plantea con el formato del examen oficial. Al terminar te dice cuántas has acertado en cada parte, si serías apto y por qué has fallado cada pregunta, con un enlace al apartado del manual que la explica. Hazlo cuando hayas estudiado los capítulos: te dirá qué temas tienes flojos y te acostumbrará al ritmo del examen.

## El formato

El simulacro sigue el formato del examen que viste en el [capítulo 1](01-autorizacion.md#formato), fijado por la base primera de la [Resolución de 3 de junio de 2014, de la Secretaría de Estado de Telecomunicaciones y para la Sociedad de la Información, por la que se establece el procedimiento para la realización del examen de capacitación para operar estaciones de radioaficionado](https://www.boe.es/buscar/doc.php?id=BOE-A-2014-6461) (comprobado en noviembre de 2026). Las materias de cada parte son las del [anexo II de la Orden IET/1311/2013](01-autorizacion.md#el-temario).

| | Parte primera | Parte segunda |
|---|---|---|
| Materia | Electricidad y radioelectricidad | Normativa |
| Preguntas | {por_parte}, tipo test, con cuatro respuestas | {por_parte}, tipo test, con cuatro respuestas |
| Para ser apto | {apto} aciertos | {apto} aciertos |
| Tiempo | {minutos} minutos | {minutos} minutos |

Las preguntas en blanco no suman y los fallos no restan, porque la resolución no dice que resten. Cada parte se califica por separado: si quieres practicar solo la que te queda pendiente, elige esa parte al empezar. Cada simulacro incluye al menos una pregunta de cada apartado del anexo II de su parte y reparte el resto al azar; el orden de las preguntas y el de las respuestas cambian cada vez.

!!! tip "Para el examen"
    Las preguntas de este simulacro son propias del manual: no son las del examen oficial ni están sacadas de ningún banco de preguntas. Sirven para comprobar que entiendes cada tema, no para memorizar respuestas. Si fallas una, lee el apartado enlazado antes de repetir.

## Simulacro

<div id="simulacro-app" class="simulacro">
<noscript><p>El simulacro necesita JavaScript. Actívalo en el navegador para hacerlo.</p></noscript>
</div>

<script type="application/json" id="simulacro-banco">{json}</script>

El simulacro funciona entero en tu navegador: no envía tus respuestas a ningún sitio ni guarda nada. Si recargas la página o cambias de capítulo, se pierde el simulacro en curso.

## El banco de preguntas

El banco tiene **{n} preguntas**: {n1} de la parte primera y {n2} de la segunda. Así se reparten entre los apartados del anexo II:

{tabla}

Las preguntas se mantienen al día con los capítulos: cuando cambia un apartado del manual, cambian también las preguntas que lo enlazan.
"""


def main() -> int:
    args = sys.argv[1:]
    fragmento = calc = None
    if "--fragmento" in args:
        i = args.index("--fragmento")
        fragmento = Path(args[i + 1])
        del args[i:i + 2]
    if "--calculos" in args:
        i = args.index("--calculos")
        calc = Path(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__)
        return 2
    mapa = anclas(Path(args[0]))
    if not mapa:
        print(f"No hay páginas compiladas en {args[0]}")
        return 1
    if calc:
        exec(compile(calc.read_text(encoding="utf-8"), str(calc), "exec"), calculos16.__dict__)

    banco = cargar_banco(fragmento or BANCO)
    errores = validar(banco, mapa, completo=fragmento is None)
    if errores:
        print("\n".join(errores))
        print(f"{len(errores)} errores")
        return 1
    for a in avisos(banco) if fragmento is None else []:
        print("Aviso:", a)
    if fragmento:
        print(f"{len(banco)} preguntas correctas en {fragmento}")
        return 0
    SALIDA.write_text(generar(banco, mapa), encoding="utf-8")
    n1 = sum(1 for p in banco if p["parte"] == 1)
    print(f"{len(banco)} preguntas ({n1} de la parte primera, {len(banco) - n1} de la segunda) en {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
