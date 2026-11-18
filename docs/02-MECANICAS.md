# 02 — Mecánicas y lógica para GDevelop 5

Todos los valores son iniciales y se ajustan al probar.

## Configuración del proyecto

- Resolución base: **640×360**, escalado para llenar la pantalla manteniendo proporción.
- Renderizado sin suavizado (pixel art).
- Tiles y sprites de 32×32 (confirmar tamaño de tiles con el profesor).
- Extensión de mandos de GDevelop (Gamepads) para la entrada de mando por número de jugador (1, 2, 3).

## Asignación de jugadores

| Jugador | Personaje |
| --- | --- |
| 1 | Ryu |
| 2 | Gao |
| 3 | Nerea |

Fija para el MVP: así el botón de cambiar elemento solo existe para el jugador 1.

## Controles

| Acción | Jugador 1 (Ryu) | Jugador 2 (Gao) | Jugador 3 (Nerea) | Mando (cualquier jugador) |
| --- | --- | --- | --- | --- |
| Moverse | W A S D | Flechas | I J K L | Stick izquierdo / cruceta |
| Golpe | F | Num 1 | U | A |
| Poder 1 | R | Num 4 | O | X |
| Poder 2 | T | Num 5 | P | Y |
| Poder 3 (especial) | G | Num 6 | H | B |
| Defensa (mantener) | Shift izquierdo | Num 0 | Espacio | RB |
| Cambiar elemento (solo Ryu) | Q | — | — | LB |
| Avanzar diálogo / interactuar | E | Num Enter | N | A |
| Pausa | Esc | Esc | Esc | Start |

Notas:
- Si algún portátil no tiene teclado numérico, reasignar al jugador 2 a otra zona libre del teclado y documentarlo aquí.
- La disposición de botones del mando varía según la marca; probar con el asistente de mapeo de GDevelop o un emulador de mando cuando no haya mando físico.
- Mostrar en pantalla solo el control que se está enseñando en cada momento del tutorial.

## Variables de objeto (Ryu, Gao, Nerea)

| Variable | Tipo | Valor inicial | Uso |
| --- | --- | --- | --- |
| jugador | número | 1, 2 o 3 | Qué jugador lo controla |
| vida | número | 100 / 130 / 90 | Vida actual |
| vidaMax | número | 100 / 130 / 90 | Vida máxima |
| energia | número | 100 | Energía actual |
| energiaMax | número | 100 | Energía máxima |
| puedeControlar | booleano | falso en intros | Bloquea entrada durante diálogos y cinemáticas |
| direccion | texto | "abajo" | "arriba", "abajo", "izquierda", "derecha" |
| defendiendo | booleano | falso | Activo mientras se mantiene defensa |
| derribado | booleano | falso | Vida en 0 |
| congeladoHasta | número | 0 | Solo enemigos (ver Nerea) |

Comportamiento de movimiento: **movimiento de arriba hacia abajo (TopDownMovement)**, 4 direcciones, sin diagonales en animación.

## Variables globales

| Variable | Tipo | Uso |
| --- | --- | --- |
| faseHistoria | número | Avance de la historia (ver `03-ESCENAS.md`) |
| aireDesbloqueado | booleano | Ryu puede usar aire |
| aguaDesbloqueada | booleano | Ryu puede usar agua |
| tierraDesbloqueada | booleano | Ryu puede usar tierra |
| elementoActivo | texto | "aire", "agua" o "tierra" (poder 2 de Ryu) |
| pistas | número | Pistas recogidas (0 a 3) |
| peleaActual | texto | Identificador de la pelea que se va a cargar |
| escenaRetorno | texto | Escena a la que se vuelve al ganar |
| retornoX, retornoY | número | Posición de regreso del grupo |
| encuentrosHechos | estructura | Marca las peleas ya ganadas para no repetirlas |

## Energía

- Se recarga sola: `energia += 10 * TimeDelta()` cada cuadro, sin pasar de `energiaMax`.
- Cada poder comprueba que haya energía suficiente antes de lanzarse; si no hay, no ocurre nada (opcional: parpadeo de la barra).
- Enfriamiento mínimo de 0,4 s entre poderes del mismo jugador (temporizador de objeto).

## Daño

| Acción | Coste de energía | Daño |
| --- | --- | --- |
| Golpe | 0 | 5 |
| Poder 1 | 15 | 10 |
| Poder 2 | 30 | 20 |
| Poder 3 | 50 | 35 |

- **Defensa:** mientras se mantiene, el personaje no se mueve y recibe el 30 % del daño.
- Al recibir daño: parpadeo de 0,5 s de invulnerabilidad y animación de daño.

## Poderes

### Ryu (Avatar)

| Slot | Poder | Comportamiento |
| --- | --- | --- |
| Poder 1 | Bola de fuego | Proyectil recto en la dirección del personaje |
| Poder 2 | Según `elementoActivo` | Aire: ráfaga que empuja enemigos (12 de daño). Agua: latigazo de alcance corto. Tierra: roca lanzada, lenta |
| Poder 3 | Llamarada | Área en forma de cono frente a Ryu |
| Cambiar elemento | — | Rota entre los elementos desbloqueados (aire → agua → tierra). Icono en la interfaz |

- Hasta despertar el aire, el poder 2 y el cambio de elemento están bloqueados.
- **Estado Avatar:** no es un botón. Se activa por guion en la arena final (ver abajo).

### Gao (tierra)

| Slot | Poder | Comportamiento |
| --- | --- | --- |
| Poder 1 | Roca lanzada | Proyectil |
| Poder 2 | Muro | Crea un muro de 3 tiles frente a Gao durante 4 s; bloquea enemigos y proyectiles; tiene 60 de vida |
| Poder 3 | Cúpula de tierra | Zona de radio 96 px durante 5 s; los aliados dentro reciben la mitad de daño |

### Nerea (agua)

| Slot | Poder | Comportamiento |
| --- | --- | --- |
| Poder 1 | Latigazo de agua | Golpe de alcance medio |
| Poder 2 | Congelar | Proyectil; el enemigo alcanzado queda inmóvil 2,5 s (el jefe solo 1 s) y recibe 5 de daño |
| Poder 3 | Curación | Cura 35 de vida a Nerea y a los aliados en radio de 128 px. No hace daño |

### Tsering (aliado automático)

- Sigue al grupo: se mueve hacia el centro de los tres jugadores, a unos 48 px de distancia.
- Cada 4 s lanza una ráfaga de aire al enemigo más cercano (8 de daño).
- Es invulnerable y no ocupa un jugador.
- Aparece en las peleas desde la zona de tierra. No participa en la primera pelea ni en la arena final.

## Proyectiles

- Crear el objeto en la posición del personaje con una fuerza permanente en su dirección.
- Variables: `danio`, `elemento`, `duenio` ("jugador" o "enemigo").
- Se eliminan al chocar con un enemigo, un muro u obstáculo, o tras 1,5 s.
- El elemento del proyectil sirve también para abrir puertas (ver abajo).

## Enemigos

| Tipo | Vida | Comportamiento | Daño |
| --- | --- | --- | --- |
| SoldadoCac (cuerpo a cuerpo) | 30 | Persigue al jugador más cercano | 8 al contacto, enfriamiento 1 s |
| SoldadoDist (a distancia) | 25 | Mantiene unos 150 px de distancia y dispara cada 2 s | 6 por proyectil |

- Cada soldado tiene la variable `elemento` y usa la variante de color y proyectil correspondiente.
- Si está congelado (`congeladoHasta` mayor que el tiempo actual), no se mueve ni ataca y muestra el efecto de hielo encima.

## Jefe: Norbu

| Fase | Condición | Comportamiento |
| --- | --- | --- |
| 1 | Vida de 300 a 151 | Ráfagas de aire cada 2 s y desplazamiento rápido corto cada 5 s |
| 2 | Vida de 150 a 76 | Invoca 2 soldados al entrar en la fase y sigue atacando |
| 3 | Vida 75 o menos | Se vuelve invulnerable y activa el sello |

**Sello (fase 3):**
- Aparece un círculo en el suelo bajo Ryu que le drena 5 de energía por segundo y le impide usar el poder 3.
- Aparecen 3 pilares (40 de vida cada uno). Cualquier jugador puede romperlos, pero el diálogo sugiere uno por jugador.
- Al caer el último pilar: cinemática corta y **estado Avatar**.

**Estado Avatar:**
- Dura 10 s. Ryu es invulnerable, tiene energía infinita y un aura animada con los cuatro elementos.
- Cada segundo, el aura hace 40 de daño en área alrededor de Ryu.
- Norbu deja de ser invulnerable. Al llegar a 0 de vida, termina la pelea y empieza el diálogo final.
- Si Norbu sobrevive a los 10 s, el estado se repite hasta vencerlo (no se puede perder en este punto).

## Derribo y derrota

- Vida en 0: el personaje queda derribado, sin control, durante 5 s, y luego se levanta con el 30 % de la vida si queda al menos un compañero en pie.
- Si los tres están derribados al mismo tiempo: pantalla de derrota y reintento desde el inicio de la escena.

## Cámara compartida

- La cámara se centra en el promedio de las posiciones de los tres jugadores.
- Se aleja un poco si los jugadores se separan, con un límite máximo.
- Los jugadores no pueden salir del área visible (se limita su posición a los bordes de la cámara).

## Puertas elementales

- Objeto `PuertaElemental` con la variable `requiere`: "tierra" o "tierra+agua".
- Se abre cuando un proyectil o poder del elemento requerido la toca.
- Para "tierra+agua": cada elemento marca un impacto y ambos deben ocurrir con menos de 3 s de diferencia; si no, se reinicia.
- Al abrirse: animación de apertura, sonido y se elimina la colisión.
- Encima de la puerta se muestran los iconos de los elementos que pide.

## Peleas como escenas separadas

- En las escenas de exploración hay zonas invisibles de encuentro (`ZonaEncuentro`) con la variable `idPelea`.
- Al entrar un jugador: guardar `escenaRetorno`, `retornoX`, `retornoY` y `peleaActual`, y cambiar a la escena `Pelea`.
- La escena `Pelea` lee `peleaActual`, coloca el fondo y lanza las oleadas definidas en `03-ESCENAS.md`.
- Al vencer todas las oleadas: marcar el encuentro en `encuentrosHechos` y volver a `escenaRetorno` en la posición guardada.

## Diálogos

- Caja de diálogo en la parte inferior con retrato y nombre del personaje.
- Las líneas de cada conversación se guardan en una variable de escena (arreglo) y se avanzan con el botón de interactuar de cualquier jugador.
- Mientras hay diálogo, `puedeControlar` es falso para los tres.
- Para interactuar con un NPC o un objeto: estar cerca (menos de 40 px) y pulsar interactuar.
