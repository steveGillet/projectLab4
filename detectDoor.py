import cv2
import numpy as np
import time
import threading
import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from simple_pid import PID
from pyzbar.pyzbar import decode

def readBox(groundBot):

    movement_pid = PID(1, 0, 0, setpoint=0, output_limits=(-1, 1))

    # Define a function that will be executed by the timer thread
    def timer_function(duration):
        # print(duration)
        global flag
        time.sleep(abs(movement_pid(duration)))
        groundBot.stop()
        flag = False

    # Set the flag variable to False initially
    flag = False

    def equalizeHistograms(hsvImage):
        h, s, v = cv2.split(hsvImage)
        v = cv2.equalizeHist(v)
        return cv2.merge((h,s,v))

    cap = cv2.VideoCapture(0)

    frameCenterX = 320
    frameCenterY = 240

    # lowerRedLow = np.array([0, 50, 50])
    # upperRedLow = np.array([10, 255, 255])
    # lowerRedHigh = np.array([175, 50, 50])
    # upperRedHigh = np.array([180, 255, 255])
    # lowerOrange = np.array([2,50,80])
    # upperOrange = np.array([15, 210, 120])
    # lowerCardboard = np.array([165, 25, 80])
    # upperCardboard = np.array([180, 90, 165])

    lowerRed = np.array([14, 152, 50])
    upperRed = np.array([179, 255, 148])

    lowerOrange = np.array([174, 0, 87])
    upperOrange = np.array([179, 14, 134])

    lowerCardboard = np.array([4, 17, 135])
    upperCardboard = np.array([17, 35, 179])

    redFlag = 0
    minWidthCardboard = 100

    look_for_qr_code = False
    frameCounter = 0
    foundFlag = 0

    while not foundFlag:
        frameCounter += 1
        _, frame = cap.read()

        if look_for_qr_code:
            print('looking for qr code')
            # Set the tilt angle to look up
            groundBot.cam1.tiltAngle = 40
            groundBot.kit.servo[groundBot.tiltPin].angle = groundBot.cam1.tiltAngle

            # Search for the QR code
            try:
                gray_img = cv2.cvtColor(frame,0)
                barcode = decode(gray_img)

                for obj in barcode:
                    points = obj.polygon
                    (x,y,w,h) = obj.rect
                    pts = np.array(points, np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

                    qrCodeValue = obj.data.decode("utf-8")
                    barcodeType = obj.type
                    string = "Data " + str(qrCodeValue) + " | Type " + str(barcodeType)
                    
                    cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                    print("Barcode: "+qrCodeValue +" | Type: "+barcodeType)

                    if qrCodeValue:
                        print(qrCodeValue)
                        groundBot.nextQRcode = qrCodeValue
                        groundBot.stop()
                        foundFlag = 1
            except Exception as e:
                print(e)

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # hsv = equalizeHistograms(hsv)

        # Apply a Gaussian blur to reduce noise
        blur = cv2.GaussianBlur(hsv, (5, 5), 0)

        # Define the lower and upper bounds of the red color

        # mask1 = cv2.inRange(hsv, lowerRedLow, upperRedLow)

        # mask2 = cv2.inRange(hsv, lowerRedHigh, upperRedHigh)

        # Combine the two masks
        redMask = cv2.inRange(blur, lowerRed, upperRed)
        orangeMask = cv2.inRange(blur, lowerOrange, upperOrange)
        cardboardMask = cv2.inRange(blur, lowerCardboard, upperCardboard)

        orangeMaskInv = cv2.bitwise_not(orangeMask)
        cardboardMaskInv = cv2.bitwise_not(cardboardMask)

        mask = cv2.bitwise_and(redMask, orangeMaskInv)
        mask = cv2.bitwise_and(mask, cardboardMaskInv)

        # mask = cv2.inRange(hsv, lowerRed, upperRed)

        # Threshold the image to make it binary
        _, thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)

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
                    # print(w*h)
                    if w * h > 280000:
                        look_for_qr_code = True
                    red_pixels = cv2.countNonZero(mask[y:y+h, x:x+w])
                    if red_pixels > 0.2 * w * h:
                        redFlag += 1
                        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
                        centerX = x + w / 2
                        centerY = y + h / 2

                        dx = centerX - frameCenterX
                        dy = centerY - frameCenterY 
                        groundBot.adjust_pan_tilt_servos(dx, dy)
                        if groundBot.cam1.panAngle < 85 and not flag:
                            groundBot.turnRight()
                            # print('right')
                            # # Create a timer thread that will execute the timer_function after 5 seconds
                            timer = threading.Thread(target=timer_function, args=(.00135*dx,))
                            # # Start the timer thread
                            timer.start()
                            flag = True
                            
                        elif groundBot.cam1.panAngle > 95 and not flag:
                            groundBot.turnLeft()
                            # print('left')
                            # # Create a timer thread that will execute the timer_function after 5 seconds
                            timer = threading.Thread(target=timer_function, args=(.00135*dx,))

                            # # Start the timer thread
                            timer.start()
                            flag = True
                        else:
                            groundBot.forward()
                            # print('forward')
                            # # Create a timer thread that will execute the timer_function after 5 seconds
                            timer = threading.Thread(target=timer_function, args=(1,))

                            # # Start the timer thread
                            timer.start()
                            flag = True
        # if frameCounter > 5:
        #     if redFlag <= 3:

        #         # Convert the frame to the HSV color space
        #         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #         hsv = equalizeHistograms(hsv)
        #         # Apply a Gaussian blur to reduce noise
        #         blur = cv2.GaussianBlur(hsv, (5, 5), 0)
        #         # Threshold the frame to extract the lighter object
        #         mask = cv2.inRange(blur, lowerCardboard, upperCardboard)

        #         # Find contours in the binary mask
        #         contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #         # Loop through each contour
        #         for cnt in contours:
        #             # Calculate the bounding box of the contour
        #             x, y, w, h = cv2.boundingRect(cnt)

        #             # If the width of the bounding box is greater than the minimum width and the height is less than or equal to the width (assuming the box is wider than it is tall)
        #             if w >= minWidthCardboard and h <= w:
        #                 # Draw a rectangle around the bounding box
        #                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
        #                 centerX = x + w / 2
        #                 centerY = y + h / 2
        #                 dx = centerX - frameCenterX
        #                 dy = centerY - frameCenterY 
        #                 groundBot.adjust_pan_tilt_servos(dx, dy)
        #                 if groundBot.cam1.panAngle < 170:
        #                     print('cardboard turn')
        #                     groundBot.turnRight()
        #                 else:
        #                     print('cardboard angle')
        #                     groundBot.angleLeft()
            

        # Show the image
        cv2.imshow("Red, square door frame detection", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            groundBot.stop()
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    readBox()