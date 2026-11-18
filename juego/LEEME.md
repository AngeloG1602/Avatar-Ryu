# Proyecto de GDevelop — Ryu: El Último Ciclo

Abrir `juego/game.json` con **GDevelop 5.6 o superior** (Archivo → Abrir proyecto). Resolución 640×360, escalado sin suavizado (pixel art).

## Cómo está organizado

| Parte | Dónde |
| --- | --- |
| Escenas (10) | MenuInicio, Controles, Intro, Ciudad, ZonaTierra, Pelea, ArenaFinal, Final, Creditos, Derrota |
| Objetos (28, globales) | Personajes, Soldado (4 elementos en un objeto), Proyectil, Efecto, puertas, pistas, HUD, diálogo, textos… |
| Variables globales | faseHistoria, pistas, aireDesbloqueado, aguaDesbloqueada, tierraDesbloqueada, elementoActivo, peleaActual, escenaRetorno, retornoX/Y, encuentrosHechos, marcas, escenaDerrota |
| Lógica | Hoja de **eventos externos «Libreria»** (un evento de código JavaScript). Cada escena la enlaza y llama a `gdjs.ryu.ejecutar(runtimeScene, "Escena")` |
| Mapas de exploración | Imágenes compuestas con los tiles (`assets/mapas/`) + colisiones y zonas en `herramientas/juego_js/mapas.json` |

La lógica **no se edita en GDevelop**: el código fuente está en `herramientas/juego_js/libreria.js`.
Después de cambiarlo, regenerar el proyecto (con GDevelop cerrado):

```bash
python3 herramientas/generar_proyecto.py
```

Y comprobar que la partida sigue completándose de principio a fin con el simulador:

```bash
node herramientas/pruebas/simular.js
```

Los valores de combate (vida, daño, energía, velocidades) están juntos al inicio de `libreria.js`, en el objeto `AJ`.

## Controles

| Acción | Ryu (J1) | Gao (J2) | Nerea (J3) | Mando |
| --- | --- | --- | --- | --- |
| Moverse | WASD | Flechas | IJKL | Stick / cruceta |
| Golpe | F | Num 1 | U | A |
| Poder 1 / 2 / 3 | R / T / G | Num 4 / 5 / 6 | O / P / H | X / Y / B |
| Defensa | Shift izq. | Num 0 | Espacio | RB |
| Cambiar elemento | Q | — | — | LB |
| Interactuar / diálogo | E | Enter | N | A |
| Pausa | Esc | Esc | Esc | Start |

Los mandos se leen directamente (mando 1 = Ryu, 2 = Gao, 3 = Nerea), sin extensiones.

## Qué probar primero

1. Abrir el proyecto y lanzar la vista previa desde **MenuInicio**.
2. Si el editor muestra algún error al abrir, copiar el mensaje exacto y avisar.
3. Probar con 3 personas en un mismo teclado: algunos teclados de portátil no registran tantas teclas a la vez.
   Si pasa, conectar mandos o cambiar teclas en `TECLAS` dentro de `libreria.js`.

## Limitaciones conocidas

- Los mapas de exploración son imágenes compuestas, no mapas de tiles editables en GDevelop. Las piezas sueltas
  están en `assets/tilesets/` por si se quiere rehacer algún mapa en el editor.
- No se ha podido abrir el proyecto en el editor real durante el desarrollo: está construido con el formato de los
  ejemplos oficiales de GDevelop 5.6 y probado con un simulador del motor (`herramientas/pruebas/simular.js`).
