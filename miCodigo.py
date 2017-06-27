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

    now = time.time()
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])
    print ("Time =", time.time() - now)

    #M = cv2.moments(contours[0])
    print(M)

    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(cx, cy)
        cv2.drawContours(img, contours, -1, (0,255,0), 3)
        plt.scatter([cx],[cy])
        plt.imshow(img, cmap="gray")

    # Area del contorno
    area = cv2.contourArea(contours[0])
    print ("Area =", area)

    # Grabar TXT
    def grabartxt():
        archi=open('datos.txt','a')
        archi.write(repr(area)) # repr convierte de float a string.
        archi.write('\n')
        archi.close()

    grabartxt()  

    

    # Pausar el video cuando hayan problemas con el area. Pulsar Enter para reanudar.
    if(area<=100):
        print("Esta imagen tiene de area 0.")
        print("Pulse una tecla para continuar... ")
        nombre = input()
        
    # Dividir en parrafos la salida por consola.
    print("")
    
print("Programa terminado")
