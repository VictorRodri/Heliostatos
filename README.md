# Heliostatos

--- Cómo abrir y ejecutar el proyecto de caracterización de helióstatos ---

Nota: el código de este proyecto se realizó mediante el programa Python e IDLE 3.6.4.

1. Acceder a la página Web donde se ubica el proyecto: https://github.com/VictorRodri/Heliostatos
2. En ella, hacer clic en el botón verde 'Clone or download' > 'Download ZIP'.
3. El proyecto se descargará en el disco duro del equipo, generalmente en 'Documentos' > 'Descargas'. De lo contrario, especificar en qué ruta exacta del equipo se realizará la descarga.
4. Descomprimir el proyecto descargado previamente, usando un software como WinRAR: https://www.winrar.es/descargas
5. Instalar la última versión de Python desde su página Web oficial: https://www.python.org/downloads/
6. Abrir la terminal de comandos de Windows. Para ello, hacer clic en 'Inicio' > 'Ejecutar'. En la ventana que aparecerá, escribir en el cuadro de texto 'cmd' y pulsar Enter.
7. La terminal mostrará la ruta o directorio del sistema donde se ubica usted actualmente, como 'C:\Users\Pc>'. Ir navegando hasta encontrar el directorio que contiene el proyecto descomprimido previamente. Para acceder a una carpeta, escribir 'cd NombreCarpeta' y pulsar Enter. Para salir del directorio actual, escribir 'cd ..'.
8. Una vez se haya navegado al directorio que contiene el proyecto, ejecutarlo con el comando 'estimacion_potencia.py Videos/varios_heliostatos.mp4 50 50', siendo respectivamente el nombre del proyecto '.py' con el software ejecutable, el directorio que contiene el vídeo de helióstatos a ser procesado, y el ancho y alto mínimos del helióstato para su detección y análisis.
9. Durante aproximadamente un minuto, se ejecutará el software que consistirá en medir la radiación de energía que proyecta cada helióstato. Concretamente, la energía se calcula como la sumatoria de los cuadrados de cada componente BGR del helióstato. Aparecerán estos resultados en tiempo de ejecución en la consola, para cada fotograma del vídeo de helióstatos.
10. Si desea cancelar la ejecución del software, pulsar 'Ctrl+C'.