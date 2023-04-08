# import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
panPin = 15
tiltPin = 14

class cam:
    def __init__(self):
        self.panAngle = 90
        self.tiltAngle = 90
        self.panAngle = 90
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

model = keras.models.load_model('cnn_model.h5')

# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (3296, 2480)}))
# picam2.start()

# cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)
turnLeftFlag = 0
turnRightFlag = 0
min_width = 100
x = 320
w = 0

# Loop over frames from the camera
while True:
    # Preprocess the image for the CNN model
    # frame = cv2.imread('right40.jpg')
    ret, frame = cap.read()
    # frame = picam2.capture_array()
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.resize(frame1, (64, 64))
    frame2 = frame2/ 255.0
    frame2 = np.reshape(frame2, (1, 64, 64, 1))

    # Define lower and upper bounds for the brown color in HSV space
    lower_color = np.array([120, 20, 120])
    upper_color = np.array([170, 30, 180])

    # Convert image to HSV and threshold it to extract the brown object
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the binary mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the contour with the largest area (assuming it is the brown object)
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate the bounding box of the contour
        tempX, tempW = x, w
        x, y, w, h = cv2.boundingRect(largest_contour)
        if w >= min_width or h>= min_width:
            # Draw a rectangle around the bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else: 
            x, w = tempX, tempW
    else:
        x, w = x, w
    # Calculate the x-coordinate of the center point of the bounding box
    centerX = x + w / 2
    frameCenterX = 320
    dx = centerX - frameCenterX 

    adjust_pan_tilt_servos(dx, 0)

    # Run the CNN model on the preprocessed image
    predictions = model.predict(frame2)
    label = ['forward', 'left', 'right'][predictions.argmax()]
    print(label)

    # Display the image and predicted label in a window
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        stop()
        break
    if turnLeftFlag:
        if centerX >= 310:
            turnLeftFlag = 0
    elif turnRightFlag:
        if centerX <= 330:
            turnRightFlag = 0
    else:
        if label == 'forward':
            if cam1.panAngle > 100:
                cam1.camForward()
                turnLeftFlag = 1
                turnLeft()
            elif cam1.panAngle < 80:
                cam1.camForward()
                turnRightFlag = 1
                turnRight()
            else:
                forward()
        elif label == 'left':
            if cam1.panAngle > 95:
                cam1.camRight()
                turnLeftFlag = 1
                turnLeft()
            else:
                angleRight()
        elif label == 'right':
            if cam1.panAngle < 85:
                cam1.camLeft()
                turnRightFlag = 1
                turnRight()
            else:
                angleLeft()   
    time.sleep(.1)                   

# Clean up the camera and OpenCV resources
cv2.destroyAllWindows()
