import cv2
import numpy as np
import RPi.GPIO as GPIO
# import Jetson.GPIO as GPIO
import time

in1 = 19
in2 = 16
in3 = 20
in4 = 21
ena = 12
enb = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
pwm1 = GPIO.PWM(ena,60)
pwm2 = GPIO.PWM(enb,60)


def turnLeft():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    pwm1.start(40)
    pwm2.start(40)
    # pwm1.ChangeDutyCycle(50)
    # pwm2.ChangeDutyCycle(50)

    
def turnRight():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.start(40)
    pwm2.start(40)
    # pwm1.ChangeDutyCycle(50)
    # pwm2.ChangeDutyCycle(50)

def moveForward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.start(40)
    pwm2.start(40)
    # pwm1.ChangeDutyCycle(50)
    # pwm2.ChangeDutyCycle(50)

def moveBackward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    pwm1.start(40)
    pwm2.start(40)
    # pwm1.ChangeDutyCycle(50)
    # pwm2.ChangeDutyCycle(50)


def stopMoving():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    pwm1.stop()
    pwm2.stop()

turnLeft()
time.sleep(1)
turnRight()
time.sleep(1)
moveForward()
time.sleep(1)
moveBackward()
time.sleep(1)
stopMoving()
GPIO.cleanup()