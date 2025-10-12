#!/bin/bash

# Define la ruta absoluta al script de Python
PYTHON_SCRIPT="/home/gerardo/Scripts_Python/main.py"
DOWNLOADS_DIR="/home/gerardo/Descargas"

echo "Iniciando monitoreo continuo y estable de descargas. Presiona Ctrl+C para detener."

# Monitorea la creación y movimiento de archivos
# La opción '-m' (monitor) asegura que el script se ejecute continuamente.
inotifywait -q -m -e create -e moved_to "$DOWNLOADS_DIR" |
while read -r directory events filename; do
    
    # --- FILTRADO DE ARCHIVOS TEMPORALES ---
    # 1. Ignorar archivos ocultos (.file)
    if [[ "$filename" == .* ]]; then
        continue
    fi
    
    # 2. Ignorar archivos de descarga en curso de Chrome/Chromium
    if [[ "$filename" == *.crdownload ]]; then
        continue
    fi
    
    # 3. Ignorar archivos temporales genéricos
    if [[ "$filename" == *.tmp ]]; then
        continue
    fi
    
    # 4. Dar un pequeño retraso para permitir que el navegador finalice y renombre el archivo.    
    sleep 3 
    
    # --- EJECUCIÓN ---
    echo "--- Archivo Detectado: $filename. Organizando... ---"
    # Pasa el nombre del archivo ($filename) como argumento
    /usr/bin/python3 "$PYTHON_SCRIPT" "$filename"
    
done
    