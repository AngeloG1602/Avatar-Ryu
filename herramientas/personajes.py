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


def generar(nombre, animaciones=ANIMACIONES, guardar=True):
    cfg = PERSONAJES[nombre]
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
    """Hoja con todas las poses de cada personaje, sobre fondo gris."""
    filas = []
    for nombre in nombres:
        cuadros = generar(nombre, guardar=False)
        fila_datos = []
        for anim, n, dirs in ANIMACIONES:
            for d in dirs:
                fila_datos.append([cuadros[(anim, d, f)] for f in range(n)])
        filas.append((nombre, fila_datos))
    # una fila por (anim, dir) y un bloque por personaje
    etiquetas = [(a, d) for a, n, ds in ANIMACIONES for d in ds]
    cols = max(n for _, n, _ in ANIMACIONES)
    celda = 32 * escala
    ancho = len(nombres) * (cols * celda + 16) + 16
    alto = len(etiquetas) * celda + 16
    hoja = Image.new("RGBA", (ancho, alto), (58, 54, 70, 255))
    for ci, (nombre, datos) in enumerate(filas):
        ox = 16 + ci * (cols * celda + 16)
        for ri, frames in enumerate(datos):
            for fi, img in enumerate(frames):
                g = img.resize((celda, celda), Image.NEAREST)
                hoja.alpha_composite(g, (ox + fi * celda, 8 + ri * celda))
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
