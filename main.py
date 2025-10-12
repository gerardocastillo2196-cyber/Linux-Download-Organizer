# main.py
from organizer_logic import DownloadOrganizer
import sys # Importante para leer argumentos

if __name__ == "__main__":
    # Lee el nombre del archivo del argumento de línea de comandos si existe
    file_to_organize = sys.argv[1] if len(sys.argv) > 1 else None

    organizer = DownloadOrganizer()
    
    # Pasa el nombre del archivo a la función
    organizer.organize_files(file_to_organize)