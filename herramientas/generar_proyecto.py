"""Genera el proyecto de GDevelop 5 (juego/game.json) con recursos, objetos, escenas y la lógica.

La lógica está en herramientas/juego_js/libreria.js y se inserta como una hoja de eventos externa
("Libreria") enlazada desde todas las escenas. Cada escena solo llama a gdjs.ryu.ejecutar(...).
Uso: python3 herramientas/generar_proyecto.py
"""
import json
import os
import sys
import uuid
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import a_rgb

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JUEGO = os.path.join(RAIZ, "juego")
A = "assets"
VERSION_LOGICA = "1.0.0"

ESCENAS = ["MenuInicio", "Controles", "Intro", "Ciudad", "ZonaTierra", "Pelea", "ArenaFinal", "Final", "Creditos", "Derrota"]
DIRS = ("abajo", "arriba", "derecha")

recursos = {}


def res(ruta, tipo="image"):
    """Registra un recurso (ruta relativa a juego/) y devuelve su nombre."""
    completo = os.path.join(JUEGO, ruta)
    assert os.path.exists(completo), "Falta el archivo " + ruta
    if ruta not in recursos:
        r = {"file": ruta, "kind": tipo, "metadata": "", "name": ruta, "userAdded": True}
        if tipo == "image":
            r["smoothed"] = False
        if tipo == "audio":
            r["preloadAsMusic"] = "musica" in ruta
            r["preloadAsSound"] = "sfx" in ruta
        recursos[ruta] = r
    return ruta


# ================================================================== objetos
def cuadro(imagen):
    return {"hasCustomCollisionMask": False, "image": res(imagen), "points": [],
            "originPoint": {"name": "origine", "x": 0, "y": 0},
            "centerPoint": {"automatic": True, "name": "centre", "x": 0, "y": 0}, "customCollisionMask": []}


def animacion(nombre, imagenes, t=0.12, bucle=True):
    return {"name": nombre, "useMultipleDirections": False,
            "directions": [{"looping": bucle, "timeBetweenFrames": t, "sprites": [cuadro(i) for i in imagenes]}]}


def sprite(nombre, animaciones):
    return {"adaptCollisionMaskAutomatically": False, "assetStoreId": "", "name": nombre, "type": "Sprite",
            "updateIfNotVisible": False, "variables": [], "effects": [], "behaviors": [], "animations": animaciones}


def texto(nombre, tam):
    fuente = res(f"{A}/ui/fuente/PressStart2P-Regular.ttf", "font")
    return {"assetStoreId": "", "bold": False, "italic": False, "name": nombre, "smoothed": False, "type": "TextObject::Text",
            "underlined": False, "variables": [], "effects": [], "behaviors": [], "string": "", "font": fuente,
            "textAlignment": "", "characterSize": tam, "color": {"b": 232, "g": 241, "r": 244},
            "content": {"bold": False, "isOutlineEnabled": False, "isShadowEnabled": False, "italic": False,
                        "outlineColor": "26;20;32", "outlineThickness": 2, "shadowAngle": 90, "shadowBlurRadius": 0,
                        "shadowColor": "26;20;32", "shadowDistance": 2, "shadowOpacity": 255, "smoothed": False,
                        "underlined": False, "text": "", "font": fuente, "textAlignment": "", "verticalTextAlignment": "top",
                        "characterSize": tam, "lineHeight": 0, "color": "244;241;232"}}


def panel(nombre, imagen, margen, ancho, alto):
    return {"assetStoreId": "", "bottomMargin": margen, "height": alto, "leftMargin": margen, "name": nombre,
            "rightMargin": margen, "texture": res(imagen), "tiled": False, "topMargin": margen,
            "type": "PanelSpriteObject::PanelSprite", "width": ancho, "variables": [], "effects": [], "behaviors": []}


def cuadros(carpeta, base, n):
    return [f"{A}/{carpeta}/{base}_{i}.png" for i in range(n)]


def anims_personaje(clave, acciones, carpeta="personajes", prefijo_anim=""):
    """acciones: [(accion, cuadros, tiempo, bucle)] con 3 direcciones (danio/derribado solo abajo)."""
    out = []
    for accion, n, t, bucle in acciones:
        if accion in ("danio", "derribado"):
            out.append(animacion(prefijo_anim + accion, cuadros(carpeta, f"{clave}_{accion}_abajo", n), t, bucle))
        else:
            for d in DIRS:
                out.append(animacion(f"{prefijo_anim}{accion}_{d}", cuadros(carpeta, f"{clave}_{accion}_{d}", n), t, bucle))
    return out


JUGABLE = [("reposo", 2, 0.45, True), ("caminar", 4, 0.12, True), ("golpe", 3, 0.08, False), ("poder", 2, 0.12, False),
           ("defensa", 1, 1, False), ("danio", 1, 1, False), ("derribado", 1, 1, False)]


def efecto(nombre, n, t=0.08, bucle=False, desde=0):
    return animacion(nombre, [f"{A}/efectos/efecto_{nombre if nombre != 'roca_impacto' else 'roca'}_{i}.png" for i in range(desde, desde + n)], t, bucle)


def crear_velo():
    from tiles_ciudad import Lienzo
    L = Lienzo(144, 80)
    L.rect(0, 0, 143, 79, "#C9A227"); L.rect(1, 1, 142, 78, "#24222B"); L.rect(1, 1, 142, 1, "#3B3846")
    L.img.save(os.path.join(JUEGO, A, "ui", "ui_velo.png"))


def objetos():
    o = []
    o.append(sprite("Ryu", anims_personaje("ryu", JUGABLE)))
    o.append(sprite("Gao", anims_personaje("gao", JUGABLE)))
    o.append(sprite("Nerea", anims_personaje("nerea", JUGABLE)))
    o.append(sprite("Tsering", anims_personaje("tsering", [("reposo", 2, 0.45, True), ("caminar", 4, 0.12, True), ("poder", 2, 0.12, False)])))
    o.append(sprite("Norbu", anims_personaje("norbu", [("reposo", 2, 0.45, True), ("caminar", 4, 0.12, True), ("golpe", 3, 0.08, False),
                                                       ("poder", 2, 0.12, False), ("derribado", 1, 1, False)])))
    sold = []
    for el in ("fuego", "agua", "tierra", "aire"):
        sold += anims_personaje(f"soldado_{el}", [("reposo", 2, 0.45, True), ("caminar", 4, 0.12, True), ("golpe", 3, 0.08, False),
                                                   ("danio", 1, 1, False), ("derribado", 1, 1, False)], "enemigos", el + "_")
    o.append(sprite("Soldado", sold))
    ciu = []
    for k in "abc":
        ciu.append(animacion(f"{k}_reposo", cuadros("personajes", f"ciudadano_{k}_reposo_abajo", 2), 0.45))
        ciu.append(animacion(f"{k}_caminar", cuadros("personajes", f"ciudadano_{k}_caminar_abajo", 4), 0.14))
    o.append(sprite("Ciudadano", ciu))
    o.append(sprite("Proyectil", [
        efecto("bola_fuego", 4, 0.08, True), efecto("rafaga_aire", 4, 0.08, True), animacion("roca", [f"{A}/efectos/efecto_roca_0.png"]),
        animacion("congelar", cuadros("efectos", "efecto_proyectil_soldado_agua", 2), 0.15),
    ] + [animacion(f"soldado_{e}", cuadros("efectos", f"efecto_proyectil_soldado_{e}", 2), 0.15) for e in ("fuego", "agua", "tierra", "aire")]))
    o.append(sprite("Efecto", [
        efecto("impacto", 3, 0.06), efecto("roca_impacto", 3, 0.07, desde=1), efecto("latigazo_agua", 4, 0.06),
        efecto("llamarada", 6, 0.06), efecto("cupula_tierra", 4, 0.08), efecto("curacion", 4, 0.1), efecto("congelado", 2, 0.3, True),
        efecto("sello", 4, 0.15, True), efecto("aura_avatar", 6, 0.08, True), efecto("fuego_suelo", 4, 0.12, True),
    ]))
    o.append(sprite("Muro", [efecto("muro_tierra", 3, 0.08)]))
    o[-1]["animations"][0]["name"] = "aparecer"
    T = f"{A}/tilesets"
    o.append(sprite("PuertaElemental", [
        animacion("cerrada_tierra", [f"{T}/obj_puerta_elemental_cerrada_tierra.png"]),
        animacion("cerrada_tierra_agua", [f"{T}/obj_puerta_elemental_cerrada_tierra_agua.png"]),
        animacion("abriendo", [f"{T}/obj_puerta_elemental_abriendo_{i}.png" for i in range(3)], 0.15, False),
        animacion("abierta", [f"{T}/obj_puerta_elemental_abierta.png"]),
    ]))
    o.append(sprite("Pista", [animacion(n, [f"{T}/obj_pista_{n}.png"]) for n in ("simbolo", "documento", "diario")]))
    o.append(sprite("Pilar", [animacion("entero", [f"{T}/obj_pilar_entero.png"]), animacion("roto", [f"{T}/obj_pilar_roto.png"])]))
    o.append(sprite("Fuente", [animacion("agua", [f"{T}/obj_fuente_{i}.png" for i in range(3)], 0.2)]))
    o.append(sprite("Fondo", [
        animacion("ciudad", [f"{A}/mapas/mapa_ciudad.png"]), animacion("tierra", [f"{A}/mapas/mapa_tierra.png"]),
        animacion("plaza", [f"{T}/fondo_pelea_plaza.png"]), animacion("canon", [f"{T}/fondo_pelea_canon.png"]),
        animacion("mina", [f"{T}/fondo_pelea_mina.png"]), animacion("arena", [f"{T}/fondo_arena_final.png"]),
    ]))
    U = f"{A}/ui"
    o.append(sprite("Pantalla", [
        animacion("titulo", [f"{U}/pantalla_titulo.png"]), animacion("controles", [f"{U}/pantalla_controles.png"]),
        animacion("final", [f"{U}/panel_final.png"]), animacion("derrota", [f"{U}/pantalla_derrota.png"]),
        animacion("velo", [f"{U}/ui_velo.png"]),
    ] + [animacion(f"panel_{i}", [f"{U}/intro_panel_{i}.png"]) for i in range(1, 5)]))
    o.append(sprite("Hud", [animacion(n, [f"{U}/ui_hud_{n}.png"]) for n in ("ryu", "gao", "nerea")]))
    o.append(sprite("BarraVida", [animacion("normal", [f"{U}/ui_barra_vida.png"]), animacion("baja", [f"{U}/ui_barra_vida_baja.png"])]))
    o.append(sprite("BarraEnergia", [animacion("normal", [f"{U}/ui_barra_energia.png"])]))
    o.append(sprite("IconoElemento", [animacion(n, [f"{U}/ui_icono_{n}.png"]) for n in ("fuego", "agua", "tierra", "aire")]))
    o.append(sprite("IconoPista", [animacion("pista", [f"{U}/ui_icono_pista.png"])]))
    o.append(sprite("MarcoRetrato", [animacion("marco", [f"{U}/ui_marco_retrato.png"])]))
    o.append(sprite("Retrato", [animacion(n, [f"{U}/retrato_{n}.png"]) for n in ("ryu", "gao", "nerea", "tsering", "norbu", "daichi")]))
    o.append(sprite("Continuar", [animacion("flecha", [f"{U}/ui_continuar_0.png", f"{U}/ui_continuar_1.png"], 0.3)]))
    o.append(panel("CajaDialogo", f"{U}/ui_caja_dialogo.png", 12, 560, 86))
    o.append(panel("PlacaNombre", f"{U}/ui_placa_nombre.png", 6, 48, 16))
    o.append(texto("Texto", 8))
    o.append(texto("TextoGrande", 16))
    return o


# ================================================================== variables globales (docs/02)
def variables():
    def v(n, t, val):
        return {"folded": True, "name": n, "type": t, "value": val}
    return [
        v("faseHistoria", "number", 0), v("aireDesbloqueado", "boolean", False), v("aguaDesbloqueada", "boolean", False),
        v("tierraDesbloqueada", "boolean", False), v("elementoActivo", "string", ""), v("pistas", "number", 0),
        v("peleaActual", "string", ""), v("escenaRetorno", "string", ""), v("retornoX", "number", 0), v("retornoY", "number", 0),
        v("escenaDerrota", "string", ""),
        {"folded": True, "name": "encuentrosHechos", "type": "structure", "children": []},
        {"folded": True, "name": "marcas", "type": "structure", "children": []},
    ]


# ================================================================== escenas
def capa(nombre):
    return {"ambientLightColorB": 200, "ambientLightColorG": 200, "ambientLightColorR": 200,
            "camera2DPlaneMaxDrawingDistance": 5000, "camera3DFarPlaneDistance": 10000, "camera3DFieldOfView": 45,
            "camera3DNearPlaneDistance": 3, "cameraType": "", "followBaseLayerCamera": False, "isLightingLayer": False,
            "isLocked": False, "name": nombre, "renderingType": "", "visibility": True,
            "cameras": [{"defaultSize": True, "defaultViewport": True, "height": 0, "viewportBottom": 1, "viewportLeft": 0,
                         "viewportRight": 1, "viewportTop": 0, "width": 0}] if nombre == "" else [],
            "effects": []}


def js(lineas):
    return {"type": "BuiltinCommonInstructions::JsCode", "inlineCode": lineas, "parameterObjects": "", "useStrict": False,
            "eventsSheetExpanded": False}


def comentario(texto):
    return {"type": "BuiltinCommonInstructions::Comment", "color": {"b": 109, "g": 230, "r": 255, "textB": 0, "textG": 0, "textR": 0},
            "comment": texto, "comment2": ""}


def escena(nombre):
    return {
        "b": 43, "disableInputWhenNotFocused": True, "mangledName": nombre, "name": nombre, "r": 36,
        "standardSortMethod": True, "stopSoundsOnStartup": False, "title": "", "v": 34,
        "uiSettings": {"grid": False, "gridType": "rectangular", "gridWidth": 32, "gridHeight": 32, "gridDepth": 32,
                       "gridOffsetX": 0, "gridOffsetY": 0, "gridOffsetZ": 0, "gridColor": 10401023, "gridAlpha": 0.8,
                       "snap": False, "zoomFactor": 1, "windowMask": False, "selectedLayer": "", "gameEditorMode": "instances-editor"},
        "objectsGroups": [], "variables": [], "instances": [], "objects": [],
        "objectsFolderStructure": {"folderName": "__ROOT"},
        "events": [
            comentario(f"Escena {nombre}. Toda la lógica está en la hoja de eventos externa «Libreria» "
                       "(generada desde herramientas/juego_js/libreria.js). Aquí solo se llama a la escena."),
            {"disabled": False, "folded": False, "type": "BuiltinCommonInstructions::Link", "include": {"includeConfig": 0}, "target": "Libreria"},
            js([f'gdjs.ryu.ejecutar(runtimeScene, "{nombre}");']),
        ],
        "layers": [capa(""), capa("UI")],
        "behaviorsSharedData": [],
    }


def proyecto():
    crear_velo()
    with open(os.path.join(RAIZ, "herramientas", "juego_js", "mapas.json")) as fh:
        mapas = json.load(fh)
    with open(os.path.join(RAIZ, "herramientas", "juego_js", "libreria.js")) as fh:
        lib = fh.read().replace("__MAPAS__", json.dumps(mapas, separators=(",", ":"))).replace("__VERSION__", VERSION_LOGICA)
    objs = objetos()
    for f in sorted(os.listdir(os.path.join(JUEGO, A, "audio"))):
        if f.endswith(".ogg"):
            res(f"{A}/audio/{f}", "audio")
    res(f"{A}/ui/fuente/PressStart2P-Regular.ttf", "font")
    icono = res(f"{A}/ui/retrato_ryu.png")
    p = {
        "firstLayout": "MenuInicio",
        "gdVersion": {"build": 279, "major": 5, "minor": 6, "revision": 0},
        "properties": {
            "adaptGameResolutionAtRuntime": False, "antialiasingMode": "none", "antialisingEnabledOnMobile": False,
            "folderProject": False, "orientation": "landscape", "packageName": "com.angeloynicoll.ryuelultimociclo",
            "pixelsRounding": True, "projectUuid": str(uuid.uuid5(uuid.NAMESPACE_URL, "ryu-el-ultimo-ciclo")),
            "scaleMode": "nearest", "sizeOnStartupMode": "", "templateSlug": "", "version": "1.0.0",
            "name": "Ryu: El Último Ciclo", "description": "Aventura cooperativa local para 3 jugadores inspirada en Avatar.",
            "author": "Ángelo y Nicoll", "windowWidth": 640, "windowHeight": 360, "latestCompilationDirectory": "",
            "maxFPS": 60, "minFPS": 20, "verticalSync": False,
            "platformSpecificAssets": {"liluo-thumbnail": icono},
            "loadingScreen": {"backgroundColor": 2367019, "backgroundFadeInDuration": 0.2, "backgroundImageResourceName": "",
                              "gdevelopLogoStyle": "light", "logoAndProgressFadeInDuration": 0.2, "logoAndProgressLogoFadeInDelay": 0.2,
                              "minDuration": 1, "progressBarColor": 15258234, "progressBarHeight": 8, "progressBarMaxWidth": 200,
                              "progressBarMinWidth": 40, "progressBarWidthPercent": 30, "showGDevelopSplash": True, "showProgressBar": True},
            "watermark": {"placement": "bottom-left", "showWatermark": True},
            "authorIds": [], "authorUsernames": [], "categories": [], "playableDevices": [], "extensionProperties": [],
            "platforms": [{"name": "GDevelop JS platform"}], "currentPlatform": "GDevelop JS platform",
        },
        "resources": {"resources": list(recursos.values())},
        "objects": objs,
        "objectsFolderStructure": {"folderName": "__ROOT", "children": [{"objectName": x["name"]} for x in objs]},
        "objectsGroups": [],
        "variables": variables(),
        "layouts": [escena(n) for n in ESCENAS],
        "externalEvents": [{
            "associatedLayout": "MenuInicio", "lastChangeTimeStamp": 0, "name": "Libreria",
            "events": [
                comentario("Lógica completa del juego en JavaScript. No editar aquí: editar herramientas/juego_js/libreria.js "
                           "y volver a ejecutar herramientas/generar_proyecto.py."),
                js(lib.split("\n")),
            ],
        }],
        "eventsFunctionsExtensions": [],
        "externalLayouts": [],
    }
    return p


if __name__ == "__main__":
    p = proyecto()
    with open(os.path.join(JUEGO, "game.json"), "w", encoding="utf-8") as fh:
        json.dump(p, fh, indent=2, ensure_ascii=False)
    print("game.json:", len(p["resources"]["resources"]), "recursos,", len(p["objects"]), "objetos,", len(p["layouts"]), "escenas")
