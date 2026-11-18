"""Definiciones de personajes y generador de sprites.

Uso: python3 herramientas/personajes.py [nombre ...]
Escribe los cuadros en juego/assets/<carpeta>/ y una hoja de vista previa en arte_fuente/previews/.
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from rig import dibujar, OSCURO
from paleta import fuera_de_paleta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ternas (base, luz, sombra)
ROJO = ("#D9481E", "#F28C28", "#8E1B1B")
ROJO_OSC = ("#8E1B1B", "#D9481E", "#2B2230")
ORO = ("#C9A227", "#E8D27A", "#7A5230")
NEGRO = ("#2B2230", "#4A3B32", "#1A1420")
VERDE = ("#6B8E3D", "#C29A5B", "#3F5A2A")
VERDE_OSC = ("#3F5A2A", "#6B8E3D", "#2B2230")
MARRON = ("#7A5230", "#C29A5B", "#4A3B32")
AZUL = ("#3A86C8", "#8FD3F0", "#1E4F8C")
AZUL_OSC = ("#1E4F8C", "#3A86C8", "#2B2230")
CELESTE = ("#8FD3F0", "#F2F7FA", "#3A86C8")
BLANCO = ("#F4F1E8", "#F4F1E8", "#C8C8C0")
GRIS_CLARO = ("#C8C8C0", "#F4F1E8", "#9AA3A8")
AMARILLO = ("#E8D27A", "#F4F1E8", "#C9A227")
GRIS_AZUL = ("#9AA3A8", "#C8C8C0", "#5A5566")
CICLO = ("#3B3846", "#5A5566", "#24222B")
CICLO_OSC = ("#24222B", "#3B3846", "#1A1420")

PIEL_CLARA = ("#F2C9A0", "#F2C9A0", "#D9A06B")
PIEL_MEDIA = ("#D9A06B", "#F2C9A0", "#A86B3C")
PIEL_OSCURA = ("#A86B3C", "#D9A06B", "#6E4426")
PIEL_PROFUNDA = ("#6E4426", "#A86B3C", "#4A3B32")

PELO_NEGRO = ("#2B2230", "#4A3B32", "#1A1420")
PELO_CAFE = ("#4A3B32", "#7A5230", "#2B2230")


def jugable(**kw):
    base = dict(ojo_color=OSCURO)
    base.update(kw)
    return base


PERSONAJES = {
    "ryu": dict(
        carpeta="personajes",
        ch=jugable(
            piel=PIEL_CLARA, pelo=PELO_NEGRO, estilo_pelo="puntas", sonrisa=True,
            cuerpo=ROJO, manga=ROJO, puno="#C9A227", dobladillo=ORO, camisa=NEGRO,
            cuello=ROJO_OSC, cierre="#C9A227",
            guante=NEGRO, pantalon=NEGRO, franja="#C9A227",
            zapato=("#D9481E", "#F28C28", "#8E1B1B"), suela="#F4F1E8",
        ),
    ),
    "gao": dict(
        carpeta="personajes",
        ch=jugable(
            piel=PIEL_MEDIA, pelo=PELO_CAFE, estilo_pelo="corto", ceja="#2B2230",
            cuerpo=VERDE_OSC, manga=VERDE, puno="#7A5230", camisa=("#6B8E3D", "#C29A5B", "#3F5A2A"),
            cinturon="#7A5230", hebilla="#C29A5B", dobladillo=MARRON,
            guante=MARRON, pantalon=("#7A5230", "#C29A5B", "#4A3B32"),
            zapato=("#4A3B32", "#7A5230", "#2B2230"), suela="#2B2230",
        ),
    ),
    "nerea": dict(
        carpeta="personajes",
        ch=jugable(
            piel=PIEL_OSCURA, pelo=PELO_NEGRO, estilo_pelo="trenza", trenza_lazo="#8FD3F0",
            ceja="#2B2230",
            cuerpo=AZUL, manga=AZUL, puno="#F2F7FA", camisa=("#F2F7FA", "#F2F7FA", "#8FD3F0"),
            cierre="#F2F7FA", bufanda=CELESTE, frasco="#F2F7FA", dobladillo=AZUL_OSC,
            pantalon=NEGRO, zapato=("#F2F7FA", "#F2F7FA", "#8FD3F0"), suela="#3A86C8",
        ),
    ),
}


ROBA_TSERING = ("#F4F1E8", "#F4F1E8", "#C8C8C0")
ELEMENTOS_SOLDADO = {
    "fuego": "#D9481E",
    "agua": "#3A86C8",
    "tierra": "#6B8E3D",
    "aire": "#F4F1E8",
}


def soldado(elemento):
    c = ELEMENTOS_SOLDADO[elemento]
    return dict(
        carpeta="enemigos",
        anims=["reposo", "caminar", "golpe", "danio", "derribado"],
        ch=jugable(
            piel=PIEL_MEDIA, pelo=NEGRO, estilo_pelo="capucha", capucha=CICLO_OSC,
            mascara=CICLO, ojo_color=c,
            cuerpo=CICLO_OSC, manga=CICLO, puno=c, banda=(c, c, c), dobladillo=CICLO,
            simbolo="#5A5566", cinturon=c, bufanda=(c, c, c),
            pantalon=CICLO_OSC, zapato=("#2B2230", "#3B3846", "#1A1420"), suela="#1A1420",
        ),
    )


def ciudadano(piel, pelo, estilo, cuerpo, pantalon, extra=None):
    ch = jugable(
        piel=piel, pelo=pelo, estilo_pelo=estilo, ceja="#2B2230", trenza_lazo="#C9A227",
        cuerpo=cuerpo, manga=cuerpo, pantalon=pantalon,
        zapato=("#4A3B32", "#7A5230", "#2B2230"), suela="#2B2230",
    )
    if extra:
        ch.update(extra)
    return dict(carpeta="personajes", anims=["reposo", "caminar"], dirs=("abajo",), ch=ch)


PERSONAJES.update({
    "tsering": dict(
        carpeta="personajes",
        anims=["reposo", "caminar", "poder"],
        ch=jugable(
            piel=PIEL_MEDIA, pelo=BLANCO, estilo_pelo="calvo", ceja="#C8C8C0",
            barba=("#F4F1E8", "#F4F1E8", "#C8C8C0"),
            cuerpo=ROBA_TSERING, manga=ROBA_TSERING, abrigo=ROBA_TSERING,
            abrigo_corte=("#C8C8C0", "#C8C8C0", "#9AA3A8"), dobladillo=AMARILLO,
            cinturon="#E8D27A", hebilla="#C9A227", puno="#E8D27A",
            bufanda=GRIS_AZUL, camisa=AMARILLO,
            baston=("#7A5230", "#C29A5B", "#4A3B32"), baston_tope=("#C9A227", "#E8D27A", "#7A5230"),
            pantalon=("#C8C8C0", "#F4F1E8", "#9AA3A8"),
            zapato=("#7A5230", "#C29A5B", "#4A3B32"), suela="#4A3B32",
        ),
    ),
    "norbu": dict(
        carpeta="personajes",
        anims=["reposo", "caminar", "golpe", "poder", "derribado"],
        ch=jugable(
            piel=PIEL_MEDIA, pelo=PELO_NEGRO, estilo_pelo="calvo", ceja="#2B2230",
            cuerpo=CICLO_OSC, manga=CICLO_OSC, abrigo=CICLO_OSC,
            abrigo_corte=("#1A1420", "#24222B", "#1A1420"), dobladillo=CICLO,
            camisa=BLANCO, cinturon="#E8D27A", hebilla="#C9A227", puno="#E8D27A",
            simbolo="#E8D27A", cierre="#5A5566",
            pantalon=CICLO_OSC, zapato=("#2B2230", "#3B3846", "#1A1420"), suela="#1A1420",
        ),
    ),
    "ciudadano_a": ciudadano(PIEL_CLARA, PELO_CAFE, "corto", ("#C9A227", "#E8D27A", "#7A5230"),
                             ("#3B3846", "#5A5566", "#24222B")),
    "ciudadano_b": ciudadano(PIEL_PROFUNDA, PELO_NEGRO, "trenza", ("#8E1B1B", "#D9481E", "#2B2230"),
                             ("#7A5230", "#C29A5B", "#4A3B32"), dict(bufanda=("#F28C28", "#E8D27A", "#D9481E"))),
    "ciudadano_c": ciudadano(PIEL_MEDIA, PELO_NEGRO, "puntas", ("#3A86C8", "#8FD3F0", "#1E4F8C"),
                             ("#24222B", "#3B3846", "#1A1420")),
})
for _e in ELEMENTOS_SOLDADO:
    PERSONAJES["soldado_" + _e] = soldado(_e)

ANIMACIONES = [
    # (nombre, cuadros, direcciones)
    ("reposo", 2, ("abajo", "arriba", "derecha")),
    ("caminar", 4, ("abajo", "arriba", "derecha")),
    ("golpe", 3, ("abajo", "arriba", "derecha")),
    ("poder", 2, ("abajo", "arriba", "derecha")),
    ("defensa", 1, ("abajo", "arriba", "derecha")),
    ("danio", 1, ("abajo",)),
    ("derribado", 1, ("abajo",)),
]


def animaciones_de(cfg):
    anims = cfg.get("anims")
    out = []
    for a, n, ds in ANIMACIONES:
        if anims is None or a in anims:
            out.append((a, n, cfg.get("dirs", ds) if len(ds) > 1 else ds))
    return out


def generar(nombre, animaciones=None, guardar=True):
    cfg = PERSONAJES[nombre]
    animaciones = animaciones or animaciones_de(cfg)
    ch = cfg["ch"]
    salida = os.path.join(RAIZ, "juego", "assets", cfg["carpeta"])
    os.makedirs(salida, exist_ok=True)
    cuadros = {}
    for anim, n, dirs in animaciones:
        for d in dirs:
            for f in range(n):
                img = dibujar(ch, d, anim, f)
                malos = fuera_de_paleta(img)
                assert not malos, f"{nombre} {anim} {d} {f}: fuera de paleta {malos}"
                cuadros[(anim, d, f)] = img
                if guardar:
                    img.save(os.path.join(salida, f"{nombre}_{anim}_{d}_{f}.png"))
    return cuadros


def hoja_previa(nombres, escala=4):
    """Hoja con las poses de cada personaje (una columna de bloques por personaje)."""
    bloques = []
    for nombre in nombres:
        cuadros = generar(nombre, guardar=False)
        filas = []
        for anim, n, dirs in animaciones_de(PERSONAJES[nombre]):
            for d in dirs:
                filas.append([cuadros[(anim, d, f)] for f in range(n)])
        bloques.append(filas)
    celda = 32 * escala
    cols = 4
    alto = max(len(f) for f in bloques) * celda + 16
    ancho = len(bloques) * (cols * celda + 16) + 16
    hoja = Image.new("RGBA", (ancho, alto), (58, 54, 70, 255))
    for ci, filas in enumerate(bloques):
        ox = 16 + ci * (cols * celda + 16)
        for ri, frames in enumerate(filas):
            for fi, img in enumerate(frames):
                hoja.alpha_composite(img.resize((celda, celda), Image.NEAREST), (ox + fi * celda, 8 + ri * celda))
    return hoja


if __name__ == "__main__":
    nombres = sys.argv[1:] or list(PERSONAJES)
    for n in nombres:
        c = generar(n)
        print(n, len(c), "cuadros")
    hoja = hoja_previa(nombres)
    ruta = os.path.join(RAIZ, "arte_fuente", "previews", "hoja_" + "_".join(nombres) + ".png")
    hoja.save(ruta)
    print(ruta)
