"""Escribe feed.xml (RSS) con los vídeos del día, para que IFTTT los mande a los borradores de TikTok.
Uso: python3 src/feed.py <carpeta_salida> <BASE_URL> <destino.xml>"""
import sys, json, os, datetime
from xml.sax.saxutils import escape
src, base, dest = sys.argv[1:4]
man = json.load(open(os.path.join(src, 'manifest.json')))
fecha = os.path.basename(src.rstrip('/'))
ahora = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')
items = []
for p in man:
    url = f'{base}/{os.path.basename(p["video"])}'
    items.append(f'''<item><title>{escape(p["titulo_tiktok"])}</title><link>{escape(url)}</link>
<guid isPermaLink="false">{fecha}-{p["id"]}</guid><pubDate>{ahora}</pubDate>
<description>{escape(p["texto"])}</description><enclosure url="{escape(url)}" type="video/mp4" length="{os.path.getsize(p["video"])}"/></item>''')
open(dest, 'w').write(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Teo Larrea - vídeos del día</title>
<link>https://github.com/Machizb16/teolarrea-contenido</link><description>Vídeos para borradores de TikTok</description>
<lastBuildDate>{ahora}</lastBuildDate>
{chr(10).join(items)}
</channel></rss>
''')
print('feed', len(items), 'vídeos')
