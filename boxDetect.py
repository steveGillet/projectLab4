import cv2
import numpy as np

lowerRed = np.array([-20, 100, 100])
upperRed = np.array([13, 255, 255])
# img = cv2.imread('redBoxWithOtherShapes.png', cv2.IMREAD_UNCHANGED)

width=1280
height=720
flip=2
camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)
while True:
  _, frame = cam.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, lowerRed, upperRed)
  contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  imgContours = np.zeros(frame.shape)
  cv2.drawContours(imgContours, contours, -1, (0,255,0), 3)
  cv2.imshow('contours',imgContours)
  k = cv2.waitKey(5000)
  if k == 27:
    break
cam.release()
cv2.destroyAllWindows()