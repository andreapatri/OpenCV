#!/usr/bin/python

import cv
tolerancia = 30

def evento_mouse(event,x,y,flags,param):
    if event==cv.CV_EVENT_LBUTTONDOWN:
        pixel=cv.Get2D(imagen,y,x) 
        print 'X =',x,'  Y =',y
        print 'R =',pixel[2],'G =',pixel[1],'B =',pixel[0]
        cv.InRangeS(imagen,(pixel[0]-tolerancia,pixel[1]-tolerancia,pixel[2]-tolerancia),(pixel[0]+tolerancia,pixel[1]+tolerancia,pixel[2]+tolerancia),temporal)
        cv.ShowImage('Color',temporal)
        for j in range(1,480,1): 
	  for i in range(1,640,1):
	     c=cv.Get2D(temporal,j,i)
	     if c[0] == 255: 
		print j,i
imagen=cv.LoadImage('im.png')
cv.ShowImage('Prueba',imagen)
temporal=cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
cv.SetMouseCallback('Prueba',evento_mouse)
cv.WaitKey(0)
