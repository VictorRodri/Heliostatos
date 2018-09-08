# Bibliotecas requeridas para este software.
import cv2
import argparse
import time
import numpy as np

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
    # Medir el tiempo de ejecución del código desde esta línea de código hasta alcanzar la línea de código 'time.time() - now'.
    now = time.time()
    
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
        
        # Cada vez que se empiece a analizar un contorno diferente, se reestablecen estas variables a cero porque cada contorno comienza con todos estos valores a cero.
        # Además, se realiza para evitar que un contorno del siguiente fotograma del vídeo tome los mismos valores o superiores del contorno del anterior fotograma del vídeo ya analizado.
        rTot = 0
        gTot = 0
        bTot = 0
        area = 0
        sumaRGB = 0
        
        # Obtener las coordenadas del contorno.
        (x, y, w, h) = cv2.boundingRect(contours[i]) # xy: coordenadas de un punto, w: ancho, h: altura.

        # Calcular el área del contorno número 'i', en el fotograma actual del vídeo. 'i' es el iterador del bucle 'for' actual.
        area = cv2.contourArea(contours[i])
        
        # Si el contorno tiene un ancho y alto mayores a los especificados por parámetros, este será analizado y reencuadrado en un rectángulo verde en el vídeo.
        if (w > args.anchoMinimoHeliostato and h > args.altoMinimoHeliostato):

            # Si se está analizando el contorno número uno en el fotograma actual del vídeo, hacer.
            if (i == 0):
                # Dibujar un rectángulo verde alrededor del contorno, en el vídeo.
                # Parámetros: fotograma actual vídeo, esquina superior izquierda, esquina inferior derecha (width: ancho, height: altura), rectángulo color verde, grosor del rectángulo 2 píxeles.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Mostrar vídeo original en una ventana/actualizar fotograma.
                cv2.imshow("Camara", frame)
                print("- Analizando el helióstato verde...")
                print("")
            # Si se está analizando el contorno número dos en el fotograma actual del vídeo, hacer.
            else:
                # En este caso, ahora se reencuadra el contorno en un rectángulo rojo, en vez de verde. Así, ambos contornos podrán ser diferenciados si se muestran en el mismo fotograma del vídeo.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                # Mostrar vídeo original en una ventana/actualizar fotograma.
                cv2.imshow("Camara", frame)
                print("")
                print("- Analizando el helióstato rojo...")
                print("")

            # CODIGO NUEVO:
            
            # Para cada píxel del contorno, hacer.
            def vectorial(frame, x, y):
                i = frame[y+2:y+h-1, x+2:x+w-1]
                mB = frame[:, 0: :3]
                mG = frame[:, 1: :3]
                mR = frame[:, 2: :3]
                
                sumB = 0
                sumG = 0
                sumR = 0
                sumB = np.sum(mB)
                sumG = np.sum(mG)
                sumR = np.sum(mR)
                print("Energía: ", sumB, sumG, sumR)
                '''
                # Obtener las componentes RGB de las coordenadas XY del píxel en análisis.
                b, g, r = num
                
                # Cada componente RGB de aquel píxel leído se eleva al cuadrado.
                r2temp = np.square(r)
                g2temp = np.square(g)
                b2temp = np.square(b)
                
                # Representar los anteriores valores entre un número de 0 a 255 porque los valores RGB se representan así.
                r2 = r2temp % 256
                g2 = g2temp % 256
                b2 = b2temp % 256
                
                # Realizar la sumatoria acumulativa de cada componente RGB de todos los píxeles al cuadrado del contorno entero.
                rTot += r2
                gTot += g2
                bTot += b2'''

            vectorial(frame, x, y)

            # CODIGO ANTIGUO:

            for xAux in range(x, x+w+1):
                for yAux in range(y, y+h+1):
                    # Dividir en parrafos la salida por consola.
                    print("")
                                 
                    
                    
                    # Obtener las componentes RGB de las coordenadas (pixel) XY
                    # Obtener las componentes RGB de las coordenadas XY del pixel en analisis.
                    b, g, r = frame[yAux, xAux]
                    
        
                    # Cada componente RGB se eleva al cuadrado.
                    # Cada componente RGB de aquel pixel leido se eleva al cuadrado.
                    r2 = r*r # Tambien vale r**r en lugar de pow(r, r)
                    g2 = g*g
                    b2 = b*b
                    
                    
                    # Realizar la sumatoria RGB (cada componente por separado) de todos los pixeles del contorno principal.
                    # Realizar la sumatoria acumulativa de cada componente RGB de todos los pixeles al cuadrado del contorno entero.
                    rTot += r2
                    gTot += g2
                    bTot += b2
                                   
            # Sumar las anteriores tres componentes entre sí, para obtener la sumatoria total de los valores de las tres componentes RGB entre sí de todos los píxeles al cuadrado del contorno entero.
            sumaRGB = rTot+gTot+bTot
            
            print("Área del helióstato en píxeles:                  ", area) # Mostrar en consola el área del helióstato en píxeles.
            print("Ancho y alto WH del helióstato en píxeles:       %4i %4i" %(w, h)) # Mostrar en consola el ancho y el alto WH del helióstato en píxeles.
            print("Esquina superior izquierda XY del helióstato:    %4i %4i" %(x, y)) # Mostrar en consola la esquina superior izquierda del helióstato.
            print("Esquinas superior e inferior derechas X+W Y+H:   %4i %4i" %(x+w, y+h)) # Mostrar en consola las esquinas superior e inferior derechas del helióstato.
	    # Mostrar en consola el valor de la sumatoria acumulativa de cada componente RGB de todos los píxeles al cuadrado del contorno entero.
            print("Sumatorias RGB al cuadrado de todos sus píxeles: %8i %8i %8i" %(rTot, gTot, bTot))
            # Mostrar en consola la sumatoria total de los valores de las tres componentes RGB entre sí de todos los píxeles al cuadrado del contorno entero.
            print("Suma total RGB al cuadrado helióstato completo:  ", sumaRGB)
            
    # Mostrar en consola cuánto tiempo (en segundos) ha tardado la ejecución de este presente bucle 'while', equivalente a la lectura del fotograma actual del vídeo.
    print("")
    print("Tiempo procesamiento fotograma vídeo actual (s): ", time.time() - now)

    # Al finalizar el bucle 'for' que analizaba hasta dos contornos por fotograma del vídeo, mostrar en consola el aviso de que se cambiará y analizará el siguiente fotograma de dicho vídeo.
    print("")
    print("")
    print("   --- Siguiente fotograma vídeo. ---")
    print("")
    print("")
    
# Cuando el bucle 'while' inicial finalice, mostrar en consola que el programa finalizó su ejecución (el vídeo fue leído y analizado completamente).
print("Programa terminado.")
