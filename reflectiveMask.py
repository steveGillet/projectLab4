import cv2
import numpy as np

def nothing(x):
    pass

def detect_reflective_red_tape():
    cv2.namedWindow("Reflective red tape detection")
    cv2.createTrackbar("Brightness Threshold", "Reflective red tape detection", 230, 255, nothing)

    cap = cv2.VideoCapture(0)

    lowerRed = np.array([0, 50, 50])
    upperRed = np.array([10, 255, 255])

    while True:
        _, frame = cap.read()

        # Get the current brightness threshold from the trackbar
        brightness_threshold = cv2.getTrackbarPos("Brightness Threshold", "Reflective red tape detection")

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Split the channels
        h, s, v = cv2.split(hsv)

        # Apply a threshold on the value (V) channel to keep only the bright regions
        _, bright_mask = cv2.threshold(v, brightness_threshold, 255, cv2.THRESH_BINARY)

        # Apply a mask on the red color in the original frame
        redMask = cv2.inRange(hsv, lowerRed, upperRed)

        # Use bitwise AND operation to combine the bright regions and red color masks
        combined_mask = cv2.bitwise_and(bright_mask, redMask)

        # Find contours in the combined mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours on the frame
        for contour in contours:
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)

        # Show the image
        cv2.imshow("Reflective red tape detection", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_reflective_red_tape()
