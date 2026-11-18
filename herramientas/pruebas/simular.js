// Simulador mínimo del motor de GDevelop para probar la lógica sin abrir el editor.
// - Valida objetos, animaciones, capas, recursos de audio y nombres de teclas contra el proyecto real.
// - Un bot juega la partida completa (menú → créditos) y falla si se atasca o hay excepciones.
// Uso: node herramientas/pruebas/simular.js [ruta/al/codigo/fuente/de/GDevelop]
const fs = require("fs");
const path = require("path");

const RAIZ = path.resolve(__dirname, "..", "..");
const P = JSON.parse(fs.readFileSync(path.join(RAIZ, "juego", "game.json"), "utf8"));
const GD = process.argv[2];

// ---------------------------------------------------------------- tamaños de imagen (cabecera PNG)
const tam = {};
function tamano(ruta) {
  if (!tam[ruta]) {
    const b = fs.readFileSync(path.join(RAIZ, "juego", ruta));
    tam[ruta] = [b.readUInt32BE(16), b.readUInt32BE(20)];
  }
  return tam[ruta];
}

// ---------------------------------------------------------------- métodos reales de gdjs (si se da el código fuente)
let metodosReales = null;
if (GD) {
  metodosReales = new Set();
  const archivos = ["GDJS/Runtime/runtimeobject.ts", "GDJS/Runtime/spriteruntimeobject.ts", "Extensions/TextObject/textruntimeobject.ts",
    "Extensions/PanelSpriteObject/panelspriteruntimeobject.ts", "GDJS/Runtime/RuntimeLayer.ts"];
  for (const a of archivos) {
    const f = path.join(GD, a);
    if (!fs.existsSync(f)) { console.log("aviso: no está", a); continue; }
    const s = fs.readFileSync(f, "utf8");
    for (const m of s.matchAll(/^\s+(?:override\s+|abstract\s+)?([a-zA-Z0-9_]+)\s*\(/gm)) metodosReales.add(m[1]);
  }
}
const teclasValidas = new Set();
if (GD) {
  const s = fs.readFileSync(path.join(GD, "GDJS/Runtime/events-tools/inputtools.ts"), "utf8");
  const bloque = s.split("keysNameToCode = {")[1].split("};")[0];
  for (const m of bloque.matchAll(/^\s+([A-Za-z0-9_]+):/gm)) teclasValidas.add(m[1]);
}
const usados = new Set();

// ---------------------------------------------------------------- objetos
const DEF = {};
for (const o of P.objects) {
  const d = { tipo: o.type, anims: {} };
  if (o.type === "Sprite") for (const a of o.animations) {
    const dir = a.directions[0];
    d.anims[a.name] = { imgs: dir.sprites.map((s) => s.image), bucle: dir.looping, t: dir.timeBetweenFrames };
  }
  if (o.type === "PanelSpriteObject::PanelSprite") d.tam = [o.width, o.height];
  DEF[o.name] = d;
}
const RECURSOS = new Set(P.resources.resources.map((r) => r.name));
const CAPAS = {};
for (const L of P.layouts) CAPAS[L.name] = new Set(L.layers.map((l) => l.name));

class Obj {
  constructor(rs, nombre) {
    this._rs = rs; this._n = nombre; this._d = DEF[nombre];
    this.x = 0; this.y = 0; this.z = 0; this.capa = ""; this.op = 255; this.ang = 0; this.sx = 1; this.sy = 1; this.oculto = false;
    this._t = 0; this.texto = ""; this.envolver = false; this.anchoEnv = 0;
    if (this._d.tipo === "Sprite") this.anim = Object.keys(this._d.anims)[0];
    if (this._d.tamTexto) {}
    this.w = this._d.tam ? this._d.tam[0] : 0; this.h = this._d.tam ? this._d.tam[1] : 0;
  }
  _uso(m) { usados.add(m); }
  getName() { this._uso("getName"); return this._n; }
  setPosition(x, y) { this._uso("setPosition"); this._num(x, y); this.x = x; this.y = y; }
  _num(...v) { for (const n of v) if (typeof n !== "number" || !isFinite(n)) throw new Error(`${this._n}: valor no numérico ${n}`); }
  setX(x) { this._uso("setX"); this._num(x); this.x = x; } getX() { this._uso("getX"); return this.x; }
  setY(y) { this._uso("setY"); this._num(y); this.y = y; } getY() { this._uso("getY"); return this.y; }
  getWidth() {
    this._uso("getWidth");
    if (this._d.tipo === "Sprite") return tamano(this._d.anims[this.anim].imgs[0])[0] * this.sx;
    if (this._d.tipo === "TextObject::Text") return this.envolver ? this.anchoEnv : this.texto.length * 8;
    return this.w;
  }
  getHeight() {
    this._uso("getHeight");
    if (this._d.tipo === "Sprite") return tamano(this._d.anims[this.anim].imgs[0])[1] * this.sy;
    if (this._d.tipo === "TextObject::Text") return 10;
    return this.h;
  }
  setWidth(w) { this._uso("setWidth"); this._num(w); this.w = w; } setHeight(h) { this._uso("setHeight"); this._num(h); this.h = h; }
  setLayer(c) { this._uso("setLayer"); if (!CAPAS[this._rs.nombre].has(c)) throw new Error("Capa inexistente " + c); this.capa = c; }
  setZOrder(z) { this._uso("setZOrder"); this._num(z); this.z = z; } getZOrder() { this._uso("getZOrder"); return this.z; }
  setOpacity(o) { this._uso("setOpacity"); this._num(o); this.op = o; } getOpacity() { this._uso("getOpacity"); return this.op; }
  setAngle(a) { this._uso("setAngle"); this._num(a); this.ang = a; }
  setColor(c) { this._uso("setColor"); if (!/^\d+;\d+;\d+$/.test(c)) throw new Error("Color mal formado " + c); }
  flipX(b) { this._uso("flipX"); }
  hide(b) { this._uso("hide"); this.oculto = b; }
  deleteFromScene() { this._uso("deleteFromScene"); this._rs._borrar(this); }
  setScaleX(s) { this._uso("setScaleX"); this._num(s); this.sx = s; } setScaleY(s) { this._uso("setScaleY"); this._num(s); this.sy = s; }
  setAnimationName(n) {
    this._uso("setAnimationName");
    if (!this._d.anims[n]) throw new Error(`${this._n}: animación inexistente "${n}"`);
    if (n !== this.anim) this._t = 0;
    this.anim = n;
  }
  getAnimationName() { this._uso("getAnimationName"); return this.anim; }
  hasAnimationEnded() {
    this._uso("hasAnimationEnded");
    const a = this._d.anims[this.anim];
    return !a.bucle && this._t >= a.imgs.length * a.t;
  }
  setText(t) { this._uso("setText"); if (typeof t !== "string") throw new Error("texto no string"); this.texto = t; }
  setWrapping(b) { this._uso("setWrapping"); this.envolver = b; } setWrappingWidth(w) { this._uso("setWrappingWidth"); this.anchoEnv = w; }
  setOutlineEnabled() { this._uso("setOutlineEnabled"); } setOutlineColor() { this._uso("setOutlineColor"); }
  setOutlineThickness() { this._uso("setOutlineThickness"); }
}

// ---------------------------------------------------------------- variables
class Var {
  constructor(v) { this.v = v; this.hijos = {}; }
  getAsNumber() { return typeof this.v === "number" ? this.v : Number(this.v) || 0; }
  setNumber(n) { this.v = n; } getAsBoolean() { return !!this.v; } setBoolean(b) { this.v = !!b; }
  getAsString() { return this.v === undefined ? "" : String(this.v); } setString(s) { this.v = s; }
  getChild(k) { if (!this.hijos[k]) this.hijos[k] = new Var(0); return this.hijos[k]; }
  hasChild(k) { return !!this.hijos[k]; } clearChildren() { this.hijos = {}; }
}
const VARS = {};
for (const v of P.variables) VARS[v.name] = new Var(v.value);
const juego = { getVariables: () => ({ get: (n) => { if (!VARS[n]) throw new Error("Variable global no declarada " + n); return VARS[n]; } }) };

// ---------------------------------------------------------------- escena
class Escena {
  constructor(nombre) {
    this.nombre = nombre; this.objs = []; this.frame = 0; this.siguiente = null;
    this.cam = { x: 0, y: 0, z: 1 };
    if (!P.layouts.find((l) => l.name === nombre)) throw new Error("Escena inexistente " + nombre);
  }
  getName() { return this.nombre; }
  getGame() { return juego; }
  getTimeManager() {
    const s = this;
    return { getElapsedTime: () => 1000 / 60, getTimeFromStart: () => s.frame * 1000 / 60, isFirstFrame: () => s.frame === 0 };
  }
  getLayer(n) {
    if (!CAPAS[this.nombre].has(n)) throw new Error("Capa inexistente " + n);
    const c = this.cam;
    return { setCameraX: (x) => { c.x = x; }, setCameraY: (y) => { c.y = y; }, setCameraZoom: (z) => { c.z = z; } };
  }
  createObject(n) { if (!DEF[n]) throw new Error("Objeto inexistente " + n); const o = new Obj(this, n); this.objs.push(o); return o; }
  getObjects(n) { if (!DEF[n]) throw new Error("Objeto inexistente " + n); return this.objs.filter((o) => o._n === n); }
  _borrar(o) { this.objs = this.objs.filter((x) => x !== o); }
}

// ---------------------------------------------------------------- gdjs simulado
const entrada = { mantenidas: new Set(), justo: new Set() };
const comprobarTecla = (k) => { if (teclasValidas.size && !teclasValidas.has(k)) throw new Error("Tecla inexistente en GDevelop: " + k); };
const comprobarAudio = (f) => { if (!RECURSOS.has(f)) throw new Error("Recurso de audio inexistente " + f); };
global.gdjs = {
  evtTools: {
    input: {
      isKeyPressed: (rs, k) => { comprobarTecla(k); return entrada.mantenidas.has(k); },
      wasKeyJustPressed: (rs, k) => { comprobarTecla(k); return entrada.justo.has(k); },
    },
    sound: {
      playSound: (rs, f) => comprobarAudio(f),
      playMusicOnChannel: (rs, f) => comprobarAudio(f),
      stopMusicOnChannel: () => {},
    },
    runtimeScene: {
      replaceScene: (rs, n) => { rs.siguiente = n; },
      stopGame: () => {},
    },
  },
};
const codigoLib = P.externalEvents.find((e) => e.name === "Libreria").events.find((e) => e.inlineCode).inlineCode.join("\n");
const ejecutarLib = new Function("runtimeScene", "eventsFunctionContext", codigoLib);

// ---------------------------------------------------------------- bot
const R = () => gdjs.ryu;
const cx = (o) => o.getX() + o.getWidth() / 2, cy = (o) => o.getY() + o.getHeight() / 2, pie = (o) => o.getY() + o.getHeight() - 4;
const TE = () => R().TECLAS;
function pulsar(p, accion) { entrada.justo.add(TE()[p][accion]); entrada.mantenidas.add(TE()[p][accion]); }
const atasco = {};
function irA(p, o, x, y, tol = 6) {
  const dx = x - cx(o), dy = y - pie(o);
  const k = TE()[p];
  const a = atasco[p] || (atasco[p] = { x: 0, y: 0, n: 0, desvio: 0 });
  if (Math.hypot(o.getX() - a.x, o.getY() - a.y) < 0.5) a.n++; else a.n = 0;
  a.x = o.getX(); a.y = o.getY();
  if (a.n > 25) { a.desvio = 40; a.n = 0; a.lado = Math.random() < 0.5 ? "izquierda" : "derecha"; }
  if (a.desvio > 0) { a.desvio--; entrada.mantenidas.add(k[a.lado]); if (Math.abs(dy) > tol) entrada.mantenidas.add(dy < 0 ? k.arriba : k.abajo); return false; }
  if (Math.abs(dx) > tol) entrada.mantenidas.add(dx < 0 ? k.izquierda : k.derecha);
  if (Math.abs(dy) > tol) entrada.mantenidas.add(dy < 0 ? k.arriba : k.abajo);
  return Math.abs(dx) <= tol && Math.abs(dy) <= tol;
}
// dentro de la mina hay que pasar por el hueco de las puertas (x = 640)
const areaMina = (y) => (y > 515 ? 0 : y > 285 ? 1 : 2);
function irMina(p, o, x, y, tol = 6) {
  const a = areaMina(pie(o)), b = areaMina(y);
  if (a === b) return irA(p, o, x, y, tol);
  if (Math.abs(cx(o) - 640) > 6) { irA(p, o, 640, [545, 315, 200][a], 4); return false; }
  irA(p, o, 640, b > a ? [430, 200, 200][a] : [545, 545, 330][a], 4);
  return false;
}
function mirarHacia(p, o, x, y) {
  const dx = x - cx(o), dy = y - cy(o), k = TE()[p];
  entrada.mantenidas.add(Math.abs(dx) > Math.abs(dy) ? (dx < 0 ? k.izquierda : k.derecha) : (dy < 0 ? k.arriba : k.abajo));
}
function combatir(rs, f) {
  const enemigos = rs.getObjects("Soldado").filter((s) => s.ryu && s.ryu.estado !== "muerto")
    .concat(rs.getObjects("Pilar").filter((p) => p.ryu && !p.ryu.roto))
    .concat(rs.getObjects("Norbu").filter((n) => n.ryu && n.ryu.activo));
  const pilares = rs.getObjects("Pilar").filter((p) => p.ryu && !p.ryu.roto);
  for (const o of R().jugadores(rs)) {
    if (o.ryu.derribado) continue;
    const p = o.ryu.p;
    let lista = pilares.length ? pilares : enemigos;
    if (!lista.length) continue;
    let obj = lista[0], md = 1e9;
    for (const e of lista) { const d = Math.hypot(cx(e) - cx(o), cy(e) - cy(o)); if (d < md) { md = d; obj = e; } }
    if (md > 24) irA(p, o, cx(obj), pie(obj) + 2, 4);
    else mirarHacia(p, o, cx(obj), cy(obj));
    if (f % 14 === p * 3) pulsar(p, md < 26 ? "golpe" : "poder1");
    if (f % 90 === p * 7 && o.ryu.energia > 60) pulsar(p, "poder3");
    if (p === 3 && o.ryu.vida < 50 && o.ryu.energia > 50) pulsar(p, "poder3");
  }
}

function bot(rs, f) {
  const st = rs.__ryu, n = rs.nombre;
  if (!st) return;
  if (st.dialogo || ["MenuInicio", "Intro", "Controles", "Final", "Derrota", "Creditos"].includes(n)) { if (f % 8 === 0) pulsar(1, "interactuar"); return; }
  const js = R().jugadores(rs);
  const ryu = rs.getObjects("Ryu")[0], gao = rs.getObjects("Gao")[0], nerea = rs.getObjects("Nerea")[0];
  const M = R().MAPAS;
  const fase = VARS.faseHistoria.getAsNumber();
  if (n === "Pelea" || n === "ArenaFinal") return combatir(rs, f);
  if (n === "Ciudad") {
    if (st.paso === "fuente") {
      const fu = M.ciudad.puntos.fuente;
      if (irA(1, ryu, fu[0] + 32, fu[1] + 64, 4) && f % 10 === 0) pulsar(1, "interactuar");
    } else if (st.paso === "mision") {
      const z = M.ciudad.zonas.salida_norte;
      for (const o of js) irA(o.ryu.p, o, (z[0] + z[2]) / 2, z[1] + 4, 4);
    }
    return;
  }
  if (n === "ZonaTierra") {
    const T = M.tierra;
    const centro = (z) => [(z[0] + z[2]) / 2, (z[1] + z[3]) / 2];
    if (st.zona === "exterior") {
      if (fase >= 5) return;
      const obj = !VARS.encuentrosHechos.hasChild("tierra1") ? centro(T.zonas.encuentro_tierra1) : centro(T.zonas.entrada_mina);
      for (const o of js) irA(o.ryu.p, o, obj[0] + (o.ryu.p - 2) * 6, obj[1], 4);
      return;
    }
    const puertas = rs.getObjects("PuertaElemental");
    const p1 = puertas.find((p) => p.ryu.id === "p1"), p2 = puertas.find((p) => p.ryu.id === "p2");
    const marca = (k) => VARS.marcas.hasChild(k);
    let objetivo;
    if (!p1.ryu.abierta) {
      if (irMina(2, gao, cx(p1), p1.getY() + 110, 6)) { mirarHacia(2, gao, cx(p1), p1.getY()); if (f % 30 === 0) pulsar(2, "poder1"); }
      return;
    }
    if (!marca("documento")) { const d = T.puntos.documento; if (irMina(1, ryu, d[0] + 16, d[1] + 30, 6) && f % 10 === 0) pulsar(1, "interactuar"); return; }
    if (!VARS.encuentrosHechos.hasChild("tierra2")) { const c = centro(T.zonas.encuentro_tierra2); irMina(1, ryu, c[0], c[1], 6); return; }
    if (!p2.ryu.abierta) {
      const okG = irMina(2, gao, cx(p2) - 14, p2.getY() + 104, 6), okN = irMina(3, nerea, cx(p2) + 14, p2.getY() + 104, 6);
      if (okG && okN) { mirarHacia(2, gao, cx(p2), p2.getY()); mirarHacia(3, nerea, cx(p2), p2.getY()); if (f % 30 === 0) { pulsar(2, "poder1"); pulsar(3, "poder2"); } }
      return;
    }
    if (!marca("diario")) { const d = T.puntos.diario; for (const o of js) irMina(o.ryu.p, o, d[0] + (o.ryu.p - 1) * 10, d[1] + 40, 6); if (Math.hypot(cx(ryu) - d[0], pie(ryu) - d[1] - 30) < 30 && f % 10 === 0) pulsar(1, "interactuar"); return; }
    if (!VARS.tierraDesbloqueada.getAsBoolean()) { const e = T.puntos.emblema; if (irMina(1, ryu, e[0] + 16, e[1] + 44, 6) && f % 10 === 0) pulsar(1, "interactuar"); return; }
    const s = centro(T.zonas.salida_mina);
    for (const o of js) irMina(o.ryu.p, o, s[0], s[1] + 4, 4);
  }
}

// ---------------------------------------------------------------- partida completa
let escena = new Escena("MenuInicio");
const visitadas = [];
let total = 0;
const LIMITE = 60 * 60 * 25;
try {
  while (total < LIMITE) {
    entrada.justo.clear(); entrada.mantenidas.clear();
    bot(escena, total);
    ejecutarLib(escena, null);
    gdjs.ryu.ejecutar(escena, escena.nombre);
    for (const o of escena.objs) o._t += 1 / 60;
    escena.frame++; total++;
    if (escena.siguiente) {
      const sig = escena.siguiente;
      visitadas.push(`${escena.nombre}(${escena.frame}f)`);
      if (escena.nombre === "Creditos" && sig === "MenuInicio") { console.log("PARTIDA COMPLETA"); break; }
      if (sig === "Derrota") console.log("  derrota en", escena.nombre, "fase", VARS.faseHistoria.getAsNumber());
      escena = new Escena(sig);
    }
  }
} catch (e) {
  console.log("ERROR en escena", escena.nombre, "frame", escena.frame, "estado", escena.__ryu && escena.__ryu.paso);
  console.log(e.stack.split("\n").slice(0, 6).join("\n"));
  process.exitCode = 1;
}
console.log("Recorrido:", visitadas.join(" → "));
console.log("Tiempo simulado:", (total / 60).toFixed(0), "s · fase", VARS.faseHistoria.getAsNumber(), "· pistas", VARS.pistas.getAsNumber());
if (total >= LIMITE) { console.log("ATASCADO en", escena.nombre, "paso", escena.__ryu && escena.__ryu.paso, "zona", escena.__ryu && escena.__ryu.zona); process.exitCode = 1; }
if (metodosReales) {
  const faltan = [...usados].filter((m) => !metodosReales.has(m));
  console.log(faltan.length ? "MÉTODOS QUE NO EXISTEN EN GDEVELOP: " + faltan.join(", ") : `Los ${usados.size} métodos usados existen en el motor de GDevelop.`);
  if (faltan.length) process.exitCode = 1;
}
if (process.exitCode && escena.__ryu) {
  for (const n of ["Ryu", "Gao", "Nerea", "PuertaElemental", "Tsering"]) for (const o of escena.getObjects(n))
    console.log(" ", n, Math.round(o.getX()), Math.round(o.getY()), o.ryu ? JSON.stringify({ ab: o.ryu.abierta, e: o.ryu.energia && Math.round(o.ryu.energia), dir: o.ryu.dir, ctl: o.ryu.control }) : "");
  console.log("  marcas", Object.keys(VARS.marcas.hijos), "encuentros", Object.keys(VARS.encuentrosHechos.hijos), "proyectiles", escena.getObjects("Proyectil").length);
}
