# Guía de estilo del manual

Reglas de redacción para todos los capítulos. Este archivo no se publica en el sitio: vive en la raíz del repositorio, fuera de `docs/`, y además figura en `exclude_docs` de `mkdocs.yml` por si alguna vez se copia dentro.

El capítulo [02 Electricidad y electrónica básica](docs/02-electricidad-electronica.md) es el piloto: cuando una regla deje dudas, se sigue lo que hace ese capítulo.

## 1. Originalidad

- **Todo el texto es de redacción propia.** Las fuentes (los libros y apuntes del directorio privado de fuentes, resumidos en su `FUENTES.md`) solo sirven para decidir **qué temas** tratar y con qué profundidad. No se copia, no se traduce y no se parafrasea frase a frase.
- **Ejemplos, cálculos y analogías son nuevos.** No se reutilizan los ejemplos numéricos de los libros, ni siquiera cambiando los números.
- **Ninguna pregunta de examen ajena.** Ni de los bancos de preguntas de EE. UU. ni del *Libro de examen* del Radio Club Utiel, que prohíbe expresamente reproducirlo.
- **Lo de EE. UU. no vale aquí.** De los libros estadounidenses se aprovecha solo la parte técnica. Clases de licencia, FCC, Part 97, planes de banda de la Región 2, ARES/RACES, enchufes de 120 V, AWG o medidas en pies se sustituyen por su equivalente español o europeo, o se omiten.
- Se omite lo obsoleto (válvulas, tubos de rayos catódicos, TV analógica, packet, AMTOR…) salvo que haga falta como curiosidad histórica en una línea.

## 2. Lengua

- **Español de España**, conforme a la norma de la RAE. Léxico peninsular: *ordenador*, *móvil*, *enchufe*, *pila*, *polímetro*.
- **Tuteo** al dirigirse al lector, en singular: «si conectas el amperímetro en paralelo, lo quemarás». Nada de *usted* ni *vosotros*.
- Frases cortas y voz activa. Un párrafo, una idea.
- Cada término técnico se define en negrita la primera vez que aparece. Si el término inglés es el que se oye en la banda, se da una vez entre paréntesis y en cursiva: **relación de ondas estacionarias** (*SWR*).
- Terminología preferida:

  | Usar | Evitar |
  |---|---|
  | tensión, diferencia de potencial | voltaje (se puede mencionar una vez como sinónimo coloquial) |
  | intensidad, corriente | amperaje |
  | condensador | capacitor |
  | bobina, inductor | inductancia (para el componente) |
  | resistencia (componente y magnitud) | resistor |
  | toma de tierra | *ground* |
  | ROE | SWR, VSWR (salvo la primera mención) |

- Siglas sin puntos y sin plural gráfico: *las ROE*, *los CI*.

## 3. Números y unidades

- **Sistema Internacional** siempre: metros, centímetros, milímetros, mm² para secciones de cable, kilogramos, grados Celsius. Nunca pies, pulgadas, millas, AWG ni °F.
- **Las constantes de las fórmulas ya van convertidas.** Por ejemplo, la longitud de un dipolo de media onda se da como $L\,(\text{m}) \approx 143 / f\,(\text{MHz})$, nunca con la constante en pies. Si una fuente usa unidades imperiales, se recalcula la constante; no se añade una nota de conversión.
- **Coma decimal** y espacio para separar millares en cifras de cinco o más dígitos: 3,3 kΩ; 14 200 kHz.
- Espacio entre el número y el símbolo de la unidad: 12 V, 50 Ω, 100 W, 3 dB, 25 %. Excepción: los grados de ángulo (90°).
- Símbolos de unidad sin punto y sin plural: 5 W, no «5 W.» ni «5 Ws».
- Prefijos SI en su forma correcta: k (no K), M, G, m, µ, n, p.
- Valores de la red eléctrica europea: 230 V y 50 Hz.

## 4. Fórmulas

- En **LaTeX**, que procesa `pymdownx.arithmatex` y muestra MathJax.
  - En línea: `$P = V \cdot I$`.
  - En bloque, en párrafo propio:

    ```latex
    $$
    I = \frac{V}{R}
    $$
    ```

- La coma decimal dentro de LaTeX se escribe `{,}` para que no deje espacio: `$3{,}3\ \text{k}\Omega$`.
- Las unidades, en redonda con `\text{}`: `$12\ \text{V}$`.
- Tras cada fórmula nueva se explica qué es cada símbolo y en qué unidad va.
- Cada fórmula importante lleva al menos un ejemplo resuelto con números propios.

## 5. Figuras

- **Solo figuras propias**, en **SVG** dibujado a mano o en **Mermaid**. Nunca se copia, se calca ni se redibuja una figura de las fuentes, ni se usan las imágenes de redes sociales del directorio de fuentes.
- Los esquemas eléctricos usan la **simbología europea IEC 60617** (resistencia rectangular, no en zigzag).
- Los SVG van en `docs/assets/figuras/` con el nombre `NN-descripcion.svg`, donde `NN` es el número de capítulo. Llevan fondo blanco opaco, para que se lean igual en modo claro y oscuro, y textos en español.
- Se insertan con texto alternativo descriptivo y un pie en cursiva:

  ```markdown
  ![Circuito con una pila, una resistencia y un amperímetro en serie](assets/figuras/02-medida.svg)

  *Figura 2.1. Cómo se conectan el amperímetro y el voltímetro.*
  ```

- Mermaid para diagramas de bloques y flujos (etapas de un receptor, pasos de un trámite), en un bloque ` ```mermaid `.
- Las figuras se numeran por capítulo (Figura 2.1, 2.2…).

## 6. Avisos

Se usan las cajas de `admonition` con estos tipos y títulos fijos:

| Caja | Sintaxis | Para qué |
|---|---|---|
| Para el examen | `!!! tip "Para el examen"` | Lo que hay que saberse de memoria, los cálculos típicos y las confusiones habituales. |
| En la práctica | `!!! example "En la práctica"` | Cómo se aplica en la estación real: equipos, medidas, montajes. |
| Seguridad | `!!! danger "Peligro"` | Riesgos para las personas: tensión de red, RF, altura, baterías. |
| Ampliación | `??? note "Para saber más"` | Contenido por encima del nivel del examen, plegado por defecto. |

No más de una caja seguida. Si un capítulo acumula cajas, sobran.

## 7. Normativa

- **Toda referencia a una norma lleva enlace a su fuente oficial**: BOE (texto consolidado, `https://www.boe.es/buscar/act.php?id=BOE-A-…`), EUR-Lex, UIT, CEPT (ECO Documentation Database), IARU Región 1 o la sede del ministerio competente.
- Se cita por su nombre completo la primera vez («Real Decreto 1066/2001, de 28 de septiembre, …») y abreviado después.
- No se dan como vigentes datos normativos sacados de libros, foros o del *Libro de examen*: se comprueban en la fuente oficial.
- Cuando un dato cambie con frecuencia (tasas, segmentos de banda), se indica la fecha de comprobación: «(comprobado en noviembre de 2026)».

## 8. Estructura de cada capítulo

1. Título `#` igual al de la navegación (sin el número).
2. Un párrafo de entrada que diga qué se aprende y por qué le sirve al radioaficionado.
3. Secciones `##` y, como mucho, subsecciones `###`.
4. Un resumen breve en lista (`## Resumen`).
5. **`## Autoevaluación`** al final, con **entre 5 y 10 preguntas propias**:
    - Escritas para este manual; nunca tomadas ni adaptadas de un banco de preguntas.
    - Mezcla de preguntas de cálculo y de concepto.
    - Cada solución va en una caja plegable que explica el porqué, no solo la letra:

      ```markdown
      **1.** Enunciado de la pregunta…

      a) …  
      b) …  
      c) …

      ??? success "Solución"
          **b)** Explicación breve del razonamiento.
      ```

## 9. Comprobación

Antes de dar un capítulo por terminado:

```sh
.venv/bin/zensical build --clean --strict
```

Debe compilar sin avisos. Revisa en `zensical serve` que se ven las fórmulas, los Mermaid y las figuras en modo claro y oscuro.
