import numpy as np
import cv2
import math
import os
def hammingDistance(phash1, phash2):
    hamming_distance = 0
    for x,y in zip(phash1,phash2):
        s = str(bin(x^y))
        for i in range(2,len(s)):
            if int(s[i]) is 1:
                hamming_distance += 1
    return hamming_distance 

wb = cv2.xphoto.createGrayworldWB()
wb.setSaturationThreshold(0.99)
faceCascade = cv2.CascadeClassifier('D:\\face.xml')
temp = cv2.imread('D:\\FaceLib\\zk.JPG')
temphash = cv2.img_hash.pHash(temp)[0]

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
        face = frame[y:y+h, x:x+w]
        facephash = cv2.img_hash.pHash(face)[0]
        print(facephash)
        print(hammingDistance(facephash,temphash))
    cv2.imshow("Cam", frame)
    cmd = cv2.waitKey(50)

capture.release()
cv2.destroyAllWindows()