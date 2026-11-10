// Ajustes de Mermaid para el manual.
//
// Zensical carga Mermaid por su cuenta, llama a mermaid.initialize() con su
// propia configuración y mete cada diagrama en un shadow DOM cerrado, así que
// ni mkdocs.yml ni una hoja de estilos llegan al SVG. Este script intercepta el
// objeto global en el momento en que Mermaid lo publica y:
//
// 1. Fija la letra base de los diagramas en LETRA_PX.
// 2. Impide que un diagrama ancho se encoja tanto que su letra quede por debajo
//    de LETRA_MIN_PX: le pone un ancho mínimo y, si no cabe en la columna,
//    extra.css hace que se desplace en horizontal dentro de su contenedor.

(function () {
  "use strict";

  var LETRA_PX = 16;      // letra base de Mermaid (su valor por defecto)
  var LETRA_MIN_PX = 12;  // letra más pequeña admitida en pantalla

  if (Object.getOwnPropertyDescriptor(window, "mermaid")) return;

  function anchoMinimo(svg) {
    var m = /viewBox="[-\d.]+ [-\d.]+ ([\d.]+) [\d.]+"/.exec(svg);
    if (!m) return svg;
    var minimo = Math.ceil(parseFloat(m[1]) * LETRA_MIN_PX / LETRA_PX);
    // Añade min-width al primer atributo style de la etiqueta <svg>.
    return svg.replace(/^(<svg[^>]*?style=")/, "$1min-width: " + minimo + "px; ");
  }

  function ajustar(mermaid) {
    if (!mermaid || mermaid.__manualAjustado) return mermaid;
    var initialize = mermaid.initialize.bind(mermaid);
    var render = mermaid.render.bind(mermaid);

    mermaid.initialize = function (config) {
      config = Object.assign({}, config);
      config.themeVariables = Object.assign({}, config.themeVariables, {
        fontSize: LETRA_PX + "px"
      });
      return initialize(config);
    };

    mermaid.render = function () {
      return render.apply(null, arguments).then(function (r) {
        return Object.assign({}, r, { svg: anchoMinimo(r.svg) });
      });
    };

    mermaid.__manualAjustado = true;
    return mermaid;
  }

  var actual;
  Object.defineProperty(window, "mermaid", {
    configurable: true,
    get: function () { return actual; },
    set: function (valor) { actual = ajustar(valor); }
  });
})();
