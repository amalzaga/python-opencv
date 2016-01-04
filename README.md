# python-opencv
opencv over python tutorial - examples written exploring opencv capabilities using python as programming lenguaje - In the hope will be helpfull for someone

Also I will use AdafruitBBIO library to handle Beaglebone PWM outputs to control pan & tilt camera servos in some examples.

Files in his repository:

test-cam.py: simple camera test program which displays captured frames on a window.

servo-test.py: Uses Adafruit BBIO library to control a servomotor.

mouse-callback.py: example of use of callback function to add mouse interaction

rgb-hsv.py: this program shows a solid color image and several trackbars to choose RGB or HSV values of color shown. It is a very                    practical way to better understanding of RGB / HSV colorspaces.

pan-tilt.py: A couple of trackbars permit camera pan and tilt movement using microservos

obj-moments.py: Ilustrates some usefull methods used in computer vision. Converts captured frames to HSV colorspace to mek possible image segmentation by objects color. I have implemented trackbars to select Hue central value and apperture wich is the radius of the interval of Hue values to detect. Also it is possible to select saturation and volume cut values that are the threshold for S & V. OpenCV inRange function creates a 8-bit mask image with pixels that contains color in selected range. This mask is anded with original to produce result image where only object with selected color appears.  
