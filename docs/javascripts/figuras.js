// Figuras SVG: que no se encojan hasta hacer ilegible su texto.
//
// Por defecto una imagen se reduce al ancho de la columna, y en un móvil una
// figura de 800 px queda a menos de la mitad. Este script lee la letra más
// pequeña de cada SVG y le pone un ancho mínimo para que esa letra no baje de
// LETRA_MIN_PX en pantalla. Si la figura no cabe, extra.css hace que se
// desplace en horizontal dentro de su párrafo.

(function () {
  "use strict";

  var LETRA_MIN_PX = 10;
  var cache = {};

  function letraMinima(src) {
    if (!cache[src]) {
      cache[src] = fetch(src)
        .then(function (r) { return r.text(); })
        .then(function (svg) {
          var tam = [], re = /font-size="([\d.]+)"/g, m;
          while ((m = re.exec(svg))) tam.push(parseFloat(m[1]));
          return tam.length ? Math.min.apply(null, tam) : null;
        })
        .catch(function () { return null; });
    }
    return cache[src];
  }

  function ajustar(img) {
    var aplicar = function () {
      letraMinima(img.src).then(function (letra) {
        if (!letra || !img.naturalWidth) return;
        var minimo = Math.ceil(img.naturalWidth * LETRA_MIN_PX / letra);
        if (minimo < img.naturalWidth) img.style.minWidth = minimo + "px";
        else img.style.minWidth = img.naturalWidth + "px";
      });
    };
    if (img.complete) aplicar(); else img.addEventListener("load", aplicar, { once: true });
  }

  function recorrer() {
    document.querySelectorAll('.md-typeset img[src$=".svg"]').forEach(ajustar);
  }

  // Con navigation.instant, document$ emite en cada cambio de página.
  if (window.document$) document$.subscribe(recorrer);
  else document.addEventListener("DOMContentLoaded", recorrer);
})();
