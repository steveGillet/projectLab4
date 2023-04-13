# import cv2
# import numpy as np

# lowerRed = np.array([0, 170, 30])
# upperRed = np.array([10, 255, 90])
# # img = cv2.imread('redBoxWithOtherShapes.png', cv2.IMREAD_UNCHANGED)

# width=1280
# height=720
# flip=2
# camSet='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam=cv2.VideoCapture(camSet)
# while True:
#   _, frame = cam.read()
#   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#   mask = cv2.inRange(hsv, lowerRed, upperRed)
#   contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#   imgContours = np.zeros(frame.shape)
#   cv2.drawContours(imgContours, contours, -1, (0,255,0), 3)
#   cv2.imshow('contours',imgContours)
#   k = cv2.waitKey(1)
#   if k == 27:
#     break
# cam.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
from pyzbar.pyzbar import decode

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break



