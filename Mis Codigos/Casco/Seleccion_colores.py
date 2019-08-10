#!/usr/bin/python

import cv
tolerancia = 30
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
    k=cv.Load("colores.xml")
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

imagen=cv.LoadImage("Desktop/OpenCV codigos/Mis Codigos/Casco/e.bmp")
cv.ShowImage('Prueba',imagen)
establecer_colores(imagen)
print 'rojo = ',pixel_rojo
print 'Verde = ', pixel_verde
print 'Azul = ', pixel_azul
