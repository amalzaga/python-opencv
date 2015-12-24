#!/usr/bin/python

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 352)
cap.set(4, 288)
mask = np.zeros((288,352,1), np.uint8)
res = np.zeros((288,352,3), np.uint8)
h = 164
ap = 12
lower_h = 152
upper_h = 176
sat_min = 98
vol_min = 90

# trackbars callback function wich reads HSV range values
def tb_callback(x):
    global lower_h, upper_h, sat_min, vol_min
    h = cv2.getTrackbarPos('Hue','HSV mask')
    ap = cv2.getTrackbarPos('Hue aperture  ','HSV mask')
    sat_min = cv2.getTrackbarPos('Saturation cut','HSV mask')
    vol_min = cv2.getTrackbarPos('Volume cut     ','HSV mask')

    lower_h = h - ap
    if lower_h < 0:
      lower_h = 0

    upper_h = h + ap
    if upper_h > 179:
      upper_h = 179



cv2.namedWindow('Live view')
cv2.namedWindow('HSV mask')

cv2.createTrackbar('Hue','HSV mask',h,179,tb_callback)
cv2.createTrackbar('Hue aperture  ','HSV mask',ap,50,tb_callback)
cv2.createTrackbar('Saturation cut','HSV mask',sat_min,255,tb_callback)
cv2.createTrackbar('Volume cut     ','HSV mask',vol_min,255,tb_callback)


while(1):
    # capture a frame and convert it to HSV colorspace
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Apply inRange method to create a  1 channel mask with image pixels
    # with color values inside the range given by trackbars values.
    lower_color = np.array([lower_h,sat_min,vol_min])
    upper_color = np.array([upper_h,255,255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Apply bitwise and to generate a result color image 
    res[:] = [0,0,0]
    _ = cv2.bitwise_and(frame,frame,res,mask)

    moments = cv2.moments(mask)
    area = int(moments['m00'])
    # If there is an object with larger area that a given value 
    # are calculated the coordinates of its gravity centre and 
    # the values of its inertial moments
    if area > 10000:
        x = int(moments['m10']/area)
        y = int(moments['m01']/area)
        Ix = int(moments['m02'] - y * moments['m01'])
        Iy = int(moments['m20'] - x * moments['m10'])
        ix = np.sqrt([Ix / area])
        iy = np.sqrt([Iy / area])
        
        # draw a cross and a circle signaling object in live view
        cv2.circle(frame,(x,y),5,(255,255,255),1)
        cv2.line(frame,(x-10,y),(x+10,y),(255,255,255),1)
        cv2.line(frame,(x,y-10),(x,y+10),(255,255,255),1)
        
        # add text info in result window
        font = cv2.FONT_HERSHEY_PLAIN
        texto = 'area: ' + str(area) + ' x: ' + str(x) + ' y: ' + str(y)
        cv2.putText(res,texto,(12,264), font, 1,(255,255,255),1,0)
        texto = 'Ix: ' + str(ix) + ' Iy: ' + str(iy)
        cv2.putText(res,texto,(12,280), font, 1,(255,255,255),1,0)

    cv2.imshow('Live view',frame)
    cv2.imshow('HSV mask',res)
   
    k = cv2.waitKey(2) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

