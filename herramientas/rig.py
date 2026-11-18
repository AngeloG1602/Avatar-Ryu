"""Motor de sprites humanoides 32x32 (vista cenital con inclinación frontal).

Una sola plantilla con parámetros produce a todos los personajes, así el estilo
es idéntico. Direcciones: abajo, arriba, derecha (la izquierda se espeja en GDevelop).
Cada color es una terna (base, luz, sombra) tomada de la paleta oficial.
"""
from PIL import Image
from paleta import CONTORNO, a_rgb

OSCURO = "#2B2230"


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


# ---------------------------------------------------------------- piezas

def _hair(L, ch, d, bob):
    e = ch.get("estilo_pelo")
    pelo = ch["pelo"]
    b = bob
    if e == "calvo":
        return
    if e == "capucha":
        cap = ch["capucha"]
        if d == "abajo":
            L.rect(10, 4 + b, 21, 8 + b, cap)
            L.rect(10, 9 + b, 12, 13 + b, cap)
            L.rect(19, 9 + b, 21, 13 + b, cap)
            L.rect(13, 8 + b, 18, 12 + b, ch["cara"])
            if ch.get("ojos", True):
                L.px(14, 10 + b, ch["ojo_color"]); L.px(17, 10 + b, ch["ojo_color"])
        elif d == "arriba":
            L.rect(10, 4 + b, 21, 13 + b, cap)
        else:
            L.rect(11, 4 + b, 21, 8 + b, cap)
            L.rect(11, 9 + b, 15, 13 + b, cap)
            L.rect(16, 8 + b, 21, 12 + b, ch["cara"])
            L.px(19, 10 + b, ch["ojo_color"])
        return
    if d == "abajo":
        L.rect(11, 5 + b, 20, 7 + b, pelo)
        L.rect(11, 8 + b, 12, 9 + b, pelo)
        L.rect(19, 8 + b, 20, 9 + b, pelo)
        if e == "puntas":
            for x, y in ((12, 4), (13, 4), (15, 3), (15, 4), (16, 3), (16, 4), (18, 4), (19, 4)):
                L.px(x, y + b, pelo[0])
            L.px(15, 3 + b, pelo[1]); L.px(16, 3 + b, pelo[1])
            L.px(13, 8 + b, pelo[0]); L.px(18, 8 + b, pelo[0])
        elif e == "trenza":
            L.rect(11, 10 + b, 12, 12 + b, pelo)
            L.rect(19, 10 + b, 20, 12 + b, pelo)
    elif d == "arriba":
        L.rect(11, 5 + b, 20, 12 + b, pelo)
        if e == "puntas":
            for x, y in ((12, 4), (13, 4), (15, 3), (15, 4), (16, 3), (16, 4), (18, 4), (19, 4)):
                L.px(x, y + b, pelo[0])
        if e == "trenza":
            L.rect(15, 13 + b, 16, 19 + b, pelo)
            L.px(15, 20 + b, ch["trenza_lazo"]); L.px(16, 20 + b, ch["trenza_lazo"])
    else:
        L.rect(12, 5 + b, 21, 7 + b, pelo)
        L.rect(12, 8 + b, 15, 11 + b, pelo)
        if e == "puntas":
            for x, y in ((13, 4), (14, 4), (16, 3), (16, 4), (17, 3), (18, 4), (19, 4)):
                L.px(x, y + b, pelo[0])
            L.px(16, 3 + b, pelo[1]); L.px(17, 3 + b, pelo[1])
            L.px(20, 8 + b, pelo[0])
        elif e == "trenza":
            L.rect(10, 8 + b, 12, 17 + b, pelo)
            L.px(10, 18 + b, ch["trenza_lazo"]); L.px(11, 18 + b, ch["trenza_lazo"])
            L.px(16, 8 + b, pelo[0]); L.px(17, 8 + b, pelo[0])


def _cabeza(L, ch, d, bob, dano=False):
    b = bob
    piel = ch["piel"]
    ex = 1 if dano else 0
    if ch.get("estilo_pelo") == "capucha":
        _hair(L, ch, d, bob)
        return
    if d == "abajo":
        L.rect(11 + ex, 5 + b, 20 + ex, 13 + b, piel)
        _hair(L, ch, d, bob)
        oc = ch["ojo_color"]
        if dano:
            for x in (13, 14, 18, 19):
                L.px(x + ex, 10 + b, oc)
            L.px(16, 12 + b, oc); L.px(17, 12 + b, oc)
        else:
            L.px(13, 10 + b, oc); L.px(18, 10 + b, oc)
            L.px(13, 11 + b, ch.get("mejilla", piel[2])); L.px(18, 11 + b, ch.get("mejilla", piel[2]))
            if ch.get("sonrisa"):
                L.px(15, 12 + b, oc); L.px(16, 12 + b, oc)
        if ch.get("barba"):
            L.rect(12, 12 + b, 19, 13 + b, ch["barba"])
            L.px(15, 12 + b, piel[2]); L.px(16, 12 + b, piel[2])
        if ch.get("mascara"):
            L.rect(11, 11 + b, 20, 13 + b, ch["mascara"])
    elif d == "arriba":
        L.rect(11, 5 + b, 20, 13 + b, piel)
        _hair(L, ch, d, bob)
        if ch.get("estilo_pelo") == "calvo":
            L.px(11, 9 + b, piel[2]); L.px(20, 9 + b, piel[2])
    else:
        L.rect(12, 5 + b, 21, 13 + b, piel)
        L.px(22, 11 + b, piel[0])
        L.px(15, 10 + b, piel[2])
        _hair(L, ch, d, bob)
        oc = ch["ojo_color"]
        if ch.get("estilo_pelo") != "capucha":
            L.px(19, 10 + b, oc)
            if ch.get("sonrisa"):
                L.px(20, 12 + b, oc)
        if ch.get("barba"):
            L.rect(16, 12 + b, 21, 13 + b, ch["barba"])
        if ch.get("mascara"):
            L.rect(16, 11 + b, 22, 13 + b, ch["mascara"])


def _manos(ch, d):
    g = ch.get("guante")
    return g


def _brazo_v(L, ch, x0, x1, y0, y1, manga=None):
    """Brazo vertical de 2 px: manga + mano."""
    manga = manga or ch["manga"]
    L.rect(x0, y0, x1, y1 - 2, manga)
    g = ch.get("guante")
    L.rect(x0, y1 - 1, x1, y1, ch["piel"])
    if g:
        L.rect(x0, y1 - 2, x1, y1 - 2, g)


def dibujar(ch, d, anim, f=0):
    """Devuelve la imagen 32x32 del personaje `ch` (dict) en una pose."""
    if anim == "derribado":
        return _derribado(ch)
    L = Lienzo()
    bob = 0
    legs = (0, 0)       # desplazamiento de y1 de cada pierna
    spread = 0
    arms = (0, 0)       # desplazamientos verticales de los brazos
    dano = anim == "danio"
    if anim == "reposo":
        bob = f % 2
    elif anim == "caminar":
        bob = 1 if f in (1, 3) else 0
        if f == 0:
            legs, arms, spread = (1, -1), (-1, 1), 3
        elif f == 2:
            legs, arms, spread = (-1, 1), (1, -1), -3
    pantalon, zapato = ch["pantalon"], ch["zapato"]
    manga = ch["manga"]
    cuerpo = ch["cuerpo"]
    abrigo = ch.get("abrigo")

    if d in ("abajo", "arriba"):
        # piernas
        for lx0, off in ((12, legs[0]), (17, legs[1])):
            y1 = 27 + off
            L.rect(lx0, 22, lx0 + 2, y1 - 1, pantalon)
            L.rect(lx0, y1 - 1, lx0 + 2, y1, zapato)
        # torso
        ty1 = 21 + bob
        if abrigo:
            L.rect(11, 14 + bob, 20, 25, abrigo)
            L.rect(15, 24, 16, 25, ch["abrigo_corte"])
        else:
            L.rect(11, 14 + bob, 20, ty1, cuerpo)
        # brazos
        la, ra = arms
        if anim == "golpe":
            _brazo_golpe(L, ch, d, f, bob)
            _brazo_v(L, ch, 9, 10, 15 + bob, 20 + bob)
        elif anim == "poder":
            _brazos_poder(L, ch, d, f, bob)
        elif anim == "defensa":
            _brazos_defensa(L, ch, d, bob)
        elif dano:
            _brazo_v(L, ch, 8, 9, 15 + bob, 19 + bob)
            _brazo_v(L, ch, 22, 23, 15 + bob, 19 + bob)
        else:
            _brazo_v(L, ch, 9, 10, 15 + bob + la, 20 + bob + la)
            _brazo_v(L, ch, 21, 22, 15 + bob + ra, 20 + bob + ra)
        # detalles del torso
        _detalles(L, ch, d, bob)
        _cabeza(L, ch, d, bob, dano)
        if ch.get("bufanda"):
            L.rect(11, 13 + bob, 20, 14 + bob, ch["bufanda"])
            if d == "abajo":
                L.rect(18, 15 + bob, 19, 18 + bob, ch["bufanda"])
        if ch.get("cuello"):
            L.rect(11, 13 + bob, 20, 14 + bob, ch["cuello"])
        if ch.get("baston"):
            L.rect(24, 8, 24, 28, ch["baston"])
            L.rect(23, 7, 25, 8, ch["baston_tope"])
    else:  # derecha
        # pierna lejana (sombra) y cercana
        lejana = (pantalon[2], pantalon[2], pantalon[2])
        far_x, near_x = 14 - spread // 2 * 1, 17 + spread // 2
        if spread == 0:
            far_x, near_x = 14, 16
        for lx0, tri, ztri in ((far_x, lejana, zapato[2]), (near_x, pantalon, zapato)):
            L.rect(lx0, 22, lx0 + 2, 25, tri)
            L.rect(lx0, 26, lx0 + 3, 27, ztri if isinstance(ztri, tuple) else (ztri,) * 3)
        if abrigo:
            L.rect(12, 14 + bob, 19, 25, abrigo)
        else:
            L.rect(12, 14 + bob, 19, 21 + bob, cuerpo)
        # brazo cercano
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
            _brazo_v(L, ch, 14 + sw * 2, 16 + sw * 2, 15 + bob, 20 + bob, manga)
        _detalles(L, ch, d, bob)
        _cabeza(L, ch, d, bob, dano)
        if ch.get("bufanda"):
            L.rect(13, 13 + bob, 19, 14 + bob, ch["bufanda"])
            L.rect(11, 14 + bob, 12, 17 + bob, ch["bufanda"])
        if ch.get("cuello"):
            L.rect(13, 13 + bob, 19, 14 + bob, ch["cuello"])
        if ch.get("baston"):
            L.rect(23, 8, 23, 28, ch["baston"])
            L.rect(22, 7, 24, 8, ch["baston_tope"])
    return L.imagen()


def _detalles(L, ch, d, bob):
    b = bob
    if ch.get("cierre") and d != "arriba":
        x = 15 if d == "abajo" else 18
        for y in range(15, 21 if not ch.get("abrigo") else 24):
            L.px(x, y + b, ch["cierre"])
            if d == "abajo":
                L.px(x + 1, y + b, ch["cierre"])
    if ch.get("banda") and d != "arriba":
        if d == "abajo":
            L.rect(9, 17 + b, 10, 18 + b, ch["banda"])
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
        if d == "abajo" or d == "arriba":
            L.rect(11, 20 + b, 20, 20 + b, c)
        else:
            L.rect(12, 20 + b, 19, 20 + b, c)
    if ch.get("frasco") and d != "arriba":
        if d == "abajo":
            L.rect(18, 20 + b, 19, 22 + b, ch["frasco"])
        else:
            L.rect(12, 19 + b, 13, 22 + b, ch["frasco"])
    if ch.get("mochila") and d == "arriba":
        L.rect(12, 15 + b, 19, 20 + b, ch["mochila"])


def _brazo_golpe(L, ch, d, f, b):
    if d == "abajo":
        y0 = (12, 19, 17)[f]
        L.rect(21, y0 + b, 22, y0 + 4 + b + (2 if f == 1 else 0) - 0, ch["manga"])
        yy = y0 + 4 + (2 if f == 1 else 0) + b
        L.rect(21, yy, 22, yy + 1, ch["piel"])
    elif d == "arriba":
        y0 = (17, 7, 13)[f]
        L.rect(21, y0 + b, 22, y0 + 4 + b, ch["manga"])
        L.rect(21, y0 + b, 22, y0 + 1 + b, ch["piel"])
    else:
        if f == 0:
            L.rect(13, 16 + b, 15, 18 + b, ch["manga"])
            L.rect(12, 16 + b, 13, 17 + b, ch["piel"])
        elif f == 1:
            L.rect(17, 16 + b, 23, 17 + b, ch["manga"])
            L.rect(24, 15 + b, 26, 18 + b, ch["piel"])
        else:
            L.rect(17, 16 + b, 21, 17 + b, ch["manga"])
            L.rect(22, 16 + b, 23, 17 + b, ch["piel"])


def _brazos_poder(L, ch, d, f, b):
    if d == "abajo":
        if f == 0:
            L.rect(11, 16 + b, 12, 21 + b, ch["manga"]); L.rect(11, 22 + b, 12, 23 + b, ch["piel"])
            L.rect(19, 16 + b, 20, 21 + b, ch["manga"]); L.rect(19, 22 + b, 20, 23 + b, ch["piel"])
        else:
            L.rect(13, 17 + b, 14, 23 + b, ch["manga"]); L.rect(14, 24 + b, 15, 25 + b, ch["piel"])
            L.rect(17, 17 + b, 18, 23 + b, ch["manga"]); L.rect(16, 24 + b, 17, 25 + b, ch["piel"])
    elif d == "arriba":
        y = 10 if f == 0 else 8
        L.rect(9, y + b, 10, y + 6 + b, ch["manga"]); L.rect(9, y + b, 10, y + 1 + b, ch["piel"])
        L.rect(21, y + b, 22, y + 6 + b, ch["manga"]); L.rect(21, y + b, 22, y + 1 + b, ch["piel"])
    else:
        n = 6 if f == 0 else 8
        L.rect(17, 15 + b, 17 + n, 17 + b, ch["manga"])
        L.rect(18 + n, 15 + b, 20 + n, 17 + b, ch["piel"])


def _brazos_defensa(L, ch, d, b):
    if d == "abajo":
        L.rect(12, 16 + b, 19, 18 + b, ch["manga"])
        L.rect(11, 15 + b, 12, 17 + b, ch["piel"]); L.rect(19, 15 + b, 20, 17 + b, ch["piel"])
    elif d == "arriba":
        L.rect(9, 14 + b, 22, 16 + b, ch["manga"])
    else:
        L.rect(18, 14 + b, 21, 19 + b, ch["manga"])
        L.rect(19, 12 + b, 21, 13 + b, ch["piel"])


def _derribado(ch):
    L = Lienzo()
    piel, pelo = ch["piel"], ch["pelo"]
    pantalon, zapato = ch["pantalon"], ch["zapato"]
    L.rect(22, 20, 28, 24, pantalon)
    L.rect(28, 20, 30, 24, zapato)
    L.rect(11, 19, 22, 25, ch.get("abrigo") or ch["cuerpo"])
    L.rect(11, 17, 17, 18, ch["manga"])
    L.rect(4, 18, 12, 26, piel)
    if ch.get("estilo_pelo") == "capucha":
        L.rect(4, 17, 12, 26, ch["capucha"])
        L.rect(3, 20, 6, 24, ch["cara"])
    elif ch.get("estilo_pelo") != "calvo":
        L.rect(4, 17, 9, 26, pelo)
    L.px(11, 21, ch["ojo_color"]); L.px(11, 22, ch["ojo_color"])
    return L.imagen()
