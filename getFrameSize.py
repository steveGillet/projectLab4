import cv2

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error opening the camera.")
else:
    # Get the resolution of the camera
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Camera resolution: {frame_width}x{frame_height}")

    # Release the camera
    cap.release()
