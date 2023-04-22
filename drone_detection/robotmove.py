from adafruit_pca9685 import PCA9685
import time
import board
import busio
import digitalio

import cv2
import numpy as np




# in1 = digitalio.DigitalInOut(board.D24)
# in2 = digitalio.DigitalInOut(board.D15)
# in3 = digitalio.DigitalInOut(board.D22)
# in4 = digitalio.DigitalInOut(board.D23)

# in1.direction = digitalio.Direction.OUTPUT
# in2.direction = digitalio.Direction.OUTPUT
# in3.direction = digitalio.Direction.OUTPUT
# in4.direction = digitalio.Direction.OUTPUT

# i2c = busio.I2C(board.SCL, board.SDA)

# pca = PCA9685(i2c)
# pca.frequency = 60

# ena = 2
# enb = 3

# def stop():
#     in1.value = False
#     in2.value = False
#     in3.value = False
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x0000
#     pca.channels[enb].duty_cycle = 0x0000

# def turn_right():
#     in1.value = True
#     in2.value = False
#     in3.value = False
#     in4.value = True
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def turn_left():
#     in1.value = False
#     in2.value = True
#     in3.value = True
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def move_backward():
#     in1.value = True
#     in2.value = False
#     in3.value = True
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def move_forward():
#     in1.value = False
#     in2.value = True
#     in3.value = False
#     in4.value = True
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

def moveToPosition(groundBot, coord):

    # Initialize camera
    cap = cv2.VideoCapture(0)

    def process_frame(frame):
        # Convert to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges using Canny edge detection
        edges = cv2.Canny(blurred, 50, 200)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def check_obstacle(area_threshold=7500, distance_threshold=1500):
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            return False

        # Process the frame and find contours
        contours = process_frame(frame)

        # Check if any of the contours are large enough and close enough to be considered obstacles
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > area_threshold:
                # Calculate the center of the contour
                moments = cv2.moments(contour)
                cX = int(moments["m10"] / moments["m00"])
                cY = int(moments["m01"] / moments["m00"])

                # Check if the contour is close enough to be an obstacle
                if cY < distance_threshold:
                    print('obstacle detected')
                    return True

        return False
    
    def avoidObstacle():
        timePerCM = 0.033
        # turn right
        currentYaw = groundBot.yaw
        while groundBot.yaw - currentYaw < 0.019:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()

        # move forward
        groundBot.forward()
        time.sleep(61 * timePerCM)

        # turn left
        currentYaw = groundBot.yaw
        while groundBot.yaw - currentYaw < 0.019:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()

        # move forward
        groundBot.forward()
        time.sleep(122 * timePerCM)

        # turn left
        currentYaw = groundBot.yaw
        while groundBot.yaw - currentYaw < 0.019:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()

        # move forward
        groundBot.forward()
        time.sleep(61 * timePerCM)

        # turn right
        currentYaw = groundBot.yaw
        while groundBot.yaw - currentYaw < 0.019:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()

    def move():
        groundBot.forward()

        while check_obstacle():
            groundBot.stop()
            avoidObstacle()

    x, y = coord

    timePerCM = 0.033

    if x > 0:
        while groundBot.yaw > -0.019:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()
    elif x < 0:
        while groundBot.yaw < 0.019:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()

    move()

    time.sleep(abs(x) * timePerCM)
    groundBot.stop()

    if x > 0 and y > 0:
        while groundBot.yaw < 0.000:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()
    elif x > 0 and y < 0:
        while groundBot.yaw > 0.000:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()
    elif x < 0 and y > 0:
        while groundBot.yaw < 0.000:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()
    elif x < 0 and y < 0:
        while groundBot.yaw > 0.000:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()

    move()
   
    time.sleep(abs(y) * timePerCM)
    groundBot.stop()


# if __name__ == "__main__":
#     try:
#         move_to_position([10, 40])
#     except KeyboardInterrupt:
#         stop()
#         pca.reset()
