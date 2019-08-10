#!/usr/bin/python

import cv
tol=15

def evento_mouse(event,x,y,flags,param):
    if event==cv.CV_EVENT_LBUTTONDOWN:
        pixel=cv.Get2D(imagen,y,x)
        #En pixel guardo los valores del pixel y luego los separo en las
        #variables azul, verde y rojo
        azul=pixel[0]
        verde=pixel[1]
        rojo=pixel[2]
        print azul,verde,rojo # las imprimo para saber sus valores
        while True:
            imagen2=cv.QueryFrame(captura)
            cv.InRangeS(imagen,(azul-tol,verde-tol,rojo-tol),(azul+tol,verde+tol,rojo+tol),temporal)
            # La funcion InRangeS me permite umbralizar las imagenes dando un rango determinado
            # en este caso el rango es el valor de el pixel menos la tolerancia y el valor del pixel
            # mas la tolerancia. Si los resultados no son los esperados se debe modificar la tolerancia
            cv.ShowImage('Umbral',temporal)
            #Muestro la imagen resultante. La cual va a mostrar en blanco el color que seleccione
            #y en negro cualquier otro color
            if cv.WaitKey(30)==27:
                break
 
captura=cv.CaptureFromCAM(0)
while True:
    imagen=cv.QueryFrame(captura)
    temporal=cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)    
    cv.ShowImage('Color',imagen)
    cv.SetMouseCallback('Color',evento_mouse)
    if cv.WaitKey(30)==27:
        break 
