#!/usr/bin/env python
 
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import time
from geometry_msgs.msg import Twist
import select, termios, tty
import sys
import cv
import numpy as np
import urllib
import math
 
# --------------------- DECLARACION DE VARIABLES -------------------- #
 
color = []
pixel_rojo, pixel_azul, pixel_verde = ([],[],[])
points = []
moveBindings = {
        'a':(1,0),
        'i':(0,1),
        'd':(0,-1),
        }
speed = 1
turn = 1
tiempo_90 = 1.3
tiempo_1m = 2.17
ancho_cancha = 350
largo_cancha = 320
alt_tripode = 220
alt_robot = 8.9
dist_trip_cancha = 211
 
 
 
# ---------------------------- FUNCIONES ---------------------------- #
 
def guardarpoints(points):
    global teclado
    p = cv.CreateMat(4,2,cv.CV_64FC1)
    for i in range(4):
       (x,y) = points[i]
       p[i,0] = x
       p[i,1] = y  
    cv.Save("puntos.xml", p)
     
def cargarpoints():
    punto, points = [] , []   
    k = cv.CreateMat(4,2,cv.CV_64FC1)
    k=cv.Load("puntos.xml")
    for i in range(4):
    punto += (k[i,0],k[i,1])
    for w in range(0, 7, 2):
        x=punto[w]
        y=punto[w+1]
        points += [(x,y)]   
    return points
     
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
    cv.Save("colores.xml", k)
 
def cargarcolores():
    global pixel_rojo, pixel_verde, pixel_azul, points  
    k = cv.CreateMat(3,3,cv.CV_64FC1)
    k=cv.Load("colores.xml")
    pixel_rojo  = (k[0,0],k[0,1],k[0,2])
    pixel_verde = (k[1,0],k[1,1],k[1,2])
    pixel_azul  = (k[2,0],k[2,1],k[2,2])
    return pixel_rojo, pixel_verde, pixel_azul
 
def mouse(evt,x,y,flags,ctx):
    if evt==cv.CV_EVENT_LBUTTONUP:
        global points
        points += [(x,y)]
 
def homografia(real_width, real_height, width, height):
    global points, teclado    
    if len(points)!=4 :
        raise Exception('falto algun punto')
 
    p = cv.CreateMat(2,4,cv.CV_64FC1)
    h = cv.CreateMat(2,4,cv.CV_64FC1)
    p2h = cv.CreateMat(3,3,cv.CV_64FC1)
 
    cv.Zero(p)
    cv.Zero(h)
    cv.Zero(p2h)
 
    for i in range(4):
        (x,y) = points[i]
        p[0,i] = (float(real_width)/float(width)) * x
        p[1,i] = (float(real_height)/float(height)) * y
 
    h[0,0] = 0
    h[1,0] = real_height
 
    h[0,1] = real_width
    h[1,1] = real_height
 
    h[0,2] = real_width
    h[1,2] = 0
 
    h[0,3] = 0
    h[1,3] = 0
 
    cv.FindHomography(p,h,p2h)
    return p2h
 
def imagen_homografia(n):
     
    global points, width, height,teclado
     
    urllib.urlretrieve("http://192.168.0.100:8080/photo.jpg", "foto.jpg")
    foto=cv.LoadImage('foto.jpg')
    im_in= cv.CloneImage(foto)
    #CALIBRACION
    width, height = cv.GetSize(im_in)
    im = cv.CloneImage(foto)
    if n == 0 and (teclado ==1 or teclado ==3):
      cv.ShowImage('Escoger 4 puntos',im)
      cv.SetMouseCallback('Escoger 4 puntos', mouse, im)
      cv.WaitKey(0)
      guardarpoints(points)      
      homo = homografia(im_in.width, im_in.height, im.width, im.height)
      cv.Save('homography.cvmat', homo)
    else:
      points = cargarpoints()
      homo = homografia(im_in.width, im_in.height, im.width, im.height)
    out_big = cv.CloneImage(im_in)
    cv.WarpPerspective(im_in, out_big, homo)
    out_small = cv.CloneImage(im)
    cv.Resize(out_big, out_small)
    return out_small, out_big
 
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
    if (teclado == 1 or teclado == 2):
    nombre_color = 'Seleccionar una de las Pelotas'
    colors(imagen, nombre_color)
    pixel_rojo = color
    cv.DestroyWindow('Seleccionar una de las Pelotas')
     
    nombre_color = 'Seleccionar la marca central del robot'
    colors(imagen, nombre_color)
    pixel_verde = color
    cv.DestroyWindow('Seleccionar la marca central del robot')
       
    nombre_color = 'Seleccionar la marca frontal del robot'
    colors(imagen, nombre_color)
    pixel_azul = color
    cv.DestroyWindow('Seleccionar la marca frontal del robot')
     
    cv.DestroyWindow('Seleccionando pixeles')
     
     
    guardarcolores(pixel_rojo, pixel_verde, pixel_azul)
     
    elif (teclado == 3 or teclado == 4):
        pixel_rojo, pixel_verde, pixel_azul = cargarcolores()
 
def reconocimiento_pelotas_y_robot ():
    global pixel_rojo, pixel_verde , width , height
    peq_imagen, imagen = imagen_homografia(1)
    tolerancia = 30    
         
    rojo      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    verde     = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
 
    cv.InRangeS(imagen,(pixel_rojo[0]-tolerancia,pixel_rojo[1]-tolerancia,pixel_rojo[2]-tolerancia),(pixel_rojo[0]+tolerancia,pixel_rojo[1]+tolerancia,pixel_rojo[2]+tolerancia),rojo)
 
    cv.InRangeS(imagen,(pixel_verde[0]-tolerancia,pixel_verde[1]-tolerancia,pixel_verde[2]-tolerancia),(pixel_verde[0]+tolerancia,pixel_verde[1]+tolerancia,pixel_verde[2]+tolerancia),verde)
     
    (cg, cr) = ([],[])
    (p1, p2, p3) = ([],[],[])
    sumx_g = sumy_g =  0
    sumx_p1 = sumx_p2 = sumx_p3 = sumy_p1 = sumy_p2 = sumy_p3 = 0
    inicio = inicio2 = inicio3 = 0
    off = 100
    old_x = old_y = 0
    for j in range(1,height,1):  
      for i in range(1,width,1):
    r = cv.Get2D(rojo ,j,i)
    g = cv.Get2D(verde,j,i)
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
    if g[0] == 255: 
        cg    += [(i,j)]
        sumx_g  = sumx_g + i
        sumy_g  = sumy_g + j  
    p_old1_x = i 
    p_old1_y = j  
 
    ro_x = sumx_g/len(cg)      #0
    ro_y = sumy_g/len(cg)   
     
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
 
def reconocimiento_robot_pos ():
   
    global pixel_azul, pixel_verde , width , height
    peq_imagen, imagen = imagen_homografia(1)
    tolerancia = 30    
 
    verde     = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
    azul      = cv.CreateImage(cv.GetSize(imagen),cv.IPL_DEPTH_8U,1)
     
    cv.InRangeS(imagen,(pixel_verde[0]-tolerancia,pixel_verde[1]-tolerancia,pixel_verde[2]-tolerancia),(pixel_verde[0]+tolerancia,pixel_verde[1]+tolerancia,pixel_verde[2]+tolerancia),verde)
 
    cv.InRangeS(imagen,(pixel_azul[0]-tolerancia,pixel_azul[1]-tolerancia,pixel_azul[2]-tolerancia),(pixel_azul[0]+tolerancia,pixel_azul[1]+tolerancia,pixel_azul[2]+tolerancia),azul)
 
    (cg, cb, cy) = ([],[],[])
    sumx_g = sumy_g = sumx_b = sumy_b = sumx_y = sumy_y = 0
     
    for j in range(1,height,1):  
      for i in range(1,width,1):
    b = cv.Get2D(azul ,j,i)
    g = cv.Get2D(verde,j,i)
    if g[0] == 255: 
        cg    += [(i,j)]
        sumx_g  = sumx_g + i
        sumy_g  = sumy_g + j  
    if b[0] == 255: 
        cb += [(i,j)]
        sumx_b  = sumx_b + i
        sumy_b  = sumy_b + j 
    p_old1_x = i 
    p_old1_y = j  
     
    ro_x = sumx_g/len(cg)   
    ro_y = sumy_g/len(cg)   
    rf_x = sumx_b/len(cb)   
    rf_y = sumy_b/len(cb)
     
     
    alt_real_tripode = alt_tripode - (float(dist_trip_cancha*alt_tripode)/float(dist_trip_cancha+largo_cancha))
    corr_ro_y =  float(ro_y) + (float(ro_y * alt_robot) / float(alt_real_tripode))
    corr_rf_y =  float(rf_y) + (float(rf_y * alt_robot) / float(alt_real_tripode))
  
    if ro_x > width/2 :
      corr_ro_x =  float(ro_x) - (float(ro_x * alt_robot) / float(alt_real_tripode))
    else:
      corr_ro_x =  float(ro_x) + (float(ro_x * alt_robot) / float(alt_real_tripode))
       
    if rf_x > width/2 :
      corr_rf_x =  float(rf_x) - (float(rf_x * alt_robot) / float(alt_real_tripode))
    else:
      corr_rf_x =  float(rf_x) + (float(rf_x * alt_robot) / float(alt_real_tripode))
       
    return ro_x,corr_ro_y+20,rf_x,corr_rf_y+20
 
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
    dis_0_1 = distancia(ro_x, ro_y, p1_x, p1_y) 
    dis_0_2 = distancia(ro_x, ro_y, p2_x, p2_y) 
    dis_0_3 = distancia(ro_x, ro_y, p3_x, p3_y) 
    dis_1_2 = distancia(p1_x, p1_y, p2_x, p2_y)  
    dis_1_3 = distancia(p1_x, p1_y, p3_x, p3_y)  
    dis_2_3 = distancia(p2_x, p2_y, p3_x, p3_y) 
 
    m_dist = [[0,1,dis_0_1],[0,2,dis_0_2],[0,3,dis_0_3],[1,2,dis_1_2],[1,3,dis_1_3],[2,3,dis_2_3]]
     
    sec1 = dis_0_1 + dis_1_2 + dis_2_3 + dis_0_3
    sec2 = dis_0_1 + dis_1_3 + dis_2_3 + dis_0_2
    sec3 = dis_0_2 + dis_1_2 + dis_1_3 + dis_0_3
     
    m_coord = []
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
 
    for j in range(0,5):
        if (((m_cord[j][0] != ro_x) and (m_cord[j][1] != ro_y)) or j==0) or j==4:
      m_coord += [(m_cord[j][0],m_cord[j][1])]
          
    return m_coord
 
def correccion(ro_x,ro_y,rf_x,rf_y,x_evaluado,y_evaluado):
    if (float(ro_x-rf_x)==0):
      calc = y_evaluado-ro_y-((float(ro_y-rf_y)/(0.001))*(x_evaluado-ro_x))
      print 'Division por 0 evitada'
    else:  
      calc = y_evaluado-ro_y-((float(ro_y-rf_y)/float(ro_x-rf_x))*(x_evaluado-ro_x))
    print 'giro=',calc
    g=50
    if ro_x > rf_x :
      if calc < -g:
     direccion='d'
      elif calc > g:
     direccion='i'
      else:
     direccion='a'
    elif ro_x < rf_x :
      if calc > g:
         direccion='d'
      elif calc < -g:
     direccion='i'
      else:
     direccion='a'
    else:
         direccion='d'
    return direccion  
 
def angulo(ro_x,ro_y,rf_x,rf_y,p_x,p_y):
    new_ro_x = 0
    new_ro_y = 0
    new_rf_x = rf_x - ro_x 
    new_rf_y = ro_y - rf_y
    new_p_x  = p_x - ro_x 
    new_p_y  = ro_y - p_y
    valor = ((new_p_x*new_rf_x)+(new_p_y*new_rf_y))/float (RaizCuadrada((new_p_x*new_p_x)+(new_p_y*new_p_y))*RaizCuadrada((new_rf_x*new_rf_x)+(new_rf_y*new_rf_y)))
    if valor < -1:
       valor = -1
    if valor >  1:
       valor = 1
    ang=math.acos(valor)*57.2957795 #Conversion de radianes a grados
    print 'angulo: ', ang
    tiempo = ang*float(tiempo_90)/float (90)
    return tiempo  
 
 
def detener():
    x  = 0
    th = 0
    twist = Twist()
    twist.linear.x  = 0
    twist.linear.y  = 0
    twist.linear.z  = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0
    pub.publish(twist)
 
def seguimiento_trayectoria( key , tiempo ):
    x = moveBindings[key][0]
    th = moveBindings[key][1]
    twist = Twist()
    twist.linear.x  = x*speed
    twist.linear.y  = 0
    twist.linear.z  = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = th*turn
    pub.publish(twist)
    time.sleep(tiempo)
     
    detener()
     
def distancia_cm(x1_pix,y1_pix,x2_pix,y2_pix):
    global width, height
    x_cm_x1 = (ancho_cancha * x1_pix)/width
    y_cm_y1 = (largo_cancha * y1_pix)/height
    x_cm_x2 = (ancho_cancha * x2_pix)/width
    y_cm_y2 = (largo_cancha * y2_pix)/height
    dist_cm = distancia(x_cm_x1,y_cm_y1,x_cm_x2,y_cm_y2)
    return dist_cm
     
 
if __name__=="__main__":
   
  settings = termios.tcgetattr(sys.stdin)
  pub = rospy.Publisher('cmd_vel', Twist)
  rospy.init_node('seguimiento_trayectoria')
  x = 0
  th = 0
   
  try:  
       
    while True:
      teclado = input("Desea definir: \n   1) Area de la cancha y colores \n   2) Solamanete colores \n   3) Solamanete area de la cancha \n   4) Ninguno \n")
      imagen, imagen_grande = imagen_homografia(0)
      establecer_colores(imagen)
      ro_x,ro_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y, num_pel = reconocimiento_pelotas_y_robot ()
      m_coord = sec_tray(ro_x, ro_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y)
      print m_coord
      for i in range(1, num_pel + 2):
    pos_destino_x = m_coord[i][0]
    pos_destino_y = m_coord[i][1]
    dist  = distancia_cm ( ro_x, ro_y, pos_destino_x , pos_destino_y )
    print 'x = ', dist
    while (dist > 10):
        ro_x,ro_y,rf_x,rf_y= reconocimiento_robot_pos () 
        direccion= correccion(ro_x,ro_y,rf_x,rf_y,pos_destino_x,pos_destino_y)  
        n_giro = 0
        while (direccion != 'a' and n_giro < 2): 
          n_giro = n_giro + 1
          print '   Giro Numero = ', n_giro
          tiempo_giro = angulo(ro_x,ro_y,rf_x,rf_y,pos_destino_x,pos_destino_y)
          seguimiento_trayectoria( direccion , tiempo_giro )
          ro_x,ro_y,rf_x,rf_y = reconocimiento_robot_pos ()
          direccion= correccion(ro_x,ro_y,rf_x,rf_y,pos_destino_x, pos_destino_y)  
        dist = distancia_cm ( ro_x, ro_y, pos_destino_x , pos_destino_y )   
        if   (dist > 300):    
          seguimiento_trayectoria( direccion , tiempo_1m * 2 )
        elif (dist > 150):
          seguimiento_trayectoria( direccion , tiempo_1m * 1.3 )          
        else:
          tiempo_seguimiento = (float(dist)*float(tiempo_1m))/100
          seguimiento_trayectoria( direccion , tiempo_seguimiento )
        ro_x,ro_y,rf_x,rf_y = reconocimiento_robot_pos ()
        dist = distancia_cm ( ro_x, ro_y, pos_destino_x , pos_destino_y )
        print '   Distancia restante = ', dist
    print 'Fin Pelota' 
      break 
   
  finally:
    twist = Twist()
    pub.publish(twist)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)