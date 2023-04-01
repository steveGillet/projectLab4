# import tensorflow as tf
from tensorflow import keras
import cv2
<<<<<<< HEAD
import numpy as np
import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685
=======
# from picamera2 import Picamera2
import time
import numpy as np
# import RPi.GPIO as GPIO
# import Jetson.GPIO as GPIO
>>>>>>> 7327af7f636f80546a2f3b439d8dd001d4b91a82
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
class cam:
    def __init__(self):
        self.camForwardFlag = 0
        self.camLeftFlag = 0
        self.camRightFlag = 0
    def camForward(self):
        kit.servo[0].angle=90
        self.camForwardFlag = 1
        self.camLeftFlag = 0
        self.camRightFlag = 0
    def camLeft(self):
        kit.servo[0].angle=0   
        self.camForwardFlag = 0
        self.camLeftFlag = 1
        self.camRightFlag = 0
    def camRight(self):
        kit.servo[0].angle=180
        self.camForwardFlag = 0
        self.camLeftFlag = 0
        self.camRightFlag = 1
cam1 = cam()
kit.servo[1].angle=90

<<<<<<< HEAD
in1 = digitalio.DigitalInOut(board.D15)
in2 = digitalio.DigitalInOut(board.D24)
in3 = digitalio.DigitalInOut(board.D22)
in4 = digitalio.DigitalInOut(board.D23)
=======
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(in3, GPIO.OUT)
# GPIO.setup(in4, GPIO.OUT)
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)
# GPIO.setup(ena, GPIO.OUT)
# GPIO.setup(enb, GPIO.OUT)
# pwm1 = GPIO.PWM(ena,60)
# pwm2 = GPIO.PWM(enb,60)
>>>>>>> 7327af7f636f80546a2f3b439d8dd001d4b91a82

in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT
in3.direction = digitalio.Direction.OUTPUT
in4.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)

# Set the PWM frequency to 60hz.
pca.frequency = 60

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

<<<<<<< HEAD
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
=======
# def turnLeft():
#     GPIO.output(in1, GPIO.HIGH)
#     GPIO.output(in2, GPIO.LOW)
#     GPIO.output(in3, GPIO.LOW)
#     GPIO.output(in4, GPIO.HIGH)
#     pwm1.start(40)
#     pwm2.start(40)
#     # pwm1.ChangeDutyCycle(50)
#     # pwm2.ChangeDutyCycle(50)

    
# def turnRight():
#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in2, GPIO.HIGH)
#     GPIO.output(in3, GPIO.HIGH)
#     GPIO.output(in4, GPIO.LOW)
#     pwm1.start(40)
#     pwm2.start(40)
#     # pwm1.ChangeDutyCycle(50)
#     # pwm2.ChangeDutyCycle(50)

# def moveForward():
#     GPIO.output(in1, GPIO.HIGH)
#     GPIO.output(in2, GPIO.LOW)
#     GPIO.output(in3, GPIO.HIGH)
#     GPIO.output(in4, GPIO.LOW)
#     pwm1.start(40)
#     pwm2.start(40)
#     # pwm1.ChangeDutyCycle(50)
#     # pwm2.ChangeDutyCycle(50)

# def moveBackward():
#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in2, GPIO.HIGH)
#     GPIO.output(in3, GPIO.LOW)
#     GPIO.output(in4, GPIO.HIGH)
#     pwm1.start(40)
#     pwm2.start(40)
#     # pwm1.ChangeDutyCycle(50)
#     # pwm2.ChangeDutyCycle(50)

# def stopMoving():
#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in3, GPIO.LOW)
#     GPIO.output(in2, GPIO.LOW)
#     GPIO.output(in4, GPIO.LOW)
#     pwm1.stop()
#     pwm2.stop()
>>>>>>> 7327af7f636f80546a2f3b439d8dd001d4b91a82

model = keras.models.load_model('cnn_model.h5')

# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (3296, 2480)}))
# picam2.start()

<<<<<<< HEAD
# cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)

=======
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)
>>>>>>> 7327af7f636f80546a2f3b439d8dd001d4b91a82
# Loop over frames from the camera
while True:
    # Preprocess the image for the CNN model
    # frame = cv2.imread('right40.jpg')
<<<<<<< HEAD
    ret, frame = cap.read()
    # frame = picam2.capture_array()
=======
    # frame = picam2.capture_array()
    ret, frame = cap.read()
>>>>>>> 7327af7f636f80546a2f3b439d8dd001d4b91a82
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(frame.shape)
    print(frame.dtype)
    frame2 = cv2.resize(frame1, (64, 64))
    frame2 = frame2/ 255.0
    frame2 = np.reshape(frame2, (1, 64, 64, 3))

    # Run the CNN model on the preprocessed image
    predictions = model.predict(frame2)
    label = ['forward', 'left', 'right'][predictions.argmax()]
    print(label)

    # Display the image and predicted label in a window
    cv2.imshow("frame", frame1)
    cv2.waitKey(1)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

    if label == 'forward':
<<<<<<< HEAD
        if cam1.camLeftFlag:
            turnRight()
            cam1.camForward()
            time.sleep(2)
        elif cam1.camRightFlag:
            turnLeft()
            cam1.camForward()
            time.sleep(2)
        forward()
        time.sleep(1)
        stop()
    elif label == 'left':
        if not cam1.camRightFlag:
            cam1.camRight()
            turnLeft()
            time.sleep(2)
        forward()
        time.sleep(1)
        stop()    
    elif label == 'right':
        if not cam1.camLeftFlag:
            cam1.camLeft()
            turnRight()
            time.sleep(2)
        forward()
        time.sleep(1)
        stop()             
=======
        # moveForward()
        time.sleep(1)
        # stopMoving()
        print('forward')
    elif label == 'left':
        # turnLeft()
        # time.sleep(2)
        # moveForward()
        time.sleep(1)
        # turnRight()
        # time.sleep(2)
        # stopMoving()    
        print('left')
    elif label == 'right':
        # turnRight()
        # time.sleep(2)
        # moveForward()
        time.sleep(1)
        # turnLeft()
        # time.sleep(2)
        # stopMoving()  
        print('right')           
>>>>>>> 7327af7f636f80546a2f3b439d8dd001d4b91a82

# Clean up the camera and OpenCV resources
cv2.destroyAllWindows()
