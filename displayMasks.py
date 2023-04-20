import cv2
import numpy as np

def equalizeHistograms(hsvImage):
    h, s, v = cv2.split(hsvImage)
    v = cv2.equalizeHist(v)
    return cv2.merge((h, s, v))

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv = equalizeHistograms(hsv)
    
    # Apply a Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(hsv, (5, 5), 0)

    # Define the lower and upper bounds of the colors
    lowerRed = np.array([0, 194, 0])
    upperRed = np.array([179, 255, 255])

    lowerOrange = np.array([0, 119, 89])
    upperOrange = np.array([24, 217, 160])

    lowerCardboard = np.array([12, 45, 114])
    upperCardboard = np.array([28, 82, 175])

    # Create the masks
    redMask = cv2.inRange(blur, lowerRed, upperRed)
    orangeMask = cv2.inRange(blur, lowerOrange, upperOrange)
    cardboardMask = cv2.inRange(blur, lowerCardboard, upperCardboard)

    # Combine the masks
    orangeMaskInv = cv2.bitwise_not(orangeMask)
    cardboardMaskInv = cv2.bitwise_not(cardboardMask)
    mask = cv2.bitwise_and(redMask, orangeMaskInv)
    mask = cv2.bitwise_and(mask, cardboardMaskInv)

    # Show the images
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Red Mask", redMask)
    cv2.imshow("Orange Mask", orangeMask)
    cv2.imshow("Cardboard Mask", cardboardMask)
    cv2.imshow("Combined Mask", mask)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
