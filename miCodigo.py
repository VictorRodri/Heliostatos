import urllib.request
import cv2
import numpy as np
import time
import metodos as met
from matplotlib import pyplot as plt
import sys # Permitir ejecutar este programa con argumentos

print("Iniciando programa...")

camara = cv2.VideoCapture("Videos/varios_heliostatos.mp4") #Leer secuencia de imagenes

# Crear TXT
def creartxt():
    archi=open('datos.txt','w')
    archi.close()

creartxt()

mayor = 0
contornoPrimero = False
areaContornoPrimero = 0

# Iteracion 'while True' para cada fotograma del video, hasta completar todos los fotogramas y llegar al final del video (cambiaria automaticamente de True a False y el bucle 'while' finaliza).
while True:
    # Obtener frame
    (grabbed, frame) = camara.read()

    # Si hemos llegado al final del vídeo salimos
    if not grabbed:
        break

    # Convertir a escala de grises el video normal.
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicamos un umbral
    ret,thresh = cv2.threshold(img,127,255,0)
    cv2.imshow("Camara2", thresh) # Mostrar video umbralizado en una ventana.
    cv2.waitKey(1)

    now = time.time() # Tomar el tiempo actual.
    # Parametros del siguiente metodo: Imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquia de familia, marcar la mínima cantidad de puntos (no todos)
    # que forman (delimitan) la figura (heliostato).
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])
    print ("Time =", time.time() - now) # Restar el tiempo actual de esta linea menos el tomado 3 lineas antes en este codigo para calcular el tiempo de 'im2' y de los momentos.
    print('Momentos: ', M)
    
    
    if M['m00'] != 0:
        print("m00 es distinto de cero, cx y cy valen: ");
        # Centroides 'cx' y 'cy'.
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(cx, cy)
        cv2.drawContours(img, contours, -1, (0,255,0), 3) # Dibujar contornos. Parametros: donde dibujar, contornos a dibujar, dibujar en todos los contornos con el '-1', color verde, grosor 3 px.
        plt.scatter([cx],[cy]) # Dispersar los centroides 'cx' y 'cy'.
        plt.imshow(img, cmap="gray") # Mostrar imagen a escala de grises?


    # print("Contornos: ", contours);
    

    # Area de varios contornos en un fotograma del video
    # Cada vez que se empiece a ejecutar el siguiente bucle 'for', se reestablece 'mayor' a cero para evitar tomar accidentalmente el valor mayor de iteraciones anteriores a la actual.
    mayor = 0
    # Recorrer todos los contornos (siguiente bucle 'for') de cada fotograma del video (bucle 'while' ejecutandose actualmente).
    # El numero maximo de contornos en cada fotograma del video es variable, y por eso se pone 'len(contours)',
    # para recorrer desde el contorno 0 hasta el numero maximo de contornos del fotograma del video en cuestion.
    for i in range(0,len(contours)):
        # Recuadros verdes en el contorno mas grande, para cada fotograma del video.
        
        # get the bounding rect
        (x, y, w, h) = cv2.boundingRect(contours[i])

        # si el ancho de un contorno cualquiera es mayor que 70, reencuadrar ese contorno con un rectangulo verde, con la siguiente linea de codigo. Asi se descartaran falsos contornos.
        if (w>70):
            # draw a green rectangle to visualize the bounding rect
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # Parametros: fotograma actual video, esq sup izda, esq inf dcha (width: ancho, height: altura), rectang color verde, grosor 2 px.

        # print("Coordenadas rectangulos verdes:", x, y, w, h)
                
        # Calcular el area del contorno numero 'i', en el fotograma actual del video. 'i' es el iterador del bucle 'for' actual.
        area = cv2.contourArea(contours[i])
        # Almacenar, para cada fotograma del video, y para el primer contorno de todos, su area.
        # Esta variable se actualizara cuando se quiera leer otro primer area de contorno de un fotograma distinto del video.
        if i==0:
            areaContornoPrimero = area
            print("Area del primer contorno:", areaContornoPrimero)
        # Mostrar por consola el numero de area que se esta calculando actualmente, y su area, para cada fotograma del video.
        # print("Calcular area", i+1, ". Resultado:", area)

        # Quedarse con el area mas grande de todas las areas localizadas en el fotograma actual del video.
        if area > mayor:
            mayor = area

        # Si el primer contorno detectado en el fotograma actual es 1000 o mas (muy grande), significa que se esta detectando correctamente el contorno principal y deseado, el grande, y no otros.
        if areaContornoPrimero>=1000:
            contornoPrimero=True
        else:
            contornoPrimero=False

        
        
    print("Final del bucle 'for'. Area mayor encontrada:", mayor)

    # Mostrar video original en una ventana. Al colocar esta linea de codigo aqui, y no al principio del todo, permitira mostrar ademas los recuadros verdes en los heliostatos
    # (esto ya se programo lineas antes).
    cv2.imshow("Camara", frame)


    # Grabar TXT
    def grabartxt():
        archi=open('datos.txt','a')
        archi.write(repr(mayor)) # repr convierte de float a string.
        archi.write('\n')
        archi.close()

    grabartxt()
    

    # Si tras analizar todos los contornos del fotograma actual, se detecto o no el contorno principal, se mostrara por consola si se detecto o no correctamente el contorno principal.
    if(contornoPrimero==True):     
        print("Se esta detectando correctamente el contorno principal.")
    else:
        print("No se esta detectando correctamente el contorno principal.")

    
    # Dividir en parrafos la salida por consola.
    print("")

    
print("Programa terminado")
