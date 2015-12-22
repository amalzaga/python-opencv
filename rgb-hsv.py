# Creates a solid color image wich can be changed by using two sets
# of trackbars RGB and HSV. Changing one affects the other
# It is a practical way to better understanding of colorspaces.
#
# Written by Amador Alzaga 

#!/usr/bin/python

import cv2
import numpy as np


def RGB_tb_callback(x):
    # get current positions of RGB trackbars and set HSV ones
    r = cv2.getTrackbarPos('R','RGB vs HSV')
    g = cv2.getTrackbarPos('G','RGB vs HSV')
    b = cv2.getTrackbarPos('B','RGB vs HSV')
    img[:] = [b,g,r]
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v = img_hsv[0][0][0],img_hsv[0][0][1],img_hsv[0][0][2]
    cv2.setTrackbarPos('H','RGB vs HSV',h)
    cv2.setTrackbarPos('S','RGB vs HSV',s)
    cv2.setTrackbarPos('V','RGB vs HSV',v)

def HSV_tb_callback(x):
    h = cv2.getTrackbarPos('H','RGB vs HSV')
    s = cv2.getTrackbarPos('S','RGB vs HSV')
    v = cv2.getTrackbarPos('V','RGB vs HSV')
    img_hsv[:] = [h,s,v]
    img = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
    b,g,r = img[0][0][0],img[0][0][1],img[0][0][2]
    cv2.setTrackbarPos('B','RGB vs HSV',b)
    cv2.setTrackbarPos('G','RGB vs HSV',g)
    cv2.setTrackbarPos('R','RGB vs HSV',r)


# Create images and windows
img = np.zeros((240,320,3), np.uint8)
img_hsv = np.zeros((240,320,3), np.uint8)
cv2.namedWindow('RGB vs HSV',0)
cv2.namedWindow('Result')

# create RGB & HSV trackbars
[r,g,b] = [0,0,0]
[h,s,v] = [0,0,0]
cv2.createTrackbar('R','RGB vs HSV',r,255,RGB_tb_callback)
cv2.createTrackbar('G','RGB vs HSV',g,255,RGB_tb_callback)
cv2.createTrackbar('B','RGB vs HSV',b,255,RGB_tb_callback)

cv2.createTrackbar('H','RGB vs HSV',h,179,HSV_tb_callback)
cv2.createTrackbar('S','RGB vs HSV',s,255,HSV_tb_callback)
cv2.createTrackbar('V','RGB vs HSV',v,255,HSV_tb_callback)


while(1):
    cv2.imshow('Result',img)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
