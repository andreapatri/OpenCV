#!/usr/bin/python

import cv
import cv2
import time
import datetime
import time
import urllib3

try: 
	urllib3.disable_warnings()
except:
	print('urllib3.disable_warnings() failed - get a recentenough urllib3 version to avoid potential InsecureRequestWarning warnings! Can and will continue though.')
http = urllib3.PoolManager()
url = 'https://iotmmsb7af91ae6.us1.hana.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/'
deviceID = '34d074e3-ad45-42b7-bc9f-d3ee28765424'
url = url +deviceID
headers = urllib3.util.make_headers()
headers['Authorization'] = 'Bearer ' + 'ecde36ac5bf57a96943c3bc34c338a6b' 
headers['Content-Type'] = 'application/json;charset=utf-8'

tolerancia = 20
color = []
pixel_rojo, pixel_azul, pixel_verde = ([],[],[])
points = []

def guardarcolores(pixel_rojo, pixel_verde, pixel_azul):
    k = cv.CreateMat(3,3,cv.CV_64FC1) 
    k[0,0] = pixel_rojo[0]
    k[0,1] = pixel_rojo[1]  
    k[0,2] = pixel_rojo[2]
    k[1,0] = pixel_verde[0]
    k[1,1] = pixel_verde[1]
    k[1,2] = pixel_verde[2]
    k[2,0] = pixel_azul[0]
    k[2,1] = pixel_azul[1]
    k[2,2] = pixel_azul[2]
    cv.Save("Desktop/OpenCV codigos/Mis Codigos/Casco/colores.xml", k)
 
def cargarcolores():
    global pixel_rojo, pixel_verde, pixel_azul, points  
    k = cv.CreateMat(3,3,cv.CV_64FC1)
    k=cv.Load("Desktop/OpenCV codigos/Mis Codigos/Casco/colores.xml")
    pixel_rojo  = (k[0,0],k[0,1],k[0,2])
    pixel_verde = (k[1,0],k[1,1],k[1,2])
    pixel_azul  = (k[2,0],k[2,1],k[2,2])
    return pixel_rojo, pixel_verde, pixel_azul

def evento_mouse(event,x,y,flags,param):   
    tolerancia = 30
    temporal=cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    if event==cv.CV_EVENT_LBUTTONDOWN:
      global color
      pixel=cv.Get2D(imagen,y,x) 
      cv.InRangeS(imagen,(pixel[0]-tolerancia,pixel[1]-tolerancia,pixel[2]-tolerancia),(pixel[0]+tolerancia,pixel[1]+tolerancia,pixel[2]+tolerancia),temporal)
      cv.ShowImage('Seleccionando pixeles',temporal)    
      color = pixel
         
def colors (imagen, nombre_color):
    cv.ShowImage(nombre_color,imagen)
    cv.SetMouseCallback(nombre_color,evento_mouse)
    cv.WaitKey(0)

def establecer_colores(imagen):
    global pixel_rojo, pixel_azul, pixel_verde,color, teclado
    nombre_color = 'Seleccionar Rojo'
    colors(imagen, nombre_color)
    pixel_rojo = color
    cv.DestroyWindow('Seleccionar Rojo')
     
    nombre_color = 'Seleccionar Verde'
    colors(imagen, nombre_color)
    pixel_verde = color
    cv.DestroyWindow('Seleccionar Verde')
       
    nombre_color = 'Seleccionar Azul'
    colors(imagen, nombre_color)
    pixel_azul = color
    cv.DestroyWindow('Seleccionar Azul')
     
    cv.DestroyWindow('Seleccionando pixeles')
     
    guardarcolores(pixel_rojo, pixel_verde, pixel_azul)

    pixel_rojo, pixel_verde, pixel_azul = cargarcolores()

def pixeles(imagen):
    global pixel_rojo, pixel_azul, pixel_verde
    rojo      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    verde     = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    azul      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    
    cv.InRangeS(imagen,(pixel_rojo[0]-tolerancia,pixel_rojo[1]-tolerancia,pixel_rojo[2]-tolerancia),(pixel_rojo[0]+tolerancia,pixel_rojo[1]+tolerancia,pixel_rojo[2]+tolerancia),rojo)
    cv.InRangeS(imagen,(pixel_verde[0]-tolerancia,pixel_verde[1]-tolerancia,pixel_verde[2]-tolerancia),(pixel_verde[0]+tolerancia,pixel_verde[1]+tolerancia,pixel_verde[2]+tolerancia),verde)
    cv.InRangeS(imagen,(pixel_azul[0]-tolerancia,pixel_azul[1]-tolerancia,pixel_azul[2]-tolerancia),(pixel_azul[0]+tolerancia,pixel_azul[1]+tolerancia,pixel_azul[2]+tolerancia),azul)

    p_red = p_green = p_blue = 0
    
    for j in range(1,imagen.height,1):  
      for i in range(1,imagen.width,1):
        green = cv.Get2D(verde,j,i)
        red   = cv.Get2D(rojo ,j,i)          
        blue  = cv.Get2D(azul ,j,i)

        if blue[0] == 255: 
             p_blue = 1

        if green[0] == 255: 
             p_green = 1

        if red[0] == 255: 
             p_red = 1

    return p_red, p_green, p_blue

def hcp(p_red, p_green, p_blue):
    current_time = int (time.time() *100) 
    timestamp =str (current_time) 

    stringRojo =  str (p_red)
    stringVerde= str (p_green) 
    stringAzul = str (p_blue) 

    print (str (current_time))
    body='{"messageType":"6dd42e38b500568838e3","mode":"sync","messages":[{"timestamp":'
    body=body+timestamp
	
    body = body +',"Rojo":'+ stringRojo
    body = body +',"Verde":'+ stringVerde
    body = body +',"Azul":'+stringAzul+'}]}'

    print ("")
    print (body)
    #r = http.urlopen('POST', url, body=body, headers=headers)
    #print ("") 
    #print(r.status) 
    #print(r.data)
    time.sleep(5)
    
inicio = 0
captura=cv.CaptureFromCAM(0)
while True:
    imagen=cv.QueryFrame(captura)
    cv.ShowImage('Color',imagen)
    ch = 0xFF & cv.WaitKey(1)
    if ch == ord(' '):
        establecer_colores(imagen)
        inicio = 1
    if cv.WaitKey(30)==27:
        break
    if inicio == 1:
        p_red, p_green, p_blue = pixeles(imagen)
        hcp(p_red, p_green, p_blue)
        #time.delay(5000)
