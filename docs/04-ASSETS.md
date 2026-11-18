# 04 — Guía de estilo e inventario de assets

## Reglas de estilo (iguales en todos los assets)

- Pixel art en vista cenital con ligera inclinación frontal (como los juegos de rol clásicos de consola portátil).
- Personajes en celdas de **32×32**; efectos en 32×32 o 64×64; retratos de diálogo en 64×64.
- Contorno de 1 píxel en `#1A1420` (nunca negro puro).
- Sombreado plano: un tono base, uno de luz y uno de sombra. Sin degradados ni suavizado.
- Fondo transparente (PNG).
- Direcciones: abajo, arriba y derecha. La izquierda se obtiene espejando la derecha en GDevelop.

## Paleta

| Grupo | Colores |
| --- | --- |
| Fuego | `#8E1B1B` `#D9481E` `#F28C28` `#C9A227` |
| Agua | `#1E4F8C` `#3A86C8` `#8FD3F0` `#F2F7FA` |
| Tierra | `#3F5A2A` `#6B8E3D` `#7A5230` `#C29A5B` |
| Aire | `#F4F1E8` `#C8C8C0` `#E8D27A` `#9AA3A8` |
| El Ciclo Roto | `#24222B` `#3B3846` `#5A5566` |
| Pieles | `#F2C9A0` `#D9A06B` `#A86B3C` `#6E4426` |
| Pelo y oscuros | `#2B2230` `#4A3B32` |
| Contorno | `#1A1420` |

Todos los assets se ajustan a esta paleta con el script de `herramientas/` antes de importarlos.

## Nombres de archivo

`<personaje>_<accion>_<direccion>_<cuadro>.png`, por ejemplo `ryu_caminar_abajo_0.png`.
Efectos: `efecto_<nombre>_<cuadro>.png`. Interfaz: `ui_<nombre>.png`. Tiles: `tiles_<zona>.png`.

## Personajes

### Animaciones de los jugables (Ryu, Gao, Nerea)

| Animación | Direcciones | Cuadros por dirección | Total |
| --- | --- | --- | --- |
| reposo | 3 | 2 | 6 |
| caminar | 3 | 4 | 12 |
| golpe | 3 | 3 | 9 |
| poder (pose de lanzar) | 3 | 2 | 6 |
| defensa | 3 | 1 | 3 |
| danio | 1 (abajo) | 1 | 1 |
| derribado | 1 | 1 | 1 |

Más un retrato de 64×64 por personaje (`retrato_ryu.png`, etc.).

### Otros personajes

| Personaje | Animaciones | Retrato |
| --- | --- | --- |
| Tsering | reposo (3×2), caminar (3×4), lanzar (3×2) | Sí |
| Norbu | reposo, caminar, ataque, invocar (2 cuadros), derribado | Sí |
| Soldado (base) | caminar (3×4), ataque (3×3), danio (1) | No |
| Soldado: variantes | Fuego, agua, tierra, aire por cambio de paleta | No |
| Ciudadanos (2 o 3) | reposo y caminar abajo | No |
| Daichi | Solo retrato (aparece en el diario) | Sí |

## Efectos

| Archivo base | Tamaño | Cuadros |
| --- | --- | --- |
| efecto_bola_fuego | 32 | 4 |
| efecto_llamarada | 64 | 6 |
| efecto_rafaga_aire | 32 | 4 |
| efecto_latigazo_agua | 64 | 4 |
| efecto_congelado (sobre el enemigo) | 32 | 2 |
| efecto_curacion | 64 | 4 |
| efecto_roca | 32 | 1 + 3 de impacto |
| efecto_muro_tierra | 96×32 | 3 (aparecer) |
| efecto_cupula_tierra | 96 | 4 |
| efecto_proyectil_soldado_<elemento> | 16 | 2 por elemento |
| efecto_impacto | 32 | 3 |
| efecto_fuego_suelo (incendio) | 32 | 4 |
| efecto_sello | 96 | 4 |
| efecto_aura_avatar | 64 | 6 |

## Escenarios

| Archivo | Contenido |
| --- | --- |
| tiles_ciudad | Calles, aceras, plaza, pasto, fachadas y techos rojos y terracota, faroles dorados, bancas, letreros, fuente (3 cuadros de agua), símbolo pintado en la pared |
| tiles_tierra | Sendero, roca, acantilados, entrada de mina con vigas, suelo y paredes de mina, rieles, vagoneta, lámparas, cámara sellada con emblema de tierra |
| tiles_arena | Plataforma de piedra blanca y gris, nubes, columnas, banderas al viento |
| obj_puerta_elemental | Estados: cerrada tierra, cerrada tierra y agua, abriéndose (3 cuadros), abierta |
| obj_pilar | Entero y roto |
| obj_pistas | Símbolo (pista 1), documento (pista 2), diario (pista 3) |
| fondo_pelea_plaza, fondo_pelea_canon, fondo_pelea_mina | 640×360 |

## Interfaz

- Barra de vida y de energía por jugador con marco de su color (fuego, tierra, agua).
- Iconos de elemento 16×16: fuego, aire, agua, tierra.
- Caja de diálogo (9-slice) con espacio para retrato y nombre.
- Pantalla de título, 4 paneles de intro, panel final, pantalla de derrota (640×360).
- Iconos de teclas y botones de mando para los avisos de controles.
- Fuente pixel con licencia libre (por ejemplo, una de Google Fonts con licencia OFL).

## Audio

| Archivo | Uso |
| --- | --- |
| musica_exploracion | Ciudad y zona de tierra |
| musica_pelea | Escena de pelea |
| musica_jefe | Arena final |
| sfx_fuego, sfx_aire, sfx_agua, sfx_tierra | Poderes |
| sfx_golpe, sfx_danio, sfx_derribo | Combate |
| sfx_puerta, sfx_pista, sfx_desbloqueo | Exploración |
| sfx_dialogo, sfx_menu | Interfaz |

## Prompts para generar las imágenes

Consejos para mantener la identidad:
- Generar primero a Ryu, aprobarlo y usar esa imagen como referencia en las demás generaciones.
- Pedir siempre hojas completas, no imágenes sueltas.
- La IA casi nunca respeta la cuadrícula exacta: después se reduce, se ajusta a la paleta y se corta con los scripts.
- Escribir los prompts en inglés suele dar mejores resultados.

### Texto base (va al inicio de todos los prompts de personajes)

```
Pixel art sprite sheet for a top-down RPG, classic 16-bit handheld style,
3/4 top-down view. Each frame fits in a 32x32 pixel cell, frames arranged
in a clean grid with equal spacing. 1-pixel dark outline (#1A1420), flat
shading with one highlight and one shadow tone, limited palette, no
anti-aliasing, no gradients, transparent background. Rows: facing down,
facing up, facing right. Columns: idle (2 frames), walk (4 frames).
```

### Personajes

- **Ryu:** `A 17-year-old boy, short spiky black hair, confident grin, modern streetwear inspired by fire martial arts: dark red hooded jacket with gold trim, black pants, red sneakers, fingerless gloves. Palette: #8E1B1B #D9481E #F28C28 #C9A227, skin #F2C9A0, hair #2B2230.`
- **Gao:** `A 17-year-old boy, broad and sturdy build, calm serious expression, short brown hair, green and brown work vest over an olive t-shirt, cargo pants, heavy boots, leather bracers. Palette: #3F5A2A #6B8E3D #7A5230 #C29A5B, skin #D9A06B.`
- **Nerea:** `A 17-year-old girl, long dark hair in a low braid, kind expression, blue windbreaker with white details, light blue scarf, dark pants, water flask on her belt. Palette: #1E4F8C #3A86C8 #8FD3F0 #F2F7FA, skin #A86B3C.`
- **Tsering:** `An elderly bald man, gentle face, short white beard, loose modern robes in off-white and soft yellow, light grey scarf, wooden walking staff. Palette: #F4F1E8 #C8C8C0 #E8D27A #9AA3A8.`
- **Norbu:** `A lean man around 40, shaved head, calm sharp eyes, long dark grey coat over off-white clothes, pale yellow sash, a symbol on the chest: a circle with four small element marks cut by a diagonal line. Palette: #24222B #3B3846 #F4F1E8 #E8D27A.`
- **Soldado:** `A masked soldier of a rebel organization, dark grey hooded uniform, face fully covered by a plain mask, small circle symbol on the chest, a red arm band (#D9481E). Palette: #24222B #3B3846 #5A5566 #D9481E.` (Las otras variantes se sacan cambiando el rojo de la banda con el script).

### Retratos

```
Pixel art character portrait, 64x64 pixels, bust view facing slightly to
the right, same character design as the reference, 1-pixel outline
#1A1420, limited palette, no anti-aliasing, transparent background.
```

### Efectos

```
Pixel art VFX sprite sheet, top-down RPG, <N> frames in a single row,
<32x32 o 64x64> pixels per frame, <descripción del efecto>, limited
palette <colores del elemento>, no anti-aliasing, transparent background.
```

Descripciones: bola de fuego redonda con estela corta; ráfaga de aire en remolino blanco; látigo de agua curvo con salpicaduras; cristales de hielo encerrando una figura; anillo de luz verde agua que sube; roca irregular con polvo; muro de tierra que emerge del suelo; aura con los cuatro elementos girando alrededor de un personaje; círculo mágico en el suelo con el símbolo roto.

### Escenarios

```
Pixel art top-down tileset, 32x32 tiles arranged on a grid, 3/4 view,
limited palette, no anti-aliasing. <descripción>
```

- **Ciudad:** `modern city plaza of a fire nation: warm red brick streets, terracotta roofs, golden street lamps, small shops, benches, a stone fountain in the center, potted plants.`
- **Tierra:** `rocky mountain path and canyon cliffs, a mine entrance with wooden supports, mine interior floor and walls, rails, a mine cart, hanging lamps, a sealed stone door with an earth emblem.`
- **Arena:** `high-altitude open-air stone platform above the clouds, white and pale grey stone, wind banners, four tall pillars.`

## Orden de producción

1. Ryu (hoja completa) → aprobar estilo → probar en GDevelop.
2. Gao, Nerea, Tsering, Norbu, soldado base.
3. Retratos.
4. Tiles de ciudad y fondo de pelea de la plaza.
5. Efectos de los poderes.
6. Tiles de tierra, fondos de cañón y mina, puertas y pistas.
7. Arena, sello, pilares y aura.
8. Interfaz y paneles.
9. Audio.
