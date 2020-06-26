import numpy as np
import cv2
import time
from launcher_usb import *
import Tkinter


def nothing(x):
    pass


cap = cv2.VideoCapture(1)
ret = False

mL = usb_launcher()
mL.take_aim(x_max/2,y_max/2)
while not ret:
	ret, frame = cap.read()

#img = np.zeros((300,512,3), np.uint8)
#cv2.namedWindow('image')

# create trackbars for color change
#cv2.createTrackbar('H','image',0,255,nothing)
#cv2.createTrackbar('S','image',0,255,nothing)
#cv2.createTrackbar('V','image',0,255,nothing)

# create switch for ON/OFF functionality
#switch = '0 : OFF \n1 : ON'
#cv2.createTrackbar(switch, 'image',0,1,nothing)
radius = 25
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    '''
    # get current positions of four trackbars
    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')
    sw = cv2.getTrackbarPos(switch,'image')
    '''
    # Display the resulting frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([96-20, 100, 100], dtype=np.uint8)
    upper = np.array([96+20,255,255], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

    _,thresh = cv2.threshold(imgray,96,255,0)
    _,contours,_= cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    if len(contours) > 1:
            cnt = contours[0]
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                #x,y,w,h = cv2.boundingRect(cnt)
                w= 50
                h=50
                cv2.rectangle(imgray,(cx,cy),(cx+w,cy+h),(255,0,0),25)
    
    '''
    if sw == 0:
        img[:] = 0
    else:
        img[:] = [v,s,h]
    '''    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',imgray)
    cv2.imshow('res',res)
    #cv2.imshow('HSV',img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


