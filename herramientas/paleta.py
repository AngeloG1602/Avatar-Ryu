"""Paleta oficial de Ryu: El Último Ciclo (ver docs/04-ASSETS.md)."""
from PIL import Image

CONTORNO = "#1A1420"

PALETA = {
    "fuego": ["#8E1B1B", "#D9481E", "#F28C28", "#C9A227"],
    "agua": ["#1E4F8C", "#3A86C8", "#8FD3F0", "#F2F7FA"],
    "tierra": ["#3F5A2A", "#6B8E3D", "#7A5230", "#C29A5B"],
    "aire": ["#F4F1E8", "#C8C8C0", "#E8D27A", "#9AA3A8"],
    "ciclo": ["#24222B", "#3B3846", "#5A5566"],
    "piel": ["#F2C9A0", "#D9A06B", "#A86B3C", "#6E4426"],
    "oscuros": ["#2B2230", "#4A3B32"],
    "contorno": [CONTORNO],
}

TODOS = sorted({c.upper() for g in PALETA.values() for c in g})


def a_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


RGB_TODOS = [a_rgb(c) for c in TODOS]


def mas_cercano(rgb):
    return min(RGB_TODOS, key=lambda p: sum((a - b) ** 2 for a, b in zip(p, rgb)))


def ajustar_a_paleta(img):
    """Ajusta cada píxel opaco al color más cercano de la paleta (alfa binario)."""
    img = img.convert("RGBA")
    px = img.load()
    cache = {}
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a < 128:
                px[x, y] = (0, 0, 0, 0)
                continue
            k = (r, g, b)
            if k not in cache:
                cache[k] = mas_cercano(k)
            px[x, y] = cache[k] + (255,)
    return img


def fuera_de_paleta(img):
    """Devuelve los colores opacos de la imagen que no están en la paleta."""
    img = img.convert("RGBA")
    malos = set()
    for r, g, b, a in img.getdata():
        if a and (r, g, b) not in RGB_TODOS:
            malos.add("#%02X%02X%02X" % (r, g, b))
    return malos
