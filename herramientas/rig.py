"""Motor de sprites humanoides 32x32 v2 (vista cenital con inclinación frontal).

Cabezas dibujadas por plantillas ASCII (rostro + peinado) y cuerpo paramétrico con
más sombreado y detalles de ropa. Direcciones: abajo, arriba, derecha (la izquierda
se espeja en GDevelop). Todos los colores salen de la paleta oficial.
"""
from PIL import Image
from paleta import CONTORNO, a_rgb

OSCURO = "#2B2230"
BLANCO = "#F4F1E8"


class Lienzo:
    def __init__(self):
        self.p = {}

    def px(self, x, y, c):
        if c and 0 <= x < 32 and 0 <= y < 32:
            self.p[(x, y)] = c

    def rect(self, x0, y0, x1, y1, tri):
        if isinstance(tri, str):
            tri = (tri, tri, tri)
        base, luz, sombra = tri
        w, h = x1 - x0 + 1, y1 - y0 + 1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = base
                if h >= 3 and y == y1:
                    c = sombra
                elif h >= 3 and y == y0 and w >= 3:
                    c = luz
                elif w >= 4 and x == x1:
                    c = sombra
                elif w >= 4 and x == x0:
                    c = luz
                self.px(x, y, c)

    def plantilla(self, filas, ox, oy, roles):
        for j, fila in enumerate(filas):
            for i, c in enumerate(fila):
                if c in roles:
                    self.px(ox + i, oy + j, roles[c])

    def imagen(self):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        px = img.load()
        for (x, y), c in self.p.items():
            px[x, y] = a_rgb(c) + (255,)
        borde = []
        for y in range(32):
            for x in range(32):
                if (x, y) in self.p:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if (x + dx, y + dy) in self.p:
                        borde.append((x, y))
                        break
        for x, y in borde:
            px[x, y] = a_rgb(CONTORNO) + (255,)
        return img


# ------------------------------------------------------------ cabezas
# Plantillas de 10 columnas x 11 filas (y = 3..13), origen x = 11.
# Roles: S/s/k piel (base/luz/sombra) · D/L/Z pelo o capucha · E ojo · W blanco ojo
#        B ceja · M boca · C mejilla · N/n/m máscara · G/g/h barba

PIEL = {
    "abajo": [
        "..........",
        ".SSSSSSSS.",
        "SSSSSSSSSS",
        "SSSSSSSSSS",
        "SSSSSSSSSS",
        "kSSSSSSSSk",
        "kSSSSSSSSk",
        "kSSSSSSSSk",
        "SSSSSSSSSS",
        ".SSSSSSSS.",
        "..kkkkkk..",
    ],
    "arriba": [
        "..........",
        ".SSSSSSSS.",
        "SSSSSSSSSS",
        "SSSSSSSSSS",
        "SSSSSSSSSS",
        "SSSSSSSSSS",
        "SSSSSSSSSS",
        "kSSSSSSSSk",
        "SSSSSSSSSS",
        ".SSSSSSSS.",
        "..kkkkkk..",
    ],
    "derecha": [
        "..........",
        ".SSSSSSSS.",
        ".SSSSSSSSS",
        ".SSSSSSSSS",
        ".SSSSSSSSS",
        ".SSSSSSSSS",
        ".SSSSSSSSS",
        ".SSSSSSSSS",
        ".SSSSSSSSS",
        "..SSSSSSS.",
        "...kkkk...",
    ],
}

ROSTRO = {
    "abajo": [
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..BB..BB..",
        "..........",
        "..WE..EW..",
        ".C.E..E.C.",
        "....kk....",
        "..........",
    ],
    "derecha": [
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "......BBB.",
        "...kk.....",
        "...sk.WE.S",
        ".......E.S",
        ".......kk.",
        "..........",
    ],
}
SONRISA = {
    "abajo": {(3, 9): "M", (4, 9): "M", (5, 9): "M", (6, 9): "M", (2, 8): "C", (7, 8): "C"},
    "derecha": {(7, 9): "M", (8, 9): "M", (8, 8): "M"},
}
DANIO = {
    "abajo": [
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..BB..BB..",
        "..........",
        ".EE....EE.",
        "..C....C..",
        "...MMMM...",
        "...MMMM...",
    ],
}

PELO = {
    "puntas": {
        "abajo": [
            "..L..LD.L.",
            ".DDDLDDDD.",
            "DLLDDDLLDD",
            "DDLDDDDLDD",
            "DD.DDDD.DD",
            "Z........Z",
            "Z........Z",
        ],
        "arriba": [
            "..L..LD.L.",
            ".DDDLDDDD.",
            "DLDDDDDLDD",
            "DDDDLDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DZDDDDDDZD",
            ".ZDDDDDDZ.",
            "..ZZZZZZ..",
        ],
        "derecha": [
            "..L.LD.L..",
            ".DDDDLDDD.",
            "DDLDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDD..",
            "DDDD......",
            "DDD.......",
            "DD........",
            "D.........",
        ],
    },
    "corto": {
        "abajo": [
            "..........",
            ".DDDDDDDD.",
            "DLLDDDDDDD",
            "DDDDDDDDDD",
            "DDD....DDD",
            "Z........Z",
            "Z........Z",
        ],
        "arriba": [
            "..........",
            ".DDDDDDDD.",
            "DLLDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DZDDDDDDZD",
            ".ZDDDDDDZ.",
            "..........",
        ],
        "derecha": [
            "..........",
            ".DDDDDDD..",
            "DLLDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDD...",
            "DDDDD.....",
            "DDD.......",
            "DD........",
            "D.........",
        ],
    },
    "trenza": {
        "abajo": [
            "..........",
            ".DDDDDDDD.",
            "DDLLDDDLDD",
            "DDDDDDDDDD",
            "DDDDD...DD",
            "DD......DD",
            "DD......DD",
            "DZ......ZD",
            "DZ......ZD",
            ".Z......Z.",
        ],
        "arriba": [
            "..........",
            ".DDDDDDDD.",
            "DLLDDDLDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DZDDDDDDZD",
            ".ZDDDDDDZ.",
            "..ZZZZZZ..",
        ],
        "derecha": [
            "..........",
            ".DDDDDDD..",
            "DLLDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDD..",
            "DDDDD.....",
            "DDDD......",
            "DDDD......",
            "DDD.......",
            ".DD.......",
        ],
    },
    "calvo": {"abajo": [], "arriba": [], "derecha": []},
    "capucha": {
        "abajo": [
            "..DDDDDD..",
            ".DLLLLDDD.",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDNNNNNNDD",
            "DNNnNNnNND",
            "DNEENNEEND",
            "DNNNNNNNND",
            "DDNNNNNNDD",
            ".DDNNNNDD.",
            "..DDDDDD..",
        ],
        "arriba": [
            "..DDDDDD..",
            ".DLLLLDDD.",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            ".DDDDDDDD.",
            "..ZZZZZZ..",
        ],
        "derecha": [
            "..DDDDDD..",
            ".DLLLLDDD.",
            "DDDDDDDDDD",
            "DDDDDDDDDD",
            "DDDDDDDNN.",
            "DDDDDNNNNN",
            "DDDDDNNEEN",
            "DDDDDNNNNN",
            "DDDDNNNNN.",
            ".DDDDNNNN.",
            "..ZZZZZZ..",
        ],
    },
}
# el pelo (excepto capucha) se pinta desde y=3 (o y=4 si empieza con fila vacía): las plantillas
# empiezan en y=3 y tienen sus propias filas vacías.

BARBA = {
    "abajo": [
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        ".GGg..gGG.",
        ".GGGGGGGG.",
        "..hGGGGh..",
    ],
    "derecha": [
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "......GGG.",
        ".....GGGGG",
        "......hGG.",
    ],
}


def _roles(ch):
    piel = ch["piel"]
    pelo = ch["capucha"] if ch.get("estilo_pelo") == "capucha" else ch["pelo"]
    r = {
        "S": piel[0], "s": piel[1], "k": piel[2],
        "D": pelo[0], "L": pelo[1], "Z": pelo[2],
        "E": ch["ojo_color"], "W": BLANCO, "M": ch["ojo_color"],
        "B": ch.get("ceja", ch["pelo"][2]), "C": piel[2],
    }
    if ch.get("mascara"):
        m = ch["mascara"]
        r.update({"N": m[0], "n": m[1], "m": m[2]})
    if ch.get("barba"):
        b = ch["barba"]
        r.update({"G": b[0], "g": b[1], "h": b[2]})
    return r


def _cabeza(L, ch, d, bob, dano=False):
    b = bob
    r = _roles(ch)
    oy = 3 + b
    cap = ch.get("estilo_pelo") == "capucha"
    if cap:
        # el interior de la capucha cubre toda la cabeza
        L.plantilla(PIEL[d], 11, oy, r)
        L.plantilla(PELO["capucha"][d], 11, oy, r)
        return
    L.plantilla(PIEL[d], 11, oy, r)
    if d != "arriba":
        if dano and d == "abajo":
            L.plantilla(DANIO[d], 11, oy, r)
        else:
            L.plantilla(ROSTRO[d], 11, oy, r)
            if ch.get("sonrisa"):
                for (i, j), rol in SONRISA[d].items():
                    L.px(11 + i, oy + j, r[rol])
    if ch.get("barba") and d != "arriba":
        L.plantilla(BARBA[d], 11, oy, r)
    est = ch.get("estilo_pelo", "corto")
    filas = PELO[est][d]
    # las plantillas de pelo empiezan en la fila y=3 salvo "puntas" arriba, que tienen 7-10 filas
    L.plantilla(filas, 11, oy, r)
    if est == "trenza" and d == "arriba":
        L.rect(15, 13 + b, 16, 19 + b, ch["pelo"])
        L.px(15, 20 + b, ch["trenza_lazo"]); L.px(16, 20 + b, ch["trenza_lazo"])
        L.px(15, 16 + b, ch["pelo"][1]); L.px(16, 18 + b, ch["pelo"][2])
    if est == "trenza" and d == "derecha":
        L.rect(10, 9 + b, 12, 17 + b, ch["pelo"])
        L.px(11, 12 + b, ch["pelo"][1]); L.px(11, 15 + b, ch["pelo"][2])
        L.px(10, 18 + b, ch["trenza_lazo"]); L.px(11, 18 + b, ch["trenza_lazo"])
        L.px(13, 9 + b, ch["pelo"][0])
    if ch.get("ceja_color") and d != "arriba":
        pass


# ------------------------------------------------------------ cuerpo

def _brazo_v(L, ch, x0, x1, y0, y1, manga=None):
    manga = manga or ch["manga"]
    L.rect(x0, y0, x1, y1 - 2, manga)
    if ch.get("puno"):
        L.rect(x0, y1 - 3, x1, y1 - 3, ch["puno"])
    g = ch.get("guante")
    L.rect(x0, y1 - 1, x1, y1, ch["piel"])
    if g:
        L.rect(x0, y1 - 2, x1, y1 - 2, g)


def _torso(L, ch, d, bob, abrigo):
    b = bob
    cuerpo = ch["cuerpo"]
    if d in ("abajo", "arriba"):
        if abrigo:
            L.rect(11, 14 + b, 20, 25, abrigo)
            L.rect(12, 13 + b, 19, 14 + b, abrigo)
            L.rect(15, 23, 16, 25, ch["abrigo_corte"])
            if ch.get("dobladillo"):
                L.rect(11, 25, 20, 25, ch["dobladillo"])
        else:
            L.rect(11, 13 + b, 20, 14 + b, cuerpo)      # hombros
            L.rect(12, 15 + b, 19, 20 + b, cuerpo)
            if ch.get("dobladillo"):
                L.rect(12, 20 + b, 19, 20 + b, ch["dobladillo"])
            L.px(13, 17 + b, cuerpo[2]); L.px(18, 16 + b, cuerpo[2])  # pliegues
        if ch.get("camisa") and d == "abajo":
            L.rect(14, 14 + b, 17, 20 + b if not abrigo else 24, ch["camisa"])
            L.px(14, 14 + b, ch["camisa"][1]); L.px(17, 14 + b, ch["camisa"][1])
    else:
        if abrigo:
            L.rect(12, 14 + b, 19, 25, abrigo)
            if ch.get("dobladillo"):
                L.rect(12, 25, 19, 25, ch["dobladillo"])
        else:
            L.rect(12, 13 + b, 19, 20 + b, cuerpo)
            if ch.get("dobladillo"):
                L.rect(12, 20 + b, 19, 20 + b, ch["dobladillo"])
            L.px(14, 17 + b, cuerpo[2])
        if ch.get("camisa"):
            L.rect(18, 14 + b, 19, 20 + b, ch["camisa"])


def _detalles(L, ch, d, bob):
    b = bob
    if ch.get("cierre") and d == "abajo":
        for y in range(15, 21 if not ch.get("abrigo") else 24):
            L.px(15, y + b, ch["cierre"]); L.px(16, y + b, ch["cierre"])
    if ch.get("cierre") and d == "derecha":
        for y in range(15, 21):
            L.px(18, y + b, ch["cierre"])
    if ch.get("banda") and d != "arriba":
        if d == "abajo":
            L.rect(10, 17 + b, 11, 18 + b, ch["banda"])
        else:
            L.rect(14, 17 + b, 16, 18 + b, ch["banda"])
    if ch.get("simbolo") and d == "abajo":
        s = ch["simbolo"]
        for x, y in ((15, 16), (16, 16), (14, 17), (17, 17), (15, 18), (16, 18)):
            L.px(x, y + b, s)
        L.px(14, 18 + b, ch["cuerpo"][2]); L.px(17, 16 + b, ch["cuerpo"][2])
    if ch.get("simbolo") and d == "derecha":
        L.px(18, 17 + b, ch["simbolo"])
    if ch.get("cinturon"):
        c = ch["cinturon"]
        if d == "derecha":
            L.rect(12, 20 + b, 19, 20 + b, c)
        else:
            L.rect(12, 20 + b, 19, 20 + b, c)
        if ch.get("hebilla") and d == "abajo":
            L.rect(15, 20 + b, 16, 20 + b, ch["hebilla"])
    if ch.get("frasco") and d != "arriba":
        if d == "abajo":
            L.rect(18, 20 + b, 19, 22 + b, ch["frasco"]); L.px(18, 19 + b, ch["pelo"][2])
        else:
            L.rect(12, 19 + b, 13, 22 + b, ch["frasco"])
    if ch.get("mochila") and d == "arriba":
        L.rect(13, 15 + b, 18, 20 + b, ch["mochila"])
    if ch.get("bufanda"):
        if d == "derecha":
            L.rect(13, 13 + b, 19, 14 + b, ch["bufanda"])
            L.rect(11, 14 + b, 12, 18 + b, ch["bufanda"])
        else:
            L.rect(11, 13 + b, 20, 14 + b, ch["bufanda"])
            if d == "abajo":
                L.rect(18, 15 + b, 19, 18 + b, ch["bufanda"])
                L.px(18, 18 + b, ch["bufanda"][2]); L.px(19, 18 + b, ch["bufanda"][2])
    if ch.get("cuello"):
        if d == "derecha":
            L.rect(13, 13 + b, 19, 14 + b, ch["cuello"])
        else:
            L.rect(11, 13 + b, 20, 14 + b, ch["cuello"])
            if d == "arriba":
                L.rect(12, 15 + b, 19, 17 + b, ch["cuello"])


def _piernas(L, ch, d, legs, spread):
    pantalon, zapato = ch["pantalon"], ch["zapato"]
    suela = ch.get("suela", OSCURO)
    if d in ("abajo", "arriba"):
        for lx0, off in ((12, legs[0]), (17, legs[1])):
            y1 = 27 + off
            L.rect(lx0, 21, lx0 + 2, y1 - 2, pantalon)
            L.rect(lx0, y1 - 2, lx0 + 2, y1 - 1, zapato)
            L.rect(lx0, y1, lx0 + 2, y1, suela)
            if ch.get("franja"):
                L.px(lx0, 23, ch["franja"]); L.px(lx0, 24, ch["franja"])
        L.px(15, 21, pantalon[2]); L.px(16, 21, pantalon[2])
    else:
        lejana = (pantalon[2], pantalon[2], pantalon[2])
        far_x, near_x = (14 - spread // 2, 17 + spread // 2) if spread else (14, 16)
        for lx0, tri, ztri in ((far_x, lejana, (zapato[2],) * 3), (near_x, pantalon, zapato)):
            L.rect(lx0, 21, lx0 + 2, 25, tri)
            L.rect(lx0, 26, lx0 + 3, 26, ztri)
            L.rect(lx0, 27, lx0 + 3, 27, suela)
            L.px(lx0 + 3, 26, ztri[1])


def dibujar(ch, d, anim, f=0):
    if anim == "derribado":
        return _derribado(ch)
    L = Lienzo()
    bob = 0
    legs = (0, 0)
    spread = 0
    arms = (0, 0)
    dano = anim == "danio"
    if anim == "reposo":
        bob = f % 2
    elif anim == "caminar":
        bob = 1 if f in (1, 3) else 0
        if f == 0:
            legs, arms, spread = (1, -1), (-1, 1), 3
        elif f == 2:
            legs, arms, spread = (-1, 1), (1, -1), -3
    abrigo = ch.get("abrigo")
    manga = ch["manga"]

    _piernas(L, ch, d, legs, spread)
    _torso(L, ch, d, bob, abrigo)

    if d in ("abajo", "arriba"):
        la, ra = arms
        if anim == "golpe":
            _brazo_golpe(L, ch, d, f, bob)
            _brazo_v(L, ch, 10, 11, 14 + bob, 20 + bob)
        elif anim == "poder":
            _brazos_poder(L, ch, d, f, bob)
        elif anim == "defensa":
            _brazos_defensa(L, ch, d, bob)
        elif dano:
            _brazo_v(L, ch, 8, 9, 14 + bob, 19 + bob)
            _brazo_v(L, ch, 22, 23, 14 + bob, 19 + bob)
        else:
            _brazo_v(L, ch, 10, 11, 14 + bob + la, 20 + bob + la)
            _brazo_v(L, ch, 20, 21, 14 + bob + ra, 20 + bob + ra)
    else:
        if anim == "golpe":
            _brazo_golpe(L, ch, d, f, bob)
        elif anim == "poder":
            _brazos_poder(L, ch, d, f, bob)
        elif anim == "defensa":
            _brazos_defensa(L, ch, d, bob)
        else:
            sw = 1 if (anim == "caminar" and f == 0) else (-1 if anim == "caminar" and f == 2 else 0)
            if dano:
                sw = -1
            _brazo_v(L, ch, 14 + sw * 2, 16 + sw * 2, 14 + bob, 20 + bob, manga)

    _detalles(L, ch, d, bob)
    _cabeza(L, ch, d, bob, dano)
    # detalles que van sobre la cabeza/cuello
    if ch.get("baston"):
        x = 24 if d != "derecha" else 23
        L.rect(x, 8, x, 28, ch["baston"])
        L.rect(x - 1, 6, x + 1, 8, ch["baston_tope"])
    return L.imagen()


def _brazo_golpe(L, ch, d, f, b):
    m, piel = ch["manga"], ch["piel"]
    if d == "abajo":
        if f == 0:
            L.rect(20, 11 + b, 21, 16 + b, m); L.rect(20, 10 + b, 21, 11 + b, piel)
        elif f == 1:
            L.rect(20, 17 + b, 21, 22 + b, m); L.rect(20, 23 + b, 22, 25 + b, piel)
        else:
            L.rect(20, 15 + b, 21, 19 + b, m); L.rect(20, 20 + b, 21, 21 + b, piel)
    elif d == "arriba":
        if f == 0:
            L.rect(20, 15 + b, 21, 20 + b, m); L.rect(20, 21 + b, 21, 22 + b, piel)
        elif f == 1:
            L.rect(20, 9 + b, 21, 14 + b, m); L.rect(20, 5 + b, 22, 8 + b, piel)
        else:
            L.rect(20, 12 + b, 21, 17 + b, m); L.rect(20, 10 + b, 21, 11 + b, piel)
    else:
        if f == 0:
            L.rect(13, 15 + b, 16, 17 + b, m); L.rect(12, 14 + b, 13, 15 + b, piel)
        elif f == 1:
            L.rect(17, 15 + b, 22, 16 + b, m); L.rect(23, 14 + b, 25, 17 + b, piel)
        else:
            L.rect(17, 15 + b, 20, 16 + b, m); L.rect(21, 15 + b, 22, 16 + b, piel)


def _brazos_poder(L, ch, d, f, b):
    m, piel = ch["manga"], ch["piel"]
    if d == "abajo":
        if f == 0:
            L.rect(11, 14 + b, 12, 20 + b, m); L.rect(11, 21 + b, 12, 22 + b, piel)
            L.rect(19, 14 + b, 20, 20 + b, m); L.rect(19, 21 + b, 20, 22 + b, piel)
        else:
            L.rect(12, 15 + b, 13, 21 + b, m); L.rect(13, 22 + b, 15, 23 + b, piel)
            L.rect(18, 15 + b, 19, 21 + b, m); L.rect(16, 22 + b, 18, 23 + b, piel)
    elif d == "arriba":
        y = 9 if f == 0 else 7
        L.rect(9, y + b, 10, y + 6 + b, m); L.rect(9, y - 1 + b, 10, y + b, piel)
        L.rect(21, y + b, 22, y + 6 + b, m); L.rect(21, y - 1 + b, 22, y + b, piel)
    else:
        n = 5 if f == 0 else 7
        L.rect(17, 15 + b, 17 + n, 16 + b, m)
        L.rect(18 + n, 14 + b, 20 + n, 17 + b, piel)


def _brazos_defensa(L, ch, d, b):
    m, piel = ch["manga"], ch["piel"]
    if d == "abajo":
        L.rect(12, 15 + b, 19, 17 + b, m)
        if ch.get("puno"):
            L.rect(12, 17 + b, 19, 17 + b, ch["puno"])
        L.rect(11, 14 + b, 12, 16 + b, piel); L.rect(19, 14 + b, 20, 16 + b, piel)
    elif d == "arriba":
        L.rect(9, 13 + b, 22, 15 + b, m)
    else:
        L.rect(18, 14 + b, 21, 19 + b, m)
        L.rect(19, 12 + b, 21, 13 + b, piel)


def _derribado(ch):
    L = Lienzo()
    piel = ch["piel"]
    pantalon, zapato = ch["pantalon"], ch["zapato"]
    L.rect(22, 20, 28, 24, pantalon)
    L.rect(28, 20, 30, 24, zapato)
    L.rect(12, 19, 22, 25, ch.get("abrigo") or ch["cuerpo"])
    L.rect(12, 16, 18, 18, ch["manga"])
    L.rect(11, 15, 13, 17, piel)
    L.rect(4, 18, 12, 26, piel)
    est = ch.get("estilo_pelo")
    if est == "capucha":
        L.rect(4, 17, 12, 26, ch["capucha"])
        L.rect(3, 20, 6, 24, ch["mascara"])
    elif est != "calvo":
        L.rect(4, 17, 9, 26, ch["pelo"])
        L.rect(5, 17, 9, 18, ch["pelo"][1:] + ch["pelo"][:1])
    L.px(11, 21, ch["ojo_color"]); L.px(11, 22, ch["ojo_color"])
    return L.imagen()
