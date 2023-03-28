import tensorflow as tf
from tensorflow import keras
import cv2
# from picamera2 import Picamera2
import time
import numpy as np
# import RPi.GPIO as GPIO
# import Jetson.GPIO as GPIO
import time

in1 = 19
in2 = 16
in3 = 20
in4 = 21
ena = 12
enb = 13

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(in3, GPIO.OUT)
# GPIO.setup(in4, GPIO.OUT)
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)
# GPIO.setup(ena, GPIO.OUT)
# GPIO.setup(enb, GPIO.OUT)
# pwm1 = GPIO.PWM(ena,60)
# pwm2 = GPIO.PWM(enb,60)


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

model = keras.models.load_model('cnn_model.h5')

# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (3296, 2480)}))
# picam2.start()

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)
# Loop over frames from the camera
while True:
    # Preprocess the image for the CNN model
    # frame = cv2.imread('right40.jpg')
    # frame = picam2.capture_array()
    ret, frame = cap.read()
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

# Clean up the camera and OpenCV resources
cv2.destroyAllWindows()
