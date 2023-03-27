import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

in1 = 37
in3 = 35
in2 = 38
in4 = 36
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
pwm1.start(40)
pwm2.start(40)

def turnLeft():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    # pwm1.ChangeDutyCycle(50)
    # pwm2.ChangeDutyCycle(50)

    
def turnRight():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    # pwm1.ChangeDutyCycle(50)
    # pwm2.ChangeDutyCycle(50)


def stopMoving():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    # pwm1.stop()
    # pwm2.stop()
    

import threading
import time

# Define a function that will be executed by the timer thread
def timer_function(event):
    # Wait for the event to be set
    event.wait()
    # Compute the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds.")

# Create an event object to signal when the event occurs
event = threading.Event()

# Record the start time
start_time = None

# Create a timer thread that will execute the timer_function
timer = threading.Thread(target=timer_function, args=(event,))

# Wait for the user to press Enter to start the timer
input("Press Enter to start the timer.")

# Record the start time
start_time = time.time()

# Start the timer thread
timer.start()
turnLeft()

# Wait for the user to press Enter to stop the timer
input("Press Enter to stop the timer.")

# Set the event to signal the timer thread
event.set()

# Wait for the timer thread to complete
timer.join()
stopMoving()
