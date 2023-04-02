from ultralytics import YOLO
import cv2
import numpy as np

# # load model
model = YOLO("D:\downloads\\best.pt")

# #Train the model

# model.train(data="D:\downloads\\newTello", epochs=100, imgsz=640, device="0")


focal_length = 730  # C920 webcam focal length 3.9mm??
drone_real_width = 0.17  # Tello width

frame_width = 640
frame_height = 480
frame_center_x = 320
frame_center_y = 240

# while True:
#     results = model.track(source="0", show=True, stream=True, tracker="bytetrack.yaml")
#     for i, (result) in enumerate(results):
#         boxes = result.boxes
#         for box in boxes:
#             x, y, w, h = box.xywh[0]  # get box coordinates in (top, left, bottom, right) format
#             distance = (drone_real_width * focal_length) / w
#             print(f"Distance: {distance:.2f}m")
#             print(f"X: {x}")
#             print(f"Y: {y}")

#             x_center = (x + w) / 2            #Calculate the center pixel of the drone_x position
#             y_center = (y + h) / 2            #Calculate the center pixel of the drone_y position
#             dx = x_center - frame_center_x      #Calculate the difference between frame_center_x and drone_x position
#             dy = y_center - frame_center_y      #Calculate the difference between frame_center_y and drone_y position

cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Run the YOLO model on the frame
    results = model.track(frame)

    # Iterate through the detected objects
    for result in results.xywh[0]:
        x, y, w, h, _, _ = result  # Get box coordinates and confidence

        # Calculate distance, dx, and dy
        distance = (drone_real_width * focal_length) / w
        x_center = (x + w) / 2
        y_center = (y + h) / 2
        dx = x_center - frame_center_x
        dy = y_center - frame_center_y

        # Draw bounding box and labels
        label = f"Distance: {distance:.2f}m, dx: {dx:.2f}, dy: {dy:.2f}"
        x, y, w, h = (x * frame_width, y * frame_height, w * frame_width, h * frame_height)
        cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(x), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the frame with overlaid information
    cv2.imshow("Drone Tracking", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
