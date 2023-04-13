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
import subprocess

def connect_to_tello_wifi(ssid, password=None):
    try:
        # If a password is provided, use it to connect to the Wi-Fi
        if password:
            command = f'nmcli device wifi connect "{ssid}" password "{password}"'
        else:
            command = f'nmcli device wifi connect "{ssid}"'

        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"Connected to {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to {ssid}: {e.output}")

def run_supervision_and_fly():
    supervision2()
    tello.send_command('takeoff')
    flyDrone(tello)

connect_to_tello_wifi('TELLO-995AD9')


time.sleep(1)

tello = Tello()

tello.send_command('command')
tello.send_command('streamon')
tello.send_command('takeoff')
tello.send_command('speed 100')

readBox(tello)
print('look for drone now')
# Create two threads to run the functions simultaneously
t1 = threading.Thread(target=run_supervision_and_fly)
t1.start()
t1.join()