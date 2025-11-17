#!/bin/bash

# Define la ruta absoluta al script de Python
PYTHON_SCRIPT="/home/gerardo/Scripts_Python/main.py"
DOWNLOADS_DIR="/home/gerardo/Descargas"

# --- NUEVO: Lógica de Limpieza de Capturas ---
# Ejecuta main.py sin argumentos, lo que activa el "Modo Mantenimiento"
# en main.py y solicita confirmación para borrar las capturas.
/usr/bin/python3 "$PYTHON_SCRIPT"
# ---------------------------------------------


echo "Iniciando monitoreo continuo y estable de descargas. Presiona Ctrl+C para detener."

# Monitorea la creación y movimiento de archivos
# ... (Resto del script inotifywait sin cambios) ...