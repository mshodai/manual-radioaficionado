# Manual de radioaficionado

Manual libre en español para preparar el examen de la autorización de radioaficionado en España y dar los primeros pasos en la radioafición.

Léelo en <https://mshodai.github.io/manual-radioaficionado/>.

## Qué es y a quién va dirigido

Cubre el temario oficial del examen (anexo II de la Orden IET/1311/2013), desde la electricidad básica hasta la normativa española, y añade operación, telegrafía, modos digitales, satélites, escucha y comunicaciones de emergencia. Está escrito para quien parte de cero: cada fórmula se explica y lleva un ejemplo resuelto. También sirve de consulta a quien ya tiene la autorización.

## Cómo usarlo para preparar el examen

1. Empieza por el capítulo 1: explica el examen y los trámites, y su tabla del temario dice qué capítulo trata cada materia.
2. Sigue el orden de los capítulos, porque cada uno se apoya en los anteriores.
3. Haz la autoevaluación del final de cada capítulo (entre 5 y 10 preguntas con la solución explicada) antes de pasar al siguiente.
4. Termina con el simulacro del capítulo 16, que saca al azar 30 preguntas de cada parte de un banco propio, con el formato del examen oficial, y enlaza la explicación de cada fallo.

El capítulo 17 es un glosario con enlaces al apartado que explica cada término.

## Estado

Están redactados los capítulos 1 a 6 y 8 a 17. **En preparación:**

- Capítulo 7, Equipos.
- Apéndice A, Proyectos con Arduino y montajes.

## Fuentes y criterio

- **Normativa oficial.** Cada norma citada enlaza a su fuente oficial (BOE, EUR-Lex, UIT, CEPT, IARU) e indica cuándo se comprobó: «(comprobado en noviembre de 2026)». Si un dato no coincide con la fuente oficial, manda la fuente.
- **Redacción propia.** Texto, ejemplos, figuras y preguntas son originales. Los libros y apuntes de radioafición solo se han usado para decidir qué temas tratar; no se copian, traducen ni parafrasean, y ninguna pregunta procede de un banco de preguntas de examen.

## Erratas y sugerencias

[Abre un issue](https://github.com/mshodai/manual-radioaficionado/issues/new) con el capítulo y el apartado, la frase afectada y qué falla. Si es un dato normativo, enlaza la fuente oficial.

## Compilar en local

Se publica con [Zensical](https://zensical.org) 0.0.72.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/zensical serve
```

Las normas de redacción y las herramientas de comprobación están en [ESTILO.md](ESTILO.md).

## Licencia

El contenido se publica bajo [CC BY-SA 4.0](LICENSE): puedes copiarlo, repartirlo y adaptarlo, también con fines comerciales, citando la procedencia y con la misma licencia. Las copias incluidas de MathJax (Apache-2.0) y Mermaid (MIT) conservan sus licencias, en `docs/javascripts/vendor/`.
