// Configuración de MathJax para pymdownx.arithmatex (modo generic).
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// Con navigation.instant las páginas se cargan sin recargar el documento:
// hay que volver a componer las fórmulas en cada cambio de página.
document$.subscribe(() => {
  if (!window.MathJax.startup) return;
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
