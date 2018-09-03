# Bibliotecas requeridas para este software.
import cv2
import argparse
import time

# Declarar e inicializar estas variables a cero.
rTot = 0
gTot = 0
bTot = 0
area = 0
sumaRGB = 0

# Argumentos o parametros necesarios para ejecutar este programa a traves de la consola de Windows.
parser = argparse.ArgumentParser(description='Parametros del programa.') # Dar un nombre al conjunto de parametros y asignarlo a la variable 'parser'.
parser.add_argument('directorioVideoHeliostatosCargar', type=str) # Crear el argumento 1: ruta o directorio del video a cargar en el PC.
parser.add_argument('anchoMinimoHeliostato', type=int) # Crear el argumento 3: ancho minimo del heliostato para su analisis.
parser.add_argument('altoMinimoHeliostato', type=int) # Crear el argumento 4: alto minimo del heliostato para su analisis.
args = parser.parse_args() # Devuelve informacion de los parametros definidos previamente.

# Mostrar en la consola este aviso de cuando se va a ejecutar el programa.
print("")
print("Iniciando programa...")
print("")

# Leer secuencia de imagenes del video a partir del directorio especificado por parametro.
camara = cv2.VideoCapture(args.directorioVideoHeliostatosCargar)

# Iteracion 'while True' para cada fotograma del video, hasta completar todos los fotogramas y llegar al final del video (cambiaria automaticamente de True a False y el bucle 'while' finaliza).
while True:
    now = time.time()
    
    # Obtener frame. Para ello, se toma un fotograma del video, se guarda en 'frame', y si se ha hecho esta accion correctamente, 'grabbed' valdra true (verdadero), y viceversa.
    (grabbed, frame) = camara.read()

    # Si se ha llegado al final del video, romper la ejecucion de este bucle 'while' y finalizar el programa.
    if not grabbed:
        break

    # Convertir a escala de grises el fotograma actual del video. Para ello, con la variable 'frame' (fotograma del video) capturada anteriormente, se llama a la funcion 'cv2.COLOR_BGR2GRAY'.
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral a ese fotograma del video. Parametros de este metodo: imagen fuente en escala de grises, valor de umbral para clasificar los valores de pixeles de esa imagen,
    # valor maximo a ser representado si el valor del pixel supera al valor del umbral, aplicar un tipo concreto de umbralizacion (0 porque no se desea hacer esto).
    # NOTA: la variable ‘ret’ que recibe como resultado en este metodo no es usada en este programa así que se puede ignorar, esto es debido a que no se está aplicando umbralización de Otsu.
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    
    cv2.imshow("Camara2", thresh) # Mostrar video umbralizado en una ventana.
    cv2.waitKey(1) # El programa hara una pequena pausa (1 milisegundo) para que de tiempo a que se muestren los videos y fotogramas en las dos ventanas que se han creado en este codigo para tal fin.

    # Buscar y detectar todos los contornos o heliostatos del fotograma actual del video.
    # Parametros del siguiente metodo: imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquia de familia, marcar la mínima cantidad de puntos (no todos)
    # que forman (delimitan) la figura (heliostato). Argumentos que devolvera dicho metodo: imagen fuente (sobra), modo de devolucion del contorno, metodo de aproximacion del contorno (sobra).
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    # Recorrer solo los dos primeros contornos, los mas grandes (siguiente bucle 'for'), para cada fotograma del video (bucle 'while' ejecutandose actualmente).
    # Al no recorrer los demas contornos, estos seran descartados porque no son muy grandes ni importantes o son falsos.
    for i in range(0,2):
        
        # Cada vez que se empiece a analizar un contorno diferente, se reestablecen estas variables a cero porque cada contorno comienza con todos estos valores a cero.
        # Ademas, se realiza para evitar que un contorno del siguiente fotograma del video tome los mismos valores o superiores del contorno del anterior fotograma del video ya analizado.
        rTot = 0
        gTot = 0
        bTot = 0
        area = 0
        sumaRGB = 0
        
        # Obtener las coordenadas del contorno.
        (x, y, w, h) = cv2.boundingRect(contours[i]) # xy: coordenadas de un punto, w: ancho, h: altura.

        # Calcular el area del contorno numero 'i', en el fotograma actual del video. 'i' es el iterador del bucle 'for' actual.
        area = cv2.contourArea(contours[i])
        
        # Si el contorno tiene un area, ancho y alto mayores a los especificados por parametros, este sera analizado y reencuadrado en un rectangulo verde en el video.
        if (w > args.anchoMinimoHeliostato and h > args.altoMinimoHeliostato):

            if (i == 0):
                # Dibujar un rectangulo verde alrededor del contorno, en el video.
                # Parametros: fotograma actual video, esquina superior izquierda, esquina inferior derecha (width: ancho, height: altura), rectangulo color verde, grosor del rectangulo 2 pixeles.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Mostrar video original en una ventana.
                cv2.imshow("Camara", frame)
                print("Analizando el helióstato verde.")
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                # Mostrar video original en una ventana.
                cv2.imshow("Camara", frame)
                print("Analizando el helióstato rojo.")
            
            # Para cada pixel del contorno, hacer.
            for xAux in range(x, x+w+1):
                for yAux in range(y, y+h+1):                  
                    
                    # Obtener las componentes RGB de las coordenadas XY del pixel en analisis.
                    b, g, r = frame[yAux, xAux]
                    
                    # Cada componente RGB de aquel pixel leido se eleva al cuadrado.
                    r2 = r*r # Tambien vale r**r en lugar de pow(r, r)
                    g2 = g*g
                    b2 = b*b
                    
                    # Realizar la sumatoria acumulativa de cada componente RGB de todos los pixeles al cuadrado del contorno entero.
                    rTot += r2
                    gTot += g2
                    bTot += b2
                    
            # Sumar las anteriores tres componentes entre si, para obtener la sumatoria total de los valores de las tres componentes RGB entre si de todos los pixeles al cuadrado del contorno entero.
            sumaRGB = rTot+gTot+bTot

            print("Área helióstato:", area) # Mostrar en consola el area del heliostato.
            print("Ancho y alto WH del helióstato:                %4i %4i" %(w, h)) # Mostrar en consola el ancho y el alto WH del heliostato.
            print("Esquina superior izquierda helióstato XY:      %4i %4i" %(x, y)) # Mostrar en consola la esquina superior izquierda del heliostato.
            print("Esquinas superior e inferior derechas X+W Y+H: %4i %4i" %(x+w, y+h)) # Mostrar en consola las esquinas superior e inferior derechas del helistato.
	    # Mostrar en consola el valor de la sumatoria acumulativa de cada componente RGB de todos los pixeles al cuadrado del contorno entero.
            print("Sumatoria componentes RGB al cuadrado:         %8i %8i %8i" %(rTot, gTot, bTot))
			
            # Mostrar en consola la sumatoria total de los valores de las tres componentes RGB entre si de todos los pixeles al cuadrado del contorno entero.
            print("")
            print("Suma de las tres componentes RGB al cuadrado:  ", sumaRGB)
            print("")
    
    # Al finalizar el bucle 'for' que analizaba dos contornos por fotograma del video, mostrar en consola el aviso de que se cambiara y analizara el siguiente fotograma de dicho video.
    print("")
    print("")
    print("   --- Siguiente fotograma vídeo. ---")
    print("")
    print("")

    print ("Time =", time.time() - now)
# Cuando el bucle 'while' inicial finalice, mostrar en consola que el programa finalizo su ejecucion (el video fue leido y analizado completamente).
print("Programa terminado.")
