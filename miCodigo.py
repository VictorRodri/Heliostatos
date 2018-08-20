import urllib.request
import cv2
import numpy as np
import time
import metodos as met
from matplotlib import pyplot as plt
import sys # Permitir ejecutar este programa con argumentos
import argparse

# Argumentos necesarios para ejecutar este programa a traves de la consola de Windows.
parser = argparse.ArgumentParser(description='Pruebas parametros.')
parser.add_argument('directorioVideoHeliostatosCargar', type=str)
parser.add_argument('areaMinimaHeliostato', type=int)
parser.add_argument('anchoMinimoHeliostato', type=int)
parser.add_argument('altoMinimoHeliostato', type=int)
args = parser.parse_args()

print("")
print("Iniciando programa...")
print("")

camara = cv2.VideoCapture(args.directorioVideoHeliostatosCargar) # Leer secuencia de imagenes

area = 0
sumaRGB = 0

# Declarar estas variables sumatorias de rojo, verde y azul, e inicializarlas a cero. Explicado posteriormente en detalle.
rTot = 0
gTot = 0
bTot = 0

# Iteracion 'while True' para cada fotograma del video, hasta completar todos los fotogramas y llegar al final del video (cambiaria automaticamente de True a False y el bucle 'while' finaliza).
while True:
    # Obtener frame. Para ello, se toma un fotograma del video, se guarda en 'frame', y si se ha hecho esta accion correctamente, 'grabbed' valdra true (verdadero), y viceversa.
    (grabbed, frame) = camara.read()

    # Si hemos llegado al final del vídeo salimos
    if not grabbed:
        break

    # Convertir a escala de grises el video normal. Para ello, con la variable 'frame' (fotograma del video) capturada anteriormente, se llama a la funcion 'cv2.COLOR_BGR2GRAY'.
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicamos un umbral
    ret,thresh = cv2.threshold(img,127,255,0) # Parametros de este metodo: fuente, umbral, valor maximo, aplicar un tipo concreto de umbralizacion (0 porque no se desea hacer esto).
    # La variable ‘ret’ de la linea de codigo anterior no es usada en este programa así que se puede ignorar, esto es debido a que no se está aplicando umbralización de Otsu.
    cv2.imshow("Camara2", thresh) # Mostrar video umbralizado en una ventana.
    cv2.waitKey(1) # El programa hara una pequena pausa (1 milisegundo) para que de tiempo a que se muestren los videos y fotogramas en las dos ventanas que se han creado en este codigo para tal fin.

    # now = time.time() # Tomar el tiempo actual.
    # Parametros del siguiente metodo: Imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquia de familia, marcar la mínima cantidad de puntos (no todos)
    # que forman (delimitan) la figura (heliostato). Argumentos que devolvera dicho metodo: imagen fuente (sobra), modo de devolucion del contorno, metodo de aproximacion del contorno (sobra).
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0]) # Calcular los momentos del primer contorno, para cada fotograma del video. Los momentos permiten calcular el centro de masa del objeto, su area, etcetera.
    #print ("Time =", time.time() - now) # Restar el tiempo actual de esta linea menos el tomado 3 lineas antes en este codigo para calcular el tiempo de 'im2' y de los momentos.
    #print('Momentos: ', M)    
    
    if M['m00'] != 0: # Si el divisor es distinto de 0, hacer.
        #print("m00 es distinto de cero, cx y cy valen: ");
        # Centroides 'cx' y 'cy', y su forma de calcularlos.
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print(cx, cy)
        cv2.drawContours(img, contours, -1, (0,255,0), 3) # Dibujar contornos. Parametros: donde dibujar, contornos a dibujar, dibujar en todos los contornos con el '-1', color verde, grosor 3 px.
        plt.scatter([cx],[cy]) # Dispersar los centroides 'cx' y 'cy'.
        #plt.imshow(img, cmap="gray") # ?Mostrar imagen a escala de grises?

    
    # Cada vez que se empiece a ejecutar el siguiente bucle 'for', se reestablece 'areaMayorDeTodas' a cero para evitar tomar accidentalmente el valor mayor de iteraciones anteriores a la actual.
    areaMayorDeTodas = 0
    
    # Recorrer todos los contornos (siguiente bucle 'for') de cada fotograma del video (bucle 'while' ejecutandose actualmente).
    # El numero maximo de contornos en cada fotograma del video es variable, y por eso se pone 'len(contours)',
    # para recorrer desde el contorno 0 hasta el numero maximo de contornos del fotograma del video en cuestion.
    for i in range(0,2):
        
        # Cada vez que se empiece a analizar un contorno diferente, se reestablece 'sumaRGB' a cero para evitar tomar accidentalmente la suma de RGB de los siguientes contornos en vez del actual.
        sumaRGB = 0
        rTot = 0
        gTot = 0
        bTot = 0
        area = 0
        # Recuadros verdes en el contorno mas grande (o en plural), para cada fotograma del video.
        # 1: get the bounding rect (obtener el contorno)
        (x, y, w, h) = cv2.boundingRect(contours[i]) # xy: coordenadas de un punto, w: ancho, h: altura.

        # Calcular el area del contorno numero 'i', en el fotograma actual del video. 'i' es el iterador del bucle 'for' actual.
        area = cv2.contourArea(contours[i])
        
        # 2: si el ancho de un contorno cualquiera es mayor que 70, reencuadrar ese contorno con un rectangulo verde, con la siguiente linea de codigo. Asi se descartaran falsos contornos.
        if (area > args.areaMinimaHeliostato and w > args.anchoMinimoHeliostato and h > args.altoMinimoHeliostato):
            print("Area heliostato", i+1, ":", area)
            # draw a green rectangle to visualize the bounding rect
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # Parametros: fotograma actual video, esq sup izda, esq inf dcha (width: ancho, height: altura), rectang color verde, grosor 2 px.
            
            # Ademas, mientras que w>70, analizar todos los pixeles del contorno principal, para obtener las componentes RGB de cada uno de ellos.
            for xAux in range(x, x+w+1):
                for yAux in range(y, y+h+1):
                    # Dividir en parrafos la salida por consola.
                    print("")
                    
                    print("- Heliostato", i+1, "en analisis. -")
                    print("")
                    print("Pixel XY en analisis del heliostato:           %4i %4i" %(xAux, yAux))
                    print("Ancho y alto WH del heliostato:                %4i %4i" %(w, h))
                    print("Esquina superior izquierda heliostato XY:      %4i %4i" %(x, y))
                    print("Esquinas superior e inferior derechas X+W Y+H: %4i %4i" %(x+w, y+h))
                    
                    # Obtener las componentes RGB de las coordenadas (pixel) XY
                    b, g, r = frame[yAux, xAux]
                    
                    print("Valores componentes RGB del pixel en analisis: %4i %4i %4i" %(r, g, b))
                    # Cada componente RGB se eleva al cuadrado.
                    r2 = r*r # Tambien vale r**r en lugar de pow(r, r)
                    g2 = g*g
                    b2 = b*b
                    print("Elevar cada componente RGB al cuadrado:        %4i %4i %4i" %(r2, g2, b2))
                    
                    # Realizar la sumatoria RGB (cada componente por separado) de todos los pixeles del contorno principal.
                    rTot += r2
                    gTot += g2
                    bTot += b2
                    print("Sumatoria componentes RGB al cuadrado:         %8i %8i %8i" %(rTot, gTot, bTot))
                    
            # Realizar la sumatoria RGB (esta vez las tres componentes al mismo tiempo) de todos los pixeles del contorno principal.
            sumaRGB = rTot+gTot+bTot
            print("")
            print("Suma de las tres componentes RGB al cuadrado:  ", sumaRGB)
            print("")
        else:
            print("No se detecta ningun heliostato", i+1)

    # Mostrar video original en una ventana. Al colocar esta linea de codigo aqui, y no al principio del todo, permitira mostrar ademas los recuadros verdes en los heliostatos
    # (esto ultimo se programo lineas antes).
    cv2.imshow("Camara", frame)
    
    # Dividir en parrafos la salida por consola.
    print("")
    print("")
    print("   --- Siguiente fotograma video. ---")
    print("")
    print("")
    
print("Programa terminado.")
