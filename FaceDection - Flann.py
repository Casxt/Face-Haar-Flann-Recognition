import numpy as np
import cv2
import math
import os

def sift_detect(img):
    kp1, des1 = sift.detectAndCompute(img, None)

    FLANN_INDEX_KDTREE = 0  
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)  
    search_params = dict(checks=20)  
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    maxMatch = 0
    MatchNum = 0
    for imgName,tempalte,kp,des2 in Tempaltes:
        matches = flann.knnMatch(des1, des2, k=2)
        good = []
        for m,n in matches:
            if m.distance  < 0.75 * n.distance:
                good.append([m])

        if len(good) > maxMatch:
            maxMatch = len(good)
            MatchNum = len(matches)
            img2 = tempalte
            kp2 = kp
            name = imgName
            if maxMatch > 50:
                break

    print(name,"有效点数:",maxMatch,"总点数:",MatchNum)

    if fllowUser and maxMatch > 20:
        tempalte = cv2.resize(face,TempSize,interpolation=cv2.INTER_CUBIC)
        kp, des = sift.detectAndCompute(tempalte, None)
        Tempaltes[FileList.index(name)] = (name,tempalte,kp,des)
    res = cv2.drawMatchesKnn(img, kp1, img2, kp2, good, None, **draw_params)
    return name, maxMatch, res

draw_params = dict(matchColor=(0, 128, 255),  
                singlePointColor=(255, 0, 0),  
                #matchesMask=matchesMask,
                flags=2)
fllowUser = False
sift = cv2.xfeatures2d.SURF_create()
handCascade = cv2.CascadeClassifier('face.xml')
TempSize = (256,256)
FileDir = "FaceLib//"
FileLocate = FileDir + "%s.JPG"
FileList = []
f_list = os.listdir(FileDir)
for i in f_list:
    name, ext = os.path.splitext(i)
    if ext == '.JPG':
        FileList.append(name)

Tempaltes = []
for imgName in FileList:
    tempalte = cv2.imread(FileLocate%(imgName))
    tempalte = cv2.resize(tempalte,TempSize,interpolation=cv2.INTER_CUBIC)
    kp, des = sift.detectAndCompute(tempalte, None)
    Tempaltes.append((imgName,tempalte,kp,des))



wb = cv2.xphoto.createGrayworldWB()
wb.setSaturationThreshold(0.99)


capture = cv2.VideoCapture(1)
while capture.isOpened():

    ret, frame = capture.read()

    frame = wb.balanceWhite(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (2,2))
    
    faces = handCascade.detectMultiScale(gray, 1.3, 5)

    area = 0
    for (x,y,w,h) in faces:
        if w*h > area : 
            area = w*h
            face = frame[y:y+h, x:x+w]

    if area != 0:
        face = cv2.resize(face,TempSize,interpolation=cv2.INTER_CUBIC)
        name, maxMatch, res = sift_detect(face)
        img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        text = name + ":" + str(maxMatch)
        cv2.putText(frame, text, (x + 6, y+h - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        cv2.imshow("Cam", frame)
        text = name + ":" + str(maxMatch)
        cv2.putText(res, text, (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        cv2.imshow("Face", res)
        cmd = cv2.waitKey(50)
        if cmd == ord('s'): #ms
            Name = input("input Save Name(input 'c' to cacel):")
            if Name == 'c':
                continue
            cv2.imwrite(FileLocate%(Name),face)
            tempalte = cv2.resize(face,TempSize,interpolation=cv2.INTER_CUBIC)
            kp, des = sift.detectAndCompute(tempalte, None)
            if Name not in FileList:
                FileList.append(Name)
                Tempaltes.append((Name,tempalte,kp,des))
            else:
                Tempaltes[FileList.index(Name)] = (imgName,tempalte,kp,des)
        elif cmd == ord('r'):
            tempalte = cv2.resize(face,TempSize,interpolation=cv2.INTER_CUBIC)
            kp, des = sift.detectAndCompute(tempalte, None)
            Tempaltes[FileList.index(name)] = (name,tempalte,kp,des)
            cv2.imwrite(FileLocate%(name),face)
        elif cmd == ord('f'):
            fllowUser = not fllowUser
    else:
        cv2.imshow("Cam", frame)
        #cv2.imshow("Face", face)
        cv2.waitKey(50)

capture.release()
cv2.destroyAllWindows()