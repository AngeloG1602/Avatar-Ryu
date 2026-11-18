# 01 — Documento de diseño del juego

## Ficha

| Campo | Valor |
| --- | --- |
| Título | Ryu: El Último Ciclo |
| Motor | GDevelop 5 |
| Género | Aventura cooperativa con combate, vista cenital |
| Jugadores | 3, local, misma pantalla |
| Controles | Teclado (3 jugadores) y mando |
| Estilo visual | Pixel art, personajes de 32×32 |
| Duración objetivo | 15 a 25 minutos |
| Entrega | 27 de noviembre al 1 de diciembre de 2026 |

## Premisa

Muchas generaciones de avatares después de los que recuerda la historia, el mundo es parecido al nuestro: ciudades modernas, tecnología, naciones convertidas en regiones conectadas. El control de los elementos y el ciclo del Avatar siguen existiendo.

El Avatar anterior, **Daichi** (maestro tierra, nombre por confirmar), murió hace diecisiete años en circunstancias poco claras. Desde entonces nadie sabe quién es el nuevo Avatar. Una organización de maestros rebeldes, **El Ciclo Roto**, lo está buscando para acabar con el ciclo.

En una ciudad de la Nación del Fuego, **Ryu**, un chico de 17 años, descubre en medio de un ataque que puede controlar el aire: es el nuevo Avatar.

## Ubicación en el universo

- El juego ocurre varias generaciones después de Pavi y Nisha (Avatar: Seven Havens). Esos avatares intermedios no se nombran, para no chocar con la historia oficial.
- El ciclo de naciones se respeta: el anterior era de tierra, el actual es de fuego, y el siguiente elemento que despierta es el aire.

## Personajes jugables

| Personaje | Jugador | Nación | Personalidad | Rol en combate | Vida |
| --- | --- | --- | --- | --- | --- |
| Ryu | 1 | Fuego (Avatar) | Impulsivo, apasionado, bromista bajo presión | Daño fuerte y versatilidad | 100 |
| Gao | 2 | Tierra | Firme, paciente, protector | Defensa y control de espacio | 130 |
| Nerea | 3 | Agua | Empática, equilibrada, observadora | Apoyo, curación y control | 90 |

- **Ryu:** creció en la ciudad sin saber que era el Avatar. Empieza dominando fuego, despierta el aire en la primera pelea, aprende agua en la fuente de la plaza y tierra en la mina. Solo puede tener activo uno de los elementos secundarios a la vez.
- **Gao:** amigo de Ryu de toda la vida. Su familia es de la Nación de la Tierra y vive en la ciudad.
- **Nerea:** recién llegada de la zona costera. Conoce a los chicos el día del ataque y decide quedarse con ellos.

## Personajes no jugables

- **Tsering (guía, aire):** el maestro más viejo de la ciudad. Entrena a Ryu, le da las misiones y lo ayuda en lo espiritual. En combate pelea en automático como aliado. Hace años fue el maestro de Norbu y no sabe en qué se convirtió.
- **Norbu (líder de El Ciclo Roto, aire):** maestro aire de nacimiento, fue el mejor amigo de Daichi. Lo vio morir aplastado por la responsabilidad de ser Avatar y concluyó que ninguna persona puede cargar con el equilibrio del mundo. Su plan es separar al nuevo Avatar de su espíritu para cortar el ciclo. Usa la filosofía aire de soltar y dejar ir para justificarlo. No es cruel: cree que está liberando a Ryu.
- **Soldados de El Ciclo Roto:** maestros encapuchados y enmascarados. Una sola base visual con variantes de color por elemento.

## El Ciclo Roto

- **Objetivo conocido desde el inicio:** encontrar y acabar con el Avatar, sembrar caos entre naciones.
- **Misterio:** por qué lo hacen y quién los lidera. Se revela poco a poco con pistas.
- **Símbolo:** un círculo con las cuatro marcas de los elementos, partido por una línea diagonal.

## Estructura de la historia (MVP)

1. **Prólogo en la ciudad:** intro tipo cómic, los tres personajes como NPC, aparece el símbolo pintado en la plaza (pista 1) y la organización ataca.
2. **Primera pelea (tutorial):** los jugadores toman el control. A mitad de la pelea Ryu despierta el aire y los soldados descubren que es el Avatar.
3. **Ciudad tras el ataque:** la plaza arde. Tsering aparece y guía a Ryu para usar la fuente: desbloquea el agua. Tsering explica la situación y los manda a las minas donde trabajó Daichi.
4. **Zona de tierra:** camino de montaña y mina. Peleas, una puerta de tierra, una puerta de tierra y agua, un documento de la organización (pista 2) y la cámara sellada con el diario de Daichi (pista 3). Ryu desbloquea la tierra.
5. **Encuentro con Norbu (mitad del juego):** a la salida de la mina, sin pelea. Norbu dice "Soltar no es perder, es liberar" y Tsering reconoce la frase que él mismo le enseñó.
6. **Arena final:** Norbu activa el sello para separar a Ryu de su espíritu. Los tres jugadores destruyen los pilares y Ryu entra en estado Avatar con los cuatro elementos.
7. **Final:** Ryu vence a Norbu sin destruirlo. El mensaje es que nadie tiene que cargar el ciclo solo. Tsering se lleva a Norbu.

## Pistas

| # | Dónde | Qué revela |
| --- | --- | --- |
| 1 | Plaza de la ciudad | El símbolo de El Ciclo Roto; están por toda la ciudad |
| 2 | Interior de la mina | Documento del plan: encontrar al Avatar y "el sello" |
| 3 | Cámara sellada | Diario de Daichi: Norbu era su mejor amigo y buscaban cómo aliviar la carga del Avatar |

## Fuera del MVP (visión de ampliación)

- Zonas completas de agua, aire y fuego industrial.
- Subcontroles (metal, lava, sangre).
- Cuarto jugador.
- Más avatares anteriores como apariciones espirituales.
