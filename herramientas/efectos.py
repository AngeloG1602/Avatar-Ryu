"""Efectos de poderes y combate (ver docs/04-ASSETS.md, sección Efectos).

Los proyectiles y la llamarada miran a la DERECHA: en GDevelop se rotan según la dirección.
Salida: juego/assets/efectos/efecto_<nombre>_<cuadro>.png
Uso: python3 herramientas/efectos.py
"""
import math
import os
import random
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import a_rgb, fuera_de_paleta
from tiles_ciudad import Lienzo as _Base, RAIZ

SALIDA = os.path.join(RAIZ, "juego", "assets", "efectos")


class L(_Base):
    def borde(self, color):
        """Contorno de 1 px de un color dado (resplandor/borde del efecto)."""
        lleno = {(x, y) for y in range(self.h) for x in range(self.w) if self.p[x, y][3]}
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in lleno and any((x + dx, y + dy) in lleno for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    self.px(x, y, color)
        return self

    def mancha(self, cx, cy, r, c):
        self.circulo(cx, cy, max(r, 0.6), c)

    def trazo(self, puntos, grosor, c):
        for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
            for i in range(n + 1):
                x = x0 + (x1 - x0) * i / n
                y = y0 + (y1 - y0) * i / n
                self.mancha(x, y, grosor / 2, c)


FUEGO = ["#8E1B1B", "#D9481E", "#F28C28", "#E8D27A", "#F4F1E8"]
AGUA = ["#1E4F8C", "#3A86C8", "#8FD3F0", "#F2F7FA"]
TIERRA = ["#4A3B32", "#7A5230", "#C29A5B", "#E8D27A"]
AIRE = ["#9AA3A8", "#C8C8C0", "#F4F1E8"]


# ================================================================== Ryu
def bola_fuego(f):
    c = L()
    rnd = random.Random(10 + f)
    for i in range(7):
        x = 13 - i * 1.7 + rnd.uniform(-0.6, 0.6)
        y = 16 + math.sin(f * 1.6 + i) * (1 + i * 0.3)
        r = 4.2 - i * 0.5
        c.mancha(x, y, r, FUEGO[1] if i < 4 else FUEGO[0])
        if i < 3:
            c.mancha(x + 0.5, y, r - 1.5, FUEGO[2])
    c.mancha(20, 16, 7, FUEGO[1])
    c.mancha(20.5, 15.5, 5.2, FUEGO[2])
    c.mancha(21, 15, 3.2 + 0.4 * (f % 2), FUEGO[3])
    c.mancha(21.5, 14.5, 1.2, FUEGO[4])
    for _ in range(3):
        c.px(rnd.randrange(14, 29), rnd.randrange(8, 24), FUEGO[3])
    return c.borde(FUEGO[0]).img


def llamarada(f):
    c = L(64, 64)
    largo = (18, 34, 50, 58, 58, 52)[f]
    rnd = random.Random(30 + f)
    for x in range(2, 2 + largo):
        t = (x - 2) / max(largo, 1)
        w = 2 + (x - 2) * 0.42
        for y in range(64):
            dy = abs(y - 32)
            ruido = math.sin(x * 0.55 + f * 1.7) * 2.2 + math.sin(y * 0.9 + x * 0.3 + f) * 1.6
            v = 1 - dy / max(w + ruido, 0.8)
            if v <= 0:
                continue
            if f == 5 and rnd.random() < 0.25:
                continue
            if v > 0.75 and t < 0.75:
                col = FUEGO[4] if t < 0.25 else FUEGO[3]
            elif v > 0.45:
                col = FUEGO[2]
            elif v > 0.15:
                col = FUEGO[1]
            else:
                col = FUEGO[0]
            if t > 0.85 and rnd.random() < 0.4:
                col = FUEGO[0]
            c.px(x, y, col)
    if f >= 4:
        for _ in range(6):
            c.mancha(rnd.randrange(30, 60), rnd.randrange(14, 50), rnd.uniform(1, 2.5), "#5A5566")
    return c.borde("#8E1B1B").img


def rafaga_aire(f):
    c = L()
    for k in range(3):
        ang0 = f * math.pi / 4 + k * 2 * math.pi / 3
        pts = []
        for i in range(14):
            a = ang0 + i * 0.32
            r = 3 + i * 0.75
            pts.append((16 + r * math.cos(a), 16 + r * math.sin(a) * 0.8))
        c.trazo(pts, 2.2 if k == 0 else 1.6, AIRE[2] if k != 2 else AIRE[1])
    for y, x0 in ((10, 1), (16, 0), (22, 2)):
        for x in range(x0 + f % 2, x0 + 6):
            c.px(x, y, AIRE[1])
    return c.borde(AIRE[0]).img


# ================================================================== Nerea
def latigazo_agua(f):
    c = L(64, 64)
    largo = (0.35, 0.7, 1.0, 0.8)[f]
    pts = []
    for i in range(30):
        t = i / 29 * largo
        x = 6 + t * 54
        y = 34 - math.sin(t * math.pi * 1.4 + f * 0.5) * 12 * (1 - t * 0.4)
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        g = 5 - i / len(pts) * 3
        c.mancha(x, y, g / 2 + 0.6, AGUA[1])
    c.trazo(pts, 1.2, AGUA[2])
    for (x, y) in pts[::7]:
        c.px(int(x), int(y) - 1, AGUA[3])
    ex, ey = pts[-1]
    rnd = random.Random(50 + f)
    if f >= 2:
        for _ in range(9):
            a, r = rnd.uniform(-1.4, 1.4), rnd.uniform(4, 11)
            c.mancha(ex + r * math.cos(a), ey + r * math.sin(a), rnd.uniform(0.7, 1.6), AGUA[2] if rnd.random() < .5 else AGUA[1])
    c.mancha(ex, ey, 3, AGUA[2])
    c.mancha(ex + 1, ey - 1, 1.2, AGUA[3])
    return c.borde(AGUA[0]).img


def congelado(f):
    c = L()
    for (cx, cy, h, ang) in ((5, 22, 9, -0.3), (26, 21, 10, 0.3), (9, 8, 6, -0.6), (23, 7, 7, 0.5), (16, 27, 6, 0)):
        dx, dy = math.sin(ang), -math.cos(ang)
        nx, ny = -dy, dx
        pts = [(cx + dx * h, cy + dy * h), (cx + nx * 2.5, cy + ny * 2.5), (cx - dx * 2, cy - dy * 2), (cx - nx * 2.5, cy - ny * 2.5)]
        for y in range(32):
            for x in range(32):
                if _dentro(x + 0.5, y + 0.5, pts):
                    c.px(x, y, AGUA[2])
        c.linea(int(cx), int(cy), int(cx + dx * (h - 2)), int(cy + dy * (h - 2)), AGUA[3])
    for (x, y) in (((14, 3), (29, 13), (3, 14)) if f == 0 else ((18, 2), (30, 26), (1, 6))):
        for d in (-1, 0, 1):
            c.px(x + d, y, "#F2F7FA"); c.px(x, y + d, "#F2F7FA")
    return c.borde(AGUA[0]).img


def _dentro(x, y, pts):
    s = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        s += (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0) > 0
    return s in (0, len(pts))


def curacion(f):
    c = L(64, 64)
    r = (14, 20, 26, 29)[f]
    c.circulo(32, 46, r, AGUA[1], ry=r * 0.38, r_in=0.78)
    c.circulo(32, 46, r - 1, AGUA[2], ry=(r - 1) * 0.38, r_in=0.86)
    rnd = random.Random(70)
    for i in range(10):
        x = 32 + rnd.uniform(-1, 1) * r * 0.9
        y = 46 - rnd.uniform(0, 8) - f * 7 - (i % 3) * 3
        if y < 3:
            continue
        cruz = i % 3 == 0
        col = "#F2F7FA" if i % 2 else AGUA[2]
        c.px(int(x), int(y), col)
        if cruz:
            for d in (-1, 1):
                c.px(int(x) + d, int(y), col); c.px(int(x), int(y) + d, col)
    for i in range(3):
        x = 22 + i * 10
        for y in range(46 - f * 8, 46):
            if (y + i + f) % 3 == 0:
                c.px(x, y, AGUA[2])
    return c.borde(AGUA[0]).img


# ================================================================== Gao
def _roca(c, cx, cy, r, semilla, colores=TIERRA):
    rnd = random.Random(semilla)
    pts = [(cx + math.cos(a) * r * rnd.uniform(0.75, 1.1), cy + math.sin(a) * r * rnd.uniform(0.75, 1.1))
           for a in [k * 2 * math.pi / 7 for k in range(7)]]
    for y in range(int(cy - r - 2), int(cy + r + 2)):
        for x in range(int(cx - r - 2), int(cx + r + 2)):
            if _dentro(x + 0.5, y + 0.5, pts):
                col = colores[1]
                if x + y < cx + cy - r * 0.4:
                    col = colores[2]
                elif x + y > cx + cy + r * 0.5:
                    col = colores[0]
                c.px(x, y, col)
    c.px(int(cx - r * 0.3), int(cy - r * 0.4), colores[3])


def roca(f):
    c = L()
    rnd = random.Random(90 + f)
    if f == 0:
        _roca(c, 17, 16, 8, 3)
        for x in range(2, 8):
            c.px(x, 14 + x % 3, TIERRA[2])
        return c.contorno().img
    n = (4, 6, 7)[f - 1]
    dist = (3, 7, 11)[f - 1]
    for k in range(n):
        a = k * 2 * math.pi / n + 0.3
        _roca(c, 16 + math.cos(a) * dist, 16 + math.sin(a) * dist, (5, 3.5, 2.5)[f - 1], k)
    for _ in range((3, 6, 8)[f - 1]):
        c.mancha(16 + rnd.uniform(-dist, dist), 16 + rnd.uniform(-dist, dist), rnd.uniform(1, 2.5), "#C29A5B")
    return c.contorno().img


def muro_tierra(f):
    c = L(96, 32)
    alto = (9, 19, 28)[f]
    y0 = 31 - alto
    rnd = random.Random(5)
    for fila in range(0, alto, 6):
        off = 6 if (fila // 6) % 2 else 0
        for bx in range(-off, 96, 12):
            col = rnd.choice([TIERRA[1], TIERRA[1], TIERRA[2], "#A86B3C"])
            yy0 = y0 + fila
            for y in range(yy0, min(yy0 + 5, 31)):
                for x in range(max(bx, 1), min(bx + 11, 95)):
                    c.px(x, y, col)
            for x in range(max(bx, 1), min(bx + 11, 95)):
                c.px(x, yy0, TIERRA[3] if col != TIERRA[1] else TIERRA[2])
    for x in range(1, 95):
        if (x * 7) % 5 == 0:
            c.px(x, y0 - 1, TIERRA[1])
    c.rect(1, 30, 94, 31, TIERRA[0])
    if f < 2:
        for _ in range(10):
            c.mancha(rnd.randrange(4, 92), rnd.randrange(y0 - 3, 30), rnd.uniform(1, 2), "#C29A5B")
    return c.contorno().img


def cupula_tierra(f):
    c = L(96, 96)
    altura = (3, 7, 11, 11)[f]
    n = 14
    for k in range(n):
        a = k * 2 * math.pi / n
        x = 48 + math.cos(a) * 42
        y = 52 + math.sin(a) * 30
        h = altura + (k % 3)
        for j in range(int(h)):
            _roca(c, x, y - j, 4.5, k * 3 + j % 2) if j == int(h) - 1 else c.rect(int(x - 3), int(y - j), int(x + 3), int(y - j), TIERRA[1] if j % 3 else TIERRA[0])
    if f == 3:
        c.circulo(48, 52, 40, "#C29A5B", ry=27, r_in=0.97)
    elif f > 0:
        rnd = random.Random(f)
        for _ in range(12):
            a = rnd.uniform(0, 2 * math.pi)
            c.mancha(48 + math.cos(a) * 44, 52 + math.sin(a) * 32, 1.5, "#C29A5B")
    return c.contorno().img


# ================================================================== combate general
def proyectil_soldado(el, f):
    c = L(16, 16)
    if el == "fuego":
        c.mancha(9, 8, 4.5, FUEGO[1]); c.mancha(9.5, 7.5, 3, FUEGO[2]); c.mancha(10, 7, 1.5, FUEGO[3])
        c.mancha(4, 8 + (f * 2 - 1), 1.5, FUEGO[1])
        borde = FUEGO[0]
    elif el == "agua":
        c.mancha(9, 8, 4, AGUA[1]); c.mancha(7, 8, 3, AGUA[1]); c.mancha(4, 8, 1.8, AGUA[1])
        c.mancha(10, 7, 1.6, AGUA[2]); c.px(10 + f, 6, AGUA[3])
        borde = AGUA[0]
    elif el == "tierra":
        _roca(c, 8, 8, 4.5, 7 + f)
        c.px(2, 8 + f, "#C29A5B"); c.px(3, 9 - f, "#C29A5B")
        borde = "#1A1420"
    else:
        pts = [(8 + 4.5 * math.cos(a + f * 1.5), 8 + 4 * math.sin(a + f * 1.5)) for a in [i * 0.5 for i in range(12)]]
        c.trazo(pts, 1.6, AIRE[2]); c.mancha(8, 8, 1.5, AIRE[1])
        borde = AIRE[0]
    return c.borde(borde).img


def impacto(f):
    c = L()
    r = (5, 10, 13)[f]
    for k in range(8):
        a = k * math.pi / 4 + (0.2 if f == 2 else 0)
        largo = r if k % 2 == 0 else r * 0.6
        ini = 0 if f < 2 else r * 0.6
        c.trazo([(16 + math.cos(a) * ini, 16 + math.sin(a) * ini), (16 + math.cos(a) * largo, 16 + math.sin(a) * largo)],
                2 if f < 2 else 1.4, "#F4F1E8" if k % 2 == 0 else "#E8D27A")
    if f < 2:
        c.mancha(16, 16, (3, 4)[f], "#F4F1E8")
    return c.borde("#C9A227").img


def fuego_suelo(f):
    c = L()
    rnd = random.Random(f)
    c.circulo(16, 27, 12, "#8E1B1B", ry=3)
    for i, x in enumerate((7, 12, 16, 20, 25)):
        h = (10, 15, 19, 14, 9)[i] + ((f + i) % 3) * 2 - 2
        sway = math.sin(f * 1.6 + i) * 1.5
        for y in range(27 - h, 28):
            t = (27 - y) / h
            w = 3.2 * (1 - t) + 0.6
            xx = x + sway * t
            for dx in range(-4, 5):
                d = abs(dx + (x - xx))
                if d <= w:
                    col = FUEGO[3] if d < w * 0.35 and t < 0.6 else FUEGO[2] if d < w * 0.7 else FUEGO[1]
                    c.px(int(round(xx + dx)), y, col)
    for _ in range(3):
        c.px(rnd.randrange(6, 26), rnd.randrange(3, 12), FUEGO[3])
    return c.borde(FUEGO[0]).img


# ================================================================== jefe final
def sello(f):
    c = L(96, 96)
    tinta, brillo = "#3B3846", "#E8D27A"
    c.circulo(48, 48, 46, tinta, ry=26, r_in=0.9)
    c.circulo(48, 48, 44, brillo, ry=24.5, r_in=0.95)
    c.circulo(48, 48, 30, brillo, ry=17, r_in=0.9)
    # cuatro marcas girando
    for k in range(4):
        a = k * math.pi / 2 + f * math.pi / 8
        x, y = 48 + math.cos(a) * 37, 48 + math.sin(a) * 21
        c.mancha(x, y, 3.2, tinta)
        c.mancha(x, y, 1.8, ("#D9481E", "#3A86C8", "#6B8E3D", "#F4F1E8")[k])
    # runas en el anillo exterior
    for k in range(16):
        a = k * math.pi / 8 - f * math.pi / 16
        x, y = 48 + math.cos(a) * 41, 48 + math.sin(a) * 23
        c.px(int(x), int(y), tinta if k % 2 else brillo)
    # línea diagonal que parte el círculo
    for i in range(-30, 31):
        x, y = 48 + i, 48 - i * 0.55
        c.px(int(x), int(y), "#8E1B1B"); c.px(int(x), int(y) + 1, "#D9481E" if f % 2 else "#8E1B1B")
    if f % 2:
        c.circulo(48, 48, 12, brillo, ry=7, r_in=0.75)
    return c.img


def aura_avatar(f):
    c = L(64, 64)
    for k in range(12):
        a = k * math.pi / 6 + f * math.pi / 18
        if (k + f) % 2 == 0:
            c.trazo([(32 + math.cos(a) * 26, 34 + math.sin(a) * 18), (32 + math.cos(a + 0.35) * 26, 34 + math.sin(a + 0.35) * 18)],
                    1.4, "#E8D27A")
    for k, (col, borde) in enumerate(((FUEGO[2], FUEGO[0]), (AGUA[1], AGUA[0]), (TIERRA[2], TIERRA[0]), (AIRE[2], AIRE[0]))):
        a = k * math.pi / 2 + f * math.pi / 12
        x, y = 32 + math.cos(a) * 24, 34 + math.sin(a) * 16
        c.mancha(x, y, 4.2, borde)
        c.mancha(x, y, 3.2, col)
        c.px(int(x) - 1, int(y) - 1, "#F4F1E8")
        # estela
        for j in range(1, 4):
            b = a - j * 0.18
            c.mancha(32 + math.cos(b) * 24, 34 + math.sin(b) * 16, 2.2 - j * 0.45, col)
    return c.img


# ================================================================== registro
EFECTOS = {
    "bola_fuego": (bola_fuego, 4),
    "llamarada": (llamarada, 6),
    "rafaga_aire": (rafaga_aire, 4),
    "latigazo_agua": (latigazo_agua, 4),
    "congelado": (congelado, 2),
    "curacion": (curacion, 4),
    "roca": (roca, 4),
    "muro_tierra": (muro_tierra, 3),
    "cupula_tierra": (cupula_tierra, 4),
    "impacto": (impacto, 3),
    "fuego_suelo": (fuego_suelo, 4),
    "sello": (sello, 4),
    "aura_avatar": (aura_avatar, 6),
}
for _el in ("fuego", "agua", "tierra", "aire"):
    EFECTOS["proyectil_soldado_" + _el] = ((lambda e: (lambda f: proyectil_soldado(e, f)))(_el), 2)


def generar():
    os.makedirs(SALIDA, exist_ok=True)
    res = {}
    for n, (fn, k) in EFECTOS.items():
        res[n] = []
        for f in range(k):
            img = fn(f)
            assert not fuera_de_paleta(img), (n, f, fuera_de_paleta(img))
            img.save(os.path.join(SALIDA, f"efecto_{n}_{f}.png"))
            res[n].append(img)
    return res


def hoja(res, escala=3):
    filas = list(res.items())
    alto = sum(max(i.height for i in fr) * escala + 8 for _, fr in filas) + 8
    ancho = max(sum(i.width * escala + 6 for i in fr) for _, fr in filas) + 16
    fondo = Image.open(os.path.join(RAIZ, "juego", "assets", "tilesets", "ciudad", "plaza.png")).convert("RGBA")
    out = Image.new("RGBA", (ancho, alto), a_rgb("#3B3846") + (255,))
    y = 8
    for n, fr in filas:
        x = 8
        h = max(i.height for i in fr)
        for i in fr:
            w = i.width
            # mitad de los cuadros sobre la plaza para ver contraste
            for tx in range(0, w, 32):
                for ty in range(0, i.height, 32):
                    out.alpha_composite(fondo.resize((32 * escala, 32 * escala), Image.NEAREST).crop((0, 0, min(32, w - tx) * escala, min(32, i.height - ty) * escala)),
                                        (x + tx * escala, y + ty * escala))
            out.alpha_composite(i.resize((w * escala, i.height * escala), Image.NEAREST), (x, y))
            x += w * escala + 6
        y += h * escala + 8
    return out


if __name__ == "__main__":
    res = generar()
    print(sum(len(v) for v in res.values()), "cuadros")
    hoja(res).save(os.path.join(RAIZ, "arte_fuente", "previews", "efectos.png"))
