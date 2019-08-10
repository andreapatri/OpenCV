#!/usr/bin/python

import cv
tolerancia = 30     
        
imagen=cv.LoadImage('e.bmp')#im.
cv.ShowImage('Prueba',imagen)

rojo      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
verde     = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
azul      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
amarillo  = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)

pixel_rojo     = [11,21,109]
pixel_verde    = [16,47,27 ]
pixel_azul     = [221,174,68]
#pixel_amarillo = [82,140,142] pelot
pixel_amarillo = [53,117,177] 

cv.InRangeS(imagen,(pixel_rojo[0]-tolerancia,pixel_rojo[1]-tolerancia,pixel_rojo[2]-tolerancia),(pixel_rojo[0]+tolerancia,pixel_rojo[1]+tolerancia,pixel_rojo[2]+tolerancia),rojo)

cv.InRangeS(imagen,(pixel_verde[0]-tolerancia,pixel_verde[1]-tolerancia,pixel_verde[2]-tolerancia),(pixel_verde[0]+tolerancia,pixel_verde[1]+tolerancia,pixel_verde[2]+tolerancia),verde)

cv.InRangeS(imagen,(pixel_azul[0]-tolerancia,pixel_azul[1]-tolerancia,pixel_azul[2]-tolerancia),(pixel_azul[0]+tolerancia,pixel_azul[1]+tolerancia,pixel_azul[2]+tolerancia),azul)

cv.InRangeS(imagen,(pixel_amarillo[0]-tolerancia,pixel_amarillo[1]-tolerancia,pixel_amarillo[2]-tolerancia),(pixel_amarillo[0]+tolerancia,pixel_amarillo[1]+tolerancia,pixel_amarillo[2]+tolerancia),amarillo)

cv.ShowImage('Color Rojo'     ,rojo)
cv.ShowImage('Color Verde'    ,verde)
cv.ShowImage('Color Azul'     ,azul)
cv.ShowImage('Color Amarillo' ,amarillo)

cr = []
cg = []
ca = []
cy = []
p = 0
count_ball = 0
(new_coord_ball, new_coord_ball0, new_coord_ball1, new_coord_ball2) = ([],[],[],[])

for j in range(1,480,1):  
  for i in range(1,640,1):
     r = cv.Get2D(rojo ,j,i)
     a = cv.Get2D(azul ,j,i)
     v = cv.Get2D(verde,j,i)
     y = cv.Get2D(amarillo,j,i)
     if r[0] == 255: 
	cr += [(i,j)]
	exec('old_coord_ball%d = new_coord_ball'%p)
	exec('new_coord_ball%d += [(i,j)]'%p)
	if exec('old_coord_ball%d - 5 < new_coord_ball%d < old_coord_ball%d + 5'%p,%p,%p):
	   exec('sumax_ball%d = averx_ball + i'%p)
	   exec('sumay_ball%d = averx_ball + j'%p)
	   exec('count_ball%d = count_ball + 1'%p)
	else:
	   p = p + 1
	   new_coord_ball += [(i,j)]
     if v[0] == 255: 
	cg += [(i,j)]
     if a[0] == 255: 
	ca += [(i,j)]
     if y[0] == 255: 
	cy += [(i,j)]
	
	
	
print 'Numero de pixeles:\nrojo: ',len(cr) ,'   verde: ', len(cg) ,'   azul: ', len(ca) ,'   amarillo: ',len(cy)
print ca
cv.WaitKey(0)