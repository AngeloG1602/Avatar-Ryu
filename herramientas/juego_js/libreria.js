// =====================================================================================
// Ryu: El Último Ciclo — lógica del juego.
// Este archivo se inserta en el proyecto de GDevelop (hoja de eventos externa "Libreria")
// mediante herramientas/generar_proyecto.py. Cada escena llama a gdjs.ryu.ejecutar(...).
// Valores de diseño: docs/02-MECANICAS.md · Escenas: docs/03-ESCENAS.md · Diálogos: docs/05-DIALOGOS.md
// =====================================================================================
if (!gdjs.ryu || gdjs.ryu.version !== "__VERSION__") {
  (function () {
    const R = {};
    gdjs.ryu = R;
    R.version = "__VERSION__";
    const MAPAS = __MAPAS__;
    R.MAPAS = MAPAS;

    // ------------------------------------------------------------------ ajustes (docs/02)
    const AJ = {
      velJugador: 90, velCac: 55, velDist: 45, regenEnergia: 10, enfriamiento: 0.4,
      costo: { poder1: 15, poder2: 30, poder3: 50 }, danio: { golpe: 5, poder1: 10, poder2: 20, poder3: 35 },
      defensa: 0.3, invulnerable: 0.5, derribo: 5, revivir: 0.3,
      soldado: { cac: { vida: 30, danio: 8, cd: 1 }, dist: { vida: 25, danio: 6, cd: 2, distancia: 150 } },
      norbu: { vida: 300, fase2: 150, fase3: 75, rafaga: 2, desplazamiento: 5 },
      pilarVida: 40, avatarDuracion: 10, avatarDanio: 15, selloDrenaje: 5,
      tsering: { cada: 4, danio: 8 }, muro: { vida: 60, dur: 4 }, cupula: { radio: 96, dur: 5 },
      curacion: { cantidad: 35, radio: 128 }, congelar: { normal: 2.5, jefe: 1 },
    };
    R.AJ = AJ;

    // ------------------------------------------------------------------ variables globales
    const G = (rs, n) => rs.getGame().getVariables().get(n);
    const num = (rs, n) => G(rs, n).getAsNumber();
    const setNum = (rs, n, v) => G(rs, n).setNumber(v);
    const bool = (rs, n) => G(rs, n).getAsBoolean();
    const setBool = (rs, n, v) => G(rs, n).setBoolean(v);
    const str = (rs, n) => G(rs, n).getAsString();
    const setStr = (rs, n, v) => G(rs, n).setString(v);
    const marca = (rs, est, k) => { const v = G(rs, est); return v.hasChild(k) && v.getChild(k).getAsBoolean(); };
    const marcar = (rs, est, k) => G(rs, est).getChild(k).setBoolean(true);
    R.reiniciarPartida = function (rs) {
      setNum(rs, "faseHistoria", 0); setNum(rs, "pistas", 0);
      setBool(rs, "aireDesbloqueado", false); setBool(rs, "aguaDesbloqueada", false); setBool(rs, "tierraDesbloqueada", false);
      setStr(rs, "elementoActivo", ""); setStr(rs, "peleaActual", ""); setStr(rs, "escenaRetorno", "");
      setNum(rs, "retornoX", 0); setNum(rs, "retornoY", 0); setStr(rs, "escenaDerrota", "");
      G(rs, "encuentrosHechos").clearChildren(); G(rs, "marcas").clearChildren();
    };

    // ------------------------------------------------------------------ utilidades
    const dist = (ax, ay, bx, by) => Math.hypot(ax - bx, ay - by);
    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    const ahora = (rs) => rs.getTimeManager().getTimeFromStart() / 1000;
    const DIRV = { abajo: [0, 1], arriba: [0, -1], izquierda: [-1, 0], derecha: [1, 0] };
    const ANG = { derecha: 0, abajo: 90, izquierda: 180, arriba: 270 };
    const dirDe = (dx, dy) => Math.abs(dx) > Math.abs(dy) ? (dx < 0 ? "izquierda" : "derecha") : (dy < 0 ? "arriba" : "abajo");
    const cx = (o) => o.getX() + o.getWidth() / 2;
    const cy = (o) => o.getY() + o.getHeight() / 2;
    const pieY = (o) => o.getY() + o.getHeight() - 4;
    R.estado = (rs) => rs.__ryu;

    R.crear = function (rs, nombre, x, y, capa) {
      const o = rs.createObject(nombre);
      if (!o) throw new Error("No existe el objeto " + nombre);
      // GDevelop recicla los objetos borrados: se limpian los datos propios y el tinte
      o.ryu = undefined;
      if (typeof o.getAnimationName === "function") o.setColor("255;255;255");
      o.setPosition(x, y);
      if (capa) o.setLayer(capa);
      return o;
    };
    R.texto = function (rs, s, x, y, opciones) {
      const op = opciones || {};
      const o = R.crear(rs, op.grande ? "TextoGrande" : "Texto", x, y, op.capa === undefined ? "UI" : op.capa);
      o.setText(s);
      if (op.color) o.setColor(op.color);
      if (op.ancho) { o.setWrapping(true); o.setWrappingWidth(op.ancho); }
      if (op.centrado) o.setX(x - o.getWidth() / 2);
      o.setZOrder(op.z || 100);
      return o;
    };
    R.sonido = function (rs, n) { gdjs.evtTools.sound.playSound(rs, "assets/audio/" + n + ".ogg", false, 100, 1); };
    R.musica = function (rs, n) {
      if (R.musicaActual === n) return;
      gdjs.evtTools.sound.stopMusicOnChannel(rs, 1);
      if (n) gdjs.evtTools.sound.playMusicOnChannel(rs, "assets/audio/" + n + ".ogg", 1, true, 60, 1);
      R.musicaActual = n;
    };
    R.ir = function (rs, escena) {
      const st = R.estado(rs);
      if (st.saliendo) return;
      st.saliendo = true;
      gdjs.evtTools.runtimeScene.replaceScene(rs, escena, true);
    };

    // ------------------------------------------------------------------ entrada (teclado + mandos)
    const TECLAS = {
      1: { arriba: "w", abajo: "s", izquierda: "a", derecha: "d", golpe: "f", poder1: "r", poder2: "t", poder3: "g",
           defensa: "LShift", elemento: "q", interactuar: "e" },
      2: { arriba: "Up", abajo: "Down", izquierda: "Left", derecha: "Right", golpe: "Numpad1", poder1: "Numpad4",
           poder2: "Numpad5", poder3: "Numpad6", defensa: "Numpad0", elemento: null, interactuar: "Return" },
      3: { arriba: "i", abajo: "k", izquierda: "j", derecha: "l", golpe: "u", poder1: "o", poder2: "p", poder3: "h",
           defensa: "Space", elemento: null, interactuar: "n" },
    };
    R.TECLAS = TECLAS;
    // Mando estándar: 0 A, 1 B, 2 X, 3 Y, 4 LB, 5 RB, 9 Start, 12-15 cruceta
    const BOTON = { golpe: 0, interactuar: 0, poder1: 2, poder2: 3, poder3: 1, defensa: 5, elemento: 4, pausa: 9,
                    arriba: 12, abajo: 13, izquierda: 14, derecha: 15 };
    R.ent = { pads: [[], [], [], []], padsAntes: [[], [], [], []], ejes: [[0, 0], [0, 0], [0, 0], [0, 0]], dirAntes: {}, dir: {} };

    R.actualizarEntrada = function (rs) {
      const e = R.ent;
      const lista = (typeof navigator !== "undefined" && navigator.getGamepads) ? navigator.getGamepads() : [];
      for (let i = 0; i < 4; i++) {
        e.padsAntes[i] = e.pads[i];
        const gp = lista && lista[i];
        e.pads[i] = gp ? gp.buttons.map((b) => !!(b && b.pressed)) : [];
        let ax = gp && gp.axes ? gp.axes[0] || 0 : 0, ay = gp && gp.axes ? gp.axes[1] || 0 : 0;
        if (Math.hypot(ax, ay) < 0.35) { ax = 0; ay = 0; }
        e.ejes[i] = [ax, ay];
      }
      for (let p = 1; p <= 3; p++) {
        e.dirAntes[p] = e.dir[p] || {};
        const d = {};
        for (const k of ["arriba", "abajo", "izquierda", "derecha"]) d[k] = R.mantiene(rs, p, k);
        e.dir[p] = d;
      }
    };
    R.mandosConectados = function () {
      const lista = (typeof navigator !== "undefined" && navigator.getGamepads) ? navigator.getGamepads() : [];
      let n = 0;
      for (let i = 0; i < (lista ? lista.length : 0); i++) if (lista[i]) n++;
      return n;
    };
    R.mantiene = function (rs, p, accion) {
      const k = TECLAS[p][accion];
      if (k && gdjs.evtTools.input.isKeyPressed(rs, k)) return true;
      const pad = R.ent.pads[p - 1];
      if (pad && pad[BOTON[accion]]) return true;
      const ej = R.ent.ejes[p - 1];
      if (accion === "arriba" && ej[1] < -0.5) return true;
      if (accion === "abajo" && ej[1] > 0.5) return true;
      if (accion === "izquierda" && ej[0] < -0.5) return true;
      if (accion === "derecha" && ej[0] > 0.5) return true;
      return false;
    };
    R.pulsa = function (rs, p, accion) {
      if (["arriba", "abajo", "izquierda", "derecha"].indexOf(accion) >= 0) {
        return !!(R.ent.dir[p] && R.ent.dir[p][accion] && !(R.ent.dirAntes[p] || {})[accion]);
      }
      const k = TECLAS[p][accion];
      if (k && gdjs.evtTools.input.wasKeyJustPressed(rs, k)) return true;
      const b = BOTON[accion], pad = R.ent.pads[p - 1], antes = R.ent.padsAntes[p - 1];
      return !!(pad && pad[b] && !(antes && antes[b]));
    };
    R.alguienPulsa = function (rs, accion) {
      for (let p = 1; p <= 3; p++) if (R.pulsa(rs, p, accion)) return p;
      return 0;
    };
    R.pausaPulsada = function (rs) {
      if (gdjs.evtTools.input.wasKeyJustPressed(rs, "Escape")) return true;
      for (let i = 0; i < 4; i++) if (R.ent.pads[i][9] && !R.ent.padsAntes[i][9]) return true;
      return false;
    };
    R.eje = function (rs, p) {
      let x = 0, y = 0;
      if (R.mantiene(rs, p, "izquierda")) x -= 1;
      if (R.mantiene(rs, p, "derecha")) x += 1;
      if (R.mantiene(rs, p, "arriba")) y -= 1;
      if (R.mantiene(rs, p, "abajo")) y += 1;
      const ej = R.ent.ejes[p - 1];
      if (x === 0 && y === 0 && (ej[0] || ej[1])) { x = ej[0]; y = ej[1]; }
      const l = Math.hypot(x, y);
      return l > 1 ? [x / l, y / l] : [x, y];
    };

    // ------------------------------------------------------------------ animación
    R.anim = function (o, accion, dir, prefijo) {
      const d = dir === "izquierda" ? "derecha" : dir;
      let n = (accion === "danio" || accion === "derribado") ? accion : accion + "_" + d;
      if (prefijo) n = prefijo + "_" + n;
      if (o.getAnimationName() !== n) o.setAnimationName(n);
      o.flipX(dir === "izquierda");
    };
    const efectoAnim = (o, n) => { if (o.getAnimationName() !== n) o.setAnimationName(n); };

    // ------------------------------------------------------------------ colisiones con el mapa
    function cajaPies(o, x, y) {
      const w = o.getWidth(), h = o.getHeight();
      return [x + w / 2 - 7, y + h - 8, x + w / 2 + 7, y + h - 1];
    }
    const solapa = (a, b) => a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
    R.obstaculos = function (rs) {
      const st = R.estado(rs);
      const lista = st.obstaculos ? st.obstaculos.slice() : [];
      for (const p of rs.getObjects("PuertaElemental")) if (!p.ryu || !p.ryu.abierta) lista.push([p.getX() + 2, p.getY() + 6, p.getX() + 62, p.getY() + 62]);
      for (const m of rs.getObjects("Muro")) if (m.ryu) lista.push(m.ryu.caja);
      for (const p of rs.getObjects("Pilar")) if (p.ryu && !p.ryu.roto) lista.push([p.getX() + 8, p.getY() + 44, p.getX() + 24, p.getY() + 62]);
      return lista;
    };
    R.choca = function (rs, o, x, y, obst) {
      const c = cajaPies(o, x, y);
      const st = R.estado(rs);
      const L = st.limites;
      if (L && (c[0] < L[0] || c[2] > L[2] || c[1] < L[1] || c[3] > L[3])) return true;
      for (const r of obst) if (solapa(c, r)) return true;
      return false;
    };
    R.mover = function (rs, o, dx, dy, obst) {
      obst = obst || R.obstaculos(rs);
      if (dx && !R.choca(rs, o, o.getX() + dx, o.getY(), obst)) o.setX(o.getX() + dx);
      if (dy && !R.choca(rs, o, o.getX(), o.getY() + dy, obst)) o.setY(o.getY() + dy);
    };
    R.ordenarProfundidad = function (rs) {
      for (const n of ["Ryu", "Gao", "Nerea", "Tsering", "Norbu", "Soldado", "Ciudadano", "Pilar", "Fuente", "Pista", "PuertaElemental", "Muro"]) {
        for (const o of rs.getObjects(n)) o.setZOrder(Math.round(pieY(o)));
      }
    };

    // ------------------------------------------------------------------ jugadores
    const JUG = [
      { obj: "Ryu", p: 1, vida: 100, clave: "ryu" },
      { obj: "Gao", p: 2, vida: 130, clave: "gao" },
      { obj: "Nerea", p: 3, vida: 90, clave: "nerea" },
    ];
    R.JUG = JUG;
    R.jugadores = function (rs) {
      const out = [];
      for (const j of JUG) for (const o of rs.getObjects(j.obj)) if (o.ryu) out.push(o);
      return out;
    };
    R.crearJugadores = function (rs, posiciones) {
      JUG.forEach((j, i) => {
        const o = R.crear(rs, j.obj, posiciones[i][0], posiciones[i][1]);
        o.ryu = { j: j, p: j.p, vida: j.vida, vidaMax: j.vida, energia: 100, energiaMax: 100, dir: "abajo",
                  estado: "libre", t: 0, cd: 0, inv: 0, derribado: false, tDerribo: 0, control: true };
        R.anim(o, "reposo", "abajo");
      });
    };
    R.controlJugadores = function (rs, si) { for (const o of R.jugadores(rs)) o.ryu.control = si; };
    R.centroGrupo = function (rs) {
      const js = R.jugadores(rs);
      if (!js.length) return [320, 180];
      let x = 0, y = 0;
      for (const o of js) { x += cx(o); y += cy(o); }
      return [x / js.length, y / js.length];
    };
    R.teletransportar = function (rs, x, y) {
      R.jugadores(rs).forEach((o, i) => o.setPosition(x - 16 + (i - 1) * 28, y - 16));
      for (const t of rs.getObjects("Tsering")) t.setPosition(x + 30, y + 10);
    };

    R.actualizarJugadores = function (rs, dt) {
      const st = R.estado(rs);
      const obst = R.obstaculos(rs);
      const enDialogo = !!st.dialogo;
      for (const o of R.jugadores(rs)) {
        const d = o.ryu;
        d.cd = Math.max(0, d.cd - dt);
        d.inv = Math.max(0, d.inv - dt);
        o.setOpacity(d.inv > 0 && Math.floor(d.inv * 20) % 2 === 0 ? 120 : 255);
        // energía
        const sellado = st.sello && d.p === 1;
        if (d.avatar) d.energia = d.energiaMax;
        else if (sellado) d.energia = Math.max(0, d.energia - AJ.selloDrenaje * dt);
        else d.energia = Math.min(d.energiaMax, d.energia + AJ.regenEnergia * dt);
        // derribado
        if (d.derribado) {
          d.tDerribo -= dt;
          R.anim(o, "derribado", "abajo");
          if (d.tDerribo <= 0 && R.jugadores(rs).some((x) => !x.ryu.derribado)) {
            d.derribado = false; d.vida = Math.round(d.vidaMax * AJ.revivir); d.inv = 1;
          }
          continue;
        }
        if (d.estado !== "libre") {
          d.t -= dt;
          if (d.t <= 0) d.estado = "libre";
          else continue;
        }
        if (!d.control || enDialogo || st.pausado) { R.anim(o, "reposo", d.dir); d.defendiendo = false; continue; }
        const p = d.p;
        d.defendiendo = R.mantiene(rs, p, "defensa");
        if (d.defendiendo) { R.anim(o, "defensa", d.dir); continue; }
        const e = R.eje(rs, p);
        if (e[0] || e[1]) {
          d.dir = dirDe(e[0], e[1]);
          R.mover(rs, o, e[0] * AJ.velJugador * dt, e[1] * AJ.velJugador * dt, obst);
          R.anim(o, "caminar", d.dir);
        } else R.anim(o, "reposo", d.dir);
        if (st.combate) {
          if (R.pulsa(rs, p, "golpe")) R.golpe(rs, o);
          else if (R.pulsa(rs, p, "poder1")) R.poder(rs, o, 1);
          else if (R.pulsa(rs, p, "poder2")) R.poder(rs, o, 2);
          else if (R.pulsa(rs, p, "poder3")) R.poder(rs, o, 3);
        }
        if (p === 1 && R.pulsa(rs, p, "elemento")) R.cambiarElemento(rs);
      }
      if (st.combate && R.jugadores(rs).every((o) => o.ryu.derribado)) R.derrota(rs);
    };

    R.elementosRyu = function (rs) {
      const l = [];
      if (bool(rs, "aireDesbloqueado")) l.push("aire");
      if (bool(rs, "aguaDesbloqueada")) l.push("agua");
      if (bool(rs, "tierraDesbloqueada")) l.push("tierra");
      return l;
    };
    R.cambiarElemento = function (rs) {
      const l = R.elementosRyu(rs);
      if (!l.length) return;
      const i = l.indexOf(str(rs, "elementoActivo"));
      setStr(rs, "elementoActivo", l[(i + 1) % l.length]);
      R.sonido(rs, "sfx_menu");
    };

    // ------------------------------------------------------------------ ataques de los jugadores
    function objetivosEnemigos(rs) {
      const l = [];
      for (const s of rs.getObjects("Soldado")) if (s.ryu && s.ryu.estado !== "muerto") l.push(s);
      for (const n of rs.getObjects("Norbu")) if (n.ryu && n.ryu.activo) l.push(n);
      for (const p of rs.getObjects("Pilar")) if (p.ryu && !p.ryu.roto) l.push(p);
      return l;
    }
    R.golpe = function (rs, o) {
      const d = o.ryu;
      if (d.cd > 0) return;
      d.cd = 0.25; d.estado = "atacando"; d.t = 0.24;
      R.anim(o, "golpe", d.dir);
      R.sonido(rs, "sfx_golpe");
      const v = DIRV[d.dir], hx = cx(o) + v[0] * 18, hy = cy(o) + v[1] * 18;
      for (const e of objetivosEnemigos(rs)) {
        if (dist(hx, hy, cx(e), cy(e)) < 22) { R.danarEnemigo(rs, e, AJ.danio.golpe, v, ""); R.efecto(rs, "impacto", hx, hy); }
      }
    };
    const PODERES = {
      ryu: {
        1: { tipo: "proyectil", anim: "bola_fuego", vel: 220, elem: "fuego", danio: AJ.danio.poder1 },
        3: { tipo: "llamarada", elem: "fuego", danio: AJ.danio.poder3 },
      },
      ryu2: {
        aire: { tipo: "proyectil", anim: "rafaga_aire", vel: 200, elem: "aire", danio: 12, empuje: 30 },
        agua: { tipo: "latigo", elem: "agua", danio: AJ.danio.poder2, alcance: 56 },
        tierra: { tipo: "proyectil", anim: "roca", vel: 120, elem: "tierra", danio: AJ.danio.poder2 },
      },
      gao: {
        1: { tipo: "proyectil", anim: "roca", vel: 170, elem: "tierra", danio: AJ.danio.poder1 },
        2: { tipo: "muro", elem: "tierra" },
        3: { tipo: "cupula", elem: "tierra" },
      },
      nerea: {
        1: { tipo: "latigo", elem: "agua", danio: AJ.danio.poder1, alcance: 56 },
        2: { tipo: "proyectil", anim: "congelar", vel: 180, elem: "agua", danio: 5, congela: AJ.congelar.normal },
        3: { tipo: "curacion" },
      },
    };
    R.poder = function (rs, o, n) {
      const d = o.ryu, st = R.estado(rs);
      if (d.cd > 0) return;
      let def;
      if (d.j.clave === "ryu") {
        if (n === 2) {
          const el = str(rs, "elementoActivo");
          if (!el) return;
          def = PODERES.ryu2[el];
        } else def = PODERES.ryu[n];
        if (n === 3 && st.sello) { R.aviso(rs, "El sello bloquea tu poder especial", 1.5); return; }
      } else def = PODERES[d.j.clave][n];
      const costo = AJ.costo["poder" + n];
      if (d.energia < costo) return;
      d.energia -= costo; d.cd = AJ.enfriamiento; d.estado = "atacando"; d.t = 0.25;
      R.anim(o, "poder", d.dir);
      const v = DIRV[d.dir], x0 = cx(o), y0 = cy(o);
      R.sonido(rs, "sfx_" + (def.elem || "agua"));
      if (def.tipo === "proyectil") R.proyectil(rs, def.anim, x0 + v[0] * 12, y0 + v[1] * 12, v[0] * def.vel, v[1] * def.vel,
        { danio: def.danio, elem: def.elem, duenio: "jugador", empuje: def.empuje || 0, congela: def.congela || 0 });
      else if (def.tipo === "latigo") R.latigo(rs, o, def);
      else if (def.tipo === "llamarada") R.llamarada(rs, o, def);
      else if (def.tipo === "muro") R.muro(rs, o);
      else if (def.tipo === "cupula") R.cupula(rs, o);
      else if (def.tipo === "curacion") R.curacion(rs, o);
    };

    R.efecto = function (rs, anim, x, y, angulo) {
      const e = R.crear(rs, "Efecto", 0, 0);
      efectoAnim(e, anim);
      e.setPosition(x - e.getWidth() / 2, y - e.getHeight() / 2);
      if (angulo) e.setAngle(angulo);
      e.setZOrder(5000);
      e.ryu = { auto: true };
      return e;
    };
    R.proyectil = function (rs, anim, x, y, vx, vy, datos) {
      const o = R.crear(rs, "Proyectil", 0, 0);
      efectoAnim(o, anim);
      o.setPosition(x - o.getWidth() / 2, y - o.getHeight() / 2);
      o.setAngle(Math.atan2(vy, vx) * 180 / Math.PI);
      o.setZOrder(5000);
      o.ryu = Object.assign({ vx: vx, vy: vy, vida: 1.5 }, datos);
      return o;
    };
    function golpeaPuerta(rs, x, y, elem, radio) {
      if (!elem) return;
      for (const p of rs.getObjects("PuertaElemental")) {
        if (!p.ryu || p.ryu.abierta) continue;
        if (dist(x, y, cx(p), cy(p)) < radio + 26) R.impactoPuerta(rs, p, elem);
      }
    }
    R.latigo = function (rs, o, def) {
      const v = DIRV[o.ryu.dir], x0 = cx(o), y0 = cy(o);
      R.efecto(rs, "latigazo_agua", x0 + v[0] * 30, y0 + v[1] * 30, ANG[o.ryu.dir]);
      for (const e of objetivosEnemigos(rs)) {
        const dx = cx(e) - x0, dy = cy(e) - y0;
        const adelante = dx * v[0] + dy * v[1], lado = Math.abs(dx * v[1] - dy * v[0]);
        if (adelante > 0 && adelante < def.alcance && lado < 22) R.danarEnemigo(rs, e, def.danio, v, "agua");
      }
      golpeaPuerta(rs, x0 + v[0] * 36, y0 + v[1] * 36, "agua", 24);
    };
    R.llamarada = function (rs, o, def) {
      const v = DIRV[o.ryu.dir], x0 = cx(o), y0 = cy(o);
      R.efecto(rs, "llamarada", x0 + v[0] * 34, y0 + v[1] * 34, ANG[o.ryu.dir]);
      for (const e of objetivosEnemigos(rs)) {
        const dx = cx(e) - x0, dy = cy(e) - y0, d = Math.hypot(dx, dy);
        if (d < 72 && d > 0 && (dx * v[0] + dy * v[1]) / d > Math.cos(40 * Math.PI / 180)) R.danarEnemigo(rs, e, def.danio, v, "fuego");
      }
      golpeaPuerta(rs, x0 + v[0] * 40, y0 + v[1] * 40, "fuego", 30);
    };
    R.muro = function (rs, o) {
      for (const m of rs.getObjects("Muro")) if (m.ryu && m.ryu.duenio === o) m.deleteFromScene(rs);
      const v = DIRV[o.ryu.dir];
      const m = R.crear(rs, "Muro", 0, 0);
      const mx = cx(o) + v[0] * 40, my = pieY(o) - 8 + v[1] * 36;
      const vertical = v[0] !== 0;
      m.setPosition(mx - 48, my - 16);
      if (vertical) m.setAngle(90);
      m.ryu = { vida: AJ.muro.vida, t: AJ.muro.dur, duenio: o,
                caja: vertical ? [mx - 10, my - 46, mx + 10, my + 46] : [mx - 46, my - 6, mx + 46, my + 14] };
      efectoAnim(m, "aparecer");
      R.sonido(rs, "sfx_tierra");
    };
    R.cupula = function (rs, o) {
      const e = R.efecto(rs, "cupula_tierra", cx(o), pieY(o) - 8);
      e.setZOrder(1);
      e.ryu = { cupula: true, t: AJ.cupula.dur, x: cx(o), y: pieY(o) };
    };
    R.curacion = function (rs, o) {
      const e = R.efecto(rs, "curacion", cx(o), pieY(o) - 20);
      e.setZOrder(1);
      R.sonido(rs, "sfx_pista");
      for (const j of R.jugadores(rs)) {
        if (!j.ryu.derribado && dist(cx(j), cy(j), cx(o), cy(o)) <= AJ.curacion.radio) j.ryu.vida = Math.min(j.ryu.vidaMax, j.ryu.vida + AJ.curacion.cantidad);
      }
    };

    // ------------------------------------------------------------------ daño
    function enCupula(rs, o) {
      for (const e of rs.getObjects("Efecto")) if (e.ryu && e.ryu.cupula && dist(e.ryu.x, e.ryu.y, cx(o), pieY(o)) < AJ.cupula.radio) return true;
      return false;
    }
    R.danarJugador = function (rs, o, cantidad) {
      const d = o.ryu;
      if (!d || d.derribado || d.inv > 0 || d.avatar) return;
      let c = cantidad;
      if (d.defendiendo) c *= AJ.defensa;
      if (enCupula(rs, o)) c *= 0.5;
      d.vida -= c; d.inv = AJ.invulnerable;
      R.sonido(rs, "sfx_danio");
      if (d.vida <= 0) {
        d.vida = 0; d.derribado = true; d.tDerribo = AJ.derribo; d.estado = "libre";
        R.sonido(rs, "sfx_derribo");
      } else if (!d.defendiendo) { d.estado = "herido"; d.t = 0.2; R.anim(o, "danio", "abajo"); }
    };
    R.danarEnemigo = function (rs, e, cantidad, v, elem) {
      const d = e.ryu;
      if (!d) return;
      if (e.getName() === "Pilar") {
        d.vida -= cantidad;
        R.efecto(rs, "impacto", cx(e), cy(e));
        if (d.vida <= 0 && !d.roto) { d.roto = true; e.setAnimationName("roto"); R.sonido(rs, "sfx_tierra"); }
        return;
      }
      if (e.getName() === "Norbu") {
        R.efecto(rs, "impacto", cx(e), cy(e));
        if (d.invulnerable) return;
        d.vida = Math.max(0, d.vida - cantidad);
        d.flash = 0.12;
        return;
      }
      if (d.estado === "muerto") return;
      d.vida -= cantidad; d.flash = 0.12;
      if (v) R.mover(rs, e, v[0] * 6, v[1] * 6);
      if (d.vida <= 0) { d.estado = "muerto"; d.t = 0.7; R.anim(e, "derribado", "abajo", d.elem); R.sonido(rs, "sfx_derribo"); }
    };

    // ------------------------------------------------------------------ proyectiles y efectos
    R.actualizarProyectiles = function (rs, dt) {
      const obst = R.estado(rs).obstaculos || [];
      for (const o of rs.getObjects("Proyectil")) {
        const d = o.ryu;
        if (!d) continue;
        o.setX(o.getX() + d.vx * dt); o.setY(o.getY() + d.vy * dt);
        d.vida -= dt;
        const x = cx(o), y = cy(o);
        let fin = d.vida <= 0;
        const caja = [x - 3, y - 3, x + 3, y + 3];
        if (!fin && obst.some((r) => solapa(caja, r))) { fin = true; R.efecto(rs, "impacto", x, y); }
        if (!fin && d.duenio === "jugador") {
          for (const e of objetivosEnemigos(rs)) {
            if (dist(x, y, cx(e), cy(e)) < 15) {
              const v = [Math.sign(d.vx), Math.sign(d.vy)];
              R.danarEnemigo(rs, e, d.danio, v, d.elem);
              if (d.empuje && e.getName() === "Soldado") R.mover(rs, e, v[0] * d.empuje, v[1] * d.empuje);
              if (d.congela && e.ryu) e.ryu.congeladoHasta = ahora(rs) + (e.getName() === "Norbu" ? AJ.congelar.jefe : d.congela);
              R.efecto(rs, d.elem === "tierra" ? "roca_impacto" : "impacto", x, y);
              fin = true; break;
            }
          }
          if (!fin) for (const p of rs.getObjects("PuertaElemental")) {
            if (p.ryu && !p.ryu.abierta && x > p.getX() && x < p.getX() + 64 && y > p.getY() && y < p.getY() + 64) {
              R.impactoPuerta(rs, p, d.elem); R.efecto(rs, "impacto", x, y); fin = true; break;
            }
          }
        } else if (!fin) {
          for (const m of rs.getObjects("Muro")) {
            if (m.ryu && solapa(caja, m.ryu.caja)) { m.ryu.vida -= d.danio; fin = true; R.efecto(rs, "impacto", x, y); break; }
          }
          if (!fin) for (const j of R.jugadores(rs)) {
            if (!j.ryu.derribado && dist(x, y, cx(j), cy(j)) < 13) { R.danarJugador(rs, j, d.danio); fin = true; break; }
          }
        }
        if (fin) o.deleteFromScene(rs);
      }
      for (const e of rs.getObjects("Efecto")) {
        const d = e.ryu || {};
        if (d.cupula) { d.t -= dt; if (d.t <= 0) e.deleteFromScene(rs); continue; }
        if (d.auto && e.hasAnimationEnded()) e.deleteFromScene(rs);
      }
      for (const m of rs.getObjects("Muro")) {
        if (!m.ryu) continue;
        m.ryu.t -= dt;
        if (m.ryu.t <= 0 || m.ryu.vida <= 0) { R.efecto(rs, "roca_impacto", cx(m), cy(m)); m.deleteFromScene(rs); }
      }
    };

    // ------------------------------------------------------------------ puertas elementales
    R.impactoPuerta = function (rs, p, elem) {
      const d = p.ryu, t = ahora(rs);
      if (d.abierta) return;
      if (d.requiere === "tierra") { if (elem === "tierra") R.abrirPuerta(rs, p); return; }
      if (elem === "tierra") d.tTierra = t;
      if (elem === "agua") d.tAgua = t;
      if (d.tTierra && d.tAgua && Math.abs(d.tTierra - d.tAgua) < 3) R.abrirPuerta(rs, p);
    };
    R.abrirPuerta = function (rs, p) {
      p.ryu.abierta = true; p.ryu.abriendo = true;
      p.setAnimationName("abriendo");
      R.sonido(rs, "sfx_puerta");
      marcar(rs, "marcas", "puerta_" + p.ryu.id);
    };
    R.actualizarPuertas = function (rs) {
      for (const p of rs.getObjects("PuertaElemental")) {
        if (p.ryu && p.ryu.abriendo && p.hasAnimationEnded()) { p.ryu.abriendo = false; p.setAnimationName("abierta"); }
      }
    };

    // ------------------------------------------------------------------ enemigos
    R.crearSoldado = function (rs, tipo, elem, x, y) {
      const o = R.crear(rs, "Soldado", x, y);
      const base = AJ.soldado[tipo];
      o.ryu = { tipo: tipo, elem: elem, vida: base.vida, vidaMax: base.vida, dir: "izquierda", t: 0, cd: 1 + Math.random(),
                congeladoHasta: 0, estado: "activo", flash: 0 };
      R.anim(o, "reposo", "izquierda", elem);
      return o;
    };
    function masCercano(o, lista) {
      let mejor = null, md = 1e9;
      for (const j of lista) { const d = dist(cx(o), cy(o), cx(j), cy(j)); if (d < md) { md = d; mejor = j; } }
      return [mejor, md];
    }
    R.actualizarEnemigos = function (rs, dt) {
      const st = R.estado(rs);
      const vivos = R.jugadores(rs).filter((j) => !j.ryu.derribado);
      const obst = R.obstaculos(rs);
      const t = ahora(rs);
      for (const o of rs.getObjects("Soldado")) {
        const d = o.ryu;
        if (!d) continue;
        d.flash = Math.max(0, d.flash - dt);
        o.setColor(d.flash > 0 ? "255;140;140" : "255;255;255");
        if (d.estado === "muerto") {
          d.t -= dt; o.setOpacity(Math.max(0, 255 * d.t / 0.7));
          if (d.hielo) { d.hielo.deleteFromScene(rs); d.hielo = null; }
          if (d.t <= 0) o.deleteFromScene(rs);
          continue;
        }
        if (d.congeladoHasta > t) {
          if (!d.hielo) { d.hielo = R.crear(rs, "Efecto", o.getX(), o.getY()); efectoAnim(d.hielo, "congelado"); d.hielo.ryu = {}; }
          d.hielo.setPosition(o.getX(), o.getY()); d.hielo.setZOrder(o.getZOrder() + 1);
          continue;
        } else if (d.hielo) { d.hielo.deleteFromScene(rs); d.hielo = null; }
        if (st.pausado || st.dialogo || !vivos.length) { R.anim(o, "reposo", d.dir, d.elem); continue; }
        d.cd -= dt;
        const [obj, dd] = masCercano(o, vivos);
        const dx = cx(obj) - cx(o), dy = cy(obj) - cy(o), l = Math.hypot(dx, dy) || 1;
        d.dir = dirDe(dx, dy);
        if (d.t > 0) { d.t -= dt; continue; }
        let mov = 0;
        if (d.tipo === "cac") {
          if (dd > 18) mov = 1;
          else if (d.cd <= 0) {
            d.cd = AJ.soldado.cac.cd; d.t = 0.25; R.anim(o, "golpe", d.dir, d.elem);
            R.danarJugador(rs, obj, AJ.soldado.cac.danio); continue;
          }
        } else {
          if (dd > AJ.soldado.dist.distancia + 20) mov = 1; else if (dd < AJ.soldado.dist.distancia - 20) mov = -1;
          if (d.cd <= 0 && dd < 260) {
            d.cd = AJ.soldado.dist.cd; d.t = 0.25; R.anim(o, "golpe", d.dir, d.elem);
            R.proyectil(rs, "soldado_" + d.elem, cx(o), cy(o), dx / l * 150, dy / l * 150, { danio: AJ.soldado.dist.danio, elem: d.elem, duenio: "enemigo" });
            continue;
          }
        }
        if (mov) {
          const v = (d.tipo === "cac" ? AJ.velCac : AJ.velDist) * dt * mov;
          R.mover(rs, o, dx / l * v, dy / l * v, obst);
          R.anim(o, "caminar", d.dir, d.elem);
        } else R.anim(o, "reposo", d.dir, d.elem);
      }
    };
    R.enemigosVivos = function (rs) {
      return rs.getObjects("Soldado").filter((s) => s.ryu && s.ryu.estado !== "muerto").length;
    };

    // ------------------------------------------------------------------ Tsering
    R.crearTsering = function (rs, x, y, combate) {
      const o = R.crear(rs, "Tsering", x, y);
      o.ryu = { dir: "abajo", t: 0, cd: AJ.tsering.cada, combate: !!combate };
      R.anim(o, "reposo", "abajo");
      return o;
    };
    R.actualizarTsering = function (rs, dt) {
      const st = R.estado(rs);
      for (const o of rs.getObjects("Tsering")) {
        const d = o.ryu;
        if (!d || d.quieto) continue;
        const [gx, gy] = R.centroGrupo(rs);
        const dx = gx + 40 - cx(o), dy = gy + 10 - cy(o), l = Math.hypot(dx, dy);
        if (!st.dialogo && l > 20) {
          const v = Math.min(l, AJ.velJugador * 1.05 * dt);
          o.setX(o.getX() + dx / l * v); o.setY(o.getY() + dy / l * v);
          d.dir = dirDe(dx, dy); R.anim(o, "caminar", d.dir);
        } else if (d.t <= 0) R.anim(o, "reposo", d.dir);
        if (d.t > 0) d.t -= dt;
        if (d.combate && !st.dialogo) {
          d.cd -= dt;
          const enemigos = rs.getObjects("Soldado").filter((s) => s.ryu && s.ryu.estado !== "muerto");
          if (d.cd <= 0 && enemigos.length) {
            d.cd = AJ.tsering.cada;
            const [e] = masCercano(o, enemigos);
            const ex = cx(e) - cx(o), ey = cy(e) - cy(o), el = Math.hypot(ex, ey) || 1;
            d.dir = dirDe(ex, ey); d.t = 0.3; R.anim(o, "poder", d.dir);
            R.proyectil(rs, "rafaga_aire", cx(o), cy(o), ex / el * 200, ey / el * 200, { danio: AJ.tsering.danio, elem: "aire", duenio: "jugador" });
            R.sonido(rs, "sfx_aire");
          }
        }
      }
    };

    // ------------------------------------------------------------------ cámara
    R.camara = function (rs, limites, fija) {
      const capa = rs.getLayer("");
      if (fija) { capa.setCameraZoom(1); capa.setCameraX(320); capa.setCameraY(180); return; }
      const js = R.jugadores(rs);
      if (!js.length) return;
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      for (const o of js) { x0 = Math.min(x0, cx(o)); x1 = Math.max(x1, cx(o)); y0 = Math.min(y0, cy(o)); y1 = Math.max(y1, cy(o)); }
      const z = clamp(Math.min(640 / (x1 - x0 + 220), 360 / (y1 - y0 + 160)), 0.75, 1);
      capa.setCameraZoom(z);
      const vw = 640 / z, vh = 360 / z, L = limites;
      let camX = (x0 + x1) / 2, camY = (y0 + y1) / 2;
      camX = (L[2] - L[0] <= vw) ? (L[0] + L[2]) / 2 : clamp(camX, L[0] + vw / 2, L[2] - vw / 2);
      camY = (L[3] - L[1] <= vh) ? (L[1] + L[3]) / 2 : clamp(camY, L[1] + vh / 2, L[3] - vh / 2);
      capa.setCameraX(camX); capa.setCameraY(camY);
      // los jugadores no pueden salir del área visible
      for (const o of js) {
        o.setX(clamp(o.getX(), camX - vw / 2 + 2, camX + vw / 2 - o.getWidth() - 2));
        o.setY(clamp(o.getY(), camY - vh / 2 - 8, camY + vh / 2 - o.getHeight()));
      }
    };

    // ------------------------------------------------------------------ HUD
    R.crearHud = function (rs, conPistas) {
      const st = R.estado(rs);
      st.hud = [];
      let x = 4;
      for (const j of JUG) {
        const h = R.crear(rs, "Hud", x, 4, "UI"); h.setAnimationName(j.clave); h.setZOrder(50);
        const bv = R.crear(rs, "BarraVida", x + 32, 20, "UI"); bv.setZOrder(51);
        const be = R.crear(rs, "BarraEnergia", x + 32, 28, "UI"); be.setZOrder(51);
        const item = { j: j, hud: h, vida: bv, energia: be };
        if (j.clave === "ryu") { item.icono = R.crear(rs, "IconoElemento", x + 113, 11, "UI"); item.icono.setZOrder(52); }
        st.hud.push(item);
        x += h.getWidth() + 6;
      }
      if (conPistas) {
        const ic = R.crear(rs, "IconoPista", 592, 8, "UI"); ic.setZOrder(50);
        st.textoPistas = R.texto(rs, "0/3", 610, 9, { color: "244;241;232" });
      }
    };
    R.actualizarHud = function (rs) {
      const st = R.estado(rs);
      if (!st.hud) return;
      for (const it of st.hud) {
        const o = rs.getObjects(it.j.obj)[0];
        if (!o || !o.ryu) continue;
        const d = o.ryu, rv = clamp(d.vida / d.vidaMax, 0, 1);
        it.vida.setScaleX(Math.max(0.001, rv)); it.vida.setAnimationName(rv < 0.3 ? "baja" : "normal");
        it.energia.setScaleX(Math.max(0.001, d.energia / d.energiaMax));
        it.hud.setOpacity(d.derribado ? 110 : 255);
        if (it.icono) {
          const el = str(rs, "elementoActivo");
          it.icono.hide(!el);
          if (el) it.icono.setAnimationName(el);
        }
      }
      if (st.textoPistas) st.textoPistas.setText(num(rs, "pistas") + "/3");
    };

    // ------------------------------------------------------------------ diálogos y avisos
    const NOMBRES = { ryu: "Ryu", gao: "Gao", nerea: "Nerea", tsering: "Tsering", norbu: "Norbu", soldado: "Soldado",
                      diario: "Diario de Daichi", daichi: "Daichi" };
    const RETRATO = { ryu: "ryu", gao: "gao", nerea: "nerea", tsering: "tsering", norbu: "norbu", diario: "daichi", daichi: "daichi" };
    R.dialogo = function (rs, lineas, alTerminar) {
      const st = R.estado(rs);
      R.cerrarDialogo(rs);
      const caja = R.crear(rs, "CajaDialogo", 76, 268, "UI"); caja.setWidth(560); caja.setHeight(86); caja.setZOrder(200);
      const marco = R.crear(rs, "MarcoRetrato", 4, 276, "UI"); marco.setZOrder(201);
      const ret = R.crear(rs, "Retrato", 8, 280, "UI"); ret.setZOrder(202);
      const placa = R.crear(rs, "PlacaNombre", 86, 258, "UI"); placa.setZOrder(203);
      const nombre = R.texto(rs, "", 92, 261, { z: 204 });
      const txt = R.texto(rs, "", 90, 286, { ancho: 532, z: 204 });
      const sig = R.crear(rs, "Continuar", 616, 338, "UI"); sig.setZOrder(204);
      st.dialogo = { lineas: lineas, i: -1, cb: alTerminar, objs: { caja, marco, ret, placa, nombre, txt, sig }, chars: 0 };
      R.siguienteLinea(rs);
    };
    R.siguienteLinea = function (rs) {
      const st = R.estado(rs), dg = st.dialogo;
      dg.i++;
      if (dg.i >= dg.lineas.length) {
        const cb = dg.cb;
        R.cerrarDialogo(rs);
        if (cb) cb();
        return;
      }
      const [quien, texto] = dg.lineas[dg.i];
      const o = dg.objs, conRetrato = !!RETRATO[quien];
      o.ret.hide(!conRetrato); o.marco.hide(!conRetrato);
      if (conRetrato) o.ret.setAnimationName(RETRATO[quien]);
      const n = NOMBRES[quien] || "";
      o.placa.hide(!n); o.nombre.setText(n);
      o.placa.setWidth(Math.max(24, o.nombre.getWidth() + 14));
      const x = conRetrato ? 90 : 20;
      o.caja.setX(conRetrato ? 76 : 8); o.caja.setWidth(conRetrato ? 560 : 624);
      o.txt.setX(x); o.txt.setWrappingWidth(conRetrato ? 532 : 600);
      o.placa.setX(x - 4); o.nombre.setX(x + 2);
      dg.texto = texto; dg.chars = 0; o.txt.setText("");
    };
    R.cerrarDialogo = function (rs) {
      const st = R.estado(rs);
      if (!st.dialogo) return;
      for (const k in st.dialogo.objs) st.dialogo.objs[k].deleteFromScene(rs);
      st.dialogo = null;
    };
    R.actualizarDialogo = function (rs, dt) {
      const st = R.estado(rs), dg = st.dialogo;
      if (!dg) return;
      const antes = Math.floor(dg.chars);
      dg.chars = Math.min(dg.texto.length, dg.chars + 45 * dt);
      const ahoraC = Math.floor(dg.chars);
      if (ahoraC !== antes) {
        dg.objs.txt.setText(dg.texto.substring(0, ahoraC));
        if (ahoraC % 3 === 0) R.sonido(rs, "sfx_dialogo");
      }
      dg.objs.sig.hide(ahoraC < dg.texto.length);
      if (R.alguienPulsa(rs, "interactuar")) {
        if (ahoraC < dg.texto.length) { dg.chars = dg.texto.length; dg.objs.txt.setText(dg.texto); }
        else R.siguienteLinea(rs);
      }
    };
    R.aviso = function (rs, texto, seg) {
      const st = R.estado(rs);
      if (st.aviso) st.aviso.o.deleteFromScene(rs);
      const o = R.texto(rs, texto, 320, 44, { centrado: true, color: "232;210;122", z: 150 });
      o.setOutlineEnabled(true); o.setOutlineColor("26;20;32"); o.setOutlineThickness(2);
      st.aviso = { o: o, t: seg || 3 };
    };
    R.actualizarAviso = function (rs, dt) {
      const st = R.estado(rs);
      if (!st.aviso) return;
      st.aviso.t -= dt;
      if (st.aviso.t <= 0) { st.aviso.o.deleteFromScene(rs); st.aviso = null; }
    };

    // ------------------------------------------------------------------ pausa y derrota
    R.actualizarPausa = function (rs) {
      const st = R.estado(rs);
      if (!R.pausaPulsada(rs) || st.dialogo) return;
      st.pausado = !st.pausado;
      if (st.pausado) {
        st.textoPausa = R.texto(rs, "PAUSA", 320, 150, { grande: true, centrado: true, color: "232;210;122", z: 300 });
        st.textoPausa2 = R.texto(rs, "Esc / Start para continuar", 320, 180, { centrado: true, z: 300 });
      } else { st.textoPausa.deleteFromScene(rs); st.textoPausa2.deleteFromScene(rs); }
    };
    R.derrota = function (rs) {
      setStr(rs, "escenaDerrota", rs.getName());
      R.ir(rs, "Derrota");
    };

    // ------------------------------------------------------------------ bucle común de las escenas jugables
    R.bucleJuego = function (rs, dt, limites, camFija) {
      const st = R.estado(rs);
      R.actualizarPausa(rs);
      R.actualizarDialogo(rs, dt);
      R.actualizarAviso(rs, dt);
      if (!st.pausado) {
        R.actualizarJugadores(rs, dt);
        R.actualizarEnemigos(rs, dt);
        R.actualizarTsering(rs, dt);
        R.actualizarProyectiles(rs, dt);
        R.actualizarPuertas(rs);
      }
      R.ordenarProfundidad(rs);
      R.camara(rs, limites, camFija);
      R.actualizarHud(rs);
    };
    const cercaDe = (o, x, y, r) => dist(cx(o), pieY(o), x, y) < r;
    R.alguienInteractuaCerca = function (rs, x, y, r, soloRyu) {
      for (const o of R.jugadores(rs)) {
        if (soloRyu && o.ryu.p !== 1) continue;
        if (!o.ryu.derribado && o.ryu.control && cercaDe(o, x, y, r) && R.pulsa(rs, o.ryu.p, "interactuar")) return true;
      }
      return false;
    };
    R.alguienEnZona = function (rs, z) {
      return R.jugadores(rs).some((o) => { const x = cx(o), y = pieY(o); return x > z[0] && x < z[2] && y > z[1] && y < z[3]; });
    };
    R.irAPelea = function (rs, id, retorno) {
      setStr(rs, "peleaActual", id); setStr(rs, "escenaRetorno", rs.getName());
      setNum(rs, "retornoX", retorno[0]); setNum(rs, "retornoY", retorno[1]);
      R.ir(rs, "Pelea");
    };
    R.volviendoDePelea = function (rs) {
      const v = str(rs, "escenaRetorno") === rs.getName() && num(rs, "retornoX") > 0;
      const pos = [num(rs, "retornoX"), num(rs, "retornoY")];
      if (v) { setStr(rs, "escenaRetorno", ""); setNum(rs, "retornoX", 0); }
      return v ? pos : null;
    };
    const posTrio = (x, y) => [[x - 16, y - 16], [x - 44, y - 6], [x + 12, y - 6]];

    // ================================================================== ESCENAS
    const E = {};
    R.escenas = E;
    R.ejecutar = function (rs, nombre) {
      R.actualizarEntrada(rs);
      if (!rs.__ryu || rs.getTimeManager().isFirstFrame()) {
        rs.__ryu = { escena: nombre };
        E[nombre].inicio(rs, rs.__ryu);
      }
      const dt = Math.min(0.05, rs.getTimeManager().getElapsedTime() / 1000);
      E[nombre].frame(rs, rs.__ryu, dt);
    };

    // ------------------------------------------------------------------ menú de inicio
    function menu(rs, st, opciones, y0, alElegir) {
      st.opciones = opciones.map((t, i) => R.texto(rs, t, 320, y0 + i * 20, { centrado: true, z: 10 }));
      st.sel = 0; st.alElegir = alElegir;
    }
    function actualizarMenu(rs, st) {
      if (R.alguienPulsa(rs, "abajo")) { st.sel = (st.sel + 1) % st.opciones.length; R.sonido(rs, "sfx_menu"); }
      if (R.alguienPulsa(rs, "arriba")) { st.sel = (st.sel + st.opciones.length - 1) % st.opciones.length; R.sonido(rs, "sfx_menu"); }
      st.opciones.forEach((o, i) => o.setColor(i === st.sel ? "232;210;122" : "244;241;232"));
      if (!st.cursor) st.cursor = R.texto(rs, ">", 0, 0, { color: "232;210;122", z: 10 });
      const o = st.opciones[st.sel];
      st.cursor.setPosition(o.getX() - 14, o.getY());
      if (R.alguienPulsa(rs, "interactuar") || R.alguienPulsa(rs, "golpe")) { R.sonido(rs, "sfx_menu"); st.alElegir(st.sel); }
    }
    E.MenuInicio = {
      inicio(rs, st) {
        R.musica(rs, "musica_exploracion");
        const f = R.crear(rs, "Pantalla", 0, 0, "UI"); f.setAnimationName("titulo"); f.setZOrder(0);
        const fondo = R.crear(rs, "Pantalla", 248, 186, "UI"); fondo.setAnimationName("velo"); fondo.setZOrder(5);
        menu(rs, st, ["Jugar", "Controles", "Salir"], 196, (i) => {
          if (i === 0) { R.reiniciarPartida(rs); R.ir(rs, "Intro"); }
          else if (i === 1) R.ir(rs, "Controles");
          else gdjs.evtTools.runtimeScene.stopGame(rs);
        });
        st.mandos = R.texto(rs, "", 632, 330, { z: 10, color: "200;200;192" });
      },
      frame(rs, st) {
        actualizarMenu(rs, st);
        const n = R.mandosConectados();
        st.mandos.setText("Mandos: " + n);
        st.mandos.setX(632 - st.mandos.getWidth());
      },
    };
    E.Controles = {
      inicio(rs, st) {
        const f = R.crear(rs, "Pantalla", 0, 0, "UI"); f.setAnimationName("controles");
        st.t = 0;
      },
      frame(rs, st, dt) {
        st.t += dt;
        if (st.t > 0.3 && (R.alguienPulsa(rs, "interactuar") || R.pausaPulsada(rs))) R.ir(rs, "MenuInicio");
      },
    };

    // ------------------------------------------------------------------ intro (4 paneles)
    const INTRO = [
      "Muchas generaciones después de los avatares que recuerda la historia, el mundo cambió. Las naciones se volvieron ciudades conectadas, pero el control de los elementos sigue vivo.",
      "Hace diecisiete años murió Daichi, el último Avatar, maestro tierra. Nadie terminó de explicar cómo.",
      "Desde entonces nadie sabe quién es el nuevo Avatar. Y una organización, El Ciclo Roto, quiere encontrarlo primero.",
      "En una ciudad de la Nación del Fuego, un chico llamado Ryu está a punto de descubrir quién es.",
    ];
    function panelTexto(rs, st, anim, texto) {
      if (st.panel) st.panel.deleteFromScene(rs);
      st.panel = R.crear(rs, "Pantalla", 0, 0, "UI"); st.panel.setAnimationName(anim); st.panel.setZOrder(0);
      if (!st.txt) st.txt = R.texto(rs, "", 16, 300, { ancho: 608, z: 10 });
      st.texto = texto; st.chars = 0; st.txt.setText("");
    }
    function actualizarPanelTexto(rs, st, dt) {
      st.chars = Math.min(st.texto.length, st.chars + 50 * dt);
      st.txt.setText(st.texto.substring(0, Math.floor(st.chars)));
      if (R.alguienPulsa(rs, "interactuar") || R.alguienPulsa(rs, "golpe")) {
        if (st.chars < st.texto.length) { st.chars = st.texto.length; return false; }
        return true;
      }
      return false;
    }
    E.Intro = {
      inicio(rs, st) { R.musica(rs, "musica_exploracion"); st.i = 0; panelTexto(rs, st, "panel_1", INTRO[0]); },
      frame(rs, st, dt) {
        if (actualizarPanelTexto(rs, st, dt)) {
          st.i++;
          if (st.i >= INTRO.length) R.ir(rs, "Ciudad");
          else panelTexto(rs, st, "panel_" + (st.i + 1), INTRO[st.i]);
        }
      },
    };

    // ------------------------------------------------------------------ diálogos (docs/05)
    const D = {
      ciudad0: [["gao", "Ryu, otra vez llegas tarde."], ["ryu", "Llegué justo a tiempo. Tarde es cuando ya no queda comida."],
        ["nerea", "Perdón… ¿ustedes también vieron ese símbolo pintado en la pared?"], ["gao", "Un círculo roto. Lo están poniendo por toda la ciudad."],
        ["ryu", "¿Y tú quién eres?"], ["nerea", "Nerea. Llegué ayer de la costa."]],
      ciudad1: [["soldado", "¡Revisen a todos los maestros! El Avatar está en esta ciudad."], ["ryu", "¿El Avatar? ¿Aquí? Bueno, nadie toca mi barrio."],
        ["gao", "Ryu, espera…"], ["nerea", "Ya es tarde. ¡Prepárense!"]],
      despertar: [["ryu", "¿Qué… qué fue ese viento?"], ["soldado", "¡Fuego y aire! ¡Es él! ¡Es el Avatar!"], ["gao", "¿¡Tú eres el Avatar!?"],
        ["ryu", "¡Me entero contigo!"]],
      ciudad2a: [["nerea", "¡La plaza se está quemando!"], ["ryu", "Sé hacer fuego, no apagarlo."],
        ["tsering", "Entonces escucha al agua. No la empujes, acompáñala."]],
      ciudad2b: [["tsering", "Soy Tsering. Te he esperado diecisiete años."], ["ryu", "¿Diecisiete? Eso es… toda mi vida."],
        ["tsering", "El Ciclo Roto ya sabe quién eres. Antes de huir, necesitas entender qué le pasó a Daichi."], ["gao", "¿Por dónde empezamos?"],
        ["tsering", "Por las minas de la montaña. Allí pasó Daichi sus últimos días."], ["nerea", "Entonces vamos juntos."]],
      puerta1: [["gao", "Esta puerta es de tierra. Déjenmela a mí."]],
      documento: [["", "Documento de El Ciclo Roto: «Fase uno: encontrar al Avatar. Fase dos: el sello.»"], ["ryu", "¿El sello? Eso no suena bien."]],
      puerta2: [["nerea", "Pide tierra y agua al mismo tiempo. Gao, a la cuenta de tres."]],
      diario: [["diario", "Norbu y yo seguimos buscando la forma de que el Avatar no cargue con todo solo. Él dice que la respuesta es soltar. Yo no estoy tan seguro."],
        ["tsering", "…¿Norbu?"]],
      norbu: [["norbu", "Así que tú eres el nuevo. Tan joven como lo era él."], ["ryu", "¿Tú eres el que pinta círculos rotos en mi ciudad?"],
        ["norbu", "No vengo a pelear, Ryu. Vengo a liberarte. Soltar no es perder, es liberar."], ["tsering", "Esa frase… yo te la enseñé. Norbu."],
        ["norbu", "Me enseñaste a soltar, maestro. La diferencia es que yo sí aprendí."], ["norbu", "Te espero en las alturas, Avatar."],
        ["tsering", "Fue mi alumno. Y el mejor amigo de Daichi. Debí verlo antes."]],
      arena: [["norbu", "Daichi cargó con el mundo y el mundo lo dejó caer. Contigo eso termina hoy."], ["ryu", "Pues tendrás que pasar por los tres."]],
      sello: [["norbu", "El sello te liberará del ciclo. Después de hoy serás solo Ryu."], ["gao", "¡Los pilares alimentan el sello! ¡Uno cada uno!"]],
      pilares: [["ryu", "No cargo con esto solo. Nunca lo hice."]],
      final: [["norbu", "Daichi tampoco estaba solo. Yo estaba ahí… y no fue suficiente."], ["ryu", "Entonces ayúdanos a que no le pase a nadie más."],
        ["tsering", "Ven conmigo, Norbu. Tenemos mucho de qué hablar."]],
    };
    R.D = D;

    // ------------------------------------------------------------------ ciudad
    E.Ciudad = {
      inicio(rs, st) {
        const M = MAPAS.ciudad;
        R.musica(rs, "musica_exploracion");
        st.obstaculos = M.obstaculos; st.limites = M.limites; st.combate = true;
        const fondo = R.crear(rs, "Fondo", 0, 0); fondo.setAnimationName("ciudad"); fondo.setZOrder(-10000);
        const fu = R.crear(rs, "Fuente", M.puntos.fuente[0], M.puntos.fuente[1]); fu.ryu = {};
        const ret = R.volviendoDePelea(rs);
        const base = ret || M.puntos.inicio;
        R.crearJugadores(rs, posTrio(base[0] + 16, base[1] + 16));
        R.crearHud(rs, true);
        const fase = num(rs, "faseHistoria");
        if (fase === 0) {
          for (let i = 0; i < 4; i++) {
            const c = R.crear(rs, "Ciudadano", 200 + i * 230, 470 + (i % 2) * 120);
            c.ryu = { tipo: "abc"[i % 3], t: 0, vx: 0, vy: 0 };
            c.setAnimationName(c.ryu.tipo + "_reposo");
          }
          R.controlJugadores(rs, false);
          st.t = 0.6; st.paso = "presentacion";
        } else if (fase === 1) {
          const e = M.puntos.entrada_soldados;
          for (let i = 0; i < 3; i++) R.crearSoldado(rs, "cac", i % 2 ? "aire" : "fuego", e[0] - 30 + i * 24, e[1] + 10);
          R.controlJugadores(rs, false); st.paso = "ataque"; st.t = 0.6;
        } else if (fase >= 2) {
          if (!bool(rs, "aguaDesbloqueada")) {
            st.fuegos = M.fuego.map((p) => { const f = R.crear(rs, "Efecto", p[0], p[1]); efectoAnim(f, "fuego_suelo"); f.ryu = {}; f.setZOrder(2); return f; });
          }
          const ts = R.crearTsering(rs, M.puntos.tsering[0], M.puntos.tsering[1], false);
          if (!marca(rs, "marcas", "ciudad2")) { ts.ryu.quieto = true; st.paso = "incendio"; st.t = 0.8; R.controlJugadores(rs, false); }
          else st.paso = "mision";
        }
      },
      frame(rs, st, dt) {
        const M = MAPAS.ciudad;
        R.bucleJuego(rs, dt, M.limites, false);
        if (st.pausado) return;
        // ciudadanos paseando
        for (const c of rs.getObjects("Ciudadano")) {
          const d = c.ryu; d.t -= dt;
          if (d.t <= 0) { d.t = 1 + Math.random() * 2; const a = Math.random() * 6.28; const m = Math.random() < 0.4 ? 0 : 25; d.vx = Math.cos(a) * m; d.vy = Math.sin(a) * m; }
          const z = M.zonas.plaza;
          if (c.getX() + d.vx * dt < z[0] || c.getX() + d.vx * dt > z[2]) d.vx = -d.vx;
          if (c.getY() + d.vy * dt < z[1] || c.getY() + d.vy * dt > z[3]) d.vy = -d.vy;
          R.mover(rs, c, d.vx * dt, d.vy * dt);
          c.setAnimationName(d.tipo + (d.vx || d.vy ? "_caminar" : "_reposo"));
          c.flipX(d.vx < 0);
        }
        if (st.t > 0) { st.t -= dt; return; }
        if (st.dialogo) return;
        // pista 1: el símbolo de la pared
        if (R.alguienInteractuaCerca(rs, M.puntos.simbolo[0], M.puntos.simbolo[1], 44)) R.aviso(rs, "Un círculo con cuatro marcas, partido por una línea.", 3);
        switch (st.paso) {
          case "presentacion":
            st.paso = "esperando";
            R.dialogo(rs, D.ciudad0, () => {
              if (num(rs, "pistas") < 1) setNum(rs, "pistas", 1);
              R.sonido(rs, "sfx_pista"); R.aviso(rs, "Pista 1 registrada: el símbolo de El Ciclo Roto", 3);
              setNum(rs, "faseHistoria", 1);
              st.paso = "ataque"; st.t = 1.2;
              const e = M.puntos.entrada_soldados;
              for (let i = 0; i < 3; i++) R.crearSoldado(rs, "cac", i % 2 ? "aire" : "fuego", e[0] - 30 + i * 24, e[1] + 10);
              for (const c of rs.getObjects("Ciudadano")) c.ryu.vy = 60;
            });
            break;
          case "ataque":
            for (const s of rs.getObjects("Soldado")) { s.setY(Math.min(s.getY() + 60 * dt, 420)); R.anim(s, "caminar", "abajo", s.ryu.elem); }
            if (rs.getObjects("Soldado").every((s) => s.getY() >= 300)) {
              st.paso = "esperando";
              R.dialogo(rs, D.ciudad1, () => R.irAPelea(rs, "ciudad1", MAPAS.ciudad.puntos.retorno_pelea));
            }
            break;
          case "incendio":
            st.paso = "esperando";
            R.dialogo(rs, D.ciudad2a, () => {
              R.controlJugadores(rs, true); st.paso = "fuente";
              R.aviso(rs, "Ryu: acércate a la fuente y pulsa interactuar", 4);
            });
            break;
          case "fuente": {
            const f = M.puntos.fuente;
            if (R.alguienInteractuaCerca(rs, f[0] + 32, f[1] + 60, 48, true)) {
              setBool(rs, "aguaDesbloqueada", true);
              if (!str(rs, "elementoActivo")) setStr(rs, "elementoActivo", "agua");
              R.sonido(rs, "sfx_desbloqueo"); R.aviso(rs, "Ryu desbloqueó el agua", 3);
              for (const e of st.fuegos || []) e.deleteFromScene(rs);
              st.fuegos = [];
              st.paso = "esperando"; R.controlJugadores(rs, false);
              R.dialogo(rs, D.ciudad2b, () => {
                marcar(rs, "marcas", "ciudad2"); R.controlJugadores(rs, true);
                for (const t of rs.getObjects("Tsering")) t.ryu.quieto = false;
                R.aviso(rs, "Misión: ir a las minas del norte", 4); st.paso = "mision";
              });
            }
            break;
          }
          case "mision":
            if (R.alguienEnZona(rs, M.zonas.salida_norte)) { setNum(rs, "faseHistoria", Math.max(3, num(rs, "faseHistoria"))); R.ir(rs, "ZonaTierra"); }
            break;
        }
      },
    };

    // ------------------------------------------------------------------ zona de tierra
    function zonaTierra(rs, st, zona) {
      st.zona = zona;
      st.limites = MAPAS.tierra.limites[zona];
    }
    E.ZonaTierra = {
      inicio(rs, st) {
        const M = MAPAS.tierra;
        R.musica(rs, "musica_exploracion");
        st.obstaculos = M.obstaculos; st.combate = true;
        const fondo = R.crear(rs, "Fondo", 0, 0); fondo.setAnimationName("tierra"); fondo.setZOrder(-10000);
        for (const [id, req, punto] of [["p1", "tierra", "puerta1"], ["p2", "tierra+agua", "puerta2"]]) {
          const p = R.crear(rs, "PuertaElemental", M.puntos[punto][0], M.puntos[punto][1]);
          const abierta = marca(rs, "marcas", "puerta_" + id);
          p.ryu = { id: id, requiere: req, abierta: abierta };
          p.setAnimationName(abierta ? "abierta" : (req === "tierra" ? "cerrada_tierra" : "cerrada_tierra_agua"));
        }
        if (!marca(rs, "marcas", "documento")) { const d = R.crear(rs, "Pista", M.puntos.documento[0], M.puntos.documento[1]); d.setAnimationName("documento"); d.ryu = { id: "documento" }; }
        if (!marca(rs, "marcas", "diario")) { const d = R.crear(rs, "Pista", M.puntos.diario[0] - 16, M.puntos.diario[1]); d.setAnimationName("diario"); d.ryu = { id: "diario" }; }
        const ret = R.volviendoDePelea(rs);
        const base = ret || M.puntos.inicio_exterior;
        zonaTierra(rs, st, base[1] < 22 * 32 ? "interior" : "exterior");
        R.crearJugadores(rs, posTrio(base[0] + 16, base[1] + 16));
        R.crearTsering(rs, base[0] + 50, base[1] + 10, false);
        R.crearHud(rs, true);
      },
      frame(rs, st, dt) {
        const M = MAPAS.tierra;
        R.bucleJuego(rs, dt, st.limites, false);
        if (st.pausado || st.dialogo || st.saliendo) return;
        if (st.t > 0) { st.t -= dt; return; }
        const fase = num(rs, "faseHistoria");
        if (st.zona === "exterior") {
          if (!marca(rs, "encuentrosHechos", "tierra1") && R.alguienEnZona(rs, M.zonas.encuentro_tierra1)) return R.irAPelea(rs, "tierra1", M.puntos.retorno_tierra1);
          if (fase < 5 && R.alguienEnZona(rs, M.zonas.entrada_mina)) {
            zonaTierra(rs, st, "interior"); R.teletransportar(rs, M.puntos.inicio_interior[0], M.puntos.inicio_interior[1]); return;
          }
          if (st.paso === "norbu_sale") {
            for (const n of rs.getObjects("Norbu")) { n.setOpacity(Math.max(0, n.getOpacity() - 200 * dt)); n.setY(n.getY() - 20 * dt); }
            st.tSalida -= dt;
            if (st.tSalida <= 0) { setNum(rs, "faseHistoria", 6); R.ir(rs, "ArenaFinal"); }
          }
          return;
        }
        // interior de la mina
        const p1 = rs.getObjects("PuertaElemental").find((p) => p.ryu.id === "p1");
        const p2 = rs.getObjects("PuertaElemental").find((p) => p.ryu.id === "p2");
        if (!marca(rs, "marcas", "dlg_puerta1") && R.jugadores(rs).some((o) => cercaDe(o, cx(p1), p1.getY() + 64, 80))) {
          marcar(rs, "marcas", "dlg_puerta1"); return R.dialogo(rs, D.puerta1, null);
        }
        if (!marca(rs, "marcas", "dlg_puerta2") && R.jugadores(rs).some((o) => cercaDe(o, cx(p2), p2.getY() + 64, 80))) {
          marcar(rs, "marcas", "dlg_puerta2"); return R.dialogo(rs, D.puerta2, null);
        }
        for (const pi of rs.getObjects("Pista")) {
          if (R.alguienInteractuaCerca(rs, cx(pi), pieY(pi), 40)) {
            const id = pi.ryu.id;
            marcar(rs, "marcas", id); pi.deleteFromScene(rs);
            setNum(rs, "pistas", num(rs, "pistas") + 1); R.sonido(rs, "sfx_pista");
            R.dialogo(rs, D[id], () => {
              R.aviso(rs, "Pista " + num(rs, "pistas") + " registrada", 2.5);
              if (id === "diario") R.aviso(rs, "Ryu: toca el emblema de la cámara", 4);
            });
            return;
          }
        }
        if (marca(rs, "marcas", "diario") && !bool(rs, "tierraDesbloqueada") &&
            R.alguienInteractuaCerca(rs, M.puntos.emblema[0] + 16, M.puntos.emblema[1] + 20, 56, true)) {
          setBool(rs, "tierraDesbloqueada", true); setNum(rs, "faseHistoria", 4);
          R.sonido(rs, "sfx_desbloqueo"); R.aviso(rs, "Ryu desbloqueó la tierra. Sal de la mina.", 4);
        }
        if (!marca(rs, "encuentrosHechos", "tierra2") && R.alguienEnZona(rs, M.zonas.encuentro_tierra2)) return R.irAPelea(rs, "tierra2", M.puntos.retorno_tierra2);
        if (num(rs, "faseHistoria") >= 4 && R.alguienEnZona(rs, M.zonas.salida_mina)) {
          zonaTierra(rs, st, "exterior");
          const s = M.puntos.salida_mina_exterior;
          R.teletransportar(rs, s[0], s[1]);
          const n = R.crear(rs, "Norbu", M.puntos.norbu[0], M.puntos.norbu[1]); n.ryu = {}; R.anim(n, "reposo", "arriba");
          R.controlJugadores(rs, false); st.t = 0.6;
          R.dialogo(rs, D.norbu, () => { setNum(rs, "faseHistoria", 5); st.paso = "norbu_sale"; st.tSalida = 1.5; });
        }
      },
    };

    // ------------------------------------------------------------------ pelea (escena reutilizable)
    const PELEAS = {
      ciudad1: { fondo: "plaza", oleadas: [["cac", "cac"], ["cac", "cac", "dist"]], tsering: false, elementos: ["fuego", "aire"], tutorial: true },
      tierra1: { fondo: "canon", oleadas: [["cac", "cac", "dist"], ["cac", "cac", "dist", "dist"]], tsering: true, elementos: ["tierra", "agua"] },
      tierra2: { fondo: "mina", oleadas: [["cac", "cac", "dist"], ["cac", "cac", "cac"], ["cac", "cac", "dist", "dist"]], tsering: true, elementos: ["tierra", "agua"] },
    };
    R.PELEAS = PELEAS;
    const TUTORIAL = ["Moverse: WASD · Flechas · IJKL · stick", "Golpe: F · Num 1 · U · A", "Poder 1: R · Num 4 · O · X",
                      "Defensa (mantener): Shift · Num 0 · Espacio · RB"];
    E.Pelea = {
      inicio(rs, st) {
        st.id = str(rs, "peleaActual") || "ciudad1";
        const P = PELEAS[st.id];
        R.musica(rs, "musica_pelea");
        st.limites = MAPAS.arenas[P.fondo].limites; st.obstaculos = [];
        const f = R.crear(rs, "Fondo", 0, 0); f.setAnimationName(P.fondo); f.setZOrder(-10000);
        R.crearJugadores(rs, [[110, 220], [80, 260], [120, 300]]);
        if (P.tsering) R.crearTsering(rs, 60, 230, true);
        R.crearHud(rs, false);
        st.combate = true; st.oleada = -1; st.t = 0.8; st.tut = P.tutorial ? 0 : -1; st.tTut = 0;
      },
      frame(rs, st, dt) {
        const P = PELEAS[st.id];
        R.bucleJuego(rs, dt, st.limites, true);
        if (st.pausado || st.saliendo) return;
        if (st.tut >= 0 && st.tut < TUTORIAL.length && !st.dialogo) {
          st.tTut -= dt;
          if (st.tTut <= 0) { R.aviso(rs, TUTORIAL[st.tut], 3); st.tut++; st.tTut = 3.2; }
        }
        if (st.dialogo) return;
        if (st.t > 0) { st.t -= dt; return; }
        if (st.victoria) { R.ir(rs, str(rs, "escenaRetorno") || "Ciudad"); return; }
        if (R.enemigosVivos(rs) > 0 || rs.getObjects("Soldado").length > 0) return;
        if (st.id === "ciudad1" && st.oleada === 0 && !bool(rs, "aireDesbloqueado")) {
          // despertar del aire
          const ryu = rs.getObjects("Ryu")[0];
          R.controlJugadores(rs, false);
          R.proyectil(rs, "rafaga_aire", cx(ryu), cy(ryu), 200, 0, { danio: 0, elem: "aire", duenio: "jugador" });
          R.sonido(rs, "sfx_aire");
          setBool(rs, "aireDesbloqueado", true); setStr(rs, "elementoActivo", "aire");
          R.dialogo(rs, D.despertar, () => {
            R.controlJugadores(rs, true); R.sonido(rs, "sfx_desbloqueo");
            R.aviso(rs, "Ryu desbloqueó el aire. Pulsa Q o LB para cambiar de elemento.", 4);
          });
          return;
        }
        st.oleada++;
        if (st.oleada >= P.oleadas.length) {
          marcar(rs, "encuentrosHechos", st.id);
          if (st.id === "ciudad1") setNum(rs, "faseHistoria", 2);
          R.sonido(rs, "sfx_desbloqueo"); R.aviso(rs, "¡Victoria!", 2);
          st.victoria = true; st.t = 1.8;
          return;
        }
        P.oleadas[st.oleada].forEach((tipo, i) => {
          const el = P.elementos[i % P.elementos.length];
          R.crearSoldado(rs, tipo, el, 540 + (i % 2) * 40, st.limites[1] + 30 + i * 46);
        });
        R.aviso(rs, "Oleada " + (st.oleada + 1) + " de " + P.oleadas.length, 2);
        st.t = 0.5;
      },
    };

    // ------------------------------------------------------------------ arena final
    E.ArenaFinal = {
      inicio(rs, st) {
        R.musica(rs, "musica_jefe");
        st.limites = MAPAS.arenas.arena.limites; st.obstaculos = [];
        const f = R.crear(rs, "Fondo", 0, 0); f.setAnimationName("arena"); f.setZOrder(-10000);
        R.crearJugadores(rs, [[300, 250], [250, 262], [350, 262]]);
        for (const o of R.jugadores(rs)) o.ryu.dir = "arriba";
        const n = R.crear(rs, "Norbu", 304, 96);
        n.ryu = { activo: false, vida: AJ.norbu.vida, fase: 1, cdRafaga: 2, cdDash: 5, dash: 0, dvx: 0, dvy: 0, invulnerable: false, flash: 0, dir: "abajo",
                  congeladoHasta: 0 };
        R.crearHud(rs, false);
        st.barraJefe = R.crear(rs, "BarraVida", 244, 340, "UI"); st.barraJefe.setScaleY(2); st.barraJefe.setZOrder(60);
        R.texto(rs, "NORBU", 244, 326, { color: "232;210;122", z: 60 });
        st.combate = true; st.paso = "intro"; st.t = 0.5;
      },
      frame(rs, st, dt) {
        R.bucleJuego(rs, dt, st.limites, true);
        const n = rs.getObjects("Norbu")[0], d = n.ryu;
        st.barraJefe.setScaleX(Math.max(0.001, d.vida / AJ.norbu.vida) * 2);
        d.flash = Math.max(0, (d.flash || 0) - dt);
        n.setColor(d.flash > 0 ? "255;140;140" : (d.invulnerable ? "200;200;255" : "255;255;255"));
        if (st.pausado || st.saliendo) return;
        if (st.dialogo) return;
        if (st.t > 0) { st.t -= dt; return; }
        const ryu = rs.getObjects("Ryu")[0];
        switch (st.paso) {
          case "intro":
            st.paso = "esperando";
            R.dialogo(rs, D.arena, () => { d.activo = true; st.paso = "pelea"; });
            return;
          case "fin":
            R.anim(n, "derribado", "abajo");
            setNum(rs, "faseHistoria", 7); R.ir(rs, "Final");
            return;
        }
        if (!d.activo) return;
        // fases según la vida
        if (d.fase === 1 && d.vida <= AJ.norbu.fase2) {
          d.fase = 2;
          R.crearSoldado(rs, "cac", "aire", 120, 120); R.crearSoldado(rs, "dist", "aire", 500, 120);
          R.aviso(rs, "¡Norbu llama refuerzos!", 2);
        }
        if (d.fase === 2 && d.vida <= AJ.norbu.fase3) {
          d.fase = 3; d.invulnerable = true;
          R.dialogo(rs, D.sello, () => {
            st.sello = R.efecto(rs, "sello", cx(ryu), pieY(ryu)); st.sello.ryu = { sello: true }; st.sello.setZOrder(1);
            [[150, 110], [470, 110], [310, 240]].forEach(([x, y]) => {
              const p = R.crear(rs, "Pilar", x, y); p.setAnimationName("entero"); p.ryu = { vida: AJ.pilarVida, roto: false };
            });
          });
          return;
        }
        if (st.sello) {
          st.sello.setPosition(cx(ryu) - 48, pieY(ryu) - 48);
          if (rs.getObjects("Pilar").every((p) => p.ryu.roto)) {
            st.sello.deleteFromScene(rs); st.sello = null;
            R.dialogo(rs, D.pilares, () => R.activarAvatar(rs, st));
            return;
          }
        }
        if (st.avatar) {
          st.avatar.t -= dt; st.avatar.tic -= dt;
          st.avatar.aura.setPosition(cx(ryu) - 32, cy(ryu) - 34);
          if (st.avatar.tic <= 0) {
            st.avatar.tic = 1;
            for (const e of objetivosEnemigos(rs)) if (dist(cx(e), cy(e), cx(ryu), cy(ryu)) < 110) R.danarEnemigo(rs, e, AJ.avatarDanio, null, "");
          }
          if (st.avatar.t <= 0) R.activarAvatar(rs, st);
        }
        if (d.vida <= 0) {
          if (st.avatar) { st.avatar.aura.deleteFromScene(rs); ryu.ryu.avatar = false; st.avatar = null; }
          d.activo = false; st.paso = "fin"; st.t = 1.2; R.sonido(rs, "sfx_derribo"); R.anim(n, "derribado", "abajo");
          return;
        }
        R.actualizarNorbu(rs, st, n, dt);
      },
    };
    R.activarAvatar = function (rs, st) {
      const ryu = rs.getObjects("Ryu")[0];
      const n = rs.getObjects("Norbu")[0];
      n.ryu.invulnerable = false;
      if (st.avatar) st.avatar.aura.deleteFromScene(rs);
      const aura = R.crear(rs, "Efecto", cx(ryu) - 32, cy(ryu) - 34); efectoAnim(aura, "aura_avatar"); aura.ryu = {}; aura.setZOrder(9000);
      ryu.ryu.avatar = true;
      st.avatar = { t: AJ.avatarDuracion, tic: 0.5, aura: aura };
      R.sonido(rs, "sfx_desbloqueo");
      R.aviso(rs, "¡Estado Avatar!", 2);
    };
    R.actualizarNorbu = function (rs, st, n, dt) {
      const d = n.ryu;
      const vivos = R.jugadores(rs).filter((j) => !j.ryu.derribado);
      if (!vivos.length) return;
      if (d.congeladoHasta > ahora(rs)) return;
      const [obj, dd] = masCercano(n, vivos);
      const dx = cx(obj) - cx(n), dy = cy(obj) - cy(n), l = Math.hypot(dx, dy) || 1;
      d.dir = dirDe(dx, dy);
      if (d.dash > 0) {
        d.dash -= dt; R.mover(rs, n, d.dvx * dt, d.dvy * dt); R.anim(n, "caminar", d.dir); return;
      }
      d.cdRafaga -= dt; d.cdDash -= dt;
      if (d.fase < 3 && d.cdDash <= 0) {
        d.cdDash = AJ.norbu.desplazamiento; d.dash = 0.25;
        const s = Math.random() < 0.5 ? 1 : -1;
        d.dvx = -dy / l * 320 * s; d.dvy = dx / l * 320 * s;
        return;
      }
      if (d.cdRafaga <= 0) {
        d.cdRafaga = AJ.norbu.rafaga;
        R.anim(n, "golpe", d.dir); R.sonido(rs, "sfx_aire");
        for (const a of [-0.25, 0, 0.25]) {
          const ang = Math.atan2(dy, dx) + a;
          R.proyectil(rs, "rafaga_aire", cx(n), cy(n), Math.cos(ang) * 170, Math.sin(ang) * 170, { danio: 8, elem: "aire", duenio: "enemigo" });
        }
        return;
      }
      const ideal = 140;
      const mov = dd > ideal + 20 ? 1 : (dd < ideal - 20 ? -1 : 0);
      if (mov) { R.mover(rs, n, dx / l * 50 * dt * mov, dy / l * 50 * dt * mov); R.anim(n, "caminar", d.dir); }
      else R.anim(n, "reposo", d.dir);
    };

    // ------------------------------------------------------------------ final, créditos y derrota
    E.Final = {
      inicio(rs, st) {
        R.musica(rs, "musica_exploracion");
        const f = R.crear(rs, "Pantalla", 0, 0, "UI"); f.setAnimationName("final"); f.setZOrder(0);
        st.paso = "dialogo";
        st.t = 0.5;
      },
      frame(rs, st, dt) {
        R.actualizarDialogo(rs, dt);
        if (st.t > 0) { st.t -= dt; return; }
        if (st.paso === "dialogo") {
          st.paso = "esperando";
          R.dialogo(rs, D.final, () => { st.paso = "panel"; panelTexto(rs, st, "final", "El ciclo continúa. Pero esta vez, nadie lo carga solo."); });
        } else if (st.paso === "panel") {
          if (actualizarPanelTexto(rs, st, dt)) R.ir(rs, "Creditos");
        }
      },
    };
    const CREDITOS = [
      ["Ryu: El Último Ciclo", true], ["", false], ["Un juego de Ángelo y Nicoll", false], ["Desarrollo de Videojuegos", false],
      ["Profesor: (por completar)", false], ["", false], ["Hecho con GDevelop 5", false],
      ["Arte, música y efectos creados con herramientas propias", false], ["Fuente Press Start 2P (SIL Open Font License)", false],
      ["", false], ["Proyecto académico sin fines comerciales,", false], ["inspirado en el universo de Avatar.", false],
      ["Avatar es propiedad de sus respectivos dueños.", false], ["", false], ["¡Gracias por jugar!", true],
    ];
    E.Creditos = {
      inicio(rs, st) {
        st.lineas = CREDITOS.map(([t, g], i) => R.texto(rs, t, 320, 380 + i * 24, { grande: g, centrado: true, color: g ? "232;210;122" : "244;241;232" }));
        st.t = 0;
      },
      frame(rs, st, dt) {
        st.t += dt;
        for (const o of st.lineas) o.setY(o.getY() - 30 * dt);
        const ultima = st.lineas[st.lineas.length - 1];
        if ((st.t > 1 && R.alguienPulsa(rs, "interactuar")) || ultima.getY() < -20) R.ir(rs, "MenuInicio");
      },
    };
    E.Derrota = {
      inicio(rs, st) {
        R.musica(rs, "");
        R.sonido(rs, "sfx_derribo");
        const f = R.crear(rs, "Pantalla", 0, 0, "UI"); f.setAnimationName("derrota"); f.setZOrder(0);
        menu(rs, st, ["Reintentar", "Menú"], 290, (i) => R.ir(rs, i === 0 ? (str(rs, "escenaDerrota") || "Ciudad") : "MenuInicio"));
      },
      frame(rs, st) { actualizarMenu(rs, st); },
    };
  })();
}
