import numpy as np
import cv2
import math
import os

wb = cv2.xphoto.createGrayworldWB()
wb.setSaturationThreshold(0.99)
faceCascade = cv2.CascadeClassifier('D:\\face.xml')

capture = cv2.VideoCapture(0)
while capture.isOpened():
    ret, frame = capture.read()
    frame = wb.balanceWhite(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (2,2))
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    area = 0
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow("Cam", frame)
    cmd = cv2.waitKey(50)

capture.release()
cv2.destroyAllWindows()