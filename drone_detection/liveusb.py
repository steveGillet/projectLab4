# import cv2
# from ultralytics import YOLO
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor

# model = YOLO("D:\downloads\\best.pt")

# results = model.track(source="0", device="0",show=True, tracker="bytetrack.yaml") #stream=True) 

import cv2
from ultralytics import YOLO
import time


# Load the YOLOv8 model
model = YOLO("D:\downloads\\best.pt")

# desired distance between the ground robot and the drone

desired_distance = 0.5

# Camera parameters
focal_length = 730  # C920 webcam focal length 3.9mm??
drone_real_width = 0.17  # Tello width

# Open the video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
frame_center_x = 320
frame_center_y = 240

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

def draw_info(frame, x1, y1, distance, dx, dy):
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(frame, f"Distance: {distance:.2f}m", (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, f"dx: {dx:.2f}", (int(x1), int(y1) - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, f"dy: {dy:.2f}", (int(x1), int(y1) - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# while cap.isOpened():
#     ret, frame = cap.read()

#     if not ret:
#         break
#     start_time = time.time()

#     # Detect objects and track using YOLOv8 and ByteTrack
#     results = model.track(frame, show=False, device="0", tracker="botsort.yaml")

#     # Iterate over tracked objects
#     if len(results) > 0 and results[0].boxes is not None:
#         boxes = results[0].boxes.xyxy.cpu().numpy()
#         names = results[0].names
#         probs = results[0].probs.cpu().numpy() if results[0].probs is not None else [None] * len(boxes)
#         track_ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.is_track else [None] * len(boxes)

#         for box, class_id, conf, track_id in zip(boxes, names, probs, track_ids):
#             x1, y1, x2, y2 = map(float, box[:4])
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
    start_time = time.time()

    # Detect objects and track using YOLOv8 and ByteTrack
    results = model.track(frame, show=False, device="0", tracker="botsort.yaml")

    # Iterate over tracked objects
    if len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        names = results[0].names
        probs = results[0].probs.cpu().numpy() if results[0].probs is not None else [None] * len(boxes)
        track_ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.is_track else [None] * len(boxes)

        # Extract Tello drones' bounding boxes using list comprehension
        tello_boxes = [(box, class_id, conf, track_id) for box, class_id, conf, track_id in zip(boxes, names, probs, track_ids) if names[int(class_id)] == "Tello"]

        for box, class_id, conf, track_id in tello_boxes:
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

                draw_info(frame, x1, y1, distance, dx, dy)              
 
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


    cv2.imshow("Frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



cap.release()
cv2.destroyAllWindows()









