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
from drone_detection.robotmove import moveToPosition 
import adafruit_mpu6050
from gridCode.WORKINGCODE import droneGrid

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
    def __init__(self):
        self.panPin = 9
        self.tiltPin = 8
        self.in1 = digitalio.DigitalInOut(board.D24)
        self.in2 = digitalio.DigitalInOut(board.D15)
        self.in3 = digitalio.DigitalInOut(board.D22)
        self.in4 = digitalio.DigitalInOut(board.D23)

        self.in1.direction = digitalio.Direction.OUTPUT
        self.in2.direction = digitalio.Direction.OUTPUT
        self.in3.direction = digitalio.Direction.OUTPUT
        self.in4.direction = digitalio.Direction.OUTPUT
        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.pca = PCA9685(self.i2c)

        # Set the PWM frequency to 60hz.
        self.pca.frequency = 60
        self.kit = ServoKit(channels=16)
        self.kit.servo[self.panPin].set_pulse_width_range(500,2500)
        self.kit.servo[self.tiltPin].set_pulse_width_range(500,2500)

        self.cam1 = Cam(self.kit, self.panPin, self.tiltPin)

        # Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
        # but the PCA9685 will only actually give 12 bits of resolution.
        self.ena = 2
        self.enb = 3

        # Create PID controllers for pan and tilt servos
        self.pan_pid = PID(0.01, 0, 0, setpoint=0)
        self.tilt_pid = PID(0.01, 0, 0, setpoint=0)

        self.nextQRcode = None
        
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c)

        self.yaw = 0.000
        self.running = True

        self.yawThread = threading.Thread(target=self.updateYaw)
        self.yawThread.start()
        self.dt = 0.01

        self.yaw_drift_correction = 0.00011

        self.box_positions = {'A': (0, 0), 'B': (0, 0), 'C':(0,0), 'D': (0,0), 'E': (0,0), 'F':(0,0), 'DONE':(0,0)}

    def stop(self):
        self.in1.value = False
        self.in2.value = False
        self.in3.value = False
        self.in4.value = False
        self.pca.channels[self.ena].duty_cycle = 0x0000
        self.pca.channels[self.enb].duty_cycle = 0x0000

    def turnRight(self):
        self.in1.value = True
        self.in2.value = False
        self.in3.value = False
        self.in4.value = True
        self.pca.channels[self.ena].duty_cycle = 0x7FFF
        self.pca.channels[self.enb].duty_cycle = 0x7FFF

    def turnLeft(self):
        self.in1.value = False
        self.in2.value = True
        self.in3.value = True
        self.in4.value = False
        self.pca.channels[self.ena].duty_cycle = 0x7FFF
        self.pca.channels[self.enb].duty_cycle = 0x7FFF

    def backward(self):
        self.in1.value = True
        self.in2.value = False
        self.in3.value = True
        self.in4.value = False
        self.pca.channels[self.ena].duty_cycle = 0x7FFF
        self.pca.channels[self.enb].duty_cycle = 0x7FFF

    def forward(self):
        self.in1.value = False
        self.in2.value = True
        self.in3.value = False
        self.in4.value = True
        self.pca.channels[self.ena].duty_cycle = 0x7FFF
        self.pca.channels[self.enb].duty_cycle = 0x7FFF

    def angleRight(self):
        self.in1.value = False
        self.in2.value = True
        self.in3.value = False
        self.in4.value = True
        self.pca.channels[self.ena].duty_cycle = 0x5FFF
        self.pca.channels[self.enb].duty_cycle = 0x7FFF

    def angleLeft(self):
        self.in1.value = False
        self.in2.value = True
        self.in3.value = False
        self.in4.value = True
        self.pca.channels[self.ena].duty_cycle = 0x7FFF
        self.pca.channels[self.enb].duty_cycle = 0x5FFF


    # Update the adjust_pan_tilt_servos function to use the PID controller
    def adjust_pan_tilt_servos(self, dx, dy):
        try:
            # Calculate the pan and tilt output using the PID controller
            pan_output = self.pan_pid(dx)
            tilt_output = self.tilt_pid(dy)

            self.cam1.panAngle += pan_output
            self.cam1.tiltAngle -= tilt_output
            # if cam1.panAngle < 0 or cam1.tiltAngle > 180:
            #     turnRight()
            # elif cam1.panAngle > 180
            #     turnLeft()
            self.cam1.panAngle = np.clip(self.cam1.panAngle, 0, 180)
            self.cam1.tiltAngle = np.clip(self.cam1.tiltAngle, 0, 180)

            self.kit.servo[self.panPin].angle = self.cam1.panAngle
            self.kit.servo[self.tiltPin].angle = self.cam1.tiltAngle
        except Exception as e:
            print(f"Error: {e}")
    
    def updateYaw(self):
        # adjust this value based on how much the yaw drifts over time
        
        while self.running:
            gyro = self.mpu.gyro
            gyro_rad = [g * np.pi / 180 for g in gyro]  # Convert gyro data to radians
            
            self.yaw += (gyro_rad[2] + self.yaw_drift_correction) * self.dt  # Subtract the correction from the yaw
            time.sleep(self.dt)
    
    def waitForBoxPosition(self, boxKey):
        while self.box_positions[boxKey] == (0, 0):
            time.sleep(0.1)


class Cam:
    def __init__(self, kit, panPin, tiltPin):
        self.kit = kit
        self.panAngle = 90
        self.tiltAngle = 90
        self.panPin = panPin
        self.tiltPin = tiltPin
        self.kit.servo[self.panPin].angle=self.panAngle
        self.kit.servo[self.tiltPin].angle=self.tiltAngle
    def camLeft(self):
        self.panAngle = 180
        self.kit.servo[self.panPin].angle=self.panAngle
    def camRight(self):
        self.panAngle = 0
        self.kit.servo[self.panPin].angle=self.panAngle
    def camForward(self):
        self.panAngle = 90
        self.kit.servo[self.panPin].angle=self.panAngle

groundBot = GroundBot()

connect_to_tello_wifi('TELLO-995AD9')

print('drone searching')
droneGrid(groundBot)

# while True:
#     # Read the first box and get the nextQRcode value
#     print('groundbot searching')
#     readBox(groundBot)
#     print('groundbot backing out')
#     groundBot.backward()
#     time.sleep(3)
    
#     if groundBot.yaw < 0.000:
#         while groundBot.yaw < 0.000:
#             groundBot.turnLeft()
#             time.sleep(0.1)
#         groundBot.stop()

#     elif groundBot.yaw > 0.000:
#         while groundBot.yaw > 0.000:
#             groundBot.turnRight()
#             time.sleep(0.1)
#         groundBot.stop()

#     print('groundbot waiting')
#     # Wait for the corresponding box_positions variable to be updated
#     groundBot.waitForBoxPosition(groundBot.nextQRcode)

#     # Check if the nextQRcode value is 'done'
#     if groundBot.nextQRcode == 'DONE':
#         # Perform the action for the 'done' QR code
#         moveToPosition(groundBot, groundBot.box_positions[groundBot.nextQRcode])

#         # Break the loop
#         break

#     # Move to the position specified by the nextQRcode
#     print('groundbot moving to next box')
#     moveToPosition(groundBot, groundBot.box_positions[groundBot.nextQRcode])
