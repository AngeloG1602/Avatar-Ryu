"""Tsering, Norbu y soldados en estilo v3 (plantillas a mano + animaciones derivadas).

Uso: python3 herramientas/npcs_v3.py
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from sprites_v3 import filas, RAIZ
import jugables_v3 as J


def bajar(segmentos, dy):
    return {y + dy: v for y, v in segmentos.items()}


# ================================================================== Tsering
_BASTON = {y: [(18, "L")] for y in range(6, 31)}
_BASTON.update({4: [(17, "OOO")], 5: [(17, "OlO")]})


def _con_baston(seg, x=18):
    out = {k: list(v) for k, v in seg.items()}
    for y in range(6, 31):
        out.setdefault(y, []).append((x, "L"))
    out.setdefault(4, []).append((x - 1, "OOO"))
    out.setdefault(5, []).append((x - 1, "OlO"))
    return out


_TS_FALDA = {
    23: [(4, "CCCCCtTCCCCD")],
    24: [(4, "CCCCCCTCCCCD")],
    25: [(4, "CCCCCCCCCCCD")],
    26: [(4, "cCCCCCDCCCCD")],
    27: [(4, "cCCCCCDCCCCD")],
    28: [(4, "TTTTTTTTTTTT")],
    29: [(5, "ZZZZ"), (11, "ZZZZ")],
    30: [(5, "zzzz"), (11, "zzzz")],
}
TSERING = {
    "abajo": filas(_con_baston({
        4: [(6, "SssSSSSS")],
        5: [(5, "SsSSSSSSSS")],
        6: [(4, "SSSSSSSSSSSS")],
        7: [(4, "SSSSSSSSSSSK")],
        8: [(4, "KSSKKSSKKSSK")],
        9: [(3, "S"), (4, "KGGGSSSSGGGK"), (16, "S")],
        10: [(3, "K"), (4, "KSEESSSSEESK"), (16, "K")],
        11: [(4, "KSSSSKKSSSSK")],
        12: [(4, "KSGGGGGGGGSK")],
        13: [(4, "GGGGSMMSGGGG")],
        14: [(4, "GGGGGGGGGGGg")],
        15: [(5, "GGGGGGGGGg")],
        16: [(3, "cCC"), (6, "GGGGGGGG"), (14, "CCD")],
        17: [(2, "cCCB"), (6, "BGGGGGGB"), (14, "BCDD")],
        18: [(2, "cCDCB"), (7, "gGGGGg"), (13, "BCCDD")],
        19: [(2, "cCDCCB"), (8, "gGGg"), (12, "BCCCDD")],
        20: [(2, "cCDCCCBggBCCCCDD")],
        21: [(2, "TTDTTTTTTTTTTDTT")],
        22: [(2, "SSDCCCCtCCCCCDKK")],
        **_TS_FALDA,
    })),
    "arriba": filas(_con_baston({
        4: [(6, "SssSSSSS")],
        5: [(5, "SsSSSSSSSS")],
        6: [(4, "SSSSSSSSSSSS")],
        7: [(4, "SSSSSSSSSSSK")],
        8: [(4, "SSSSSSSSSSSK")],
        9: [(3, "S"), (4, "SSSSSSSSSSSK"), (16, "S")],
        10: [(3, "K"), (4, "KSSSSSSSSSSK"), (16, "K")],
        11: [(4, "KSSSSSSSSSSK")],
        12: [(4, "KSSSSSSSSSSK")],
        13: [(5, "KSSSSSSSSK")],
        14: [(6, "KKSSSSKK")],
        15: [(5, "GGKKKKKKGG")],
        16: [(3, "cCCCCCCCCCCCCD")],
        17: [(2, "cCCBBBBBBBBBBCDD")],
        18: [(2, "cCDCCCCBBCCCCCDD")],
        19: [(2, "cCDCCCCBBCCCCCDD")],
        20: [(2, "cCDCCCCCCCCCCCDD")],
        21: [(2, "TTDTTTTTTTTTTDTT")],
        22: [(2, "SSDCCCCCCCCCCDKK")],
        **{**_TS_FALDA, 23: [(4, "CCCCCCCCCCCD")], 24: [(4, "CCCCCCCCCCCD")]},
    })),
    "derecha": filas(_con_baston({
        4: [(6, "SssSSS")],
        5: [(5, "SsSSSSSS")],
        6: [(4, "SSSSSSSSSS")],
        7: [(4, "SSSSSSSSSSS")],
        8: [(4, "KSSSSSSKKSS")],
        9: [(4, "KSSSSSSSGGGS")],
        10: [(4, "KSSSSKSSSSES")],
        11: [(4, "KSSSSKSSSSSSS")],
        12: [(4, "KSSSSSSSGGGGG")],
        13: [(5, "KSSSSGGGGGGG")],
        14: [(6, "KSSGGGGGGG")],
        15: [(7, "GGGGGGGG")],
        16: [(5, "cCCCCGGGGG")],
        17: [(5, "cBBBBBGGGg")],
        18: [(5, "cCCcCDCgGg")],
        19: [(5, "cCCcCDCCgC")],
        20: [(5, "cCCcCDCCCC")],
        21: [(5, "TTTTTTTTTT")],
        22: [(5, "CCCSSSCCCC")],
        23: [(5, "cCCCCCCCCD")],
        24: [(5, "cCCCCCCCCD")],
        25: [(5, "cCCCCCCCCD")],
        26: [(5, "cCCCCCDCCD")],
        27: [(5, "cCCCCCDCCD")],
        28: [(5, "TTTTTTTTTT")],
        29: [(7, "ZZZZZ")],
        30: [(7, "zzzzz")],
    }, x=16)),
}
TSERING_COL = {
    "S": "#D9A06B", "s": "#F2C9A0", "K": "#A86B3C",
    "G": "#F4F1E8", "g": "#C8C8C0",
    "E": "#2B2230", "M": "#A86B3C", "I": "#9AA3A8", "W": "#F4F1E8",
    "C": "#F4F1E8", "c": "#F4F1E8", "D": "#C8C8C0",
    "B": "#9AA3A8", "T": "#E8D27A", "t": "#C9A227",
    "L": "#7A5230", "l": "#C29A5B", "O": "#C9A227",
    "Z": "#7A5230", "z": "#4A3B32", "Q": "#9AA3A8",
}

# ================================================================== Norbu
NORBU = {
    "abajo": filas({
        3: [(7, "SsSSSS")],
        4: [(5, "SssSSSSSSS")],
        5: [(4, "SSSSSSSSSSSS")],
        6: [(4, "SSSSSSSSSSSK")],
        7: [(4, "KSSSSSSSSSSK")],
        8: [(4, "KSSSSSSSSSSK")],
        9: [(4, "KSEESSSSEESK")],
        10: [(3, "S"), (4, "KSSSSSSSSSSK"), (16, "S")],
        11: [(3, "K"), (4, "KSIESSSSEISK"), (16, "K")],
        12: [(4, "KSSSSSKSSSSK")],
        13: [(4, "KKSSSSSSSSKK")],
        14: [(5, "KSSMMMMSSK")],
        15: [(6, "KSSSSSSK")],
        16: [(7, "KKSSKK")],
        17: [(4, "DDD"), (7, "KKKKKK"), (13, "DDD")],
        18: [(2, "cCCCDBBBBBBDCCCD")],
        19: [(2, "cDCCDBBBBBBDCCDD")],
        20: [(2, "cDCCDTTBBBBDCODD")],
        21: [(2, "cDCCDBBTTBBDCODD")],
        22: [(2, "cDCCDBBBBTTDCCDD")],
        23: [(2, "SSDCCCCCCCTTCCKK")],
        24: [(4, "CCCCCDCCCCCD")],
        25: [(4, "CCCCCDCCCCCD")],
        26: [(4, "cCCCCDCCCCCD")],
        27: [(4, "cCCCCDDCCCCD")],
        28: [(6, "pPP"), (11, "pPQ")],
        29: [(6, "ZZZ"), (11, "ZZZ")],
        30: [(5, "XXXX"), (11, "XXXX")],
    }),
    "arriba": filas({
        3: [(7, "SsSSSS")],
        4: [(5, "SssSSSSSSS")],
        5: [(4, "SSSSSSSSSSSS")],
        6: [(4, "SSSSSSSSSSSK")],
        7: [(4, "SSSSSSSSSSSK")],
        8: [(4, "KSSSSSSSSSSK")],
        9: [(4, "KSSSSSSSSSSK")],
        10: [(3, "S"), (4, "KSSSSSSSSSSK"), (16, "S")],
        11: [(3, "K"), (4, "KSSSSSSSSSSK"), (16, "K")],
        12: [(4, "KSSSSSSSSSSK")],
        13: [(4, "KSSSSSSSSSSK")],
        14: [(5, "KSSSSSSSSK")],
        15: [(6, "KKSSSSKK")],
        16: [(6, "KKKKKKKK")],
        17: [(4, "DDDDDDDDDDDD")],
        18: [(2, "cCCCCCCCCCCCCCCD")],
        19: [(2, "cDCCCCCDDCCCCCDD")],
        20: [(2, "cDCCCCCDDCCCCCDD")],
        21: [(2, "cDCCCCCDDCCCCCDD")],
        22: [(2, "cDTTTTTTTTTTTTDD")],
        23: [(2, "SSDCCCCDDCCCCCKK")],
        24: [(4, "CCCCCDDCCCCD")],
        25: [(4, "CCCCCDDCCCCD")],
        26: [(4, "cCCCCDDCCCCD")],
        27: [(4, "cCCCCDDCCCCD")],
        28: [(6, "pPP"), (11, "pPQ")],
        29: [(6, "ZZZ"), (11, "ZZZ")],
        30: [(5, "XXXX"), (11, "XXXX")],
    }),
    "derecha": filas({
        3: [(7, "SsSSS")],
        4: [(5, "SssSSSSS")],
        5: [(4, "SSSSSSSSSS")],
        6: [(4, "SSSSSSSSSSS")],
        7: [(4, "KSSSSSSSSSS")],
        8: [(4, "KSSSSSSSSSSS")],
        9: [(4, "KSSSSSSSSEES")],
        10: [(4, "KSSSSKSSSSSS")],
        11: [(4, "KSSSSKSSSIES")],
        12: [(4, "KSSSSSSSSSSSS")],
        13: [(5, "KSSSSSSSSSK")],
        14: [(5, "KSSSSSSSSMM")],
        15: [(6, "KSSSSSSSK")],
        16: [(7, "KKSSSKK")],
        17: [(5, "DDKKKKDD")],
        18: [(5, "cCCCCCCDBB")],
        19: [(5, "cCCcCDCDBB")],
        20: [(5, "cCCcCDCDTT")],
        21: [(5, "cCCcCDCCBO")],
        22: [(5, "cCCcCDCCCD")],
        23: [(5, "cCCSSSCCCD")],
        24: [(5, "cCCCCCCCCD")],
        25: [(5, "cCCCCCCCCD")],
        26: [(5, "cCCCCCCCCCD")],
        27: [(5, "cCCCCCCCCCD")],
        28: [(8, "pPPQ")],
        29: [(8, "ZZZZZ")],
        30: [(8, "XXXXX")],
    }),
}
NORBU_COL = {
    "S": "#D9A06B", "s": "#F2C9A0", "K": "#A86B3C",
    "E": "#1A1420", "I": "#E8D27A", "W": "#F4F1E8", "M": "#6E4426",
    "C": "#3B3846", "c": "#5A5566", "D": "#24222B",
    "B": "#F4F1E8", "T": "#E8D27A", "O": "#E8D27A",
    "P": "#24222B", "p": "#3B3846", "Q": "#1A1420",
    "Z": "#2B2230", "X": "#1A1420",
}

# ================================================================== Soldados
_SOL_CUERPO_FRENTE = {
    15: [(2, "cCCCCCRRRRCCCCCD")],
    16: [(2, "cDCCCCCRRCCCCCDD")],
    17: [(2, "RRDCCCCCCCCCCCRR")],
    18: [(2, "cDCCCCCOOCCCCCDD")],
    19: [(2, "cDCCCCCOOCCCCCDD")],
    20: [(2, "cDRRRRRRRRRRRRDD")],
    21: [(2, "GGPPPPPPPPPPPPGG")],
    22: [(4, "PPPPPPPPPPPP")],
    23: [(4, "pPPPPQQPPPPQ")],
    24: [(5, "pPPP"), (11, "pPPQ")],
    25: [(5, "pPPP"), (11, "pPPQ")],
    26: [(5, "ZZZZ"), (11, "ZZZZ")],
    27: [(5, "zZZZ"), (11, "zZZZ")],
    28: [(5, "XXXX"), (11, "XXXX")],
}
SOLDADO = {
    "abajo": filas(bajar({
        2: [(7, "CCCCCC")],
        3: [(5, "CcCCCCCCCC")],
        4: [(4, "CccCCCCCCCCD")],
        5: [(3, "CCCCCCCCCCCCCD")],
        6: [(3, "CCCCCCCCCCCCCD")],
        7: [(3, "CCDNNNNNNNNDCD")],
        8: [(3, "CCDnNNNNNNNDCD")],
        9: [(3, "CCDNEINNIENDCD")],
        10: [(3, "CCDNNNNNNNNDCD")],
        11: [(3, "CCDmNNNNNNmDCD")],
        12: [(3, "CCCDmmmmmmDCCD")],
        13: [(4, "CCCDDDDDDCCD")],
        14: [(4, "rRRRRRRRRRRR")],
        **_SOL_CUERPO_FRENTE,
    }, 2)),
    "arriba": filas(bajar({
        2: [(7, "CCCCCC")],
        3: [(5, "CcCCCCCCCC")],
        4: [(4, "CccCCCCCCCCD")],
        5: [(3, "CCCCCCCCCCCCCD")],
        6: [(3, "CCCCCCDCCCCCCD")],
        7: [(3, "CCCCCCDCCCCCCD")],
        8: [(3, "CCCCCCDCCCCCCD")],
        9: [(3, "CCCCCCDCCCCCCD")],
        10: [(3, "CCCCCCDCCCCCCD")],
        11: [(3, "CCCCCCCCCCCCCD")],
        12: [(3, "CCCCCCCCCCCCCD")],
        13: [(4, "CCCCCCCCCCCD")],
        14: [(4, "rRRRRRRRRRRR")],
        **{**_SOL_CUERPO_FRENTE,
           15: [(2, "cCCCCCCCCCCCCCCD")],
           16: [(2, "cDCCCCCCCCCCCCDD")],
           18: [(2, "cDCCCCCCCCCCCCDD")],
           19: [(2, "cDCCCCCCCCCCCCDD")]},
    }, 2)),
    "derecha": filas(bajar({
        2: [(7, "CCCCC")],
        3: [(5, "CcCCCCCC")],
        4: [(4, "CccCCCCCCC")],
        5: [(3, "CCCCCCCCCCCC")],
        6: [(3, "CCCCCCCCCCCCC")],
        7: [(3, "CCCCCCCCDNNNN")],
        8: [(3, "CCCCCCCCDnNNN")],
        9: [(3, "CCCCCCCCDNEIN")],
        10: [(3, "CCCCCCCCDNNNN")],
        11: [(3, "CCCCCCCCDmNNN")],
        12: [(3, "CCCCCCCCCDmmm")],
        13: [(4, "CCCCCCCCDD")],
        14: [(5, "rRRRRRRR")],
        15: [(4, "R"), (5, "cCCCCCCCD")],
        16: [(4, "R"), (5, "cCCcCDCCD")],
        17: [(5, "cCCRRRCCD")],
        18: [(5, "cCCcCDCOD")],
        19: [(5, "cCCcCDCCD")],
        20: [(5, "RRRcCDRRR")],
        21: [(5, "PPPGGGPPP")],
        22: [(6, "PPPPPPP")],
        23: [(7, "pPPPQ")],
        24: [(8, "pPPQ")],
        25: [(8, "pPPQ")],
        26: [(8, "ZZZZZ")],
        27: [(8, "zZZZZ")],
        28: [(8, "XXXXX")],
    }, 2)),
}
SOLDADO_BASE = {
    "C": "#3B3846", "c": "#5A5566", "D": "#24222B",
    "N": "#C8C8C0", "n": "#F4F1E8", "m": "#9AA3A8", "E": "#1A1420",
    "O": "#5A5566", "G": "#2B2230",
    "P": "#24222B", "p": "#3B3846", "Q": "#1A1420",
    "Z": "#2B2230", "z": "#3B3846", "X": "#1A1420",
}
ELEMENTOS = {
    "fuego": ("#D9481E", "#F28C28", "#F28C28"),
    "agua": ("#3A86C8", "#8FD3F0", "#8FD3F0"),
    "tierra": ("#6B8E3D", "#C29A5B", "#C29A5B"),
    "aire": ("#E8D27A", "#F4F1E8", "#E8D27A"),
}

# ================================================================== registro
J.JUGABLES["tsering"] = dict(
    poses=TSERING, colores=TSERING_COL, manga="C", mano="S",
    brazos={"abajo": ((2, 3), (16, 17), (18, 22)), "arriba": ((2, 3), (16, 17), (18, 22)),
            "derecha": ((8, 10), None, (18, 22))},
    piernas={"abajo": 29, "arriba": 29, "derecha": 29},
    anims=["reposo", "caminar", "poder"], carpeta="personajes")
J.JUGABLES["norbu"] = dict(
    poses=NORBU, colores=NORBU_COL, manga="C", mano="S",
    brazos={"abajo": ((2, 3), (16, 17), (19, 23)), "arriba": ((2, 3), (16, 17), (19, 23)),
            "derecha": ((8, 10), None, (19, 23))},
    piernas={"abajo": 28, "arriba": 28, "derecha": 28},
    anims=["reposo", "caminar", "golpe", "poder", "derribado"], carpeta="personajes")
for _el, (_r, _rl, _ojo) in ELEMENTOS.items():
    _col = dict(SOLDADO_BASE)
    _col.update({"R": _r, "r": _rl, "I": _ojo})
    J.JUGABLES["soldado_" + _el] = dict(
        poses=SOLDADO, colores=_col, manga="C", mano="G", ojos_cerrados={"I": "E"},
        brazos={"abajo": ((2, 3), (16, 17), (18, 23)), "arriba": ((2, 3), (16, 17), (18, 23)),
                "derecha": ((8, 10), None, (18, 23))},
        piernas={"abajo": 26, "arriba": 26, "derecha": 26},
        anims=["reposo", "caminar", "golpe", "danio", "derribado"], carpeta="enemigos")

NPCS = ["tsering", "norbu"] + ["soldado_" + e for e in ELEMENTOS]


def generar(nombre, guardar=True):
    cfg = J.JUGABLES[nombre]
    salida = os.path.join(RAIZ, "juego", "assets", cfg["carpeta"])
    res = {}
    for anim, n, dirs in J.ANIMS:
        if anim not in cfg["anims"]:
            continue
        for d in dirs:
            for f in range(n):
                img = J.derribado(nombre) if anim == "derribado" else J.cuadro(nombre, d, anim, f)
                res[(anim, d, f)] = img
                if guardar:
                    img.save(os.path.join(salida, f"{nombre}_{anim}_{d}_{f}.png"))
    return res


if __name__ == "__main__":
    for n in NPCS:
        print(n, len(generar(n)), "cuadros")
    E = 6
    out = Image.new("RGBA", (len(NPCS) * 3 * (32 * E + 4) + 8, 32 * E + 16), (58, 54, 70, 255))
    i = 0
    for n in NPCS:
        for d in ("abajo", "derecha", "arriba"):
            out.alpha_composite(J.cuadro(n, d, "reposo", 0).resize((32 * E, 32 * E), Image.NEAREST), (8 + i * (32 * E + 4), 8))
            i += 1
    out.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_npcs_vistas.png"))
