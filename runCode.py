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
from ultralytics import YOLO
from TelloPython.Single_Tello_Test.tello import Tello
from TelloPython.Single_Tello_Test.tello_test import flyDrone
import sys
from datetime import datetime
from detectDoor import readBox
from drone_detection.supervision2 import supervision2

tello = Tello()

tello.send_command('command')
tello.send_command('streamon')
tello.send_command('takeoff')
tello.send_command('speed 100')

readBox(tello)
print('look for drone now')
# supervision2()
flyDrone()