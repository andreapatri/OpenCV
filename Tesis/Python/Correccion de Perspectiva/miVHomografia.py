import sys
import cv
import numpy as np

points = []

def mouse(evt,x,y,flags,ctx):
    if evt==cv.CV_EVENT_LBUTTONUP:
        global points
        points += [(x,y)]
        
def homografia(real_width, real_height, width, height):
    global points
    if len(points)!=4:
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
        print p[0,i]
        p[1,i] = (float(real_height)/float(height)) * y
        print p[1,i]

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
    
captura=cv.CaptureFromCAM(1)
vid=cv.QueryFrame(captura)
im_in= cv.CloneImage(vid)
#im_in = cv.LoadImage('foto5.jpg', 4)
width, height = cv.GetSize(im_in)
im = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
cv.Resize(im_in, im)

cv.ShowImage('Escoger 4 puntos',im)
cv.SetMouseCallback('Escoger 4 puntos', mouse, im)
cv.WaitKey(0)

homo = homografia(im_in.width, im_in.height, im.width, im.height)
cv.Save('homography.cvmat', homo)

out = cv.CloneImage(im_in)
cv.WarpPerspective(im_in, out, homo)
out_small = cv.CloneImage(im)
cv.Resize(out, out_small)
cv.ShowImage('Homografia', out_small)
cv.WaitKey(0)
 
#captura=cv.CaptureFromCAM(1)
out = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
imagen=cv.QueryFrame(captura)      

creavideo = cv.CreateVideoWriter("reencode.avi",cv.CV_FOURCC('M', 'J', 'P', 'G'), 29.97,(640, 480))
#creavideo =cv.CreateVideoWriter("output.avi", 0, 15,(800,600) , 1)


while True:
    cv.WarpPerspective(imagen, out, homo)
    cv.ShowImage('Video',imagen)
    cv.ShowImage('Perspectiva',out)     
    cv.WriteFrame(creavideo, out)
    imagen=cv.QueryFrame(captura)      
    if cv.WaitKey(30)==27:
        break 
       
