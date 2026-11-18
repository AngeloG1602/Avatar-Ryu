# 03 — Escenas y flujo

## Flujo general

```
MenuInicio → Intro → Ciudad ⇄ Pelea (pelea 1)
                       ↓
                  ZonaTierra ⇄ Pelea (peleas 2 y 3)
                       ↓
                  ArenaFinal → Final → Creditos
Derrota → reintento de la escena donde se perdió
```

## Fases de la historia (`faseHistoria`)

| Valor | Momento |
| --- | --- |
| 0 | Intro y llegada a la plaza |
| 1 | Ataque y primera pelea |
| 2 | Plaza en llamas, encuentro con Tsering, agua desbloqueada |
| 3 | En la zona de tierra |
| 4 | Diario encontrado, tierra desbloqueada |
| 5 | Encuentro con Norbu, rumbo a la arena |
| 6 | Arena final |
| 7 | Final |

## Escenas

### MenuInicio
- Fondo con el título "Ryu: El Último Ciclo".
- Opciones: Jugar, Controles, Salir.
- Muestra cuántos mandos están conectados.

### Intro
- 4 paneles tipo cómic (640×360) con texto. Cada jugador puede avanzar con interactuar.
- Textos en `05-DIALOGOS.md`.

### Ciudad (Nación del Fuego)
- Mapa urbano: calles, plaza central con fuente, casas, faroles, NPC ciudadanos caminando.
- **Fase 0:** los tres personajes son NPC (`puedeControlar` falso). Diálogo de presentación; se ve el símbolo pintado (pista 1).
- **Fase 1:** aparecen soldados, diálogo corto y transición a `Pelea` con `peleaActual = "ciudad1"`.
- **Fase 2 (al volver):** objetos de fuego en la plaza (incendio). Aparece Tsering. Ryu interactúa con la fuente → agua desbloqueada → el fuego se apaga. Diálogo de misión. Salida hacia la zona de tierra por el borde norte.

### ZonaTierra
- Parte exterior: sendero de montaña, cañón, entrada de la mina. Una zona de encuentro (`tierra1`).
- Parte interior (mina): suelo de roca, rieles, vagonetas, lámparas.
  - Puerta 1: requiere tierra.
  - Documento de la organización en el suelo (pista 2).
  - Zona de encuentro (`tierra2`).
  - Puerta 2: requiere tierra y agua.
  - Cámara sellada con el diario de Daichi (pista 3) → tierra desbloqueada.
- Al salir de la mina: encuentro con Norbu (diálogo, sin pelea). Después, transición a `ArenaFinal`.

### Pelea (reutilizable)
- Arena cerrada de 640×360 con fondo según `peleaActual`.
- Lee la configuración de oleadas:

| peleaActual | Fondo | Oleadas | Tsering aliado |
| --- | --- | --- | --- |
| ciudad1 | Plaza | 1) 2 cuerpo a cuerpo → evento: despertar del aire → 2) 2 cuerpo a cuerpo + 1 a distancia | No |
| tierra1 | Cañón | 1) 2 cuerpo a cuerpo + 1 a distancia → 2) 2 cuerpo a cuerpo + 2 a distancia | Sí |
| tierra2 | Mina | 1) 2 cuerpo a cuerpo + 1 a distancia → 2) 3 cuerpo a cuerpo → 3) 2 cuerpo a cuerpo + 2 a distancia | Sí |

- Elementos de los soldados: en la ciudad, fuego y aire; en la zona de tierra, tierra y agua.
- **Despertar del aire (ciudad1):** al terminar la oleada 1 se pausa la pelea, Ryu lanza una ráfaga automática, diálogo corto, `aireDesbloqueado = verdadero`, aviso del botón de cambiar elemento y empieza la oleada 2.
- Tutorial (solo ciudad1): mensajes de controles al inicio (moverse, golpe, poder 1, defensa).

### ArenaFinal
- Plataforma de piedra al aire libre, en las alturas, rodeada de nubes y banderas al viento.
- Diálogo inicial con Norbu → pelea en 3 fases → sello y pilares → estado Avatar → diálogo final.
- Sin Tsering como aliado (aparece en el diálogo final).

### Final
- Diálogo final y panel de cierre.

### Creditos
- Nombres de Ángelo y Nicoll, materia, profesor, herramientas usadas y aviso de que es un proyecto académico inspirado en Avatar.

### Derrota
- Mensaje y botones: Reintentar (vuelve al inicio de la escena) y Menú.

## Interfaz en todas las escenas jugables

- Esquina superior izquierda, centro y derecha: retrato pequeño, barra de vida y barra de energía de cada jugador.
- Junto a Ryu: icono del elemento activo.
- Contador de pistas (0/3) en exploración.
