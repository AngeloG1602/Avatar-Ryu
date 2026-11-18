"""Retratos v3: bustos de 32x32 dibujados a mano (mismo estilo que los sprites), ampliados x2 a 64x64.

Uso: python3 herramientas/retratos_v3.py
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import CONTORNO, a_rgb, fuera_de_paleta
from sprites_v3 import RAIZ, GAO_COLORES
from catalogo_ryu import COLORES as RYU_COL
from jugables_v3 import NEREA_COL


def filas32(seg):
    out = []
    for y in range(32):
        f = ["."] * 32
        for x0, t in seg.get(y, []):
            for i, ch in enumerate(t):
                assert 0 <= x0 + i < 32, (y, x0, t)
                f[x0 + i] = ch
        out.append("".join(f))
    return out


def render32(filas, colores):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = img.load()
    lleno = set()
    for y, f in enumerate(filas):
        for x, ch in enumerate(f):
            if ch != ".":
                px[x, y] = a_rgb(colores[ch]) + (255,)
                lleno.add((x, y))
    for y in range(32):
        for x in range(32):
            if (x, y) not in lleno and any((x + dx, y + dy) in lleno for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = a_rgb(CONTORNO) + (255,)
    assert not fuera_de_paleta(img)
    return img


# ------------------------------------------------------------------ cara común de los chicos
def _cara_chico(cejas_y12, boca, mandibula_ancha=False, cejas_y11="SSEEEESSSSEEEESS"):
    seg = {
        11: [(6, "j"), (7, cejas_y11), (23, "j")],
        12: [(6, "j"), (7, cejas_y12), (23, "j")],
        13: [(5, "SS"), (7, "SSEEEESSSSEEEESS"), (23, "SS")],
        14: [(5, "SK"), (7, "SSWIEWSSSSWEIWSS"), (23, "KS")],
        15: [(5, "SK"), (7, "SSKIIKSSSSKIIKSS"), (23, "KS")],
        16: [(5, "S"), (7, "SSSSSSSKSSSSSSSS"), (23, "S")],
        17: [(7, "KSSSSSSKKSSSSSSK")],
        18: [(7, "KSSSSSSSSSSSSSSK")],
        19: [(7, boca)],
    }
    if mandibula_ancha:
        seg.update({20: [(7, "KSSSSSSSSSSSSSSK")], 21: [(8, "KKSSSSSSSSSSKK")], 22: [(9, "KKKKKKKKKKKK")],
                    23: [(10, "KKKKKKKKKK")]})
    else:
        seg.update({20: [(8, "KSSSSSSSSSSSSK")], 21: [(9, "KKSSSSSSSSKK")], 22: [(10, "KKKKKKKKKK")],
                    23: [(11, "KKKKKKKK")]})
    return seg


# ------------------------------------------------------------------ Ryu
RYU = filas32({
    1: [(11, "H"), (15, "H"), (19, "H")],
    2: [(9, "HH"), (13, "HHH"), (17, "HHH"), (21, "H")],
    3: [(8, "HHHHHHHhHHHHHHH")],
    4: [(7, "HHHhHHHHHHHhHHHH")],
    5: [(6, "HHHHHHHHhHHHHHHHH")],
    6: [(6, "HHHhHHHHHHHHHHhHHH")],
    7: [(6, "HHHHHHHHHHHHHHHHHH")],
    8: [(6, "jHHHHjHHHHHjHHHHHj")],
    9: [(6, "jHSSHHSSHHSSHHSSHj")],
    10: [(6, "jSSSSHSSSSSSSHSSSj")],
    **_cara_chico("SSSSSESSSSESSSSS", "KSSSSSMMMMSSSSSK"),
    24: [(7, "DDDD"), (11, "KSSSSSSK"), (19, "DDDD")],
    25: [(4, "cCCDDDDBBBBBBBBDDDCCCD")],
    26: [(1, "cCCCCCCTBBBBBBBBBBBBTCCCCCCD")],
    27: [(0, "cCCCCCCCTBBBBBBBBBBBBTCCCCCCCD")],
    28: [(0, "cCCCDCCCTBBBBBBBBBBBBTCCCDCCCD")],
    29: [(0, "cCCCDCCCTBBBBBbBBBBBBTCCCDCCCD")],
    30: [(0, "cCCCDCCCTBBBBBBBBBBBBTCCCDCCCD")],
    31: [(0, "TTTTTTTTTBBBBBBBBBBBBTTTTTTTTT")],
})

# ------------------------------------------------------------------ Gao
GAO = filas32({
    0: [(15, "H")],
    1: [(14, "Hh")],
    2: [(13, "HhH")],
    3: [(9, "HHHHHHhHHHHHH")],
    4: [(7, "HHHHHHHHhHHHHHHH")],
    5: [(6, "HHhHHHHHHHHHHhHHH")],
    6: [(6, "HHHHHHHHHHHHHHHHHH")],
    7: [(6, "HHHHHHHHHHHHHHHHHH")],
    8: [(6, "jHHHHHHjHHHHHHHHHj")],
    9: [(6, "jHHSSHHHSSSHHHSSHj")],
    10: [(6, "jHSSSSHSSSSSSHSSSj")],
    **_cara_chico("SSSSSSSSSSSSSSSS", "KSSSSMMMMMMSSSSK", mandibula_ancha=True,
                  cejas_y11="SEEEEESSSSEEEEES"),
    24: [(6, "CCCC"), (10, "KSSSSSSSSK"), (20, "CCCC")],
    25: [(4, "cCCCCCBBBBBBBBBBCCCCCD")],
    26: [(1, "bBBcCCCCCBBBBBBBBBBCCCCCDBBV")],
    27: [(0, "bBBBcCCCCCBBBBBBBBBBCCCCCDBBBV")],
    28: [(0, "bBBBcCCCCCBBBBBBBBBBCCCCCDBBBV")],
    29: [(0, "bBBBcCCCCCBBBBbBBBBBCCCCCDBBBV")],
    30: [(0, "bBBBcCCCCCBBBBBBBBBBCCCCCDBBBV")],
    31: [(0, "bBBBcCCCCCBBBBBBBBBBCCCCCDBBBV")],
})

# ------------------------------------------------------------------ Nerea
_COLA = {y: [(24, "hHj")] for y in range(11, 23)}
_NEREA = {
    1: [(19, "HHH")],
    2: [(10, "HHHHHH"), (17, "XXHhH")],
    3: [(8, "HHHHHHHHHXxHhHH")],
    4: [(7, "HHHHHHHHHHHHHHHH"), (23, "HhH")],
    5: [(6, "HHhhHHHHHHHHHHHHH"), (23, "HhHH")],
    6: [(6, "HHHHhhHHHHHHhhHHH"), (23, "HhHH")],
    7: [(6, "HHHHHHHHjHHHHHHHH"), (23, "HhHH")],
    8: [(6, "HHHHHHHjSjHHHHHHH"), (23, "HhHj")],
    9: [(6, "HHHHHHjSSSjHHHHHH"), (23, "HhHj")],
    10: [(6, "HHHHHjSSSSSjHHHHH"), (23, "HhH")],
    11: [(6, "HHHHjSSSSSSSjHHHH")],
    12: [(6, "HHH"), (9, "SBBBSSSSBBBS"), (21, "HH")],
    13: [(6, "HH"), (8, "EEEEESSSSEEEEE"), (22, "HH")],
    14: [(6, "HH"), (8, "SWIEWSSSSWEIWS"), (22, "HH")],
    15: [(6, "HH"), (8, "SKIIKSSSSKIIKS"), (22, "HH")],
    16: [(6, "HH"), (8, "SUUSSSKSSSSUUS"), (22, "HH")],
    17: [(6, "HH"), (8, "SSSSSSKKSSSSSS"), (22, "HH")],
    18: [(6, "HH"), (8, "KSSSSSSSSSSSSK"), (22, "HH")],
    19: [(6, "HH"), (8, "KSSSSSMMSSSSSK"), (22, "HH")],
    20: [(6, "HHH"), (9, "KSSSSSSSSSSK"), (21, "HHH")],
    21: [(6, "HHHH"), (10, "KKSSSSSSKK"), (20, "HHHH")],
    22: [(7, "HH"), (11, "KKKKKKKK"), (21, "HH")],
    23: [(12, "KSSSSK")],
    24: [(6, "cCCCC"), (11, "KBBBBBBK"), (19, "CCCCD")],
    25: [(3, "cCCCCCCCBBBBBBBBCCCCCCCD")],
    26: [(1, "cCCCCCCCCCBBBBBBBBCCCCCCCCCD")],
    27: [(0, "cCCCcCCCCCBBBBBBBBBBCCCCCDCCCD")],
    28: [(0, "cCCCcCCCCCVBBBBBBBBVCCCCCDCCCD")],
    29: [(0, "cCCCcCCCCCVBBBBBBBBVCCCCCDCCCD")],
    30: [(0, "cCCCcCCCCCVBBBBBBBBVCCCCCDCCCD")],
    31: [(0, "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")],
}
for _y, _s in _COLA.items():
    _NEREA.setdefault(_y, []).append(_s[0])
NEREA = filas32(_NEREA)
NEREA_RET = dict(NEREA_COL)
NEREA_RET["B"] = "#F2F7FA"
NEREA_RET["B_"] = ""
NEREA_RET.pop("B_")
_NEREA_CEJA = dict(NEREA_RET)

RYU_RET = dict(RYU_COL)
RYU_RET.update({"E": "#1A1420"})

# en la cara de Nerea "B" son cejas (castaño), en el cuerpo es el top blanco: se separa por fila
NEREA_FILAS = [f if y != 12 else f.replace("B", "e") for y, f in enumerate(NEREA)]
NEREA_RET["e"] = "#4A3B32"

RETRATOS = {
    "ryu": (RYU, RYU_RET),
    "gao": (GAO, GAO_COLORES),
    "nerea": (NEREA_FILAS, NEREA_RET),
}


# ------------------------------------------------------------------ Tsering
from npcs_v3 import TSERING_COL, NORBU_COL

TSERING = filas32({
    3: [(10, "SssSSSSSSS")],
    4: [(8, "SsSSSSSSSSSSSS")],
    5: [(7, "SSSSSSSSSSSSSSSS")],
    6: [(6, "SSSSSSSSSSSSSSSSSK")],
    7: [(6, "SSSSSSSSSSSSSSSSSK")],
    8: [(6, "KSSSSSSSSSSSSSSSSK")],
    9: [(6, "KSSSSKKKKKKSSSSSSK")],
    10: [(6, "KSSSSSSSSSSSSSSSSK")],
    11: [(6, "K"), (7, "SGGGGGSSSSGGGGGS"), (23, "K")],
    12: [(6, "K"), (7, "GGSGGSSSSSSGGSGG"), (23, "K")],
    13: [(5, "SS"), (7, "SSEEEESSSSEEEESS"), (23, "SS")],
    14: [(5, "SK"), (7, "SSSKKSSSSSSKKSSS"), (23, "KS")],
    15: [(5, "SK"), (7, "SSSSSSSSSSSSSSSS"), (23, "KS")],
    16: [(5, "S"), (7, "SSSSSSSKKSSSSSSS"), (23, "S")],
    17: [(7, "KSSSSSKKKKSSSSSK")],
    18: [(7, "KSGGGGGGGGGGGGSK")],
    19: [(7, "GGGGGGMMMMGGGGGG")],
    20: [(7, "GGGGGGGGGGGGGGGG")],
    21: [(7, "gGGGGGGGGGGGGGGg")],
    22: [(8, "GGGGGGGGGGGGGG")],
    23: [(8, "gGGGGGGGGGGGGg")],
    24: [(5, "CCCC"), (9, "GGGGGGGGGGGG"), (21, "CCCC")],
    25: [(2, "cCCCCCCB"), (10, "gGGGGGGGGg"), (20, "BCCCCCD")],
    26: [(0, "cCCCCCCCBBB"), (11, "gGGGGGGg"), (19, "BBBCCCCCCCD")],
    27: [(0, "cCCCCCCCCBBTT"), (13, "gGGg"), (17, "TTBBCCCCCCCCD")],
    28: [(0, "cCCCDCCCCCBTTT"), (14, "GG"), (16, "TTTBCCCCCDCCCD")],
    29: [(0, "cCCCDCCCCCBTTTTTTTTTBCCCCDCCCD")],
    30: [(0, "cCCCDCCCCCBTTTTTTTTTBCCCCDCCCD")],
    31: [(0, "cCCCDCCCCCBTTTTTTTTTBCCCCDCCCD")],
})

# ------------------------------------------------------------------ Norbu
NORBU = filas32({
    3: [(10, "SssSSSSSSS")],
    4: [(8, "SsSSSSSSSSSSSS")],
    5: [(7, "SSSSSSSSSSSSSSSS")],
    6: [(7, "SSSSSSSSSSSSSSSK")],
    7: [(7, "SSSSSSSSSSSSSSSK")],
    8: [(7, "KSSSSSSSSSSSSSSK")],
    9: [(7, "KSSSSSSSSSSSSSSK")],
    10: [(7, "KSSSSSSSSSSSSSSK")],
    11: [(7, "KSEESSSSSSSSEESK")],
    12: [(7, "KSSSEEESSEEESSSK")],
    13: [(5, "SS"), (7, "SSEEEESSSSEEEESS"), (23, "SS")],
    14: [(5, "SK"), (7, "SSWIEWSSSSWEIWSS"), (23, "KS")],
    15: [(5, "SK"), (7, "SSSKKSSSSSSKKSSS"), (23, "KS")],
    16: [(5, "S"), (7, "SSSSSSSKSSSSSSSS"), (23, "S")],
    17: [(7, "KKSSSSSKKSSSSSKK")],
    18: [(7, "KKSSSSSSSSSSSSKK")],
    19: [(7, "KSSSSSMMMMSSSSSK")],
    20: [(8, "KSSSSSSSSSSSSK")],
    21: [(9, "KKSSSSSSSSKK")],
    22: [(10, "KKKKKKKKKK")],
    23: [(8, "DDD"), (11, "KKKKKKKK"), (19, "DDD")],
    24: [(6, "DDDDD"), (11, "KBBBBBBK"), (19, "DDDDD")],
    25: [(3, "cCCCDDDDBBBBBBBBDDDDCCCD")],
    26: [(1, "cCCCCCCCDTTBBBBBBBBDCCCCCCCD")],
    27: [(0, "cCCCCCCCCDBBTTBBBBBBDCOOCCCCCD")],
    28: [(0, "cCCCCCCCCDBBBBTTBBBBDCOOCCCCCD")],
    29: [(0, "cCCCDCCCCDBBBBBBTTBBDCCCCDCCCD")],
    30: [(0, "cCCCDCCCCDBBBBBBBBTTDCCCCDCCCD")],
    31: [(0, "cCCCDCCCCDBBBBBBBBBBTTCCCDCCCD")],
})

# ------------------------------------------------------------------ Daichi (Avatar anterior)
DAICHI = filas32({
    0: [(13, "HHHH")],
    1: [(12, "HhHHHH")],
    2: [(13, "LLLL")],
    3: [(9, "HHHHHHhHHHHHH")],
    4: [(7, "HHHHHhhHHHHHHHHH")],
    5: [(6, "HHHHHHHHHHHHHhHHH")],
    6: [(6, "HHHHHHHHHHHHHHHHHH")],
    7: [(6, "jHHHHHHHHHHHHHHHHj")],
    8: [(6, "jHHHHHHHHHHHHHHHHj")],
    9: [(6, "jHSSSSHSSSSSSSSSHj")],
    10: [(6, "jSSSSSHSSSSSSSSSSj")],
    **_cara_chico("SSSSSSSSSSSSSSSS", "KSSSSSSMMMSSSSSK"),
    16: [(5, "S"), (7, "SSKKKKSKSSKKKKSS"), (23, "S")],
    24: [(7, "BBBB"), (11, "KSSSSSSK"), (19, "BBBB")],
    25: [(4, "cCCBBBBBBKKKKBBBBBBCCD")],
    26: [(1, "cCCCCCCCBBBBBBBBBBBBCCCCCCCD")],
    27: [(0, "cCCCCCCCCCBBBBBBBBBBCCCCCCCCCD")],
    28: [(0, "cCCCDCCCCCCCCOOOOCCCCCCCCDCCCD")],
    29: [(0, "cCCCDCCCCCCCOOooOOCCCCCCCDCCCD")],
    30: [(0, "cCCCDCCCCCCCOOooOOCCCCCCCDCCCD")],
    31: [(0, "cCCCDCCCCCCCCOOOOCCCCCCCCDCCCD")],
})
DAICHI_COL = {
    "H": "#4A3B32", "h": "#7A5230", "j": "#2B2230", "L": "#C29A5B",
    "S": "#F2C9A0", "s": "#F2C9A0", "K": "#D9A06B",
    "E": "#2B2230", "W": "#F4F1E8", "I": "#6B8E3D", "M": "#A86B3C",
    "C": "#3F5A2A", "c": "#6B8E3D", "D": "#2B2230",
    "B": "#7A5230", "O": "#C29A5B", "o": "#3F5A2A",
}

RETRATOS.update({
    "tsering": (TSERING, TSERING_COL),
    "norbu": (NORBU, NORBU_COL),
    "daichi": (DAICHI, DAICHI_COL),
})


def retrato(nombre):
    filas, col = RETRATOS[nombre]
    return render32(filas, col).resize((64, 64), Image.NEAREST)


if __name__ == "__main__":
    salida = os.path.join(RAIZ, "juego", "assets", "ui")
    nombres = sys.argv[1:] or list(RETRATOS)
    imgs = []
    for n in nombres:
        im = retrato(n)
        im.save(os.path.join(salida, f"retrato_{n}.png"))
        imgs.append(im)
    E = 5
    hoja = Image.new("RGBA", (len(imgs) * (64 * E + 12) + 12, 64 * E + 24), (58, 54, 70, 255))
    for i, im in enumerate(imgs):
        hoja.alpha_composite(im.resize((64 * E, 64 * E), Image.NEAREST), (12 + i * (64 * E + 12), 12))
    hoja.save(os.path.join(RAIZ, "arte_fuente", "previews", "retratos_v3.png"))
    print("ok")
