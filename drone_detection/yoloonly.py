import cv2
from ultralytics import YOLO
import time
import board
import digitalio
from adafruit_servokit import ServoKit
import numpy as np
from adafruit_pca9685 import PCA9685
import busio
from simple_pid import PID

def followDrone():

    kit=ServoKit(channels=16)

    model = YOLO("best.onnx")

    focal_length = 730  # C920 webcam focal length 3.9mm??
    drone_real_width = 0.17  # Tello width

    frame_width = 640
    frame_height = 480
    frame_center_x = 320
    frame_center_y = 240

    panPin = 15
    tiltPin = 14

    kit = ServoKit(channels=16)
    kit.servo[panPin].set_pulse_width_range(500,2500)
    kit.servo[tiltPin].set_pulse_width_range(500,2500)

        # Create PID controllers for pan and tilt servos
    pan_pid = PID(0.01, 0, 0, setpoint=0)
    tilt_pid = PID(0.01, 0, 0, setpoint=0)

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

    cam1 = cam()

    while True:
        results = model.track(source="0", show=True, stream=True)
        for i, (result) in enumerate(results):
            boxes = result.boxes
            for box in boxes:
                x, y, w, h = box.xywh[0]  # get box coordinates in (top, left, bottom, right) format
                distance = (drone_real_width * focal_length) / w
                print(f"Distance: {distance:.2f}m")
                print(f"X: {x}")
                print(f"Y: {y}")

                x_center = (x + w) / 2            #Calculate the center pixel of the drone_x position
                y_center = (y + h) / 2            #Calculate the center pixel of the drone_y position
                dx = x_center - frame_center_x      #Calculate the difference between frame_center_x and drone_x position
                dy = y_center - frame_center_y      #Calculate the difference between frame_center_y and drone_y position

                adjust_pan_tilt_servos(dx, dy)
