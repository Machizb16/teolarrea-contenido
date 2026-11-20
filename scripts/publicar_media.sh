#!/bin/bash
# Sube los archivos de una carpeta de salida a la rama "media" (reemplaza su contenido: solo se guarda el último lote).
# Uso: scripts/publicar_media.sh /ruta/salida/AAAA-MM-DD
set -e
SRC="$(cd "$1" && pwd)"; FECHA=$(basename "$SRC")
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE=$(git -C "$ROOT" remote get-url origin)
D=$(mktemp -d)
cd "$D"; git init -q; git checkout -q -b media
git config user.name "Teo Larrea bot"; git config user.email "bot@users.noreply.github.com"
mkdir -p "$FECHA"; cp "$SRC"/*.mp4 "$SRC"/*.jpg "$FECHA"/
BASE="https://raw.githubusercontent.com/Machizb16/teolarrea-contenido/media/$FECHA"
python3 "$ROOT/src/feed.py" "$SRC" "$BASE" feed.xml
git add "$FECHA" feed.xml; git commit -qm "media $FECHA"
git remote add origin "$REMOTE"; git push -q -f origin media
echo "BASE_URL=https://raw.githubusercontent.com/Machizb16/teolarrea-contenido/media/$FECHA"
