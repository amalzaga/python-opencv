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


def tb_callback_pan(x):
    angle_pan = cv2.getTrackbarPos('Pan','camera')
    duty_pan = 100 - ((float(angle_pan) / 180) * duty_span + duty_min)
    PWM.set_duty_cycle(servo_pan, duty_pan)
      
 
def tb_callback_tilt(x):
    angle_tilt = cv2.getTrackbarPos('Tilt','camera')
    duty_tilt = 100 - ((float(angle_tilt) / 180) * duty_span + duty_min)
    PWM.set_duty_cycle(servo_tilt, duty_tilt)
    

PWM.start(servo_tilt,100 - ((float(angle_tilt) / 180) * duty_span + duty_min),60.0,1
PWM.start(servo_pan,100 - ((float(angle_pan) / 180) * duty_span + duty_min),60.0,1)

cv2.namedWindow("camera", 1)
cv2.createTrackbar('Pan','camera',angle_pan,180,tb_callback_pan)
cv2.createTrackbar('Tilt','camera',angle_tilt,180,tb_callback_tilt)

cap = cv2.VideoCapture(0)
if not cap.isOpened:
    print "Unable to open device"
    sys.exit(1)

cap.set(3, 320)
cap.set(4, 240)

while True:
    ret, img = cap.read()
    if not ret:
        print "Unable to retrieve frame from the device"
        sys.exit(1)
    
    cv2.imshow('camera',img)

    if cv2.waitKey(10) & 0xFF == 27:
        PWM.stop(servo_pan)
        PWM.stop(servo_tilt)
        PWM.cleanup()
        break


cap.release()
cv2.destroyAllWindows()
