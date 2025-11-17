from pathlib import Path
import os
import shutil
import sys # Añadido para procesar el archivo específico pasado por Bash

class DownloadOrganizer:
    """
    Clase encargada de la lógica de organizar archivos en la carpeta de Descargas
    basándose en su extensión.
    """

    # Diccionario de mapeo de extensiones a nombres de carpeta
    # ... (EXT_TO_DIR sin cambios) ...
    EXT_TO_DIR = {
        # Imágenes
        'jpg': 'Imágenes', 'jpeg': 'Imágenes', 'png': 'Imágenes', 'gif': 'Imágenes', 'svg': 'Imágenes', 'webp': 'Imágenes',

        # Video
        'mp4': 'Video', 'mkv': 'Video', 'avi': 'Video', 'mov': 'Video',

        # Audio
        'mp3': 'Audio', 'wav': 'Audio', 'flac': 'Audio', 'm4a': 'Audio',

        # Documentos - Oficina
        'pdf': 'Documentos/Oficina', 'docx': 'Documentos/Oficina', 'xlsx': 'Documentos/Oficina',
        'pptx': 'Documentos/Oficina', 'doc': 'Documentos/Oficina', 'xls': 'Documentos/Oficina',

        # Documentos - Texto Plano
        'txt': 'Documentos/Texto_Plano', 'csv': 'Documentos/Texto_Plano', 'log': 'Documentos/Texto_Plano',

        # Comprimidos e Instaladores
        'zip': 'Comprimidos', 'rar': 'Comprimidos', 'gz': 'Comprimidos', 'deb': 'Instaladores',
    }

    def __init__(self):
        username = os.getlogin()
        self.downloads_dir = Path(f"/home/{username}/Descargas")
        # Carpeta  para archivos no clasificados 
        self.unclassified_dir = self.downloads_dir / "No_Clasificados"
        self.results = {'moved': 0, 'skipped': 0, 'errors': 0}
        print(f"Iniciando organizador para: {self.downloads_dir}")


     # --- NUEVO MÉTODO PARA CONTAR ---
    def count_screenshots(self, screenshot_dir_path: str = "/home/gerardo/Imágenes/Capturas de pantalla") -> int:
        """
        Cuenta el número de archivos dentro de la carpeta de capturas de pantalla.
        """
        screenshots_dir = Path(screenshot_dir_path)
        
        if not screenshots_dir.is_dir():
            return 0

        # Contar solo archivos (ignorando subdirectorios)
        return sum(1 for item in screenshots_dir.iterdir() if item.is_file())   


    # --- MÉTODO DE ELIMINACIÓN (MODIFICADO) ---
    def delete_screenshots(self, screenshot_dir_path: str = "/home/gerardo/Imágenes/Capturas de pantalla"):
        """
        Elimina de forma permanente todos los archivos dentro de la carpeta
        especificada para capturas de pantalla. (Asume que la confirmación ya fue hecha).
        """
        screenshots_dir = Path(screenshot_dir_path)
        
        if not screenshots_dir.is_dir():
            print(f"Advertencia: El directorio de capturas de pantalla no existe en: {screenshots_dir}")
            return

        deleted_count = 0
        print(f"\n--- Iniciando eliminación de archivos en {screenshots_dir} ---")
        
        try:
            # Iterar sobre todos los elementos dentro de la carpeta
            for item in screenshots_dir.iterdir():
                if item.is_file():
                    item.unlink()  # Elimina el archivo
                    deleted_count += 1
            
            print(f"\n✅ Eliminación completada. Total de archivos borrados: {deleted_count}")
        
        except Exception as e:
            print(f"Error al intentar eliminar archivos: {e}")

    # --- FUNCIÓN PARA GESTIONAR DUPLICADOS ---
    def _generate_unique_name(self, destination_path: Path, item_name: str) -> Path:
        """
        Genera un nombre de archivo único añadiendo un contador (ej. archivo(1).ext) 
        si el nombre original ya existe en la ruta de destino.
        """
        destination_file_path = destination_path / item_name
        
        # Si no existe, devuelve la ruta original
        if not destination_file_path.exists():
            return destination_file_path

        # Si ya existe, prepara el renombramiento
        # Separar nombre de extensión, manejando casos sin extensión
        if '.' in item_name:
            base_name, suffix = item_name.rsplit('.', 1)
            suffix = '.' + suffix
        else:
            base_name, suffix = item_name, ''
        
        counter = 1
        while True:
            # Crea el nuevo nombre: "nombre (1).ext"
            new_name = f"{base_name} ({counter}){suffix}"
            new_path = destination_path / new_name
            
            if not new_path.exists():
                return new_path # Devuelve el primer nombre único encontrado
            
            counter += 1

    def _get_destination_path(self, item: Path) -> Path:
        """
        Determina la ruta completa de destino. Si no está mapeada, usa la carpeta 'Otros_Descargas'.
        """
        ext = item.suffix.lstrip('.').lower()
        destino_relativo = self.EXT_TO_DIR.get(ext)
        
        if destino_relativo:
            # Archivo clasificado: ruta dentro de Descargas
            return self.downloads_dir / destino_relativo
        else:
            # Archivo NO clasificado: ruta a la carpeta externa
            return self.unclassified_dir

    def organize_files(self, specific_file: str = None):
        """
        Método principal que mueve un archivo específico o itera sobre la carpeta.
        """
        if not self.downloads_dir.is_dir():
            print(f"Error: La carpeta {self.downloads_dir} no existe.")
            return

        # Crea la carpeta externa para no clasificados
        self.unclassified_dir.mkdir(parents=True, exist_ok=True) 

        # Lógica para procesar un solo archivo (ideal con monitor.sh)
        if specific_file:
            items_to_process = [self.downloads_dir / specific_file]
        else:
            # Procesar toda la carpeta (lógica anterior, menos eficiente)
            items_to_process = self.downloads_dir.iterdir()
            
        
        for item in items_to_process:
            # Solo procesar archivos
            if item.is_file() and item.suffix:
                
                destination_path = self._get_destination_path(item)
                
                # Crea la subcarpeta de destino si no existe
                destination_path.mkdir(parents=True, exist_ok=True) 
                
                # Obtiene la ruta de destino, renombrando si ya existe un duplicado
                destination_file_path = self._generate_unique_name(destination_path, item.name)

                try:
                    # Mueve y renombra el archivo
                    item.rename(destination_file_path)
                    
                    # Mensajes de log para el usuario
                    if destination_path == self.unclassified_dir:
                        # Muestra si el archivo fue renombrado al ir a 'Otros_Descargas'
                        move_msg = f"Movido (No clasificado): {item.name} -> {destination_file_path.name} en {destination_path.name}"
                    elif destination_file_path.name != item.name:
                        # Muestra si fue renombrado al ir a una carpeta clasificada
                        relative_path = destination_path.relative_to(self.downloads_dir)
                        move_msg = f"Movido (Duplicado - Renombrado): {item.name} -> {destination_file_path.name} en {relative_path}"
                    else:
                        # Mensaje normal
                        relative_path = destination_path.relative_to(self.downloads_dir)
                        move_msg = f"Movido: {item.name} -> {relative_path}"
                        
                    print(move_msg)
                    self.results['moved'] += 1
                    
                except Exception as e:
                    print(f"Error: No se pudo mover {item.name}. Razón: {e}")
                    self.results['errors'] += 1

        print("\n--- Resumen de la Organización ---")
        print(f"Archivos movidos: {self.results['moved']}")
        print(f"Archivos saltados: {self.results['skipped']}")
        print(f"Errores: {self.results['errors']}")