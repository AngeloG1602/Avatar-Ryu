"""Mapas de exploración compuestos con los tiles + datos de colisión y puntos de interés.

Genera:
  juego/assets/mapas/mapa_ciudad.png   (1280x736)
  juego/assets/mapas/mapa_tierra.png   (1280x1472: interior de la mina arriba, exterior abajo)
  herramientas/juego_js/mapas.json     (obstáculos, zonas y puntos que usa la lógica del juego)
Uso: python3 herramientas/mapas.py
"""
import json
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import a_rgb, fuera_de_paleta
from tiles_ciudad import Lienzo, RAIZ, T
import tiles_ciudad as C
import tiles_tierra as TT

SAL = os.path.join(RAIZ, "juego", "assets", "mapas")
DATOS = os.path.join(RAIZ, "herramientas", "juego_js", "mapas.json")


def rect(x0, y0, x1, y1):
    return [int(x0), int(y0), int(x1), int(y1)]


def pegar_plano(img, t, plano, oy=0):
    for y, fila in enumerate(plano):
        for x, n in enumerate(fila):
            if n:
                img.alpha_composite(t[n], (x * T, oy + y * T))


# ================================================================== ciudad
def mapa_ciudad():
    tiles = C.construir()
    t = dict(tiles); t.update(C.GRANDES())
    W, H = 40, 23
    img = Image.new("RGBA", (W * T, H * T), a_rgb("#24222B") + (255,))
    obst, puntos, zonas = [], {}, {}

    alto = ["pared_ventana", "pared", "pared_ventana", "pared_viga"]
    bajo = ["pared_puerta", "pared_tienda", "pared_baja", "pared_viga_baja"]
    plano = []
    for y in range(H):
        fila = []
        for x in range(W):
            hueco = x in (19, 20)
            terr = 12 <= x < 18 or 24 <= x < 30
            if y == 0:
                n = "acera" if hueco else ("cumbrera_terracota" if terr else "cumbrera_roja")
            elif y == 1:
                n = "acera" if hueco else ("techo_terracota" if terr else "techo_rojo")
            elif y == 2:
                n = "acera" if hueco else ("alero_terracota" if terr else "alero_rojo")
            elif y == 3:
                n = "acera" if hueco else ("pared_viga" if x in (18, 21) else ("pared_simbolo" if x == 10 else alto[x % 4]))
            elif y == 4:
                n = "acera" if hueco else ("pared_viga_baja" if x in (18, 21) else bajo[(x * 3) % 4])
            elif y == 5:
                n = "acera" if hueco else "acera_sombra"
            elif y == 6:
                n = ("acera", "acera_b")[x % 2]
            elif y == 7:
                n = "bordillo_s"
            elif y in (8, 10):
                n = "paso_peatonal" if hueco else ("alcantarilla" if (y, x) == (8, 30) else "asfalto")
            elif y == 9:
                n = "paso_peatonal" if hueco else "asfalto_linea"
            elif y == 11:
                n = "bordillo_n"
            elif y in (12, 22):
                n = "pasto" if x in (0, 39) else ("pasto_borde_e" if x == 1 else "pasto_borde_o" if x == 38 else "cenefa_h")
            else:
                if x == 0 or x == 39:
                    n = "pasto_flores" if (x + y) % 3 == 0 else "pasto"
                elif x == 1:
                    n = "pasto_borde_e"
                elif x == 38:
                    n = "pasto_borde_o"
                else:
                    n = ("plaza", "plaza_b", "plaza", "plaza_musgo", "plaza", "plaza_grieta")[(x * 7 + y * 3) % 6]
            fila.append(n)
        plano.append(fila)
    pegar_plano(img, t, plano)
    obst += [rect(0, 0, 19 * T, 5 * T - 4), rect(21 * T, 0, W * T, 5 * T - 4)]

    def obj(n, x, y, caja=None):
        img.alpha_composite(t[n], (x, y))
        if caja:
            obst.append(rect(x + caja[0], y + caja[1], x + caja[2], y + caja[3]))

    for x in (3, 9, 15, 24, 31, 36):
        obj("farolillo", x * T, 4 * T - 6)
    obj("letrero", 6 * T + 2, 3 * T + 6)
    for x in (4, 13, 26, 35):
        obj("maceta", x * T, 5 * T + 2, (8, 22, 24, 30))
    obj("barril", 16 * T, 5 * T + 4, (8, 10, 24, 28)); obj("cajas", 23 * T, 5 * T + 4, (3, 10, 29, 28))
    obj("puesto", 32 * T, 5 * T - 24, (4, 36, 60, 58))
    for x in (5, 14, 25, 34):
        img.alpha_composite(t["farol_arriba"], (x * T, 12 * T)); img.alpha_composite(t["farol_abajo"], (x * T, 13 * T))
        obst.append(rect(x * T + 11, 13 * T + 22, x * T + 21, 13 * T + 31))
    for (x, y) in ((2, 13), (36, 13), (2, 19), (36, 19)):
        obj("arbol", x * T, y * T - 4, (22, 40, 42, 60))
    for (x, y) in ((8, 19), (30, 19), (12, 15), (26, 15)):
        obj("banca", x * T, y * T, (2, 12, 30, 22))
    obj("arbusto", 1 * T, 17 * T, (6, 10, 26, 28)); obj("arbusto", 38 * T, 17 * T, (6, 10, 26, 28))
    # la fuente es un objeto animado del juego: aquí solo se reserva su colisión
    fx, fy = 19 * T, 16 * T - 8
    obst.append(rect(fx + 6, fy + 10, fx + 58, fy + 58))
    puntos.update({
        "inicio": [600, 610], "inicio_gao": [560, 620], "inicio_nerea": [660, 620],
        "fuente": [fx, fy], "simbolo": [10 * T + 16, 5 * T + 20], "entrada_soldados": [624, 8],
        "tsering": [700, 560], "retorno_pelea": [600, 620],
    })
    zonas.update({"salida_norte": rect(19 * T, 0, 21 * T, 24), "plaza": rect(3 * T, 13 * T, 37 * T, 21 * T)})
    fuego = [[x * T, y * T] for (x, y) in ((6, 14), (10, 17), (15, 13), (23, 14), (28, 18), (33, 15), (17, 20), (21, 19), (8, 21), (31, 21))]
    return img, {"ancho": W * T, "alto": H * T, "obstaculos": obst, "puntos": puntos, "zonas": zonas,
                 "limites": rect(0, 0, W * T, H * T), "fuego": fuego}


# ================================================================== zona de tierra
def roca_oscura():
    L = Lienzo(fondo="#24222B")
    import random
    rnd = random.Random(5)
    for _ in range(14):
        L.px(rnd.randrange(32), rnd.randrange(32), "#2B2230")
    for _ in range(4):
        L.px(rnd.randrange(32), rnd.randrange(32), "#3B3846")
    return L.img


def mapa_tierra():
    tiles = TT.construir()
    t = dict(tiles); t.update(TT.objetos()); t["roca_oscura"] = roca_oscura()
    W, H = 40, 46
    img = Image.new("RGBA", (W * T, H * T), a_rgb("#24222B") + (255,))
    obst, puntos, zonas = [], {}, {}
    plano = [[None] * W for _ in range(H)]
    # ---------------- interior (filas 0-21, columnas 8-31)
    for y in range(22):
        for x in range(W):
            if x < 8 or x > 31:
                plano[y][x] = "roca_oscura"; continue
            hueco = x in (19, 20)
            if y == 0:
                n = "mina_pared_borde"
            elif y == 1:
                n = "camara_emblema" if x in (19, 20) else "camara_pared"
            elif 2 <= y <= 6:
                n = "camara_suelo" if 14 <= x <= 25 else "roca_oscura"
            elif y == 7:
                n = "camara_suelo" if hueco else "mina_pared_borde"
            elif y == 8:
                n = "camara_suelo" if hueco else ("mina_viga" if x % 6 == 2 else "mina_pared")
            elif 9 <= y <= 13:
                n = "rieles_h" if y == 11 else ("mina_suelo", "mina_suelo_b")[(x + y) % 2]
                if y == 9:
                    n = "mina_base" if not hueco else "mina_suelo"
            elif y == 14:
                n = "mina_suelo" if hueco else "mina_pared_borde"
            elif y == 15:
                n = "mina_suelo" if hueco else ("mina_viga" if x % 6 == 2 else "mina_pared")
            else:
                n = "rieles_v" if x == 13 and y < 21 else ("mina_suelo", "mina_suelo_b")[(x * 3 + y) % 2]
                if y == 16:
                    n = "mina_base" if not hueco else "mina_suelo"
                if y == 21 and 18 <= x <= 21:
                    n = "sendero"
            plano[y][x] = n
    # ---------------- exterior (filas 22-45)
    for y in range(22, H):
        for x in range(W):
            if y == 22:
                n = "acantilado_borde"
            elif y in (23, 24):
                n = "acantilado" if (x + y) % 3 else "acantilado_b"
            elif y == 25:
                n = "acantilado_base"
            else:
                if 17 <= x <= 22:
                    n = "sendero_b" if (x * 5 + y) % 4 == 0 else "sendero"
                elif x == 16:
                    n = "sendero_borde_e"
                elif x == 23:
                    n = "sendero_borde_o"
                else:
                    n = "pasto_monte"
            plano[y][x] = n
    pegar_plano(img, t, plano)

    def obj(n, x, y, caja=None):
        img.alpha_composite(t[n], (x, y))
        if caja:
            obst.append(rect(x + caja[0], y + caja[1], x + caja[2], y + caja[3]))

    # interior: lámparas, vagoneta, piedras
    for x in (10, 16, 24, 29):
        obj("lampara_mina", x * T, 8 * T + 4)
        obj("lampara_mina", x * T, 15 * T + 4)
    obj("vagoneta", 26 * T, 11 * T - 6, (3, 12, 29, 28))
    obj("piedras", 9 * T, 18 * T, (6, 16, 26, 30)); obj("piedras", 29 * T, 19 * T, (6, 16, 26, 30))
    # exterior: entrada de la mina, pinos y rocas
    img.alpha_composite(t["entrada_mina"], (18 * T - 16, 23 * T))
    for (x, y) in ((3, 28), (9, 31), (5, 37), (12, 41), (27, 29), (33, 33), (30, 39), (36, 43), (1, 43)):
        obj("pino", x * T, y * T, (24, 44, 40, 60))
    for (x, y) in ((14, 30), (25, 36), (7, 34), (31, 27)):
        obj("roca_grande", x * T, y * T, (4, 10, 28, 28))
    for (x, y) in ((24, 31), (15, 39), (10, 27), (34, 41)):
        obj("arbusto_seco", x * T, y * T)

    # obstáculos fijos
    obst += [rect(0, 0, 8 * T, 22 * T), rect(32 * T, 0, W * T, 22 * T), rect(8 * T, 0, 32 * T, 2 * T - 4),
             rect(8 * T, 2 * T, 14 * T, 7 * T), rect(26 * T, 2 * T, 32 * T, 7 * T),
             rect(8 * T, 7 * T, 19 * T, 9 * T + 8), rect(21 * T, 7 * T, 32 * T, 9 * T + 8),
             rect(8 * T, 14 * T, 19 * T, 16 * T + 8), rect(21 * T, 14 * T, 32 * T, 16 * T + 8),
             rect(0, 22 * T, W * T, 25 * T + 16)]
    puntos.update({
        "inicio_exterior": [624, 1390], "salida_mina_exterior": [624, 860], "inicio_interior": [624, 640],
        "puerta1": [19 * T, 14 * T], "puerta2": [19 * T, 7 * T], "documento": [11 * T, 12 * T],
        "diario": [19 * T + 16, 4 * T], "emblema": [624, 76], "norbu": [624, 980], "tsering": [680, 1400],
        "retorno_tierra1": [624, 1180], "retorno_tierra2": [24 * T, 12 * T],
    })
    zonas.update({
        "entrada_mina": rect(18 * T, 25 * T + 10, 22 * T, 26 * T + 10),
        "salida_mina": rect(18 * T, 21 * T + 12, 22 * T, 22 * T),
        "encuentro_tierra1": rect(16 * T, 33 * T, 24 * T, 35 * T),
        "encuentro_tierra2": rect(22 * T, 10 * T, 30 * T, 13 * T),
        "salida_sur": rect(0, H * T - 16, W * T, H * T),
    })
    limites = {"interior": rect(8 * T, 0, 32 * T, 22 * T), "exterior": rect(0, 22 * T, W * T, H * T)}
    return img, {"ancho": W * T, "alto": H * T, "obstaculos": obst, "puntos": puntos, "zonas": zonas, "limites": limites}


# ================================================================== arenas de pelea
ARENAS = {
    "plaza": {"limites": rect(16, 124, 624, 352)},
    "canon": {"limites": rect(36, 90, 604, 352)},
    "mina": {"limites": rect(20, 104, 620, 352)},
    "arena": {"limites": rect(70, 72, 570, 300)},
}


if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True)
    os.makedirs(os.path.dirname(DATOS), exist_ok=True)
    datos = {"arenas": ARENAS}
    for nombre, fn in (("ciudad", mapa_ciudad), ("tierra", mapa_tierra)):
        img, d = fn()
        assert not fuera_de_paleta(img), (nombre, fuera_de_paleta(img))
        img.save(os.path.join(SAL, f"mapa_{nombre}.png"))
        datos[nombre] = d
        prev = img.copy()
        L = Lienzo.de(prev)
        for r in d["obstaculos"]:
            for x in range(r[0], r[2]):
                for y in (r[1], r[3] - 1):
                    L.px(x, y, "#D9481E")
            for y in range(r[1], r[3]):
                for x in (r[0], r[2] - 1):
                    L.px(x, y, "#D9481E")
        for r in d["zonas"].values():
            for x in range(r[0], r[2]):
                for y in (r[1], r[3] - 1):
                    L.px(x, y, "#3A86C8")
        L.img.save(os.path.join(RAIZ, "arte_fuente", "previews", f"mapa_{nombre}_colisiones.png"))
    with open(DATOS, "w") as fh:
        json.dump(datos, fh, indent=1)
    print("ok")
