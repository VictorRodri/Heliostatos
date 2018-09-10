# Bibliotecas requeridas para este software.
import cv2
import argparse
import time
import numpy as np

start_time = time.time() # Obtener el tiempo de ejecución inicial de este programa.
frame_counter = 0 # Contador de fotogramas totales del vídeo. Se irá incrementando progresivamente en líneas de código posteriores.

# Argumentos o parámetros necesarios para ejecutar este programa a través de la consola de Windows.
parser = argparse.ArgumentParser(description='Parametros del programa.') # Dar un nombre al conjunto de parámetros y asignarlo a la variable 'parser'.
parser.add_argument('directorioVideoHeliostatosCargar', type=str) # Crear el argumento 1: ruta o directorio del vídeo a cargar en el PC.
parser.add_argument('anchoMinimoHeliostato', type=int) # Crear el argumento 3: ancho mínimo del helióstato para su análisis.
parser.add_argument('altoMinimoHeliostato', type=int) # Crear el argumento 4: alto mínimo del helióstato para su análisis.
args = parser.parse_args() # Devuelve información de los parámetros definidos previamente.

# Mostrar en la consola este aviso de cuando se va a ejecutar el programa.
print("")
print("Iniciando programa...")
print("")

# Leer secuencia de imágenes del vídeo a partir del directorio especificado por parámetro.
camara = cv2.VideoCapture(args.directorioVideoHeliostatosCargar)

# Iteración 'while True' para cada fotograma del vídeo, hasta completar todos los fotogramas y llegar al final del vídeo (cambiaría automáticamente de True a False y el bucle 'while' finaliza).
while True:
    
    # Obtener frame. Para ello, se toma un fotograma del vídeo, se guarda en 'frame', y si se ha hecho esta acción correctamente, 'grabbed' valdrá true (verdadero), y viceversa.
    (grabbed, frame) = camara.read()

    # Si se ha llegado al final del vídeo, romper la ejecución de este bucle 'while' y finalizar el programa.
    if not grabbed:
        break

    # Convertir a escala de grises el fotograma actual del vídeo. Para ello, con la variable 'frame' (fotograma del vídeo) capturada anteriormente, se llama a la función 'cv2.COLOR_BGR2GRAY'.
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral a ese fotograma del vídeo. Parámetros de este método: imagen fuente en escala de grises, valor de umbral para clasificar los valores de píxeles de esa imagen,
    # valor máximo a ser representado si el valor del píxel supera al valor del umbral, aplicar un tipo concreto de umbralización (0 porque no se desea hacer esto).
    # NOTA: la variable ‘ret’ que recibe como resultado en este método no es usada en este programa así que se puede ignorar, esto es debido a que no se está aplicando umbralización de Otsu.
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    
    cv2.imshow("Camara2", thresh) # Mostrar vídeo umbralizado en una ventana.
    cv2.waitKey(1) # El programa hará una pequeña pausa (1 milisegundo) para que de tiempo a que se muestren los vídeos y fotogramas en las dos ventanas que se han creado en este código para tal fin.

    # Buscar y detectar todos los contornos o helióstatos del fotograma actual del vídeo.
    # Parámetros del siguiente método: imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquía de familia, marcar la mínima cantidad de puntos (no todos)
    # que forman (delimitan) la figura (helióstato). Argumentos que devolverá dicho método: imagen fuente (sobra), modo de devolución del contorno, método de aproximación del contorno (sobra).
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    # Recorrer solo los dos primeros contornos, los más grandes (siguiente bucle 'for'), para cada fotograma del vídeo (bucle 'while' ejecutándose actualmente).
    # Al no recorrer los demás contornos, éstos serán descartados porque no son muy grandes ni importantes o son falsos.
    for i in range(0,2):
        
        # Obtener las coordenadas del contorno.
        (x, y, w, h) = cv2.boundingRect(contours[i]) # xy: coordenadas de un punto, w: ancho, h: altura.

        # Calcular el área del contorno número 'i', en el fotograma actual del vídeo. 'i' es el iterador del bucle 'for' actual.
        area = cv2.contourArea(contours[i])
        
        # Si el contorno tiene un ancho y alto mayores a los especificados por parámetros, este será analizado y reencuadrado en un rectángulo verde en el vídeo.
        if (w > args.anchoMinimoHeliostato and h > args.altoMinimoHeliostato):

            # Si se está analizando el helióstato número uno en el fotograma actual del vídeo, hacer.
            if (i == 0):
                
                # Dibujar un rectángulo verde alrededor del contorno, en el vídeo.
                # Parámetros: fotograma actual vídeo, esquina superior izquierda, esquina inferior derecha (width: ancho, height: altura), rectángulo color verde, grosor del rectángulo 2 píxeles.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Mostrar en consola que se está analizando el helióstato reencuadrado en un rectángulo verde en el vídeo.
                print("")
                print("- Analizando el helióstato verde...")
                print("")
                
            # Si se está analizando el helióstato número dos en el fotograma actual del vídeo (en caso de que ya exista el otro helióstato en ese mismo fotograma del vídeo), hacer.
            else:
                
                # En este caso, ahora se reencuadra el contorno en un rectángulo rojo, en vez de verde. Así, ambos contornos podrán ser diferenciados si se muestran en el mismo fotograma del vídeo.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

                # Mostrar en consola que se está analizando el helióstato reencuadrado en un rectángulo rojo en el vídeo.
                print("")
                print("- Analizando el helióstato rojo...")
                print("")

            # Leer y analizar todos los píxeles del helióstato.
            def vectorial(frame, x, y):
                
                # Del fotograma actual del vídeo, se leerá únicamente donde haya un helióstato (su ancho y alto), y así con todos los helióstatos de cada fotograma del vídeo.
                m = frame[y+2:y+h-1, x+2:x+w-1] # ANTES: i = frame[y+2:y+h-1, x+2:x+w]
                
                # Matrices BGR resultado de la lectura de ese helióstato.
                mB = m[:, :, 2]
                mG = m[:, :, 1]
                mR = m[:, :, 0]
                
                # Elevar al cuadrado cada dato BGR del helióstato.
                mB2 = np.power(mB, 2)
                mG2 = np.power(mG, 2)
                mR2 = np.power(mR, 2)

                # Realizar la sumatoria acumulativa de cada BGR al cuadrado de ese helióstato.
                sumB = np.sum(mB2)
                sumG = np.sum(mG2)
                sumR = np.sum(mR2)

                # Sumar las anteriores tres componentes entre sí, para obtener la sumatoria total de los valores de las tres componentes RGB entre sí de todos los píxeles al cuadrado del contorno entero.
                sumaBGR = sumR+sumG+sumB
                
                # Mostrar en consola los resultados del helióstato o helióstatos localizados y analizados, para cada fotograma del vídeo.
                print("Ancho y alto WH del helióstato en píxeles:       %4i %4i" %(w, h)) # Mostrar en consola el ancho y el alto WH del helióstato en píxeles.
                print("Área del helióstato en píxeles:                  ", area) # Mostrar en consola el área del helióstato en píxeles.
                print("Sumatorias BGR al cuadrado de todos sus píxeles: %8i %8i %8i" %(sumB, sumG, sumR)) # Mostrar en consola el valor de la sumatoria acumulativa de cada componente RGB de todos los pixeles al cuadrado del helióstato entero.
                print("Suma total BGR al cuadrado helióstato completo:  ", sumaBGR) # Mostrar en consola la sumatoria total de los valores de las tres componentes RGB entre si de todos los pixeles al cuadrado del helióstato entero.

            # Llamar a la función definida 'vectorial(frame, x, y)', siendo 'frame' el fotograma actual del vídeo a tratar, y XY las coordenadas de la esquina superior izquierda del helióstato.
            vectorial(frame, x, y)

    # Mostrar vídeo original en una ventana/actualizar fotograma.
    cv2.imshow("Camara", frame)

    # Al alcanzar esta línea de código, ya se habrá leído y analizado el fotograma actual del vídeo. Antes de pasar al siguiente fotograma, hacer:
    frame_counter += 1 # Incrementar el contador de fotogramas leídos del vídeo a uno.
    end_time = time.time() # Obtener el tiempo de ejecución tras haber leído el fotograma actual del vídeo.
    fps = frame_counter / float(end_time - start_time) # Calcular los FPS (fotogramas por segundo del vídeo) dividiendo el contador de fotogramas actual por la diferencia entre ambos tiempos medidos.
    print("")
    print("FPS:", fps) # Mostrar en consola los FPS (fotogramas por segundo del vídeo). Se mostrará cada vez que se haya analizado el fotograma actual del vídeo.
    print("")
    print("")
    
# Cuando el bucle 'while' inicial finalice, mostrar en consola que el programa finalizó su ejecución (el vídeo fue leído y analizado completamente).
print("Programa terminado.")
