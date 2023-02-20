import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

in4 = 37
in3 = 35
in2 = 36
in1 = 38
enb = 33
ena = 32

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
pwm1 = GPIO.PWM(ena,60)
pwm2 = GPIO.PWM(enb,60)

def turnLeft():
    pwm2.start(100)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    pwm1.start(100)
    pwm1.ChangeDutyCycle(100)

def stopMoving():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    # GPIO.output(ena, GPIO.LOW)

turnLeft()
time.sleep(60)
stopMoving()
GPIO.cleanup()