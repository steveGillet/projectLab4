from djitellopy import Tello
import cv2
from pyzbar import pyzbar

tello = Tello()

# Connect to the drone
tello.connect()

# Start the video stream
tello.streamon()

while True:
    # Get the current frame from the video stream
    frame = tello.get_frame_read().frame

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the QR code in the image
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(gray)

    # Display the frame in a window
    cv2.imshow("Tello Video Stream", frame)

    # If a QR code is detected, print the decoded information
    if data:
        print("Detected QR code:", data)

    # Wait for a key press and exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
tello.streamoff()
tello.end()
