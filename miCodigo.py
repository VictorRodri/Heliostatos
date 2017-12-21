import urllib.request
import cv2
import numpy as np
import time
import metodos as met
from matplotlib import pyplot as plt
import sys # Permitir ejecutar este programa con argumentos

print("Iniciando programa...")

camara = cv2.VideoCapture("Videos/varios_heliostatos.mp4") # Leer secuencia de imagenes

# Crear TXT
def creartxt():
    archi=open('datos.txt','w')
    archi.close()

creartxt()

areaMayorDeTodas = 0
contornoPrimero = False
areaContornoPrimero = 0
sumaRGB = 0

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
    cv2.imshow("Camara2", thresh) # Mostrar video umbralizado en una ventana.
    cv2.waitKey(1) # El programa hara una pequena pausa (1 milisegundo) para que de tiempo a que se muestren los videos y fotogramas en las dos ventanas que se han creado en este codigo para tal fin.

    now = time.time() # Tomar el tiempo actual.
    # Parametros del siguiente metodo: Imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquia de familia, marcar la mínima cantidad de puntos (no todos)
    # que forman (delimitan) la figura (heliostato).
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0]) # Calcular los momentos del primer contorno, para cada fotograma del video.
    #print ("Time =", time.time() - now) # Restar el tiempo actual de esta linea menos el tomado 3 lineas antes en este codigo para calcular el tiempo de 'im2' y de los momentos.
    #print('Momentos: ', M)
    
    
    if M['m00'] != 0:
        #print("m00 es distinto de cero, cx y cy valen: ");
        # Centroides 'cx' y 'cy', y su forma de calcularlos.
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print(cx, cy)
        cv2.drawContours(img, contours, -1, (0,255,0), 3) # Dibujar contornos. Parametros: donde dibujar, contornos a dibujar, dibujar en todos los contornos con el '-1', color verde, grosor 3 px.
        plt.scatter([cx],[cy]) # Dispersar los centroides 'cx' y 'cy'.
        #plt.imshow(img, cmap="gray") # ?Mostrar imagen a escala de grises?


    # print("Contornos: ", contours);

    '''
    x = 240
    y = 178

    b = frame.item(y, x, 0)
    g = frame.item(y, x, 1)
    r = frame.item(y, x, 2)

    print('pixel:', b, g, r)
    '''
    b, g, r = frame[100, 100]
    print('pixel:', b, g, r)
    
    sumaRGB = b + g + r
    print('sumaRGB:', sumaRGB)
    

    # Area de varios contornos en un fotograma del video
    # Cada vez que se empiece a ejecutar el siguiente bucle 'for', se reestablece 'areaMayorDeTodas' a cero para evitar tomar accidentalmente el valor mayor de iteraciones anteriores a la actual.
    areaMayorDeTodas = 0
    # Recorrer todos los contornos (siguiente bucle 'for') de cada fotograma del video (bucle 'while' ejecutandose actualmente).
    # El numero maximo de contornos en cada fotograma del video es variable, y por eso se pone 'len(contours)',
    # para recorrer desde el contorno 0 hasta el numero maximo de contornos del fotograma del video en cuestion.
    for i in range(0,len(contours)):
        
        # Recuadros verdes en el contorno mas grande (o en plural), para cada fotograma del video.
        # 1: get the bounding rect (obtener el contorno)
        (x, y, w, h) = cv2.boundingRect(contours[i]) # x: esquina superior izquierda, y: esquina inferior derecha, w: ancho, h: altura.
        # 2: si el ancho de un contorno cualquiera es mayor que 70, reencuadrar ese contorno con un rectangulo verde, con la siguiente linea de codigo. Asi se descartaran falsos contornos.
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
            #print("Area del primer contorno:", areaContornoPrimero) # Esta salida por consola tambien se muestra al final de este codigo, por eso es mejor dejar esta deshabilitada (comentada).
        # Mostrar por consola el numero de area que se esta calculando actualmente, y su area, para cada fotograma del video.
        # print("Calcular area", i+1, ". Resultado:", area)

        # Quedarse con el area mas grande de todas las areas localizadas en el fotograma actual del video.
        if area > areaMayorDeTodas:
            areaMayorDeTodas = area

        # Si el primer contorno detectado en el fotograma actual es 1000 o mas (muy grande), significa que se esta detectando correctamente el contorno principal y deseado, el grande, y no otros.
        if areaContornoPrimero>=1000:
            contornoPrimero=True
        else:
            contornoPrimero=False
        
    print("Final del bucle 'for'. Area mayor encontrada:", areaMayorDeTodas)

    # Mostrar video original en una ventana. Al colocar esta linea de codigo aqui, y no al principio del todo, permitira mostrar ademas los recuadros verdes en los heliostatos
    # (esto ya se programo lineas antes).
    cv2.imshow("Camara", frame)


    # Grabar TXT
    def grabartxt():
        archi=open('datos.txt','a') # abrir y crear el archivo de texto 'datos.txt' en el mismo directorio donde se esta ejecutando este programa
        archi.write(repr(areaMayorDeTodas)) # repr convierte de float a string. Escribir en el TXT el area mas grande de todas las areas (contornos) detectadas en cada fotograma actual del video
        archi.write('\n') # retorno de carro, para que cada valor escrito en el archivo de texto este en una unica linea
        archi.close() # tras realizar todas las operaciones anteriores, cerrar el archivo de texto
    grabartxt()
    

    # Si tras analizar todos los contornos del fotograma actual, se detecto o no el contorno principal (el primer contorno de todos), se mostrara por consola si lo detecto o no correctamente.
    if(contornoPrimero==True):     
        print("Se esta detectando correctamente el contorno principal (primero). Su area:", areaContornoPrimero)
    else:
        print("No se esta detectando correctamente el contorno principal (primero). Su area:", areaContornoPrimero)

    
    # Dividir en parrafos la salida por consola.
    print("")

    
print("Programa terminado")
