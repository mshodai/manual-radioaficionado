# Manual de radioaficionado

Manual libre (CC BY-SA 4.0) en español para preparar la autorización de radioaficionado en España. Se publica con Zensical 0.0.72 en GitHub Pages.

## Redacción

**Lee y sigue [ESTILO.md](ESTILO.md) antes de escribir o revisar cualquier capítulo.** Lo esencial:

- Redacción propia: las fuentes solo indican qué temas tratar; no se copian, traducen ni parafrasean, ni se toman sus preguntas o figuras.
- Español de España, tuteo, unidades SI, fórmulas en LaTeX, figuras propias en SVG o Mermaid.
- Normativa siempre enlazada a la fuente oficial.
- Privacidad: el manual es público; nada de datos personales del autor ni de su entorno (ver ESTILO.md §11).

Las fuentes están en `../manual-radioaficionado-fuentes/` (privado, con derechos de autor); su `FUENTES.md` indica qué secciones consultar para cada capítulo.

## Estructura

- `docs/`: contenido publicado, un archivo por capítulo (`NN-tema.md`); figuras en `docs/assets/figuras/`.
- `docs/javascripts/`: MathJax 3.2.2 (`vendor/mathjax/`, Apache-2.0) y Mermaid 11.17.2 (`vendor/mermaid/`, MIT) incluidos en el repositorio, sin CDN; `mathjax.js` configura MathJax, `mermaid.js` ajusta el tamaño de letra de los diagramas y `figuras.js` el de las figuras SVG. Estilos en `docs/stylesheets/extra.css`.
- `herramientas/`: scripts que generan contenido y no se publican. `figurasNN.py` dibuja los SVG del capítulo NN: `python3 herramientas/figurasNN.py docs/assets/figuras`. `glosario.py` genera el glosario (cap. 17) a partir de `glosario-entradas.txt` y valida sus anclas; ver ESTILO.md §12. `simulacro.py` valida el banco `simulacro.yml` y genera el simulacro (cap. 16); ver ESTILO.md §13.
- `mkdocs.yml`: configuración y navegación.
- `ESTILO.md` y `CLAUDE.md` están en la raíz, fuera de `docs/`, y no se publican.

## Compilar

    .venv/bin/zensical serve                   # vista previa local
    .venv/bin/zensical build --clean --strict  # lo que ejecuta la CI; debe pasar sin avisos
