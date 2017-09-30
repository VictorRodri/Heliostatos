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

while True:
    # Obtener frame
    (grabbed, frame) = camara.read()

    # Mostrar la imagen de la camara.
    cv2.imshow("Camara", frame)

    # Si hemos llegado al final del vídeo salimos
    if not grabbed:
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convertimos a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicamos un umbral
    ret,thresh = cv2.threshold(img,127,255,0)
    cv2.imshow("Camara2", thresh)
    cv2.waitKey(1)

    # Mostrar imagen
    #plt.imshow(thresh, cmap="gray")

    now = time.time() # Tomar el tiempo actual.
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Parametros: Imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquia de familia, marcar la mínima cantidad de puntos (no todos) que forman (delimitan) la figura (heliostato).
    M = cv2.moments(contours[0])
    print ("Time =", time.time() - now) # Restar el tiempo actual de esta linea menos el tomado 3 lineas antes en este codigo para calcular el tiempo de 'im2' y de los momentos.

    #M = cv2.moments(contours[0])
    print('Momentos: ', M)
    
    
    if M['m00'] != 0:
        print("m00 es distinto de cero, cx y cy valen: ");
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(cx, cy)
        cv2.drawContours(img, contours, -1, (0,255,0), 3) # Dibujar contornos. Parametros: 1: donde dibujar. 2: contornos a dibujar. 3: dibujar en todos los contornos con el '-1'.
        plt.scatter([cx],[cy]) # Dispersar
        plt.imshow(img, cmap="gray") # Mostrar imagen normal


    # print("Contornos: ", contours);

    # Area del contorno
    # area = cv2.contourArea(contours[0]) # Maximo hasta 'contours[33]'.
    # print ("Area =", area) # Mostrar por consola el area del contorno.

    # Area de varios contornos en un fotograma del video
    # Cada vez que se empiece a ejecutar el siguiente bucle 'for', se reestablece 'mayor' a cero para evitar tomar accidentalmente el valor mayor de iteraciones anteriores a la actual.
    mayor = 0
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
              22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]:
        area = cv2.contourArea(contours[i])
        print("Calcular area", i, ". Resultado:", area)

        # Quedarse con el area mas grande de todas las areas localizadas en el fotograma actual del video.
        if area > mayor:
            mayor = area
        
    print("Final del bucle 'for'. Area mayor encontrada:", mayor)
    
    
    '''
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000 and area < 10000:
            cv2.drawContours(img, contours, 0, (0, 255, 0), 2, cv2.LINE_AA)
            '''

    # Grabar TXT
    def grabartxt():
        archi=open('datos.txt','a')
        archi.write(repr(mayor)) # repr convierte de float a string.
        archi.write('\n')
        archi.close()

    grabartxt()


    
    # Pausar el video cuando hayan problemas con el area del contorno. Pulsar Enter para reanudar.
    if(mayor<=100):
        # Guardar imagen en disco con area menor o igual que 100.
        #cv2.imwrite("Imagenes/ImagenNormal"+str(iteracion)+".png", gris)
        #cv2.imwrite("Imagenes/ImagenUmbral"+str(iteracion)+".png", im2)
        #iteracion += 1

        
        print("ATENCION: esta imagen tiene de area 100 o menos.")
        print("Pulse una tecla para continuar... ")
        #nombre = input()

    '''
    if area > 1000 and area < 10000:
        cv2.drawContours(img, contours, 0, (0, 255, 0), 2, cv2.LINE_AA)
        print("Dibujar contorno mayor que 1000 y menor que 10000")
        '''
        
    # Dividir en parrafos la salida por consola.
    print("")

    
print("Programa terminado")
