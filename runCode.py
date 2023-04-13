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

class GroundBot:
    panPin = 15
    tiltPin = 14

    class cam:
        def __init__(self):
            self.panAngle = 90
            self.tiltAngle = 90
            kit.servo[panPin].angle=self.panAngle
            kit.servo[tiltPin].angle=self.tiltAngle
        def camLeft(self):
            self.panAngle = 180
            kit.servo[panPin].angle=self.panAngle
        def camRight(self):
            self.panAngle = 0
            kit.servo[panPin].angle=self.panAngle
        def camForward(self):
            self.panAngle = 90
            kit.servo[panPin].angle=self.panAngle


    in1 = digitalio.DigitalInOut(board.D24)
    in2 = digitalio.DigitalInOut(board.D15)
    in3 = digitalio.DigitalInOut(board.D22)
    in4 = digitalio.DigitalInOut(board.D23)

    in1.direction = digitalio.Direction.OUTPUT
    in2.direction = digitalio.Direction.OUTPUT
    in3.direction = digitalio.Direction.OUTPUT
    in4.direction = digitalio.Direction.OUTPUT

    i2c = busio.I2C(board.SCL, board.SDA)

    pca = PCA9685(i2c)

    # Set the PWM frequency to 60hz.
    pca.frequency = 60

    kit = ServoKit(channels=16)
    kit.servo[panPin].set_pulse_width_range(500,2500)
    kit.servo[tiltPin].set_pulse_width_range(500,2500)

    cam1 = cam()

    # Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
    # but the PCA9685 will only actually give 12 bits of resolution.
    ena = 2
    enb = 3

    def stop():
        in1.value = False
        in2.value = False
        in3.value = False
        in4.value = False
        pca.channels[ena].duty_cycle = 0x0000
        pca.channels[enb].duty_cycle = 0x0000

    def turnRight():
        in1.value = True
        in2.value = False
        in3.value = False
        in4.value = True
        pca.channels[ena].duty_cycle = 0x7FFF
        pca.channels[enb].duty_cycle = 0x7FFF

    def turnLeft():
        in1.value = False
        in2.value = True
        in3.value = True
        in4.value = False
        pca.channels[ena].duty_cycle = 0x7FFF
        pca.channels[enb].duty_cycle = 0x7FFF

    def backward():
        in1.value = True
        in2.value = False
        in3.value = True
        in4.value = False
        pca.channels[ena].duty_cycle = 0x7FFF
        pca.channels[enb].duty_cycle = 0x7FFF

    def forward():
        in1.value = False
        in2.value = True
        in3.value = False
        in4.value = True
        pca.channels[ena].duty_cycle = 0x7FFF
        pca.channels[enb].duty_cycle = 0x7FFF

    def angleRight():
        in1.value = False
        in2.value = True
        in3.value = False
        in4.value = True
        pca.channels[ena].duty_cycle = 0x5FFF
        pca.channels[enb].duty_cycle = 0x7FFF

    def angleLeft():
        in1.value = False
        in2.value = True
        in3.value = False
        in4.value = True
        pca.channels[ena].duty_cycle = 0x7FFF
        pca.channels[enb].duty_cycle = 0x5FFF

    # Create PID controllers for pan and tilt servos
    pan_pid = PID(0.01, 0, 0, setpoint=0)
    tilt_pid = PID(0.01, 0, 0, setpoint=0)

    # Update the adjust_pan_tilt_servos function to use the PID controller
    def adjust_pan_tilt_servos(dx, dy):
        # Calculate the pan and tilt output using the PID controller
        pan_output = pan_pid(dx)
        tilt_output = tilt_pid(dy)

        cam1.panAngle += pan_output
        cam1.tiltAngle -= tilt_output
        # if cam1.panAngle < 0 or cam1.tiltAngle > 180:
        #     turnRight()
        # elif cam1.panAngle > 180
        #     turnLeft()
        cam1.panAngle = np.clip(cam1.panAngle, 0, 180)
        cam1.tiltAngle = np.clip(cam1.tiltAngle, 0, 180)

        kit.servo[panPin].angle = cam1.panAngle
        kit.servo[tiltPin].angle = cam1.tiltAngle

groundBot = GroundBot()

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