#!/usr/bin/python
# This code only showws camera captured frames on a window if all works as expected
# An USB webcam like Logitech C270 must be connected on USB bus

import cv2
import numpy as np

cv2.namedWindow("camera", 1)
cap = cv2.VideoCapture(0)
if not cap.isOpened:
    print "Unable to open device"
    sys.exit(1)

# Set frame size to 320 x 240 pixels
cap.set(3, 320)
cap.set(4, 240)

# Main loop. Exits on error or ESC key pressed.
while True:
    ret, img = cap.read()
    if not ret:
        print "Unable to retrieve frame from the device"
        sys.exit(1)
        
    cv2.imshow('camera',img)
    
    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
