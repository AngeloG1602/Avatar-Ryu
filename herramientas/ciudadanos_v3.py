"""Ciudadanos de la ciudad en estilo v3 (solo reposo y caminar de frente, según docs/04-ASSETS.md).

Uso: python3 herramientas/ciudadanos_v3.py
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from sprites_v3 import filas, RAIZ
import jugables_v3 as J

# ------------------------------------------------------------------ A: vendedor con bigote y delantal
CIUDADANO_A = filas({
    3: [(6, "HHHHHHHH")],
    4: [(4, "HHHHhHHHHHHH")],
    5: [(3, "HHHHHHHHhHHHHH")],
    6: [(3, "HHHHHHHHHHHHHH")],
    7: [(3, "jHHHHHHHHHHHHj")],
    8: [(3, "jHHHHHHHHHHHHj")],
    9: [(3, "jSSSSSSHHHHHSj")],
    10: [(3, "jSSSSSSSSSSSSj")],
    11: [(3, "KSEEESSSSEEESK")],
    12: [(3, "KSSSSSSSSSSSSK")],
    13: [(3, "KSSEESSSSEESSK")],
    14: [(3, "KSSIESSSSEISSK")],
    15: [(3, "KSSSSSSKSSSSSK")],
    16: [(3, "KSSSHHHHHHSSSK")],
    17: [(4, "KKSSSMMSSSKK")],
    18: [(5, "KKKKKKKKKK")],
    19: [(2, "cCCCCBBBBBBCCCCD")],
    20: [(2, "cDCCBBBBBBBBCCDD")],
    21: [(2, "cDCCBBBBBBBBCCDD")],
    22: [(2, "cDCCBBBVBBBBCCDD")],
    23: [(2, "SSPPBBBBBBBBPPKK")],
    24: [(4, "PPBBBBBBBBPP")],
    25: [(4, "pPPPPQQPPPPQ")],
    26: [(5, "pPPP"), (11, "pPPQ")],
    27: [(5, "pPPP"), (11, "pPPQ")],
    28: [(5, "ZZZZ"), (11, "ZZZZ")],
    29: [(5, "zZZZ"), (11, "zZZZ")],
    30: [(5, "XXXX"), (11, "XXXX")],
})
COL_A = {
    "H": "#4A3B32", "h": "#7A5230", "j": "#2B2230",
    "S": "#F2C9A0", "K": "#D9A06B", "E": "#2B2230", "I": "#4A3B32", "M": "#A86B3C", "W": "#F4F1E8",
    "C": "#C9A227", "c": "#E8D27A", "D": "#7A5230",
    "B": "#F4F1E8", "V": "#C8C8C0",
    "P": "#3B3846", "p": "#5A5566", "Q": "#24222B",
    "Z": "#4A3B32", "z": "#7A5230", "X": "#2B2230",
}

# ------------------------------------------------------------------ B: mujer con moño, chal y falda larga
CIUDADANO_B = filas({
    2: [(8, "HHHH")],
    3: [(8, "HhHH")],
    4: [(5, "HHHHHHHHHH")],
    5: [(4, "HHhhHHHHHHHH")],
    6: [(3, "HHHHHHHHHHHHHH")],
    7: [(3, "HHHHHHHHHHHHHH")],
    8: [(3, "HHHHHHjjHHHHHH")],
    9: [(3, "HHHSSSSSSSSHHH")],
    10: [(3, "HHSSSSSSSSSSHH")],
    11: [(3, "HSSeeSSSSeeSSH")],
    12: [(3, "HSEEESSSSEEESH")],
    13: [(3, "HSSIESSSSEISSH")],
    14: [(3, "KSUSSSSKSSSUSK")],
    15: [(3, "KSSSSSMMSSSSSK")],
    16: [(4, "KKSSSSSSSSKK")],
    17: [(7, "KKKKKK")],
    18: [(3, "oOOOOCCCCOOOOO")],
    19: [(2, "oOOOOCCCCCCOOOOO")],
    20: [(2, "oODOCCCCCCCCOODO")],
    21: [(2, "oODCCCCCCCCCCODO")],
    22: [(2, "SSDTTTTTTTTTTDKK")],
    23: [(4, "RRRRRRRRRRRR")],
    24: [(4, "rRRRRRRRRRRR")],
    25: [(4, "rRRRRRfRRRRR")],
    26: [(3, "rRRRRRRfRRRRRR")],
    27: [(3, "rRRRRRRfRRRRRR")],
    28: [(3, "TTTTTTTTTTTTTT")],
    29: [(5, "ZZZ"), (12, "ZZZ")],
})
COL_B = {
    "H": "#2B2230", "h": "#4A3B32", "j": "#1A1420",
    "S": "#D9A06B", "K": "#A86B3C", "U": "#A86B3C", "e": "#2B2230",
    "E": "#2B2230", "I": "#4A3B32", "M": "#8E1B1B", "W": "#F4F1E8",
    "O": "#F28C28", "o": "#E8D27A", "D": "#D9481E",
    "C": "#8E1B1B", "T": "#C9A227",
    "R": "#2B2230", "r": "#4A3B32", "f": "#1A1420", "Z": "#C9A227", "Q": "#7A5230",
}

# ------------------------------------------------------------------ C: chico con gorra y camiseta
CIUDADANO_C = filas({
    3: [(6, "RRRRRRRR")],
    4: [(4, "RrRRRRRRRRRR")],
    5: [(3, "RRRrRRRRRRRRRR")],
    6: [(3, "RRRRRRRRRRRRRR")],
    7: [(3, "HddddddddddddH")],
    8: [(3, "HHSHHSHHSHHSHH")],
    9: [(3, "HSSSSSSSSSSSSH")],
    10: [(3, "KSSSSSSSSSSSSK")],
    11: [(3, "KSeeeSSSSeeeSK")],
    12: [(3, "KSSSSSSSSSSSSK")],
    13: [(3, "KSSEESSSSEESSK")],
    14: [(3, "KSSIESSSSEISSK")],
    15: [(3, "KSSSSSSKSSSSSK")],
    16: [(3, "KSSSSMMMSSSSSK")],
    17: [(4, "KKSSSSSSSSKK")],
    18: [(5, "KKKKKKKKKK")],
    19: [(2, "cCCCCCCCCCCCCCCD")],
    20: [(2, "cDCCCCCOOCCCCCDD")],
    21: [(2, "SKCCCCCOOCCCCCSK")],
    22: [(2, "SKCCCCCCCCCCCCSK")],
    23: [(2, "SSPPPPPPPPPPPPKK")],
    24: [(4, "PPPPPPPPPPPP")],
    25: [(4, "pPPPPQQPPPPQ")],
    26: [(5, "pPPP"), (11, "pPPQ")],
    27: [(5, "pPPP"), (11, "pPPQ")],
    28: [(5, "ZZZZ"), (11, "ZZZZ")],
    29: [(5, "zZZZ"), (11, "zZZZ")],
    30: [(5, "XXXX"), (11, "XXXX")],
})
COL_C = {
    "R": "#D9481E", "r": "#F28C28", "d": "#8E1B1B",
    "H": "#2B2230", "j": "#24222B",
    "S": "#F2C9A0", "K": "#D9A06B", "e": "#2B2230", "E": "#2B2230", "I": "#4A3B32",
    "M": "#A86B3C", "W": "#F4F1E8",
    "C": "#3A86C8", "c": "#8FD3F0", "D": "#1E4F8C", "O": "#F4F1E8",
    "P": "#24222B", "p": "#3B3846", "Q": "#1A1420",
    "Z": "#F4F1E8", "z": "#F4F1E8", "X": "#D9481E",
}

CIUDADANOS = {
    "ciudadano_a": (CIUDADANO_A, COL_A, ((2, 3), (16, 17), (20, 23)), 26),
    "ciudadano_b": (CIUDADANO_B, COL_B, ((2, 3), (16, 17), (19, 22)), 29),
    "ciudadano_c": (CIUDADANO_C, COL_C, ((2, 3), (16, 17), (19, 23)), 26),
}
for _n, (_pose, _col, _br, _pi) in CIUDADANOS.items():
    J.JUGABLES[_n] = dict(poses={"abajo": _pose}, colores=_col, manga="C", mano="S",
                          brazos={"abajo": _br}, piernas={"abajo": _pi})


def generar(nombre, guardar=True):
    salida = os.path.join(RAIZ, "juego", "assets", "personajes")
    res = {}
    for anim, n in (("reposo", 2), ("caminar", 4)):
        for f in range(n):
            img = J.cuadro(nombre, "abajo", anim, f)
            res[(anim, f)] = img
            if guardar:
                img.save(os.path.join(salida, f"{nombre}_{anim}_abajo_{f}.png"))
    return res


if __name__ == "__main__":
    E = 8
    out = Image.new("RGBA", (3 * (32 * E + 8) + 8, 2 * (32 * E + 8) + 8), (58, 54, 70, 255))
    for i, n in enumerate(CIUDADANOS):
        r = generar(n)
        print(n, len(r), "cuadros")
        out.alpha_composite(r[("reposo", 0)].resize((32 * E, 32 * E), Image.NEAREST), (8 + i * (32 * E + 8), 8))
        out.alpha_composite(r[("caminar", 0)].resize((32 * E, 32 * E), Image.NEAREST), (8 + i * (32 * E + 8), 16 + 32 * E))
    out.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_ciudadanos.png"))
