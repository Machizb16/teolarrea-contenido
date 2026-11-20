#!/bin/bash
# Prepara un entorno limpio: dependencias de Python y ffmpeg.
python3 -c "import numpy, scipy, PIL" 2>/dev/null || pip install -q --break-system-packages numpy scipy pillow
which ffmpeg >/dev/null || (sudo apt-get update -q && sudo apt-get install -y -q ffmpeg)
echo "entorno listo"
