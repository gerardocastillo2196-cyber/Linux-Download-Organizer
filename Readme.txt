Organización Automática de Descargas (Linux)
Este sistema es una solución continua y potente para mantener tu carpeta de descargas siempre limpia. Utiliza Bash para monitorear eventos del sistema y Python para aplicar una lógica de organización detallada.


1. Componentes y Flujo del Sistema
El sistema opera con tres archivos y sigue un flujo preciso para garantizar que los archivos en curso y los duplicados sean manejados correctamente.

Archivo	Tipo	Función
monitor.sh	Bash Script		
Monitoreo Continuo: Utiliza inotifywait para vigilar la carpeta de descargas. Filtra activamente archivos temporales (.crdownload, .tmp). Ejecuta el script de Python, pasándole el nombre del archivo finalizado como argumento.



main.py	Python Script		
Punto de Entrada: Recibe el nombre del archivo del monitor.sh y lo pasa a la clase organizadora.

organizer_logic.py	Python Class		
Lógica Avanzada: Contiene el mapeo de extensiones, maneja el renombrado automático de duplicados y mueve los archivos no clasificados a una carpeta externa, fuera de Descargas.


Exportar a Hojas de cálculo
2. Requisitos Previos

Sistema Operativo: Cualquier distribución de Linux (probado en Ubuntu/Debian).


python3: Debe estar instalado en el sistema (/usr/bin/python3).


inotify-tools: Este paquete es esencial para el monitoreo continuo de Bash.

Instalación en Debian/Ubuntu:

Bash

sudo apt update && sudo apt install inotify-tools
3. Configuración Inicial e Instalación
Paso 3.1: Estructura de Carpetas
Organiza tus archivos en la siguiente estructura. Reemplaza usuario_linux por tu nombre de usuario real en el sistema:

/home/usuario_linux/
├── Descargas/         (Carpeta a Monitorear)
├── Otros_Descargas/   (Carpeta de Destino para Archivos No Clasificados)
└── Scripts_Python/
    ├── monitor.sh
    ├── main.py
    └── organizer_logic.py
Paso 3.2: Ajuste de Rutas en monitor.sh
Debes verificar que las rutas dentro de monitor.sh sean absolutas y correctas.

Contenido a verificar en monitor.sh:

Bash

# Define la ruta absoluta al script de Python
PYTHON_SCRIPT="/home/usuario_linux/Scripts_Python/main.py" 
DOWNLOADS_DIR="/home/usuario_linux/Descargas"

Nota: La lógica de Python determina automáticamente la ruta de Descargas y Otros_Descargas utilizando os.getlogin(), pero el script de monitoreo de Bash necesita las rutas explícitas.

Paso 3.3: Permisos de Ejecución
Debes dar permisos de ejecución al script de Bash.

Bash

cd /home/usuario_linux/Scripts_Python
chmod +x monitor.sh
4. Lógica de Organización Robusta
El sistema implementa dos características clave para asegurar que la carpeta Descargas quede siempre vacía de archivos completados:

A. Manejo de Archivos Duplicados (Renombrado Automático)
Si descargas un archivo que ya existe en la carpeta de destino (ej. descargas imagen.jpg y ya existe Imágenes/imagen.jpg), el script no lo saltará. En su lugar, lo renombrará automáticamente añadiendo un contador y luego lo moverá.


Archivo Original: imagen.jpg 


Archivos Movidos: imagen (1).jpg, imagen (2).jpg, etc. 

B. Mover Archivos No Clasificados a Carpeta Externa
Los archivos con extensiones que no están en el diccionario de mapeo (.iso, archivos sin extensión, etc.) ya no se quedan en una subcarpeta Otros dentro de Descargas. Todos estos archivos son movidos a la carpeta externa: /home/usuario_linux/Otros_Descargas.


Tipo de Archivo	Extensiones Mapeadas	Carpeta de Destino
Documentos	pdf, docx, xlsx, pptx, doc, xls	Descargas/Documentos/Oficina
Imágenes	jpg, png, gif, webp, etc.	Descargas/Imágenes
Video	mp4, mkv, avi, mov	Descargas/Video
Comprimidos	zip, rar, gz	Descargas/Comprimidos
No Clasificados	Cualquier extensión no listada	/home/usuario_linux/Otros_Descargas

Exportar a Hojas de cálculo
5. Ejecución y Control
Iniciar el Monitoreo
Para activar el sistema, ejecuta el script de Bash monitor.sh en tu terminal:

Bash

/home/usuario_linux/Scripts_Python/monitor.sh
Salida Esperada al Inicio:

Iniciando monitoreo continuo y estable de descargas. Presiona Ctrl+C para detener.


Manejo de Temporales y Descargas Largas
El sistema espera automáticamente a que las descargas finalicen antes de mover el archivo:


Filtrado Activo: El script monitor.sh ignora de inmediato cualquier archivo con extensión temporal (.crdownload, .tmp).


Tiempo de Espera: Una vez que el archivo es detectado como finalizado (renombrado), el script espera 3 segundos (sleep 3) para asegurar que el sistema de archivos haya terminado todas las operaciones de escritura.

Solo entonces se ejecuta la lógica de Python para mover el archivo finalizado, clasificado o renombrado a su destino.

Detener el Monitoreo
Para detener el sistema, simplemente regresa a la ventana del terminal donde se está ejecutando el script y presiona las teclas Ctrl + C.
