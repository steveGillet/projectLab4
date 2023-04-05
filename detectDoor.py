import cv2
import numpy as np
import time
import threading
import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

# Define a function that will be executed by the timer thread
def timer_function(duration):
    print(duration)
    global flag
    time.sleep(abs(duration))
    stop()
    flag = False

# Set the flag variable to False initially
flag = False

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
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

def adjust_pan_tilt_servos(dx, dy):

    pan_output = 2*np.sign(dx)
    tilt_output = 2*np.sign(dy)

    cam1.panAngle -= pan_output
    cam1.tiltAngle += tilt_output

    cam1.panAngle = np.clip(cam1.panAngle, 0, 180)
    cam1.tiltAngle = np.clip(cam1.tiltAngle, 0, 180)

    kit.servo[panPin].angle = cam1.panAngle
    kit.servo[tiltPin].angle = cam1.tiltAngle

cap = cv2.VideoCapture(0)

frameCenterX = 320
frameCenterY = 240

lowerRedLow = np.array([0, 50, 50])
upperRedLow = np.array([10, 255, 255])
lowerRedHigh = np.array([175, 50, 50])
upperRedHigh = np.array([180, 255, 255])
lowerOrange = np.array([2,50,80])
upperOrange = np.array([15, 210, 120])
lowerCardboard = np.array([165, 25, 80])
upperCardboard = np.array([180, 90, 165])

redFlag = 0
minWidthCardboard = 100

while True:
    _, frame = cap.read()

    try:
        detect = cv2.QRCodeDetector()
        qrCodeValue, points, straight_qrcode = detect.detectAndDecode(frame)
        
        if qrCodeValue:
            print(qrCodeValue)
            stop()
            break
    except:
        pass

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the red color

    mask1 = cv2.inRange(hsv, lowerRedLow, upperRedLow)

    mask2 = cv2.inRange(hsv, lowerRedHigh, upperRedHigh)

    # Combine the two masks
    redMask = cv2.bitwise_or(mask1, mask2)

    orangeMask = cv2.inRange(hsv, lowerOrange, upperOrange)

    mask = cv2.bitwise_and(redMask, cv2.bitwise_not(orangeMask))

    # mask = cv2.inRange(hsv, lowerRed, upperRed)

    # Apply a Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(mask, (5, 5), 0)

    # Threshold the image to make it binary
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Look for red, square door frame shape
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        if len(approx) >= 3:
            x,y,w,h = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            # print(w)
            if w>= 12*25:
                red_pixels = cv2.countNonZero(mask[y:y+h, x:x+w])
                if red_pixels > 0.2 * w * h:
                    redFlag += 1
                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
                    centerX = x + w / 2
                    centerY = y + h / 2

                    dx = centerX - frameCenterX
                    dy = centerY - frameCenterY 
                    adjust_pan_tilt_servos(dx, dy)
                    if cam1.panAngle < 85 and not flag:
                        turnRight()
                        print('right')
                        # # Create a timer thread that will execute the timer_function after 5 seconds
                        timer = threading.Thread(target=timer_function, args=(.00135*dx,))
                        # # Start the timer thread
                        timer.start()
                        flag = True
                        
                    elif cam1.panAngle > 95 and not flag:
                        turnLeft()
                        print('left')
                        # # Create a timer thread that will execute the timer_function after 5 seconds
                        timer = threading.Thread(target=timer_function, args=(.00135*dx,))

                        # # Start the timer thread
                        timer.start()
                        flag = True
                    else:
                        forward()
                        print('forward')
                        # # Create a timer thread that will execute the timer_function after 5 seconds
                        timer = threading.Thread(target=timer_function, args=(1,))

                        # # Start the timer thread
                        timer.start()
                        flag = True
    if redFlag <= 3:

        # Convert the frame to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the frame to extract the lighter object
        mask = cv2.inRange(hsv, lowerCardboard, upperCardboard)

        # Find contours in the binary mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through each contour
        for cnt in contours:
            # Calculate the bounding box of the contour
            x, y, w, h = cv2.boundingRect(cnt)

            # If the width of the bounding box is greater than the minimum width and the height is less than or equal to the width (assuming the box is wider than it is tall)
            if w >= minWidthCardboard and h <= w:
                # Draw a rectangle around the bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                centerX = x + w / 2
                centerY = y + h / 2
                dx = centerX - frameCenterX
                dy = centerY - frameCenterY 
                adjust_pan_tilt_servos(dx, dy)
        if cam1.panAngle < 170:
            print('cardboard turn')
            turnRight()
        else:
            print('cardboard angle')
            angleLeft()
        

    # Show the image
    cv2.imshow("Red, square door frame detection", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        stop()
        break


cap.release()
cv2.destroyAllWindows()