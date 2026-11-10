// Simulacro del examen (capítulo 16).
//
// Lee el banco de preguntas que herramientas/simulacro.py incrusta en la página
// como JSON (<script id="simulacro-banco">) y monta el simulacro dentro de
// <div id="simulacro">. En las demás páginas no hace nada. Todo ocurre en el
// navegador y en memoria: no se envía ni se guarda nada, ni siquiera en
// localStorage.

(function () {
  "use strict";

  var NOMBRE_PARTE = { 1: "parte primera", 2: "parte segunda" };
  var TITULO_PARTE = { 1: "Parte primera: electricidad y radioelectricidad", 2: "Parte segunda: normativa" };

  var banco = null;     // datos del JSON
  var raiz = null;      // <div id="simulacro">
  var estado = null;    // simulacro en curso
  var reloj = null;     // setInterval del cronómetro
  var barra = null;     // barra fija con el progreso y el tiempo

  // --- Utilidades -----------------------------------------------------------

  function el(etiqueta, atributos, hijos) {
    var nodo = document.createElement(etiqueta);
    Object.keys(atributos || {}).forEach(function (k) {
      if (k === "texto") nodo.textContent = atributos[k];
      else if (k === "clase") nodo.className = atributos[k];
      else nodo.setAttribute(k, atributos[k]);
    });
    (hijos || []).forEach(function (h) {
      if (h) nodo.appendChild(typeof h === "string" ? document.createTextNode(h) : h);
    });
    return nodo;
  }

  function barajar(lista) {
    var a = lista.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function mmss(segundos) {
    var s = Math.max(0, Math.ceil(segundos));
    var m = Math.floor(s / 60);
    s = s % 60;
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function pararReloj() {
    if (reloj) clearInterval(reloj);
    reloj = null;
  }

  function quitarBarra() {
    if (barra && barra.parentNode) barra.parentNode.removeChild(barra);
    barra = null;
  }

  function limpiar() {
    pararReloj();
    quitarBarra();
    while (raiz.firstChild) raiz.removeChild(raiz.firstChild);
  }

  function subir() {
    var y = raiz.getBoundingClientRect().top + window.pageYOffset - 80;
    window.scrollTo(0, Math.max(0, y));
  }

  // --- Pantalla inicial -----------------------------------------------------

  function inicio() {
    limpiar();
    estado = null;
    var n1 = banco.preguntas.filter(function (p) { return p.parte === 1; }).length;
    var n2 = banco.preguntas.length - n1;

    var partes = el("fieldset", { clase: "simulacro-opciones" }, [
      el("legend", { texto: "Qué partes quieres hacer" }),
      opcionInicio("partes", "12", "Las dos partes (" + 2 * banco.porParte + " preguntas)", true),
      opcionInicio("partes", "1", "Solo la parte primera, técnica (" + banco.porParte + " de " + n1 + ")"),
      opcionInicio("partes", "2", "Solo la parte segunda, normativa (" + banco.porParte + " de " + n2 + ")")
    ]);
    var crono = el("input", { type: "checkbox", id: "simulacro-crono", checked: "checked" });
    var tiempo = el("fieldset", { clase: "simulacro-opciones" }, [
      el("legend", { texto: "Tiempo" }),
      el("label", { clase: "simulacro-opcion" }, [crono, " Cronómetro de " + banco.minutos + " minutos por parte"])
    ]);
    var boton = el("button", { type: "button", clase: "md-button md-button--primary", texto: "Empezar el simulacro" });
    boton.addEventListener("click", function () {
      var elegido = raiz.querySelector('input[name="partes"]:checked').value;
      empezar(elegido.split("").map(Number), crono.checked);
    });
    raiz.appendChild(el("div", { clase: "simulacro-inicio" }, [partes, tiempo, boton]));
  }

  function opcionInicio(nombre, valor, texto, marcado) {
    var input = el("input", { type: "radio", name: nombre, value: valor });
    if (marcado) input.checked = true;
    return el("label", { clase: "simulacro-opcion" }, [input, " " + texto]);
  }

  // --- Examen ---------------------------------------------------------------

  function empezar(partes, conReloj) {
    estado = {
      partes: partes,
      conReloj: conReloj,
      actual: 0,
      preguntas: {},
      respuestas: {},
      agotado: {}
    };
    partes.forEach(function (parte) {
      var deLaParte = banco.preguntas.filter(function (p) { return p.parte === parte; });
      estado.preguntas[parte] = elegir(deLaParte).map(function (p) {
        // La correcta es siempre opciones[0] en el banco; aquí se barajan.
        var orden = barajar([0, 1, 2, 3]);
        return { p: p, orden: orden, correcta: orden.indexOf(0) };
      });
      estado.respuestas[parte] = estado.preguntas[parte].map(function () { return null; });
    });
    mostrarParte();
  }

  // Selección estratificada: una pregunta al azar de cada materia del anexo II
  // que tenga preguntas en el banco y el resto, hasta porParte, al azar entre
  // todas las demás. Al final se baraja el orden para no agruparlas por materia.
  function elegir(deLaParte) {
    var porMateria = {};
    barajar(deLaParte).forEach(function (p) {
      (porMateria[p.materia] = porMateria[p.materia] || []).push(p);
    });
    var materias = barajar(Object.keys(porMateria));
    var elegidas = materias.map(function (m) { return porMateria[m].shift(); });
    var resto = [];
    materias.forEach(function (m) { resto = resto.concat(porMateria[m]); });
    elegidas = elegidas.slice(0, banco.porParte)
      .concat(barajar(resto).slice(0, Math.max(0, banco.porParte - elegidas.length)));
    return barajar(elegidas);
  }

  function mostrarParte() {
    limpiar();
    var parte = estado.partes[estado.actual];
    var lista = estado.preguntas[parte];

    var cabecera = el("div", { clase: "simulacro-cabecera" }, [
      el("h3", { texto: TITULO_PARTE[parte] }),
      el("p", {
        texto: lista.length + " preguntas. Apto con " + banco.apto + " aciertos" +
          (estado.conReloj ? "; tienes " + banco.minutos + " minutos." : ".")
      })
    ]);
    raiz.appendChild(cabecera);

    var ol = el("ol", { clase: "simulacro-preguntas" });
    lista.forEach(function (item, i) {
      var nombre = "sim-" + parte + "-" + i;
      var opciones = item.orden.map(function (k, j) {
        var input = el("input", { type: "radio", name: nombre, value: String(j) });
        input.addEventListener("change", function () {
          estado.respuestas[parte][i] = j;
          actualizarBarra();
        });
        return el("label", { clase: "simulacro-opcion" }, [
          input,
          el("span", { clase: "simulacro-letra", texto: "abcd"[j] + ")" }),
          el("span", { texto: item.p.opciones[k] })
        ]);
      });
      var fs = el("fieldset", { clase: "simulacro-pregunta" }, [
        el("legend", { texto: item.p.pregunta })
      ].concat(opciones));
      ol.appendChild(el("li", {}, [fs]));
    });
    raiz.appendChild(ol);

    var aviso = el("p", { clase: "simulacro-aviso", role: "status" });
    var terminar = el("button", {
      type: "button", clase: "md-button md-button--primary",
      texto: "Terminar la " + NOMBRE_PARTE[parte]
    });
    var confirmar = false;
    terminar.addEventListener("click", function () {
      var blancas = estado.respuestas[parte].filter(function (r) { return r === null; }).length;
      if (blancas && !confirmar) {
        confirmar = true;
        aviso.textContent = "Te quedan " + blancas + (blancas === 1 ? " pregunta" : " preguntas") +
          " sin responder. Pulsa otra vez para terminar de todos modos.";
        terminar.textContent = "Terminar de todos modos";
        return;
      }
      cerrarParte(false);
    });
    raiz.appendChild(el("div", { clase: "simulacro-pie" }, [aviso, terminar]));

    barra = el("div", { clase: "simulacro-barra", "aria-live": "off" });
    document.body.appendChild(barra);
    if (estado.conReloj) {
      var fin = Date.now() + banco.minutos * 60 * 1000;
      estado.fin = fin;
      reloj = setInterval(function () {
        if (!document.body.contains(raiz)) { limpiarTodo(); return; }
        if (Date.now() >= fin) cerrarParte(true);
        else actualizarBarra();
      }, 1000);
    }
    actualizarBarra();
    subir();
  }

  function actualizarBarra() {
    if (!barra || !estado) return;
    var parte = estado.partes[estado.actual];
    var hechas = estado.respuestas[parte].filter(function (r) { return r !== null; }).length;
    var texto = (estado.partes.length > 1 ? "Parte " + (estado.actual + 1) + " de 2 · " : "") +
      hechas + "/" + estado.preguntas[parte].length + " respondidas";
    barra.textContent = "";
    barra.appendChild(el("span", { texto: texto }));
    if (estado.conReloj) {
      var resta = (estado.fin - Date.now()) / 1000;
      barra.appendChild(el("span", {
        clase: "simulacro-tiempo" + (resta < 300 ? " simulacro-tiempo--poco" : ""),
        texto: mmss(resta)
      }));
    }
  }

  function cerrarParte(porTiempo) {
    pararReloj();
    var parte = estado.partes[estado.actual];
    estado.agotado[parte] = porTiempo;
    estado.actual++;
    if (estado.actual < estado.partes.length) {
      mostrarParte();
      if (porTiempo) {
        raiz.insertBefore(el("p", {
          clase: "simulacro-aviso",
          texto: "Se acabó el tiempo de la parte primera. Las preguntas sin responder cuentan como no acertadas."
        }), raiz.firstChild);
      }
    } else {
      resultados();
    }
  }

  // --- Corrección -----------------------------------------------------------

  function resultados() {
    limpiar();
    var aptos = 0;
    var bloques = [];
    estado.partes.forEach(function (parte) {
      var lista = estado.preguntas[parte];
      var resp = estado.respuestas[parte];
      var aciertos = 0, blancas = 0;
      var fallos = [];
      lista.forEach(function (item, i) {
        if (resp[i] === item.correcta) aciertos++;
        else {
          if (resp[i] === null) blancas++;
          fallos.push({ item: item, numero: i + 1, respuesta: resp[i] });
        }
      });
      var apto = aciertos >= banco.apto;
      if (apto) aptos++;
      bloques.push({ parte: parte, aciertos: aciertos, blancas: blancas, fallos: fallos, apto: apto, total: lista.length });
    });

    var resumen = el("div", { clase: "simulacro-resumen" });
    bloques.forEach(function (b) {
      var detalle = b.aciertos + " de " + b.total + " aciertos";
      if (b.blancas) detalle += " (" + b.blancas + " en blanco)";
      if (estado.agotado[b.parte]) detalle += ", con el tiempo agotado";
      resumen.appendChild(el("div", { clase: "simulacro-nota " + (b.apto ? "simulacro-apto" : "simulacro-noapto") }, [
        el("strong", { texto: TITULO_PARTE[b.parte].split(":")[0] + ": " + (b.apto ? "apto" : "no apto") }),
        el("span", { texto: detalle })
      ]));
    });
    var veredicto;
    if (estado.partes.length === 2) {
      veredicto = aptos === 2
        ? "Serías apto en las dos partes: aprobarías el examen."
        : aptos === 1
          ? "Serías apto en una parte. En el examen real la conservarías y repetirías solo la otra."
          : "No serías apto en ninguna parte. Repasa los apartados de las preguntas falladas y vuelve a intentarlo.";
    } else {
      veredicto = aptos ? "Serías apto en esta parte." : "No serías apto en esta parte. Repasa los apartados de las preguntas falladas.";
    }
    raiz.appendChild(el("h3", { texto: "Resultado" }));
    raiz.appendChild(resumen);
    raiz.appendChild(el("p", { clase: "simulacro-veredicto", texto: veredicto }));
    raiz.appendChild(botonNuevo());

    bloques.forEach(function (b) {
      raiz.appendChild(el("h3", { texto: "Preguntas falladas o en blanco de la " + NOMBRE_PARTE[b.parte] }));
      if (!b.fallos.length) {
        raiz.appendChild(el("p", { texto: "Ninguno: has acertado todas las preguntas de esta parte." }));
        return;
      }
      raiz.appendChild(porMateria(b));
      var ol = el("ol", { clase: "simulacro-fallos" });
      b.fallos.forEach(function (f) {
        var p = f.item.p;
        var tuya = f.respuesta === null ? "En blanco" : "abcd"[f.respuesta] + ") " + p.opciones[f.item.orden[f.respuesta]];
        var buena = "abcd"[f.item.correcta] + ") " + p.opciones[0];
        var li = el("li", { value: String(f.numero) }, [
          el("p", { clase: "simulacro-enunciado", texto: p.pregunta }),
          el("p", { clase: "simulacro-tuya" }, [el("strong", { texto: "Tu respuesta: " }), tuya]),
          el("p", { clase: "simulacro-buena" }, [el("strong", { texto: "Correcta: " }), buena]),
          el("p", { texto: p.explicacion }),
          el("p", {}, ["Repasa: ", el("a", { href: p.url, texto: p.apartado }), "."])
        ]);
        ol.appendChild(li);
      });
      raiz.appendChild(ol);
    });
    if (bloques.some(function (b) { return b.fallos.length > 3; })) raiz.appendChild(botonNuevo());
    subir();
  }

  function porMateria(b) {
    var cuenta = {};
    b.fallos.forEach(function (f) {
      var m = f.item.p.materia;
      cuenta[m] = (cuenta[m] || 0) + 1;
    });
    var nombres = banco.materias[String(b.parte)];
    var orden = Object.keys(cuenta).sort(function (x, y) { return cuenta[y] - cuenta[x] || x - y; });
    return el("p", { clase: "simulacro-materias" }, [
      el("strong", { texto: "Por materias del anexo II: " }),
      orden.map(function (m) { return nombres[m] + " (" + cuenta[m] + ")"; }).join(" · ")
    ]);
  }

  function botonNuevo() {
    var b = el("button", { type: "button", clase: "md-button", texto: "Hacer otro simulacro" });
    b.addEventListener("click", function () { inicio(); subir(); });
    return b;
  }

  // --- Arranque -------------------------------------------------------------

  function limpiarTodo() {
    pararReloj();
    quitarBarra();
    estado = null;
  }

  function arrancar() {
    // Con navigation.instant la página cambia sin recargar: se para lo que hubiera.
    limpiarTodo();
    raiz = document.getElementById("simulacro");
    var datos = document.getElementById("simulacro-banco");
    if (!raiz || !datos) return;
    try {
      banco = JSON.parse(datos.textContent);
    } catch (e) {
      raiz.textContent = "No se ha podido leer el banco de preguntas.";
      return;
    }
    inicio();
  }

  if (window.document$) document$.subscribe(arrancar);
  else document.addEventListener("DOMContentLoaded", arrancar);
})();
