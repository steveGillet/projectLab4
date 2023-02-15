import cv2
import numpy as np

img = cv2.imread('redBoxWithOtherShapes.png', cv2.IMREAD_UNCHANGED)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lowerRed = np.array([-20, 100, 100])
upperRed = np.array([13, 255, 255])

mask = cv2.inRange(hsv, lowerRed, upperRed)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

imgContours = np.zeros(img.shape)
cv2.drawContours(imgContours, contours, -1, (0,255,0), 3)
cv2.imshow('contours',imgContours) 

while True:
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break