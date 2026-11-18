# Ryu: El Último Ciclo — instrucciones para Claude Code

Videojuego de clase (Desarrollo de Videojuegos) hecho en **GDevelop 5** por Ángelo y Nicoll.
Juego cooperativo local para **3 jugadores**, vista cenital en **pixel art**, con soporte para **teclado y mando**.
Inspirado en el universo de Avatar, con personajes propios.

**Entrega:** entre el 27 de noviembre y el 1 de diciembre de 2026. El alcance es un MVP: no agregar zonas ni sistemas que no estén en estos documentos sin preguntar.

## Lee primero

1. `docs/01-GDD.md`: historia, personajes, mundo y misiones.
2. `docs/02-MECANICAS.md`: combate, controles, variables y lógica para GDevelop.
3. `docs/03-ESCENAS.md`: lista de escenas, flujo y contenido de cada una.
4. `docs/04-ASSETS.md`: guía de estilo, paleta, inventario de assets, nombres de archivo y prompts para generar imágenes.
5. `docs/05-DIALOGOS.md`: borrador de todos los diálogos.
6. `docs/06-PLAN.md`: plan de trabajo por fechas y checklist de entrega.

## Estructura esperada del repositorio

```
ryu-el-ultimo-ciclo/
├── CLAUDE.md
├── docs/                  # diseño (estos documentos)
├── juego/                 # proyecto de GDevelop (game.json y recursos)
│   └── assets/
│       ├── personajes/
│       ├── enemigos/
│       ├── efectos/
│       ├── tilesets/
│       ├── ui/
│       └── audio/
├── arte_fuente/           # imágenes originales generadas con IA, sin procesar
└── herramientas/          # scripts de procesamiento de assets (Python)
```

## Reglas de trabajo

- El proyecto de GDevelop se crea primero en el editor (escenas y objetos base). Claude Code trabaja sobre los archivos, los assets y los scripts.
- **Antes de editar `game.json`:** el editor de GDevelop debe estar cerrado y debe haber un commit de git reciente. Después de editar, abrir el proyecto en GDevelop y comprobar que carga.
- Si un cambio de eventos es grande o delicado, es preferible escribir los eventos paso a paso (condiciones y acciones) para hacerlos en el editor, en vez de modificar el JSON a mano.
- Nombres de objetos, variables y escenas: en español, sin tildes ni espacios, en camelCase para variables (`vida`, `energiaMax`) y PascalCase para objetos y escenas (`Ryu`, `SoldadoCac`, `ZonaTierra`).
- Nombres de archivos de assets: minúsculas, sin tildes, con guion bajo (ver `docs/04-ASSETS.md`).
- Textos del juego y comentarios en español.
- Activar en el proyecto el renderizado sin suavizado (pixel art) para que los sprites no se vean borrosos.

## Primeras tareas sugeridas para Claude Code

1. Crear los scripts de `herramientas/` para procesar el arte generado con IA:
   - reducir una imagen grande a la cuadrícula real (32×32 por celda) con escalado por vecino más cercano;
   - ajustar los colores a la paleta definida en `docs/04-ASSETS.md`;
   - cortar hojas de sprites en cuadros individuales con los nombres de archivo correctos;
   - generar las variantes de color de los soldados (cambio de paleta).
2. Revisar que cada asset del inventario exista con el tamaño y nombre correctos y listar lo que falta.
3. Escribir la lógica de combate, energía y controles descrita en `docs/02-MECANICAS.md`.
4. Montar el flujo de escenas de `docs/03-ESCENAS.md`.

## Pendientes que no se deben inventar

- Tamaño de tiles y herramienta de mapas que usa el profesor (confirmar antes de hacer los tilesets).
- Nombre definitivo del Avatar anterior (sugerencia actual: Daichi).
