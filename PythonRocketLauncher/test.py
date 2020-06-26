# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from launcher_usb import *

mL = usb_launcher()
send_move(LEFT,7000)
ctr = 0
while(1):
        send_move(RIGHT, 100)
        if(ctr >360):
                time.sleep(.5)
        ctr = ctr+1
        print ctr
mL.release()

