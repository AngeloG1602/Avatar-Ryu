# Audio

Todo el audio está sintetizado con `herramientas/audio.py` (chiptune, sin samples externos), así que no tiene problemas de licencia.

| Archivo | Uso | Notas |
| --- | --- | --- |
| musica_exploracion.ogg | Ciudad y zona de tierra | Loop exacto de 16 compases, 100 BPM, pentatónica de Re |
| musica_pelea.ogg | Escena Pelea | Loop de 16 compases, 144 BPM, pentatónica de La menor |
| musica_jefe.ogg | Arena final | Loop de 16 compases, 150 BPM, Mi menor con tambores taiko |
| sfx_fuego / aire / agua / tierra | Poderes de cada elemento | |
| sfx_golpe, sfx_danio, sfx_derribo | Combate | |
| sfx_puerta, sfx_pista, sfx_desbloqueo | Exploración | |
| sfx_dialogo, sfx_menu | Interfaz | sfx_dialogo es muy corto: reproducirlo cada 2-3 letras |

Sugerencia en GDevelop: música en un canal con volumen 60 % y con "repetir" activado; efectos al 100 %.
Para regenerar o cambiar una melodía: editar las listas `melodia` en `herramientas/audio.py` y ejecutar
`python3 herramientas/audio.py`.
