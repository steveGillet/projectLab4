import cv2
import numpy as np

width=1280
height=720
flip=0
camSet='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap = cv2.VideoCapture(camSet)

while True:
    _, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the red color
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine the two masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Apply a Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(mask, (5, 5), 0)

    # Threshold the image to make it binary
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Look for red, square door frame shape
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            if aspect_ratio > 0.8 and aspect_ratio < 1.2:
                red_pixels = cv2.countNonZero(mask[y:y+h, x:x+w])
                if red_pixels > 0.2 * w * h:
                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)

    # Show the image
    cv2.imshow("Red, square door frame detection", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()