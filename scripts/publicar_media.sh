#!/bin/bash
# Sube los archivos de una carpeta de salida a la rama "media" (reemplaza su contenido: solo se guarda el último lote).
# Uso: scripts/publicar_media.sh /ruta/salida/AAAA-MM-DD
set -e
SRC="$1"; FECHA=$(basename "$SRC")
REMOTE=$(git -C "$(dirname "$0")/.." remote get-url origin)
D=$(mktemp -d)
cd "$D"; git init -q; git checkout -q -b media
git config user.name "Teo Larrea bot"; git config user.email "bot@users.noreply.github.com"
mkdir -p "$FECHA"; cp "$SRC"/*.mp4 "$SRC"/*.jpg "$FECHA"/
git add "$FECHA"; git commit -qm "media $FECHA"
git remote add origin "$REMOTE"; git push -q -f origin media
echo "BASE_URL=https://raw.githubusercontent.com/Machizb16/teolarrea-contenido/media/$FECHA"
