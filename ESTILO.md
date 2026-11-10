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

### Legibilidad de diagramas y figuras

El texto de cualquier figura tiene que leerse **sin zoom**, en el móvil y en el escritorio (columna de unos 690 px).

- **Diagramas Mermaid en vertical por defecto**: `flowchart TB` (o `TD`). `LR` solo si caben **como máximo 4 nodos por fila**; con más, en vertical.
- **Etiquetas cortas**: unas 25 o 30 letras por línea como mucho. Si no caben, se parten con `<br/>` o se resume el texto; el detalle va en el párrafo, no en la caja. Lo mismo para las etiquetas de las flechas, que conviene reducir a una o dos palabras.
- En pantalla, la letra de un diagrama Mermaid no baja de **12 px** y la de una figura SVG, de **10 px**. Si un diagrama o una figura no caben en la columna sin bajar de ese tamaño, se desplazan en horizontal dentro de su caja en lugar de encogerse. Lo hacen `docs/javascripts/mermaid.js`, `docs/javascripts/figuras.js` y `docs/stylesheets/extra.css`; no hay que hacer nada en cada figura.
- **Figuras SVG nuevas**: letra de **12 px como mínimo** en el propio SVG y ancho natural (`viewBox`) de **800 px como máximo**, preferiblemente 700 o menos. Con eso se leen a más de 10 px en el escritorio sin desplazarse.
- Antes de dar por buena una figura, mírala en `zensical serve` con la ventana estrecha (unos 390 px, como un móvil) y ancha.
- **Al actualizar Zensical** (o la copia de Mermaid de `docs/javascripts/vendor/mermaid/`), comprueba que los diagramas Mermaid y las figuras siguen legibles en las dos anchuras. `mermaid.js` depende de cómo carga Zensical Mermaid: que use el objeto global `mermaid` si ya existe en lugar de descargarlo, que llame a `mermaid.initialize()` y `mermaid.render()` y que meta el SVG en un shadow DOM. Si una versión nueva cambia eso, el ajuste deja de aplicarse sin dar ningún error, y los diagramas vuelven a encogerse, o Zensical vuelve a descargar Mermaid de unpkg.

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
- **Cada vez que se cite normativa**, se indica el mes y el año en que se comprobó en la fuente oficial, con el formato «(comprobado en noviembre de 2026)». Es obligatorio en todas las citas, no solo en los datos que cambian con frecuencia (tasas, segmentos de banda).

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

Antes de dar un capítulo por terminado, compila una copia del proyecto en `/tmp/manual-build`, desde la raíz del repositorio:

```sh
rm -rf /tmp/manual-build
rsync -a --exclude .git --exclude .venv --exclude site ./ /tmp/manual-build/
.venv/bin/zensical build --clean --strict -f /tmp/manual-build/mkdocs.yml
```

Debe compilar sin avisos. El sitio queda en `/tmp/manual-build/site` y el repositorio no se ensucia. Se hace con una copia porque Zensical 0.0.72 no tiene opción para elegir la carpeta de salida (`zensical build` no admite `-d` ni `--site-dir`) y rechaza un `site_dir` o un `docs_dir` fuera de la carpeta del `mkdocs.yml` («must be within project root»). Repite la copia antes de cada compilación: si no, compilas la versión anterior. La CI (`.github/workflows/pages.yml`) ejecuta `zensical build --clean --strict` sobre el propio repositorio. Revisa en `zensical serve` que se ven las fórmulas, los Mermaid y las figuras en modo claro y oscuro.

## 10. Comandos de terminal

- **Los comandos con `rm` usan rutas absolutas.** Nunca `cd directorio && rm ruta/relativa`: si el `cd` falla o el directorio de trabajo no es el esperado, el borrado cae en otro sitio. Escribe `rm -f /ruta/completa/al/fichero` en una sola orden.
- La regla vale tanto para el trabajo en el repositorio y en los directorios temporales como para los ejemplos de comandos que aparezcan en los capítulos.

## 11. Privacidad

El manual es público. **No contiene datos personales del autor ni de su entorno**:

- Ni equipos presentados como propios («mi equipo», «los míos», «el que uso en casa»).
- Ni la ubicación concreta de la estación o del domicilio (municipio, barrio, calle, coordenadas, localizador de cuadrícula).
- Ni indicativos reales, salvo los oficiales o institucionales que se citen como referencia pública.
- Ni frecuencias, canales, tonos, protocolos, horarios o nombres de personas de su grupo de emergencias o de cualquier otro grupo al que pertenezca.

Los equipos se presentan como **ejemplos genéricos de equipos habituales** («un portátil bibanda de VHF/UHF de gama económica», «un receptor de onda corta de bolsillo»). Si hace falta nombrar un modelo concreto, se presenta como un equipo frecuente en el mercado, no como el del autor. Los ejemplos de indicativos usan formatos ficticios y se dicen ficticios.

## 12. Glosario

El capítulo 17 no se edita a mano: lo genera `herramientas/glosario.py` a partir de `herramientas/glosario-entradas.txt`, con una línea por término:

```text
Término @ página#ancla @ Definición breve.
```

- **Al cambiar o añadir un capítulo, actualiza las entradas afectadas y regenera el glosario.** Revisa los términos nuevos que se definen en negrita, las definiciones que cambian y los apartados que se renombran o se mueven, porque con ellos cambian las anclas.
- Cada definición ocupa una o dos líneas, con la unidad si la tiene, y solo dice lo que dice el capítulo enlazado. Si un término aparece en varios capítulos, se enlaza al apartado que mejor lo explica.
- Las siglas llevan su desarrollo y, si son inglesas, su significado en español. El desarrollo inglés tiene que estar también en el capítulo, donde se presenta la sigla.
- Los sinónimos y las siglas inglesas que tienen entrada propia en español remiten a ella con «Véase **Término**».

Para regenerarlo, compila la copia como en el §9 y ejecuta el script sobre ella:

```sh
rm -rf /tmp/manual-build
rsync -a --exclude .git --exclude .venv --exclude site ./ /tmp/manual-build/
.venv/bin/zensical build --clean --strict -f /tmp/manual-build/mkdocs.yml
python3 herramientas/glosario.py /tmp/manual-build/site
```

El script lee las anclas del sitio compilado y no escribe nada si una entrada apunta a un apartado que no existe, si hay términos duplicados o si una remisión «Véase» no tiene entrada. Después repite la copia y la compilación para comprobar el capítulo generado.

## 13. Simulacro del examen

El capítulo 16 no se edita a mano: lo genera `herramientas/simulacro.py` a partir del banco de preguntas `herramientas/simulacro.yml`, y la página la monta `docs/javascripts/simulacro.js`. El formato de cada pregunta está al principio de `simulacro.py`.

- **Al cambiar un capítulo, mantén el banco al día.** Busca en `simulacro.yml` las preguntas cuyo `enlace` apunta a ese capítulo y revisa que su enunciado, su respuesta correcta, sus incorrectas y su explicación sigan diciendo lo mismo que el texto. Si renombras o mueves un apartado, cambia el ancla. Si cambia una cifra, cámbiala también en `herramientas/calculos16.py`. Si un capítulo añade un tema que puede entrar en el examen, añade preguntas sobre él.
- Las preguntas son **propias**, como las de las autoevaluaciones de los capítulos (§1 y §8): nunca copiadas ni adaptadas del *Libro de examen* del Radio Club Utiel ni de ningún otro banco, y distintas de las de la autoevaluación del propio capítulo.
- Cada pregunta tiene una respuesta correcta y tres incorrectas plausibles, que sean errores típicos, de longitud parecida, sin «todas/ninguna de las anteriores» ni opciones que dependan de su orden, porque el simulacro las baraja. La explicación dice por qué es correcta y enlaza el apartado que la respalda, con el formato `página#ancla` del glosario.
- Texto plano, sin LaTeX ni Markdown: el simulacro lo muestra tal cual. Las respuestas van sin punto final, salvo el de una abreviatura («1000 W p. c. e.»); el enunciado y la explicación, con su puntuación normal.
- El banco necesita al menos 60 preguntas por parte y al menos una por materia del anexo II, porque cada simulacro saca una de cada materia y reparte el resto al azar. Procura que cada materia tenga unas diez, para que no se repitan siempre las mismas. `simulacro.py` avisa de las materias con menos de tres preguntas.

Para regenerarlo, compila la copia como en el §9 y ejecuta los scripts sobre ella:

```sh
rm -rf /tmp/manual-build
rsync -a --exclude .git --exclude .venv --exclude site ./ /tmp/manual-build/
.venv/bin/zensical build --clean --strict -f /tmp/manual-build/mkdocs.yml
python3 herramientas/calculos16.py
python3 herramientas/simulacro.py /tmp/manual-build/site
```

`simulacro.py` no escribe nada si una pregunta enlaza un apartado que no existe, si le falta un campo, si tiene opciones repetidas, si hay identificadores o enunciados duplicados o casi iguales, o si una cifra no coincide con `calculos16.py`. Después repite la copia y la compilación para comprobar la página generada.

Si cambias `simulacro.js`, pasa también la prueba sin navegador de `herramientas/prueba-simulacro.js`, que usa jsdom (instálalo en una carpeta temporal, fuera del repositorio):

```sh
npm install --prefix /tmp/jsdom jsdom@24.1.3
NODE_PATH=/tmp/jsdom/node_modules node herramientas/prueba-simulacro.js \
  /tmp/manual-build/site/16-autoevaluacion/index.html \
  /tmp/manual-build/site/javascripts/simulacro.js
```

Recorre un simulacro completo, la corrección y el cierre por tiempo, y comprueba en 300 simulacros por parte que siempre salen todas las materias. Todas las líneas tienen que empezar por «OK».
