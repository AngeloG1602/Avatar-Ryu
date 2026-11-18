"""Catálogo de peinados para Ryu sobre una cara con la estructura de Gao."""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_v3 import filas, render, RYU_COLORES, _RYU_CARA_CUERPO, RAIZ

CARA = {
    11: [(3, "jSEEESSSSEEESj")],
    12: [(3, "KSSSSSSSSSSSSK")],
    13: [(3, "KSSEESSSSEESSK")],
    14: [(3, "KSSIESSSSEISSK")],
    15: [(3, "KSSSSSSKSSSSSK")],
    16: [(3, "KSSSSMMMSSSSSK")],
    17: [(4, "KKSSSSSSSSKK")],
    18: [(5, "KKKKKKKKKK")],
}
CUERPO = {k: v for k, v in _RYU_CARA_CUERPO.items() if k >= 19}

PEINADOS = {
    "1 Erizo": {
        1: [(5, "H"), (8, "H"), (11, "H"), (14, "H")],
        2: [(4, "HH"), (7, "HH"), (10, "HH"), (13, "HH")],
        3: [(4, "HHhHHhHHhHHH")],
        4: [(3, "HHHHHHHHHHHHHH")],
        5: [(3, "HHhHHHHHHhHHHH")],
        6: [(3, "HHHHHHHHHHHHHH")],
        7: [(3, "jHHHHHHHHHHHHj")],
        8: [(3, "jHHHHHHHHHHHHj")],
        9: [(3, "jHSSSSSSSSSSHj")],
        10: [(3, "jSSSSSSSSSSSSj")],
    },
    "2 Tupe": {
        2: [(7, "HHHHH")],
        3: [(5, "HHHhhHHHH")],
        4: [(4, "HHHHhhHHHHHH")],
        5: [(4, "HHHHHHHhHHHH")],
        6: [(3, "jHHHHHHHHHHHHj")],
        7: [(3, "jjHHHHHHHHHHjj")],
        8: [(3, "jjSHHHHHHHHSjj")],
        9: [(3, "jSSSSSSSSSSSSj")],
        10: [(3, "jSSSSSSSSSSSSj")],
    },
    "3 Flequillo": {
        3: [(6, "HHHHHHHH")],
        4: [(4, "HHHHhHHHhHHH")],
        5: [(3, "HHHhHHHHHHhHHH")],
        6: [(3, "HHHHHHHHHHHHHH")],
        7: [(3, "jHHHHHHHHHHHHj")],
        8: [(3, "jHHHjHHHjHHHHj")],
        9: [(3, "jSHHSHHSSHHSHj")],
        10: [(3, "jSSHSSSSSSHSSj")],
    },
    "4 Mono": {
        1: [(8, "HHHH")],
        2: [(8, "HhHH")],
        3: [(8, "RRRR")],
        4: [(5, "HHHHhhHHHH")],
        5: [(4, "HHHHHHhhHHHH")],
        6: [(3, "HHHHHHHHHHHHHH")],
        7: [(3, "jHHHHHHHHHHHHj")],
        8: [(3, "jHHHHHHHHHHHHj")],
        9: [(3, "jHSSSSSSSSSSHj")],
        10: [(3, "jHSSSSSSSSSSHj")],
    },
    "5 De lado": {
        3: [(5, "HHHHHHHHH")],
        4: [(4, "HHHhhHHHHHHH")],
        5: [(3, "HHHHHHhhHHHHHH")],
        6: [(3, "HHHHHHHHHHHHHH")],
        7: [(3, "jHHHHHHHHHHHHHH")],
        8: [(3, "jSSHHHHHHHHHHH")],
        9: [(3, "jSSSSHHHHHHHHj")],
        10: [(3, "jSSSSSSSHHHHSj")],
    },
    "6 Rapado": {
        4: [(5, "HHHHHHHHHH")],
        5: [(4, "HHHHHHHHHHHH")],
        6: [(3, "HjHHjHHjHHjHHH")],
        7: [(3, "HHHHHHHHHHHHHH")],
        8: [(3, "jSSSSSSSSSSSSj")],
        9: [(3, "KSSSSSSSSSSSSK")],
        10: [(3, "KSSSSSSSSSSSSK")],
    },
}

COLORES = dict(RYU_COLORES)
COLORES.update({"H": "#2B2230", "h": "#4A3B32", "g": "#4A3B32", "j": "#24222B",
                "I": "#7A5230", "M": "#A86B3C", "R": "#D9481E"})

if __name__ == "__main__":
    E = 8
    nombres = list(PEINADOS)
    celda = 32 * E
    hoja = Image.new("RGBA", (3 * (celda + 10) + 10, 2 * (celda + 34) + 10), (58, 54, 70, 255))
    d = ImageDraw.Draw(hoja)
    for i, n in enumerate(nombres):
        img = render(filas({**PEINADOS[n], **CARA, **CUERPO}), COLORES)
        x = 10 + (i % 3) * (celda + 10)
        y = 10 + (i // 3) * (celda + 34)
        hoja.alpha_composite(img.resize((celda, celda), Image.NEAREST), (x, y + 24))
        d.text((x + 8, y + 4), n, fill=(244, 241, 232, 255))
    ruta = os.path.join(RAIZ, "arte_fuente", "previews", "catalogo_peinados_ryu.png")
    hoja.save(ruta)
    print(ruta)
