import numpy as np
import cv2
import math
import os
capture = cv2.VideoCapture(0)
# 背景减除器，设置阴影检测
bs = cv2.createBackgroundSubtractorMOG2()
# 保留20帧历史
bs.setHistory(20)
while capture.isOpened():
    ret, frame = capture.read()
    gray = bs.apply(frame)

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    cv2.imshow("Cam", gray)
    cmd = cv2.waitKey(50)

capture.release()
cv2.destroyAllWindows()