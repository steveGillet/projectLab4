import cv2
import numpy as np
# import RPi.GPIO as GPIO
import Jetson.GPIO as GPIO
import time

in4 = 22
in3 = 13
in2 = 18
in1 = 16
enb = 32
ena = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
pwm1 = GPIO.PWM(ena, 60)
pwm2 = GPIO.PWM(enb, 60)


def turnLeft():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)
    pwm1.start(100)
    pwm2.start(100)

    
def turnRight():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)
    pwm1.start(50)
    pwm2.start(50)
    

def stopMoving():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    # GPIO.output(ena, GPIO.LOW)
    GPIO.output(enb, GPIO.LOW)
    GPIO.output(ena, GPIO.LOW)

turnLeft()
time.sleep(5)
turnRight()
time.sleep(5)
stopMoving()
GPIO.cleanup()