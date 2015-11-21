#!/usr/bin/python
import cv2
import numpy as np
import Adafruit_BBIO.PWM as PWM 

servo_pan = "P9_14"
servo_tilt = "P9_22" 
duty_min = 3 
duty_max = 14.5 
duty_span = duty_max - duty_min 
angle_pan = 90
angle_tilt = 40

tracking = 0

im_width, im_height = 352,288

cap = cv2.VideoCapture(0)
cap.set(3, im_width)
cap.set(4, im_height)
mask = np.zeros((288,352,1), np.uint8)
res = np.zeros((288,352,3), np.uint8)
h = 164
ap = 12
lower_h = 152
upper_h = 176
sat_min = 98
vol_min = 90


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


# mouse callback function
def draw_circle(event,x,y,flags,param):
    global tracking
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(res,(x,y),20,(255,0,0),-1)
        tracking = not(tracking)


cv2.namedWindow('Live view')
cv2.namedWindow('HSV mask')

cv2.setMouseCallback('Live view',draw_circle)

cv2.createTrackbar('Hue','HSV mask',h,179,tb_callback)
cv2.createTrackbar('Hue aperture  ','HSV mask',ap,50,tb_callback)
cv2.createTrackbar('Saturation cut','HSV mask',sat_min,255,tb_callback)
cv2.createTrackbar('Volume cut     ','HSV mask',vol_min,255,tb_callback)


PWM.start(servo_tilt,100 - ((float(angle_tilt) / 180) * duty_span + duty_min),60.0,1)
PWM.start(servo_pan,100 - ((float(angle_pan) / 180) * duty_span + duty_min), 60.0,1)


while(1):

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_color = np.array([lower_h,sat_min,vol_min])
    upper_color = np.array([upper_h,255,255])

    mask = cv2.inRange(hsv, lower_color, upper_color)

    res[:] = [0,0,0]
    _ = cv2.bitwise_and(frame,frame,res,mask)

    moments = cv2.moments(mask)
    area = int(moments['m00'])
    x, y = 0, 0
    font = cv2.FONT_HERSHEY_PLAIN
    
    if tracking == 0:
        texto = 'Tracking = OFF'
    else:
        texto = 'Tracking = ON'

    cv2.putText(res,texto,(12,16), font, 1,(255,255,255),1,0)


    if area > 10000:
        x = int(moments['m10']/area)
        y = int(moments['m01']/area)
        Ix = int(moments['m02'] - y * moments['m01'])
        Iy = int(moments['m20'] - x * moments['m10'])
        ix = Ix / area
        iy = Iy / area
        cv2.circle(frame,(x,y),5,(255,255,255),1)
        cv2.line(frame,(x-10,y),(x+10,y),(255,255,255),1)
        cv2.line(frame,(x,y-10),(x,y+10),(255,255,255),1)
      
        texto = 'area: ' + str(area) + ' x: ' + str(x) + ' y: ' + str(y)
        cv2.putText(res,texto,(12,264), font, 1,(255,255,255),1,0)
        texto = 'Ix: ' + str(ix) + ' Iy: ' + str(iy)
        cv2.putText(res,texto,(12,280), font, 1,(255,255,255),1,0)
        
        if tracking == 1:
            if x > (im_width/2 + 20):
                angle_pan = angle_pan - 1
                duty_pan = 100 - ((float(angle_pan) / 180) * duty_span + duty_min)
                PWM.set_duty_cycle(servo_pan, duty_pan)

            if x < (im_width/2 - 20):
                angle_pan = angle_pan + 1
                duty_pan = 100 - ((float(angle_pan) / 180) * duty_span + duty_min)
                PWM.set_duty_cycle(servo_pan, duty_pan)

            if y > (im_height/2 + 20):
                angle_tilt = angle_tilt - 1
                duty_tilt = 100 - ((float(angle_tilt) / 180) * duty_span + duty_min)
                PWM.set_duty_cycle(servo_tilt, duty_tilt)

            if y < (im_height/2 - 20):
                angle_tilt = angle_tilt + 1
                duty_tilt = 100 - ((float(angle_tilt) / 180) * duty_span + duty_min)
                PWM.set_duty_cycle(servo_tilt, duty_tilt)

    
    cv2.imshow('Live view',frame)
    cv2.imshow('HSV mask',res)
   
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        PWM.stop(servo_pan)
        PWM.stop(servo_tilt)
        PWM.cleanup()
        break

cv2.destroyAllWindows()

