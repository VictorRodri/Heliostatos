# Bibliotecas requeridas para este software.
import cv2
import argparse
import time
import numpy as np

# Crear y abrir los siguientes archivos de texto en modo escritura.
f1 = open("SumasBGRHeliostatosVerdes.txt", "w")
f2 = open("SumasBGRHeliostatosRojos.txt", "w")

start_time = time.time() # Obtener el tiempo de ejecución inicial de este programa.
frame_counter = 0 # Contador de fotogramas totales del vídeo. Se irá incrementando progresivamente en líneas de código posteriores.

# Argumentos o parámetros necesarios para ejecutar este programa a través de la consola de Windows.
parser = argparse.ArgumentParser(description='Parametros del programa.') # Dar un nombre al conjunto de parámetros y asignarlo a la variable 'parser'.
parser.add_argument('directorioVideoHeliostatosCargar', type=str) # Crear el argumento 1: ruta o directorio del vídeo a cargar en el PC.
parser.add_argument('anchoMinimoHeliostato', type=int) # Crear el argumento 3: ancho mínimo del helióstato para su análisis.
parser.add_argument('altoMinimoHeliostato', type=int) # Crear el argumento 4: alto mínimo del helióstato para su análisis.
parser.add_argument('umbralVideoHeliostatos', type=int) # Crear el argumento 5: umbral o nivel de color mínimo del vídeo de helióstatos a partir del cual podría estar detectándose un helióstato.
parser.add_argument('numeroHeliostatosAnalizar', type=int) # Crear el argumento 6: número máximo de helióstatos a detectar y analizar en cada fotograma del vídeo de helióstatos.
args = parser.parse_args() # Devuelve información de los parámetros definidos previamente.

# Mostrar en la consola este aviso de cuando se va a ejecutar el programa.
print("")
print("Iniciando programa...")
print("")

# Leer secuencia de imágenes del vídeo a partir del directorio especificado por parámetro.
camara = cv2.VideoCapture(args.directorioVideoHeliostatosCargar)

# Declarar estos arrays con el fin de almacenar toda la información sobre los resultados de los helióstatos analizados en el vídeo de helióstatos.
# Además, son usados especialmente con el fin de mostrar, para cada información, hasta dos resultados distintos (uno para cada helióstato) en una misma línea de texto, en la consola.
heliostato = []
anchoAlto = []
areaTotal = []
sumaBGRparcial = []
sumaBGRtotal = []

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
    ret, thresh = cv2.threshold(img, args.umbralVideoHeliostatos, 255, 0)
    
    cv2.imshow("Camara2", thresh) # Mostrar vídeo umbralizado en una ventana.
    cv2.waitKey(1) # El programa hará una pequeña pausa (1 milisegundo) para que de tiempo a que se muestren los vídeos y fotogramas en las dos ventanas que se han creado en este código para tal fin.

    # Buscar y detectar todos los contornos o helióstatos del fotograma actual del vídeo.
    # Parámetros del siguiente método: imagen umbralizada, devolver todos los contornos y crear una lista completa de jerarquía de familia, marcar la mínima cantidad de puntos (no todos)
    # que forman (delimitan) la figura (helióstato). Argumentos que devolverá dicho método: imagen fuente (sobra), modo de devolución del contorno, método de aproximación del contorno (sobra).
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Guardar en los distintos arrays los siguientes textos, para luego ser mostrados por consola junto con los respectivos resultados de los helióstatos.
    heliostato.append("                                               ")
    anchoAlto.append("Ancho y alto WH del helióstato en píxeles:      ")
    areaTotal.append("Área del helióstato en píxeles:                 ")
    sumaBGRparcial.append("Sumatorias BGR al cuadrado de todos sus píxeles:")
    sumaBGRtotal.append("Suma total BGR al cuadrado helióstato completo: ")
        
    # Recorrer solo los 'args.numeroHeliostatosAnalizar' primeros contornos, los más grandes (siguiente bucle 'for'), para cada fotograma del vídeo (bucle 'while' ejecutándose actualmente).
    # Al no recorrer los demás contornos, éstos serán descartados porque no son muy grandes ni importantes o son falsos.
    # Siendo 'args.numeroHeliostatosAnalizar' el número de contornos deseado por el usuario por parámetro en la consola que se quiere analizar como máximo para cada fotograma.
    for i in range(0, args.numeroHeliostatosAnalizar):
        
        # Obtener las coordenadas del contorno.
        (x, y, w, h) = cv2.boundingRect(contours[i]) # xy: coordenadas de un punto, w: ancho, h: altura.
        
        # Calcular el área del contorno número 'i', en el fotograma actual del vídeo. 'i' es el iterador del bucle 'for' actual.
        area = int(cv2.contourArea(contours[i]))
        
        # Si el contorno tiene un ancho y alto mayores a los especificados por parámetros, este será analizado y reencuadrado en un rectángulo verde en el vídeo.
        if (w > args.anchoMinimoHeliostato and h > args.altoMinimoHeliostato):

            # Si se está analizando el helióstato número uno en el fotograma actual del vídeo, hacer.
            if (i == 0):
                
                # Dibujar un rectángulo verde alrededor del contorno, en el vídeo.
                # Parámetros: fotograma actual vídeo, esquina superior izquierda, esquina inferior derecha (width: ancho, height: altura), rectángulo color verde, grosor del rectángulo 2 píxeles.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
            # Si se está analizando el helióstato número dos en el fotograma actual del vídeo (en caso de que ya exista el otro helióstato en ese mismo fotograma del vídeo), hacer.
            else:
                
                # En este caso, ahora se reencuadra el contorno en un rectángulo rojo, en vez de verde. Así, ambos contornos podrán ser diferenciados si se muestran en el mismo fotograma del vídeo.
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            # Leer y analizar todos los píxeles del helióstato.
            def vectorial(frame, x, y):
                
                # Del fotograma actual del vídeo, se leerá únicamente donde haya un helióstato (su ancho y alto), y así con todos los helióstatos de cada fotograma del vídeo.
                m = frame[y+2:y+h-1, x+2:x+w-1]
                             
                # Obtener en matrices las componentes BGR de todos los píxeles del helióstato.
                mB = m[:, :, 2]
                mG = m[:, :, 1]
                mR = m[:, :, 0]
                
                # Elevar al cuadrado cada dato BGR del helióstato.
                mB2 = mB*mB
                mG2 = mG*mG
                mR2 = mR*mR

                # Realizar la sumatoria acumulativa de cada BGR al cuadrado de ese helióstato.
                sumB = np.sum(mB2)
                sumG = np.sum(mG2)
                sumR = np.sum(mR2)

                # Sumar las anteriores tres componentes entre sí, para obtener la sumatoria total de los valores de las tres componentes RGB entre sí de todos los píxeles al cuadrado del contorno entero.
                sumaBGR = sumR+sumG+sumB

                # Introducir en el array 'heliostato' qué helióstato(s) se ha(n) leído y analizado en el fotograma actual del vídeo (reencuadre verde o rojo).
                if (i == 0):
                    heliostato.append("Verde                           ")
                else:
                    heliostato.append("Rojo")

                # Ir introduciendo en los arrays las informaciones de los resultados de los helióstatos, con el fin de mostrarlas después por consola.
                # Al ser arrays acumulativos, si en un mismo fotograma del vídeo se obtienen datos de dos helióstatos, para cada array se guardarán los datos de esos dos helióstatos a la vez.
                # De esta forma, se compactará más la información mostrada en consola al estar esta a dos columnas: helióstato verde y helióstato rojo, para cada línea de texto o array.
                anchoAlto.append(w)
                anchoAlto.append(h)
                anchoAlto.append("                      ")
                
                areaTotal.append(area)
                areaTotal.append("                       ")
                
                sumaBGRparcial.append(sumB)
                sumaBGRparcial.append(sumG)
                sumaBGRparcial.append(sumR)
                sumaBGRparcial.append("     ")
                
                sumaBGRtotal.append(sumaBGR)
                sumaBGRtotal.append("                       ")

                # Dependiendo de qué helióstato se esté analizando (reencuadre verde o rojo), los resultados de la estimación de potencia para cada fotograma del vídeo se guardarán en un fichero o en otro.
                if (i == 0):
                    f1.write(str(sumaBGR)+"\n")
                else:
                    f2.write(str(sumaBGR)+"\n")
                
            # Llamar a la función definida 'vectorial(frame, x, y)', siendo 'frame' el fotograma actual del vídeo a tratar, y XY las coordenadas de la esquina superior izquierda del helióstato.
            vectorial(frame, x, y)
            
        else:

            # Si el ancho y alto proporcionados por el usuario en consola no son mayores al ancho y alto del helióstato actual (en análisis), aparte de no analizarlo,
            # marcar su estimación de potencia como cero y guardarlo en un fichero o en otro, dependiendo de si se trata del helióstato con reencuadre verde o rojo.
            if (i == 0):
                f1.write(str(0)+"\n")
            else:
                f2.write(str(0)+"\n")

    # Mostrar vídeo original en una ventana/actualizar fotograma.
    cv2.imshow("Camara", frame)

    # Mostrar en consola el valor del área del helióstato en píxeles, su ancho y alto también en píxeles,
    # los valores de las sumatorias acumulativas RGB al cuadrado (cada componente por separado) de todos los píxeles del helióstato, y esto mismo pero sumando esta vez las tres componentes entre sí.
    print(heliostato)
    print(anchoAlto)
    print(areaTotal)
    print(sumaBGRparcial)
    print(sumaBGRtotal)

    # Borrar el contenido de los arrays, ya que se ha mostrado toda la información en consola del helióstato (o helióstatos) para el fotograma actual del vídeo de helióstatos.
    del heliostato[:]
    del anchoAlto[:]
    del areaTotal[:]
    del sumaBGRparcial[:]
    del sumaBGRtotal[:]

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

# Tras finalizar la edición de ambos ficheros, cerrarlos.
f1.close()
f2.close()
