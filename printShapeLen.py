import cv2
import numpy as np

frame = cv2.imread('box.jpg')

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
redMask = cv2.bitwise_or(mask1, mask2)

lowerOrange = np.array([10,100,100])
upperOrange = np.array([20, 255, 255])
orangeMask = cv2.inRange(hsv, lowerOrange, upperOrange)

mask = cv2.bitwise_and(redMask, cv2.bitwise_not(orangeMask))

# Apply a Gaussian blur to reduce noise
blur = cv2.GaussianBlur(mask, (5, 5), 0)

# Threshold the image to make it binary
_, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

# gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

# edges = cv2.Canny(mask, 100, 200)

# lines = cv2.HoughLines(edges, 1, 3.14/180, 50)

# # Find contours in the binary image
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Look for red, square door frame shape
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    if len(approx) >= 3:
        # print(len(approx))
        x,y,w,h = cv2.boundingRect(contour)
        aspect_ratio = float(w)/h
        if w>= 12*45:
            red_pixels = cv2.countNonZero(mask[y:y+h, x:x+w])
            if red_pixels > 0.2 * w * h:
                print(aspect_ratio)
                cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
                center = x + w / 2

# cv2.drawContours(frame, [lines], 0, (0, 255, 0), 3)
# cv2.drawContours(frame, contours, 0, (0, 255, 0), 3)

cv2.namedWindow("Red, square door frame detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Red, square door frame detection", 400, 400)

cv2.imshow("Red, square door frame detection", frame)
    # Exit the loop if 'q' is pressed
cv2.waitKey(0)
    
cv2.destroyAllWindows()