import cv2
from ultralytics import YOLO
import time
import board
import digitalio
from adafruit_servokit import ServoKit
import numpy as np
import busio
from adafruit_pca9685 import PCA9685
import keyboard

kit=ServoKit(channels=16)

model = YOLO("best.onnx")

focal_length = 730  # C920 webcam focal length 3.9mm??
drone_real_width = 0.17  # Tello width

# frame_width = 640
# frame_height = 480
frame_center_x = 320  # frame center x of the live feed
frame_center_y = 240  # frame center y of the live feed

pan_angle = 90
tilt_angle = 90
kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle

in1 = digitalio.DigitalInOut(board.D15)
in2 = digitalio.DigitalInOut(board.D24)
in3 = digitalio.DigitalInOut(board.D22)
in4 = digitalio.DigitalInOut(board.D23)

in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT
in3.direction = digitalio.Direction.OUTPUT
in4.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 60
ena = 2
enb = 3

# Setting up DC motors for ground robot
def set_motor_speeds(speed_a, speed_b):
    if speed_a > 0:
        in1.value = True
        in2.value = False
        pca.channels[ena].duty_cycle = 0x7fff
        
    else:
        in1.value = False
        in2.value = True

    if speed_b > 0:
        in3.value = True
        in4.value = False
        pca.channels[ena].duty_cycle = 0x7fff
        
    else:
        in3.value = False
        in4.value = True

# Stop ground robot motors
def stop_motors():
    in1.value = False
    in2.value = False
    in3.value = False
    in4.value = False
    pca.channels[ena].duty_cycle = 0
    pca.channels[enb].duty_cycle = 0
    

# PID class for ground robot distance control
class PIDG:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
        self.prev_time = time.time()

    def update(self, error):
        dt = time.time() - self.prev_time
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error
        self.prev_time = time.time()

        return output
    
distance_pid = PIDG(0.1, 0.01, 0.01) # PID parameters for ground robot distance control, need to adjust the PID parameters
desired_distance = 0.5  # meters beteen drone and ground robot
    

def adjust_pan_tilt_servos(dx, dy):
    global pan_angle
    global tilt_angle

    pan_output = pid_pan.update(dx)
    tilt_output = pid_tilt.update(dy)

    pan_angle -= pan_output
    tilt_angle += tilt_output

    pan_angle = np.clip(pan_angle, 0, 180)
    tilt_angle = np.clip(tilt_angle, 0, 180)

    kit.servo[0].angle = pan_angle
    kit.servo[1].angle = tilt_angle

# PID class for servo control
class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
        self.prev_time = time.time()

    def update(self, error):
        dt = time.time() - self.prev_time
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error
        self.prev_time = time.time()

        return output
    
pid_pan = PID(0.1, 0.01, 0.01)  # PID parameters for pan servo, need to adjust the PID parameters
pid_tilt = PID(0.1, 0.01, 0.01) # PID parameters for tilt servo, need to adjust the PID parameters


while True:
    if keyboard.is_pressed('q'):  # Check if the 'q' key is pressed
        print("Exiting the program.")
        stop_motors()  # Stop the motors before exiting the loop
        break  # Exit the loop, which will end the program

    
    while True:
        results = model.track(source = "0", device = "0",show=True, stream=True, tracker = "bytetrack.yaml") # Added YOLO Tracker
        for i, (result) in enumerate(results):
            boxes = result.boxes
            for box in boxes:
                x, y, w, h = box.xywh[0]  # get box coordinates in (top, left, bottom, right) format

                # Calculate the distance between the drone and the ground robot
                distance = (drone_real_width * focal_length) / w
                print(f"Distance: {distance:.2f}m")
                print(f"X: {x}")
                print(f"Y: {y}")

                x_center = (x + w) / 2            #Calculate the center pixel of the drone_x position
                y_center = (y + h) / 2            #Calculate the center pixel of the drone_y position
                dx = x_center - frame_center_x      #Calculate the difference between frame_center_x and drone_x position
                dy = y_center - frame_center_y      #Calculate the difference between frame_center_y and drone_y position

                adjust_pan_tilt_servos(dx, dy)

                #calculate speed based on distance error
                distance_error = desired_distance - distance
                speed = distance_pid.update(distance_error)

                #set motor speeds to maintain desired distance
                set_motor_speeds(speed, speed)

                # delay to allow the servo to move
                time.sleep(0.1)

# cleanup gpio
GPIO.cleanup()

