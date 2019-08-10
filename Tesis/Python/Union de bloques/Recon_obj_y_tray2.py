#!/usr/bin/python

import cv

def reconocimiento_pelotas_y_robot (imagen):

    tolerancia = 30     
	    
    cv.ShowImage('Prueba',imagen)

    rojo      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    verde     = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    azul      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    amarillo  = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)

    pixel_rojo     = [36,28,237]
    pixel_verde    = [76,177,34]
    pixel_azul     = [232,162,0]
    pixel_amarillo = [164,73,163] 

    cv.InRangeS(imagen,(pixel_rojo[0]-tolerancia,pixel_rojo[1]-tolerancia,pixel_rojo[2]-tolerancia),(pixel_rojo[0]+tolerancia,pixel_rojo[1]+tolerancia,pixel_rojo[2]+tolerancia),rojo)

    cv.InRangeS(imagen,(pixel_verde[0]-tolerancia,pixel_verde[1]-tolerancia,pixel_verde[2]-tolerancia),(pixel_verde[0]+tolerancia,pixel_verde[1]+tolerancia,pixel_verde[2]+tolerancia),verde)

    cv.InRangeS(imagen,(pixel_azul[0]-tolerancia,pixel_azul[1]-tolerancia,pixel_azul[2]-tolerancia),(pixel_azul[0]+tolerancia,pixel_azul[1]+tolerancia,pixel_azul[2]+tolerancia),azul)

    cv.InRangeS(imagen,(pixel_amarillo[0]-tolerancia,pixel_amarillo[1]-tolerancia,pixel_amarillo[2]-tolerancia),(pixel_amarillo[0]+tolerancia,pixel_amarillo[1]+tolerancia,pixel_amarillo[2]+tolerancia),amarillo)

    cv.ShowImage('Color Rojo'     ,rojo)
    cv.ShowImage('Color Verde'    ,verde)
    cv.ShowImage('Color Azul'     ,azul)
    cv.ShowImage('Color Amarillo' ,amarillo)

    (cg, ca, cy, cr) = ([],[],[],[])
    (p1, p2, p3) = ([],[],[])
    sumx_g = sumy_g = sumx_a = sumy_a = sumx_y = sumy_y = 0 
    sumx_p1 = sumx_p2 = sumx_p3 = sumy_p1 = sumy_p2 = sumy_p3 = 0 
    inicio = inicio2 = inicio3 = 0
    off = 20
    old_x = old_y = 0
    for j in range(1,480,1):  
      for i in range(1,640,1):
	r = cv.Get2D(rojo ,j,i)
	a = cv.Get2D(azul ,j,i)
	v = cv.Get2D(verde,j,i)
	y = cv.Get2D(amarillo,j,i)
	if r[0] == 255: 
	    cr += [(i,j)]
	    if   inicio == 0 :
		inicio = 1
		old_x = i  
		old_y = j
	    elif i > old_x-off and i < old_x+off and j > old_y-off and j < old_y+off :
		p1 += [(i,j)]
		sumx_p1 = sumx_p1 + i
		sumy_p1 = sumy_p1 + j 
		old_x = i 
		old_y = j
	    else:
		if   inicio2 == 0 :
		    inicio2 = 1
		    old_x2 = i  
		    old_y2 = j
		elif i > old_x2-off and i < old_x2+off and j > old_y2-off and j < old_y2+off :
		    p2 += [(i,j)]
		    sumx_p2 = sumx_p2 + i
		    sumy_p2 = sumy_p2 + j 
		    old_x2 = i 
		    old_y2 = j
		else:
		    if  inicio3 == 0 :
			inicio3 = 1
			old_x3 = i  
			old_y3 = j
		    elif i > old_x3-off and i < old_x3+off and j > old_y3-off and j < old_y3+off :
			p3 += [(i,j)]
			sumx_p3 = sumx_p3 + i
			sumy_p3 = sumy_p3 + j 
			old_x3 = i 
			old_y3 = j
	if v[0] == 255: 
	    cg    += [(i,j)]
	    sumx_g  = sumx_g + i
	    sumy_g  = sumy_g + j  
	if a[0] == 255: 
	    ca += [(i,j)]
	    sumx_a  = sumx_a + i
	    sumy_a  = sumy_a + j 
	if y[0] == 255: 
	    cy += [(i,j)]
	    sumx_y  = sumx_y + i
	    sumy_y  = sumy_y + j
	p_old1_x = i 
	p_old1_y = j  

    ro_x = sumx_g/len(cg)	   #0
    ro_y = sumy_g/len(cg)	
    rf_x = sumx_a/len(ca)	
    rf_y = sumy_a/len(ca)
    rb_x = sumx_y/len(cy)	
    rb_y = sumy_y/len(cy)
    
    num_pel = 0

    if(len(p1)==0):
      p1_x = ro_x 
      p1_y = ro_y
    else:
      p1_x = sumx_p1/len(p1)      #1
      p1_y = sumy_p1/len(p1) 
      num_pel = num_pel + 1

    if(len(p2)==0):
      p2_x = ro_x       
      p2_y = ro_y 
    else:
      p2_x = sumx_p2/len(p2)      #2
      p2_y = sumy_p2/len(p2) 
      num_pel = num_pel + 1
      
    if(len(p3)==0):
      p3_x = ro_x       
      p3_y = ro_y
    else:
      p3_x = sumx_p3/len(p3)      #3
      p3_y = sumy_p3/len(p3) 
      num_pel = num_pel + 1
      
     
    return ro_x,ro_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,num_pel


def reconocimiento_robot_pos (imagen):

    tolerancia = 30     
	    
    cv.ShowImage('Prueba',imagen)

    verde     = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    azul      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    amarillo  = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)

    pixel_verde    = [76,177,34]
    pixel_azul     = [232,162,0]
    pixel_amarillo = [164,73,163] 

    cv.InRangeS(imagen,(pixel_verde[0]-tolerancia,pixel_verde[1]-tolerancia,pixel_verde[2]-tolerancia),(pixel_verde[0]+tolerancia,pixel_verde[1]+tolerancia,pixel_verde[2]+tolerancia),verde)

    cv.InRangeS(imagen,(pixel_azul[0]-tolerancia,pixel_azul[1]-tolerancia,pixel_azul[2]-tolerancia),(pixel_azul[0]+tolerancia,pixel_azul[1]+tolerancia,pixel_azul[2]+tolerancia),azul)

    cv.InRangeS(imagen,(pixel_amarillo[0]-tolerancia,pixel_amarillo[1]-tolerancia,pixel_amarillo[2]-tolerancia),(pixel_amarillo[0]+tolerancia,pixel_amarillo[1]+tolerancia,pixel_amarillo[2]+tolerancia),amarillo)

    cv.ShowImage('Color Verde'    ,verde)
    cv.ShowImage('Color Azul'     ,azul)
    cv.ShowImage('Color Amarillo' ,amarillo)

    (cg, ca, cy) = ([],[],[])
    sumx_g = sumy_g = sumx_a = sumy_a = sumx_y = sumy_y = 0 
    
    for j in range(1,480,1):  
      for i in range(1,640,1):
	a = cv.Get2D(azul ,j,i)
	v = cv.Get2D(verde,j,i)
	y = cv.Get2D(amarillo,j,i)
	if v[0] == 255: 
	    cg    += [(i,j)]
	    sumx_g  = sumx_g + i
	    sumy_g  = sumy_g + j  
	if a[0] == 255: 
	    ca += [(i,j)]
	    sumx_a  = sumx_a + i
	    sumy_a  = sumy_a + j 
	if y[0] == 255: 
	    cy += [(i,j)]
	    sumx_y  = sumx_y + i
	    sumy_y  = sumy_y + j
	p_old1_x = i 
	p_old1_y = j  

    ro_x = sumx_g/len(cg)	   #0
    ro_y = sumy_g/len(cg)	
    rf_x = sumx_a/len(ca)	
    rf_y = sumy_a/len(ca)
    rb_x = sumx_y/len(cy)	
    rb_y = sumy_y/len(cy)

    return ro_x,ro_y,rf_x,rf_y,rb_x,rb_y

def RaizCuadrada(X):
	R = X
	T = 0
	while (T != R):
		T = R
		R = (X/R + R)/2
	return R
	
def distancia(x1,y1,x2,y2):
    u = RaizCuadrada(((y2-y1)*(y2-y1))+((x2-x1)*(x2-x1)))
    return u
    
def sec_tray(ro_x, ro_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
    #Distancia entre cada par de puntos
    dis_0_1 = distancia(ro_x, ro_y, p1_x, p1_y) 
    dis_0_2 = distancia(ro_x, ro_y, p2_x, p2_y) 
    dis_0_3 = distancia(ro_x, ro_y, p3_x, p3_y) 
    dis_1_2 = distancia(p1_x, p1_y, p2_x, p2_y)  
    dis_1_3 = distancia(p1_x, p1_y, p3_x, p3_y)  
    dis_2_3 = distancia(p2_x, p2_y, p3_x, p3_y) 

    m_dist = [[0,1,dis_0_1],[0,2,dis_0_2],[0,3,dis_0_3],[1,2,dis_1_2],[1,3,dis_1_3],[2,3,dis_2_3]]
    
    print 'distancias: ',dis_0_1, dis_0_2, dis_0_3, dis_1_2, dis_1_3, dis_2_3

    #Hallar las distancias para las secuencias:
    # sec1  0  1  2  3  0
    # sec2  0  1  3  2  0
    # sec3  0  2  1  3  0
    sec1 = dis_0_1 + dis_1_2 + dis_2_3 + dis_0_3
    sec2 = dis_0_1 + dis_1_3 + dis_2_3 + dis_0_2
    sec3 = dis_0_2 + dis_1_2 + dis_1_3 + dis_0_3
    print 'Sumatoria secuencias: ' ,sec1, sec2, sec3
    
    #Menor trayecto
    menor=0; 
    if(sec1<sec2):
      if(sec1<sec3):
	  menor  = sec1
	  m_cord = [[ro_x,ro_y],[p1_x,p1_y],[p2_x,p2_y],[p3_x,p3_y],[ro_x,ro_y]] 
      else:
	  menor  = sec3
	  m_cord = [[ro_x,ro_y],[p2_x,p2_y],[p1_x,p1_y],[p3_x,p3_y],[ro_x,ro_y]] 
    else:
      if(sec2<sec3):
	  menor  = sec2
	  m_cord = [[ro_x,ro_y],[p1_x,p1_y],[p3_x,p3_y],[p2_x,p2_y],[ro_x,ro_y]] 
      else:
	  menor  = sec3
	  m_cord = [[ro_x,ro_y],[p2_x,p2_y],[p1_x,p1_y],[p3_x,p3_y],[ro_x,ro_y]] 

    m_pos_rob = [[rb_x,rb_y],[ro_x,ro_y],[rf_x,rf_y]]
    
    m_coord = []
    

    for j in range(0,5):
        if (((m_cord[j][0] != ro_x) and (m_cord[j][1] != ro_y)) or j==0) or j==4:
	  m_coord += [(m_cord[j][0],m_cord[j][1])]
         
    return menor, m_coord, m_pos_rob

#------------------------------------ FIN FUNCIONES ------------------------------------#

imagen=cv.LoadImage('4.png')
ro_x,ro_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y, num_pel = reconocimiento_pelotas_y_robot (imagen)
ro_x,ro_y,rf_x,rf_y,rb_x,rb_y                    = reconocimiento_robot_pos (imagen)

print 'ro:    ', ro_x , ro_y,'   rf:    ', rf_x , rf_y,'   rb:    ', rb_x , rb_y
print 'ball1: ', p1_x , p1_y,'   ball2: ', p2_x , p2_y,'   ball3: ', p3_x , p3_y
print 'Numero pelotas: ', num_pel
menor, m_cord, m_pos_rob = sec_tray(ro_x, ro_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y)

print 'menor distancia = ',menor
print 'm_cord          = ',m_cord
print 'm_pos_rob       = ',m_pos_rob

cv.WaitKey(0)