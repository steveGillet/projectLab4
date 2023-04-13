import cv2
import numpy as np
import time
import threading
import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from simple_pid import PID
from pyzbar.pyzbar import decode


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 1)

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    
    try:
        detect = decode(frame)
        qrCodeValue = None
        for obj in detect:
            qrCodeValue = obj.data.decode()
            print(obj.data.decode())
            cv2.rectangle(frame, (obj.rect.left, obj.rect.top), (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (0,255,0), 2)
        # detect = cv2.QRCodeDetector()
        # qrCodeValue, points, straight_qrcode = detect.detectAndDecode(frame)

        if qrCodeValue:
            print(qrCodeValue)
            stop()
            break
    except:
        pass

    cv2.imshow('QR CODE DETECTOR', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()