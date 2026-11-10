// Ajustes de Mermaid para el manual.
//
// Zensical carga Mermaid por su cuenta, llama a mermaid.initialize() con su
// propia configuración y mete cada diagrama en un shadow DOM cerrado, así que
// ni mkdocs.yml ni una hoja de estilos llegan al SVG. Este script:
//
// 1. Hace que Mermaid salga de la copia del repositorio
//    (vendor/mermaid/mermaid.min.js) y no de unpkg, y solo en las páginas que
//    tienen algún diagrama. Zensical solo descarga Mermaid si no existe ya un
//    objeto global «mermaid»; aquí se le da un sustituto que guarda la
//    configuración y, al pedirle el primer diagrama, carga la copia local.
//    Como Zensical solo llama a render() cuando encuentra un diagrama, una
//    página sin diagramas (o una navegación sin recarga a una de ellas) no
//    descarga nada.
// 2. Fija la letra base de los diagramas en LETRA_PX.
// 3. Impide que un diagrama ancho se encoja tanto que su letra quede por debajo
//    de LETRA_MIN_PX: le pone un ancho mínimo y, si no cabe en la columna,
//    extra.css hace que se desplace en horizontal dentro de su contenedor.
//
// Depende de cómo usa Zensical 0.0.72 el objeto global: initialize() y luego
// render(id, texto). Al actualizar Zensical, compruébalo (ver ESTILO.md §5).

(function () {
  "use strict";

  var LETRA_PX = 16;      // letra base de Mermaid (su valor por defecto)
  var LETRA_MIN_PX = 12;  // letra más pequeña admitida en pantalla
  var COPIA = new URL("vendor/mermaid/mermaid.min.js", document.currentScript.src).href;

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

  var actual;       // el Mermaid de verdad, cuando ya se ha cargado
  var config;       // lo que Zensical pasó a initialize() antes de la carga
  var cargando;     // promesa de la carga de la copia local

  function cargar() {
    if (!cargando) {
      cargando = new Promise(function (resolver, rechazar) {
        var s = document.createElement("script");
        s.src = COPIA;
        s.onload = function () {
          if (!actual) return rechazar(new Error("Mermaid no se ha publicado"));
          if (config) actual.initialize(config);
          resolver(actual);
        };
        s.onerror = rechazar;
        document.head.appendChild(s);
      });
    }
    return cargando;
  }

  var sustituto = {
    initialize: function (c) { config = c; },
    render: function () {
      var args = arguments;
      return cargar().then(function (m) { return m.render.apply(m, args); });
    }
  };

  Object.defineProperty(window, "mermaid", {
    configurable: true,
    get: function () { return actual || sustituto; },
    set: function (valor) { actual = ajustar(valor); }
  });
})();
