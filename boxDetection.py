import cv2
import numpy as np

# Define the lower and upper bounds for the lighter color in HSV space
lower_color = np.array([120, 20, 120])
upper_color = np.array([170, 30, 180])

# Minimum width of the detected box in pixels
min_width = 200

# Open the default camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the frame to extract the lighter object
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the binary mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through each contour
    for cnt in contours:
        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(cnt)

        # If the width of the bounding box is greater than the minimum width and the height is less than or equal to the width (assuming the box is wider than it is tall)
        if w >= min_width and h <= w:
            # Draw a rectangle around the bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
