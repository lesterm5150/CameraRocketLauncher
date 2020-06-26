import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
x_max = 0; y_max = 0
cap = cv2.VideoCapture(1)
cap.set( 3, 640 );
cap.set( 4, 480 );
while(1):
    (_, img) = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.4, 3,
                                          0,(25,25),( 500,500))
    x_max = 0; y_max = 0
    
    for (x,y,w,h) in faces:
        if x > x_max and y >y_max:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            x_max = x; y_max = y
     
    cv2.imshow('img',img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
