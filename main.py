# main.py 
from organizer_logic import DownloadOrganizer
import sys 

if __name__ == "__main__":
    file_to_organize = sys.argv[1] if len(sys.argv) > 1 else None

    organizer = DownloadOrganizer()
    
    if file_to_organize:
        # LÓGICA 1: ORGANIZACIÓN DE UN SOLO ARCHIVO (Usado por monitor.sh)
        # Esto se activa cuando se pasa un nombre de archivo como argumento.
        organizer.organize_files(file_to_organize)
    else:
        # LÓGICA 2: MODO MANTENIMIENTO (Se ejecuta cuando llamas a main.py sin argumentos)
        print("\n--- MODO MANTENIMIENTO: Limpieza y Organización de Tareas Pendientes ---")
        
        # ----------------------------------------------------
        # --- 1. TAREA: LIMPIEZA DE CAPTURAS DE PANTALLA ---
        # ----------------------------------------------------
        
        count = organizer.count_screenshots() # 1. Contar cuántos archivos hay
        
        print(f"\n--- Tarea 1/2: Limpieza de Capturas ({count} encontradas) ---")
        
        if count > 0:
            # 2. Informar y PEDIR CONFIRMACIÓN
            print(f"Se encontraron {count} capturas de pantalla en la ruta.")
            print(f"¿Deseas eliminar estas {count} capturas de pantalla de forma permanente? (s/n)")
            
            user_input = input().lower()
            
            if user_input == 's':
                # 3. Eliminar si se confirma
                organizer.delete_screenshots() 
            else:
                print("No se realizó la eliminación de capturas de pantalla.")
        else:
            print("No se encontraron capturas de pantalla para eliminar. Saltando la limpieza.")

        
        # ------------------------------------------------------
        # --- 2. TAREA: ORGANIZACIÓN COMPLETA DE DESCARGAS ---
        # ------------------------------------------------------
        print(f"\n--- Tarea 2/2: Organización de Carpeta Descargas ---")
        # Al llamar a organize_files() sin argumentos, el método procesará *todos* los
        # archivos que queden en /home/gerardo/Descargas.
        organizer.organize_files()