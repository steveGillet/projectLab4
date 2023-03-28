# import cv2
# from ultralytics import YOLO
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor

# model = YOLO("D:\downloads\\best.pt")

# results = model.track(source="0", device="0",show=True, tracker="bytetrack.yaml") #stream=True) 

#model.predict(source="0",show=True,conf=0.5)

# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model.track(frame, show=True, tracker="bytetrack.yaml")

#     #draw a vertical line at the center of the frame
#     height, width, _ = frame.shape
#     center_x = int(width/2)
#     cv2.line(frame, (center_x, 0), (center_x, height),(0,255,0), 2)

#     cv2.imshow('Live Feed', frame)


#     # Break the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cap.release()
# cv2.destroyAllWindows()

# import cv2
# from ultralytics import YOLO
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor

# model = YOLO("D:\downloads\\tello.pt")
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Run YOLOv8 detection without showing the output window
#     results = model.track(frame, show=False, tracker="bytetrack.yaml")

#     # Draw bounding boxes and labels
#     for *xyxy, conf, cls in results.xyxy[0]:
#         label = f'{model.names[int(cls)]} {conf:.2f}'
#         plot_one_box(xyxy, frame, label=label, color=(0, 0, 255), line_thickness=2)

#     # Draw a vertical line at the center of the frame
#     height, width, _ = frame.shape
#     center_x = int(width / 2)
#     cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 2)

#     # Display the frame with the center line overlay and bounding boxes
#     cv2.imshow('Live Feed', frame)

#     # Break the loop when 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# import random
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor
# import cv2
# import numpy as np
# from ultralytics import YOLO

# def plot_one_box(x, img, color=None, label=None, line_thickness=None):
#     # Plots one bounding box on image img
#     tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
#     color = color or [random.randint(0, 255) for _ in range(3)]
#     c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
#     cv2.rectangle(img, c1, c2, color, thickness=tl)
#     if label:
#         tf = max(tl - 1, 1)  # font thickness
#         t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
#         c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
#         cv2.rectangle(img, c1, c2, color, -1)  # filled
#         cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

# model = YOLO("D:\downloads\\best.pt")
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Run YOLOv8 detection without showing the output window
#     results = model.track(frame, show=False, tracker="bytetrack.yaml")

#     # Draw bounding boxes and labels
#     if len(results) > 0 and results[0].boxes is not None:
#         boxes = results[0].boxes.xyxy.cpu().numpy()
#         names = results[0].names
#     if results[0].probs is not None:
#         probs = results[0].probs.cpu().numpy()
#     else:
#         probs = [None] * len(boxes)

#     # Include track IDs if available
#     if results[0].boxes.is_track:
#         track_ids = results[0].boxes.id.cpu().numpy()
#     else:
#         track_ids = [None] * len(boxes)

#     for box, label, conf, track_id in zip(boxes, names, probs, track_ids):
#         x1, y1, x2, y2 = map(int, box)

#         # Include track ID and confidence score in the label
#         label_str = f"{label}"
#         if track_id is not None:
#             label_str += f" ID: {track_id}"
#         if conf is not None:
#             label_str += f" {conf:.2f}"

#         plot_one_box((x1, y1, x2, y2), frame, color=(0, 0, 255), label=label_str, line_thickness=2)


#     # Draw a vertical line at the center of the frame
#     height, width, _ = frame.shape
#     center_x = int(width / 2)
#     cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 2)

#     # Display the frame with the center line overlay and bounding boxes
#     cv2.imshow('Live Feed', frame)

#     # Break the loop when 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
from ultralytics import YOLO
import time
import board
import digitalio




# Load the YOLOv8 model
model = YOLO("D:\downloads\\best.pt")

# desired distance between the ground robot and the drone

desired_distance = 0.5

# Camera parameters
focal_length = 730  # C920 webcam focal length 3.9mm??
drone_real_width = 0.17  # Tello width

# Open the video capture
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_center_x = frame_width // 2
frame_center_y = frame_height // 2

# Function to control the camera pan-tilt servos
def adjust_pan_tilt_servos(dx, dy):
    # logic to control servo will go here!!!!!!!!
    pass

def adjust_robot_movement(distance):
    if distance < desired_distance - 0.05:
        #move the robot forward
        pass

    elif distance > desired_distance + 0.05:
        #move the robot backwards
        pass

    else:
        #stop the robot
        pass



while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Detect objects and track using YOLOv8 and ByteTrack
    results = model.track(frame, show=False, device="0", tracker="bytetrack.yaml")

    # Iterate over tracked objects
    if len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        names = results[0].names
        probs = results[0].probs.cpu().numpy() if results[0].probs is not None else [None] * len(boxes)
        track_ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.is_track else [None] * len(boxes)

        for box, class_id, conf, track_id in zip(boxes, names, probs, track_ids):
            x1, y1, x2, y2 = map(float, box[:4])
            class_name = names[int(class_id)]

            if class_name == "Tello":
                x_center = (x1 + x2) / 2            #Calculate the center pixel of the drone_x position
                y_center = (y1 + y2) / 2            #Calculate the center pixel of the drone_y position
                dx = x_center - frame_center_x      #Calculate the difference between frame_center_x and drone_x position
                dy = y_center - frame_center_y      #Calculate the difference between frame_center_y and drone_y position

                adjust_pan_tilt_servos(dx, dy)

                drone_pixel_width = x2 - x1
                distance = (drone_real_width * focal_length) / drone_pixel_width
                print("Estimated distance to drone:", distance)

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"Distance: {distance:.2f}m", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                

                # Show the dx and dy values on the video feed
                cv2.putText(frame, f"dx: {dx:.2f}", (int(x1), int(y1) - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, f"dy: {dy:.2f}", (int(x1), int(y1) - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    cv2.imshow("Frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



cap.release()
cv2.destroyAllWindows()
