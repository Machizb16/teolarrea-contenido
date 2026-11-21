# Contenido diario de Teo Larrea: procedimiento

Este repositorio genera cada día **2 piezas de vídeo vertical** para promocionar los libros de Teo Larrea. Cada día se eligen al azar **dos libros distintos** entre cuatro: «Nadie se va del todo» (`nadie`) y los tres de la colección Libros prohibidos: «No abras este libro» (`abras`), «No mires este libro» (`mires`) y «No creas este libro» (`creas`). Cada pieza se deja como **BORRADOR en Buffer** para TikTok (subido con Zapier) y como **vídeo PRIVADO en YouTube** (subido con Zapier) para YouTube Shorts. **Nunca publiques nada directamente**: el autor revisa y publica a mano.

## Datos fijos
- **Buffer (por Zapier):** organización `6b00e2681362765e2282a51e`, canal TikTok `6b00e2d0ece6dfde5f3c1b2e`. Los borradores no tienen límite mensual.
- **Metricool:** blogId `7495260`, zona horaria `Europe/Madrid`. Solo es la alternativa si fallan Buffer o Zapier.
- **Zapier:** app YouTube (`YouTubeV4CLIAPI`), acción `upload_video`. El plan gratuito permite 5 subidas al día y 100 tareas al mes.
- **Repositorio:** `Machizb16/teolarrea-contenido`. Rama `main` para el código, las ideas y el estado; rama `media` para los vídeos del día, que se sobrescribe en cada ejecución.
- **Fichas y reglas de spoilers:** `docs/libro.md` («Nadie se va del todo») y `docs/coleccion.md` (los otros tres). Lee la que corresponda antes de crear ideas nuevas y usa SOLO lo que pone en ella.

## Pasos de cada ejecución
1. Ejecuta `bash scripts/setup.sh`.
2. Ejecuta `TRABAJO=/tmp/teolarrea python3 src/diario.py --n 2`. Tarda unos 4 minutos y escribe `/tmp/teolarrea/salida/<fecha>/manifest.json`.
   - Elige solo los libros y las ideas. Al final imprime cuántas ideas quedan sin usar de cada libro.
   - También elige solo la música (`src/musica.py`: cine, piano, pulso, lofi, pizzicato o ambiente) y el formato de cada pieza (gancho en franja oscura, franja roja o palabra a palabra; texto en cursiva, mayúsculas o máquina de escribir; transiciones por fundido, corte o zoom), distintos entre las dos piezas del día. Quedan anotados en el manifest (`musica`, `formato`).
   - La primera vez que sale un libro de la colección, también genera sus escenas de cierre (es normal que tarde algo más).
   - Si responde «NO QUEDAN IDEAS», haz antes el paso 7 y repite este paso.
3. Ejecuta `bash scripts/publicar_media.sh /tmp/teolarrea/salida/<fecha>`. Devuelve `BASE_URL`.
   - Comprueba con `curl -sI` que `BASE_URL/<archivo>.mp4` responde 200.
   - El script también publica `feed.xml` (RSS de los vídeos del día). Ahora no se usa; no hagas nada con él.
4. Por cada pieza del manifest:
   **a) TikTok: BORRADOR en Buffer con Zapier.** Llama a `execute_zapier_write_action` con `selected_api: "BufferCLIAPI"`, `action: "update"` (Add to Queue) y estos `params`:
     - `organizationId: "6b00e2681362765e2282a51e"` · `channelId: "6b00e2d0ece6dfde5f3c1b2e"` (teolarreabooks TikTok)
     - `method: "draft"` (OBLIGATORIO: se guarda como borrador, no se publica) · `attachment: "video"`
     - `text`: el campo `texto` del manifest
     - `dynamic_properties: {"video": "BASE_URL/<id>_<slug>.mp4", "scheduling_type": "direct"}`
   - Si Buffer falla, crea en su lugar un borrador de TikTok en Metricool con `createScheduledPost` y dilo en el resumen:
     - **date / publicationDate:** la primera pieza para mañana a las 13:00 y la segunda a las 20:00, hora de Madrid.
     - **info:** `draft: true` (OBLIGATORIO), `autoPublish: true`, `media: [BASE_URL/<id>_<slug>.mp4]`, `videoThumbnailUrl: BASE_URL/<id>_<slug>.jpg`, `providers: [{"network":"tiktok"}]`, `text`: `texto`, `tiktokData`: `{"privacyOption":"PUBLIC_TO_EVERYONE","commercialContentOwnBrand":true,"commercialContentThirdParty":false,"title":<titulo_tiktok>,"isAigc":true,"autoAddMusic":false,"disableComment":false,"disableDuet":false,"disableStitch":false,"photoCoverIndex":0}` y el resto de campos por defecto (`descendants: []`, `smartLinkData: {"ids": []}`, etc.).

   **b) YouTube Shorts: vídeo PRIVADO con Zapier.** Llama a `execute_zapier_write_action` con `selected_api: "YouTubeV4CLIAPI"`, `action: "upload_video"` y estos `params`:
     - `title`: `titulo_youtube` · `description`: `texto` · `tags`: `tags_youtube`
     - `video`: `BASE_URL/<id>_<slug>.mp4` · `thumbnail`: `BASE_URL/<id>_<slug>.jpg`
     - `privacy_status: "private"` (OBLIGATORIO: el autor lo pasa a público a mano) · `made_for_kids: false` · `notify_subscribers: false`
     - `default_language: "es"` · `default_audio_language: "es"`
     - Apunta el enlace del vídeo que devuelva (`https://youtu.be/<id>`).
   - Si Zapier falla (sin conexión, cuota o error), crea en su lugar un borrador de YouTube en Metricool como en a), con `providers: [{"network":"youtube"}]` y `youtubeData`: `{"title":<titulo_youtube>,"type":"short","privacy":"public","tags":<tags_youtube>,"category":"ENTERTAINMENT","madeForKids":false,"isAiGeneratedContent":true}`, y dilo en el resumen.
   - Si Metricool también da un error, NO publiques nada por otra vía: anótalo en el resumen.
5. Cuando estén creados los borradores y los vídeos privados, ejecuta `python3 src/diario.py --marcar <id1> <id2>`. Después haz commit de `estado.json` en `main` y súbelo con `git push`.
6. **Resumen final** para el autor, en español y breve: el libro, el título y la música de cada pieza, si cada borrador de TikTok quedó en Buffer (o en Metricool, con su `plannerUrl`), el enlace de cada vídeo privado de YouTube e ideas que quedan sin usar de cada libro. Si a algún libro le quedan menos de 4, avisa de que el paso 7 ya se ha hecho o se hará.
7. **Ampliar ideas**, solo para los libros a los que les queden menos de 4 sin usar (el paso 2 los marca con «AMPLIAR»):
   - Añade 10 ideas nuevas de ese libro a `ideas.json`, siguiendo el formato de las existentes del mismo libro y las reglas de su ficha.
   - Ids consecutivos: `nXX` para Nadie, `aXX` para No abras, `mXX` para No mires y `cXX` para No creas. Las de la colección llevan el campo `"libro"` (`abras`, `mires` o `creas`).
   - No repitas ganchos ya usados y alterna los fondos.
   - Fondos de «Nadie se va del todo»:
     - `walter_front`, `walter_face`, `walter_prof`
     - `garage_shelf`, `garage_window`, `garage_wide`
     - `kenn`, `ghost`, `desert`, `lights`, `headlights`, `dossier`, `radar`, `card`, `hangar_door`
     - `{"clock":[h,m]}`
     - `{"notebook":["línea", ...]}` (máximo 3 líneas cortas)
     - `{"sketch":N, "zoom":[z0,z1], "centro":[[x,y],[x,y]], "luz":[[x,y],[x,y]]}` con N de 0 a 8. Bocetos: 0 calle con coche gris · 1 plano del taller · 2 tira de metal · 3 mapa de Groom Lake · 4 A-12 · 5 hangar 7 y su raíl · 6 luces sobre la sierra · 7 la pieza · 8 calle en 1986. El boceto 9 no está disponible.
   - Fondos de la colección (ver `src/coleccion.py` y los ejemplos de `ideas.json`):
     - No abras: `faro`, `tipos`, `llave_carta`, `{"pagina":{"notas":["nota corta", ...]}}` (máximo 3), `{"numeros":{}}` o `{"numeros":{"resaltar":N,"desde":s}}`, `{"palabras":[12 palabras]}`
     - No mires: `camara`, `{"camara":{"cuenta":10}}`, `telefono`, `cuenta_atras`, `{"foto":{"anio":AAAA}}`, `{"foto":{"anio":AAAA,"cambio":C}}` con C en `estrella`, `lampara`, `cuadro`, `vela` o `cortina`; `{"foto":{"anio":AAAA,"cuenta":10}}`. No uses nunca el año 1996 en una foto.
     - No creas: `sobre`, `pueblo`, `anuncio`, `{"telegrama":["LÍNEA STOP", ...]}`, `{"rayas":N}`, `{"mentirometro":{"frases":[3 frases],"mentira":i,"desde":5.0}}`
     - Comunes: `{"cubierta":"abras"|"mires"|"creas"}` (la cubierta real del libro, de `assets/cubiertas/`)
   - Colocación del texto: el gancho va arriba en el primer plano, así que el primer plano no puede ser `mentirometro`, `telegrama` ni `anuncio`. Usa `"pos"` (0 = arriba, 1 = abajo) para que el texto no tape el dibujo: unos 0.86 sobre `foto` y `anuncio`, 0.8 sobre `sobre`, 0.75 sobre `tipos`, 0.85 sobre `llave_carta`, 0.3 sobre `pagina` o `numeros`, 0.35 sobre `rayas` y 0.25 sobre `camara`. Sobre `mentirometro` y `palabras`, sin texto.
   - Mentirómetros: frases propias y comprobadas. La mentira tiene que ser un mito conocido y falso, y la solución va en la descripción.
   - Opcional: una idea puede fijar su música con `"musica": "piano"` (o otro estilo de `src/musica.py`).
   - Haz commit y push de `ideas.json`.

## Normas
- No cambies el código salvo para corregir un error que impida generar; si lo cambias, explícalo en el resumen.
- Nunca subas manuscritos, capítulos ni detalles de la trama que no estén en las fichas: este repositorio es público.
- Colección Libros prohibidos: no reveles ni insinúes giros o finales; el libro no lee la mente; no uses el miedo como gancho; no inventes reseñas, estudios ni cifras; no anuncies «No elijas este libro» ni «No leas este libro».
