#!/usr/bin/python

print '\nRecorrido'

# m_cord= |  Xro , Yro  |      Coordenada posicion inicial del robot
#	  |  Xp1 , Yp1  |      Coordenada pelota 1
#         |  Xp2 , Yp2  |      Coordenada pelota 2
#         |  Xp3 , Yp3  |      Coordenada pelota 3
#         |  Xro , Yro  |      Coordenada posicion final del robot

# m_pos_rob= |  Xrb , Yrb  |      Coordenada marca de atras del robot
#	     |  Xro , Yro  |      Coordenada marca central del robot
#            |  Xrf , Yrf  |      Coordenada marca frontal del robot

m_cord    = [[0,2],[3,5],[3,5],[3,5],[3,5]]
m_pos_rob = [[0,2],[3,5],[3,5]]

#Coordenadas
x_dest       = m_cord[n][0]  #Posicion destino
y_dest       = m_cord[n][1]
xrb = m_pos_rob[0][0]  #Posicion actual de atras del robot
yrb = m_pos_rob[0][1]
xro = m_pos_rob[1][0]  #Posicion actual del centro del robot
yro = m_pos_rob[1][1]
xrf = m_pos_rob[2][0]  #Posicion actual del frente del robot
yrf = m_pos_rob[2][1]


# ------------ FUNCIONES -------------- #

#Raiz Cuadrada  
def RaizCuadrada(X):
	R = X
	T = 0
	while (T != R):
		T = R
		R = (X/R + R)/2
	return R

#Hallar la ecuacion de recta y evaluar en punto
def correccion(x1,y1,x2,y2,x_evaluado,y_evaluado):
    pendiente = (y2 - y1)/(x2 - x1)
    if(((x_evaluado-x1)*pendiente)-y_evaluado+y1>0):
      direccion='d' #girar hacia la derecha
    elif(((x_evaluado-x1)*pendiente)-y_evaluado+y1<0):
      direccion='i' #girar hacia la izquierda
    else:
      direccion='a' #ir hacia adelante
    return direccion

#Distancia entre 2 puntos
def distancia(x1,y1,x2,y2):
    u = RaizCuadrada(((y2-y1)*(y2-y1))+((x2-x1)*(x2-x1)))
    return u
    
#Girar hacia la derecha
#def derecha()

#Girar hacia la derecha
#def izquierda()

#Ir hacia adelante
#def adelante()

#------------------------------------------------------------#

giro = correccion(xrb,yrb,xrf,yrf,x_dest,y_dest)
while (giro != 'a'): # si giro=2  ya es colineal
    seguimiento_trayectoria( giro , 0,04 )
    giro = correccion(xrb,yrb,xrf,yrf,x_dest,y_dest)
    
dist_ro_dest = distancia(xro,yro,x_dest,y_dest)    
if(dist_ro_dest >= 1) # distancia entre robot y prox. pelota mayor a 1 metro
    seguimiento_trayectoria( giro , 3 )
else
    seguimiento_trayectoria( giro , 1 )

#------------------------------------------------------------#