# Manual de radioaficionado

Manual libre (CC BY-SA 4.0) en español para preparar la autorización de radioaficionado en España. Se publica con Zensical 0.0.72 en GitHub Pages.

## Redacción

**Lee y sigue [ESTILO.md](ESTILO.md) antes de escribir o revisar cualquier capítulo.** Lo esencial:

- Redacción propia: las fuentes solo indican qué temas tratar; no se copian, traducen ni parafrasean, ni se toman sus preguntas o figuras.
- Español de España, tuteo, unidades SI, fórmulas en LaTeX, figuras propias en SVG o Mermaid.
- Normativa siempre enlazada a la fuente oficial.

Las fuentes están en `../manual-radioaficionado-fuentes/` (privado, con derechos de autor); su `FUENTES.md` indica qué secciones consultar para cada capítulo.

## Estructura

- `docs/`: contenido publicado, un archivo por capítulo (`NN-tema.md`); figuras en `docs/assets/figuras/`.
- `docs/javascripts/`: configuración de MathJax (`mathjax.js`) y MathJax 3.2.2 incluido en el repositorio (`vendor/mathjax/`, Apache-2.0), sin CDN.
- `herramientas/`: scripts que generan contenido y no se publican. `figurasNN.py` dibuja los SVG del capítulo NN: `python3 herramientas/figurasNN.py docs/assets/figuras`.
- `mkdocs.yml`: configuración y navegación.
- `ESTILO.md` y `CLAUDE.md` están en la raíz, fuera de `docs/`, y no se publican.

## Compilar

    .venv/bin/zensical serve                   # vista previa local
    .venv/bin/zensical build --clean --strict  # lo que ejecuta la CI; debe pasar sin avisos
