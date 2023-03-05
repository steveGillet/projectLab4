import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import threading

# Define a function that will be executed by the timer thread
def timer_function(duration):
    global flag
    print("Timer thread is running!")
    time.sleep(duration)
    stopMoving()
    flag = False

# Set the flag variable to False initially
flag = False

print("Timer thread has completed.")

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
    

width=1280
height=720
flip=0 
camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap = cv2.VideoCapture(camSet)

while True:
    _, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerRed = np.array([155, 75, 80])
    upperRed = np.array([180, 230, 130])

    # # Define the lower and upper bounds of the red color
    # lower_red = np.array([0, 50, 50])
    # upper_red = np.array([10, 255, 255])
    # mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # lower_red = np.array([170, 50, 50])
    # upper_red = np.array([180, 255, 255])
    # mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # # Combine the two masks
    # redMask = cv2.bitwise_or(mask1, mask2)

    # lowerOrange = np.array([10,100,100])
    # upperOrange = np.array([20, 255, 255])
    # orangeMask = cv2.inRange(hsv, lowerOrange, upperOrange)

    # mask = cv2.bitwise_and(redMask, cv2.bitwise_not(orangeMask))

    mask = cv2.inRange(hsv, lowerRed, upperRed)

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
                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
                    center = x + w / 2
                    if center < 620 and not flag:
                        turnLeft()
                        offCenter = 635 - center
                        # # Create a timer thread that will execute the timer_function after 5 seconds
                        timer = threading.Thread(target=timer_function, args=(.00135*offCenter,))
                        # # Start the timer thread
                        timer.start()
                        flag = True
                        
                    elif center > 650 and not flag:
                        turnRight()
                        offCenter = center - 635
                        # # Create a timer thread that will execute the timer_function after 5 seconds
                        timer = threading.Thread(target=timer_function, args=(.00135*offCenter,))

                        # # Start the timer thread
                        timer.start()
                        flag = True
                

    # Show the image
    cv2.imshow("Red, square door frame detection", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()