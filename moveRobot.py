import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

in4 = 38
in3 = 36
in2 = 35
in1 = 31
# enb = 27
# ena = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
# GPIO.setup(ena, GPIO.OUT)
# GPIO.setup(enb, GPIO.OUT)


def turnLeft():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    # GPIO.output(ena, GPIO.HIGH)
    # GPIO.output(enb, GPIO.HIGH)

def stopMoving():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    # GPIO.output(ena, GPIO.LOW)
    # GPIO.output(enb, GPIO.LOW)
    # GPIO.output(ena, GPIO.LOW)

turnLeft()
time.sleep(1 )
stopMoving()
GPIO.cleanup()