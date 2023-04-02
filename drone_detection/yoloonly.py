import cv2
from ultralytics import YOLO
import time
import board
import digitalio
from adafruit_servokit import ServoKit
import numpy as np

kit=ServoKit(channels=16)

model = YOLO("best.onnx")

focal_length = 730  # C920 webcam focal length 3.9mm??
drone_real_width = 0.17  # Tello width

frame_width = 640
frame_height = 480
frame_center_x = 320
frame_center_y = 240

pan_angle = 90
tilt_angle = 90
kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle

# Initialize the previous positions to zero
prev_dx, prev_dy = 0, 0

def adjust_pan_tilt_servos(dx, dy):
    global pan_angle
    global tilt_angle
    global prev_dx
    global prev_dy
    changeSpeed = 2 + (abs(dx) + abs(dy)) // 50  # Increase speed when the object is far from the center
    # Smooth the servo's movement using a low-pass filter
    dx_smooth = 0.5 * dx + 0.5 * prev_dx
    dy_smooth = 0.5 * dy + 0.5 * prev_dy
    pan_angle -= changeSpeed * np.sign(dx_smooth)
    tilt_angle += changeSpeed * np.sign(dy_smooth)  # Reverse the sign of dy
    # Clamp the angles to avoid exceeding the servo limits
    pan_angle = np.clip(pan_angle, 0, 180)
    tilt_angle = np.clip(tilt_angle, 0, 180)

    # Set the new angles for the servos
    kit.servo[0].angle = pan_angle
    kit.servo[1].angle = tilt_angle
    
    # Update the previous positions
    prev_dx, prev_dy = dx_smooth, dy_smooth

while True:
    results = model(source="0", show=True, stream=True)
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
