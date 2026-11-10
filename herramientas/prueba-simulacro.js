// Prueba del simulacro del capítulo 16 con jsdom, sin navegador.
//
// Uso, con el sitio compilado en /tmp/manual-build (ESTILO.md §9 y §13) y
// jsdom instalado fuera del repositorio (npm install jsdom@24.1.3 en una
// carpeta temporal, que se indica con NODE_PATH):
//
//   NODE_PATH=/carpeta/node_modules node herramientas/prueba-simulacro.js \
//     /tmp/manual-build/site/16-autoevaluacion/index.html \
//     /tmp/manual-build/site/javascripts/simulacro.js
//
// Recorre un simulacro completo, comprueba la corrección, el cierre por tiempo
// y que la selección estratificada saca siempre todas las materias.
const fs = require("fs");
const { JSDOM } = require("jsdom");
const [html, js] = [fs.readFileSync(process.argv[2], "utf8"), fs.readFileSync(process.argv[3], "utf8")];
const dom = new JSDOM(html, { runScripts: "outside-only", pretendToBeVisual: true });
const w = dom.window, d = w.document;
w.scrollTo = () => {};
w.eval(js);
d.dispatchEvent(new w.Event("DOMContentLoaded"));
const banco = JSON.parse(d.getElementById("simulacro-banco").textContent);
// La correcta de cada pregunta, por su enunciado: una opción incorrecta de una
// pregunta puede coincidir con la correcta de otra («25 W», «ROE 1,67»).
const correctaDe = new Map(banco.preguntas.map(p => [p.pregunta, p.opciones[0]]));
const buenaDe = f => [...f.querySelectorAll("label")]
  .find(l => l.lastChild.textContent === correctaDe.get(f.querySelector("legend").textContent));
const ok = (c, m) => { console.log((c ? "OK  " : "MAL ") + m); if (!c) process.exitCode = 1; };
const raiz = d.getElementById("simulacro-app");
const boton = t => [...raiz.querySelectorAll("button")].find(b => b.textContent.startsWith(t));

ok(raiz.tagName === "DIV" && raiz.classList.contains("simulacro") && d.querySelectorAll("#simulacro-app").length === 1,
  "contenedor único <div class=\"simulacro\">, no un título con el mismo id");

ok(raiz.querySelectorAll('input[name="partes"]').length === 3, "pantalla inicial con 3 opciones de partes");
boton("Empezar").click();
let preguntas = raiz.querySelectorAll(".simulacro-pregunta");
ok(preguntas.length === 30, "parte primera con 30 preguntas (" + preguntas.length + ")");
const ids1 = new Set([...preguntas].map(f => f.querySelector("legend").textContent));
ok(ids1.size === 30, "sin preguntas repetidas en la parte");
ok(d.querySelector(".simulacro-barra") && /0\/30/.test(d.querySelector(".simulacro-barra").textContent), "barra con progreso y tiempo: " + d.querySelector(".simulacro-barra").textContent);
// Parte 1: 20 correctas, 10 incorrectas.
[...preguntas].forEach((f, i) => {
  const labels = [...f.querySelectorAll("label")];
  const buena = buenaDe(f);
  const elegida = i < 20 ? buena : labels.find(l => l !== buena);
  const input = elegida.querySelector("input");
  input.checked = true;
  input.dispatchEvent(new w.Event("change"));
});
ok(/30\/30/.test(d.querySelector(".simulacro-barra").textContent), "progreso 30/30");
boton("Terminar").click();
preguntas = raiz.querySelectorAll(".simulacro-pregunta");
ok(preguntas.length === 30 && /Parte segunda/.test(raiz.textContent), "pasa a la parte segunda");
// Parte 2: 10 correctas, 20 en blanco.
[...preguntas].slice(0, 10).forEach(f => {
  const buena = buenaDe(f);
  buena.querySelector("input").checked = true;
  buena.querySelector("input").dispatchEvent(new w.Event("change"));
});
boton("Terminar").click();
ok(/20 preguntas sin responder/.test(raiz.textContent), "pide confirmación con preguntas en blanco");
boton("Terminar de todos modos").click();
const texto = raiz.textContent;
ok(/Parte primera: apto20 de 30 aciertos/.test(texto), "parte primera apta con 20");
ok(/Parte segunda: no apto10 de 30 aciertos \(20 en blanco\)/.test(texto), "parte segunda no apta con 10 y 20 en blanco");
ok(/Serías apto en una parte/.test(texto), "veredicto de una parte");
const fallos = raiz.querySelectorAll(".simulacro-fallos > li");
ok(fallos.length === 30, "30 fallos listados (" + fallos.length + ")");
ok([...fallos].every(li => li.querySelector("a[href^='../']") && /Correcta: [a-d]\)/.test(li.textContent)), "cada fallo con correcta y enlace");
ok(/En blanco/.test(texto), "las blancas aparecen como «En blanco»");
ok(!d.querySelector(".simulacro-barra"), "la barra desaparece al corregir");
console.log("Ejemplo de fallo:\n  " + fallos[0].textContent.slice(0, 400));
boton("Hacer otro").click();
ok(raiz.querySelectorAll('input[name="partes"]').length === 3, "vuelve a la pantalla inicial");
// Solo la parte segunda y sin cronómetro.
raiz.querySelector('input[value="2"]').checked = true;
d.getElementById("simulacro-crono").checked = false;
boton("Empezar").click();
ok(/Parte segunda/.test(raiz.textContent) && !d.querySelector(".simulacro-tiempo"), "solo parte segunda, sin cronómetro");
w.close();

// Selección estratificada: en 300 simulacros de cada parte, todas las materias
// salen siempre y no se repite ninguna pregunta dentro de un simulacro.
{
  const dom2 = new JSDOM(html, { runScripts: "outside-only", pretendToBeVisual: true });
  const w2 = dom2.window, d2 = w2.document;
  w2.scrollTo = () => {};
  w2.eval(js);
  const porTexto = new Map(banco.preguntas.map(p => [p.pregunta, p]));
  const veces = new Map();
  for (const parte of [1, 2]) {
    const materias = Object.keys(banco.materias[parte]).map(Number)
      .filter(m => banco.preguntas.some(p => p.parte === parte && p.materia === m));
    let fallos = 0;
    for (let i = 0; i < 300; i++) {
      d2.dispatchEvent(new w2.Event("DOMContentLoaded"));
      const r2 = d2.getElementById("simulacro-app");
      r2.querySelector(`input[name="partes"][value="${parte}"]`).checked = true;
      d2.getElementById("simulacro-crono").checked = false;
      [...r2.querySelectorAll("button")].find(b => b.textContent.startsWith("Empezar")).click();
      const qs = [...r2.querySelectorAll(".simulacro-pregunta legend")].map(l => porTexto.get(l.textContent));
      const vistas = new Set(qs.map(p => p.materia));
      if (qs.length !== 30 || new Set(qs).size !== 30 || !materias.every(m => vistas.has(m))) fallos++;
      qs.forEach(p => veces.set(p.id, (veces.get(p.id) || 0) + 1));
    }
    ok(fallos === 0, `parte ${parte}: 300 simulacros con 30 preguntas distintas y las ${materias.length} materias (${fallos} fallos)`);
  }
  const nunca = banco.preguntas.filter(p => !veces.has(p.id)).map(p => p.id);
  ok(nunca.length === 0, "todas las preguntas del banco salen alguna vez" + (nunca.length ? ": faltan " + nunca.join(", ") : ""));
  w2.close();
}

// Cierre por tiempo: con el reloj adelantado 46 minutos, la parte primera se
// cierra sola y pasa a la segunda.
{
  const dom3 = new JSDOM(html, { runScripts: "outside-only", pretendToBeVisual: true });
  const w3 = dom3.window, d3 = w3.document;
  w3.scrollTo = () => {};
  w3.eval(js);
  w3.addEventListener("load", () => {
    const r3 = d3.getElementById("simulacro-app");
    [...r3.querySelectorAll("button")].find(b => b.textContent.startsWith("Empezar")).click();
    const real = w3.Date.now;
    w3.Date.now = () => real() + 46 * 60 * 1000;
    setTimeout(() => {
      ok(/Parte segunda/.test(r3.textContent) && /Se acabó el tiempo/.test(r3.textContent),
        "la parte primera se cierra al agotarse el tiempo");
      w3.close();
    }, 1500);
  });
}
