import cv2
from ultralytics import YOLO
#from ultralytics.yolo.v8.detect.predict import DetectionPredictor

model = YOLO("D:\downloads\\best.pt")

for results in model.track(source="D:\downloads\IMG_0637.mov",show=False, stream=True, tracker="bytetrack.yaml"):
    frame = results.orig_img
    cv2.imshow("yolov8", frame)
    if (cv2.waitKey(30) == 27):
        break

# import cv2
# from ultralytics import YOLO
# import time


# # Load the YOLOv8 model
# model = YOLO("D:\downloads\\best.pt")

# # desired distance between the ground robot and the drone

# desired_distance = 0.75

# # Camera parameters
# focal_length = 730  # C920 webcam focal length 3.9mm??
# drone_real_width = 0.17  # Tello width

# # Open the video capture
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# frame_center_x = 320
# frame_center_y = 240

# pan_angle = 90
# tilt_angle = 90
# kit.servo[0].angle = pan_angle
# kit.servo[1].angle = tilt_angle

# def adjust_pan_tilt_servos(dx, dy):
#     global pan_angle
#     global tilt_angle
#     changeSpeed = 2
#     pan_angle -= changeSpeed * np.sign(dx)
#     tilt_angle -= changeSpeed * np.sign(dy)  # Reverse the sign of dy
#     # Clamp the angles to avoid exceeding the servo limits
#     pan_angle = np.clip(pan_angle, 0, 180)
#     tilt_angle = np.clip(tilt_angle, 0, 180)

# def adjust_robot_movement(distance):
#     if distance < desired_distance - 0.05:
#         #move the robot forward
#         pass

#     elif distance > desired_distance + 0.05:
#         #move the robot backwards
#         pass

#     else:
#         #stop the robot
#         pass

# def draw_info(frame, x1, y1, distance, dx, dy):
#     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#     cv2.putText(frame, f"Distance: {distance:.2f}m", (int(x1), int(y1) - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#     cv2.putText(frame, f"dx: {dx:.2f}", (int(x1), int(y1) - 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#     cv2.putText(frame, f"dy: {dy:.2f}", (int(x1), int(y1) - 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# #     else:
# #         stop()

# # while cap.isOpened():
# #     ret, frame = cap.read()

# #     if not ret:
# #         break
# #     start_time = time.time()

# #     # Detect objects and track using YOLOv8 and ByteTrack
# #     results = model.track(frame, show=False, device="0", tracker="botsort.yaml")

# #     # Iterate over tracked objects
# #     if len(results) > 0 and results[0].boxes is not None:
# #         boxes = results[0].boxes.xyxy.cpu().numpy()
# #         names = results[0].names
# #         probs = results[0].probs.cpu().numpy() if results[0].probs is not None else [None] * len(boxes)
# #         track_ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.is_track else [None] * len(boxes)

# #         for box, class_id, conf, track_id in zip(boxes, names, probs, track_ids):
# #             x1, y1, x2, y2 = map(float, box[:4])
# while cap.isOpened():
#     ret, frame = cap.read()

#     if not ret:
#         break
#     start_time = time.time()

#     scale_factor = 0.5
#     frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

#     frame_center_x = int(frame_width * scale_factor) // 2
#     frame_center_y = int(frame_height * scale_factor) // 2

#     # Detect objects and track using YOLOv8 and ByteTrack
#     results = model.track(frame, show=False, device="0", tracker="botsort.yaml")

#     # Perform object detection using the ONNX model
#     # results = session.run(None, {input_name: input_frame})
#     # Iterate over tracked objects
#     if len(results) > 0 and results[0].boxes is not None:
#         boxes = results[0].boxes.xyxy.cpu().numpy()
#         names = results[0].names
#         probs = results[0].probs.cpu().numpy() if results[0].probs is not None else [None] * len(boxes)
#         track_ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.is_track else [None] * len(boxes)

#         # Extract Tello drones' bounding boxes using list comprehension
#         tello_boxes = [(box, class_id, conf, track_id) for box, class_id, conf, track_id in zip(boxes, names, probs, track_ids) if names[int(class_id)] == "Tello"]

#         for box, class_id, conf, track_id in tello_boxes:
#             x1, y1, x2, y2 = map(float, box[:4])
#             class_name = names[int(class_id)]

#             if class_name == "Tello":
#                 x_center = (x1 + x2) / 2            #Calculate the center pixel of the drone_x position
#                 y_center = (y1 + y2) / 2            #Calculate the center pixel of the drone_y position
#                 dx = x_center - frame_center_x      #Calculate the difference between frame_center_x and drone_x position
#                 dy = y_center - frame_center_y      #Calculate the difference between frame_center_y and drone_y position

#                 adjust_pan_tilt_servos(dx, dy)

#                 drone_pixel_width = x2 - x1
#                 distance = (drone_real_width * focal_length) / drone_pixel_width
#                 print("Estimated distance to drone:", distance)

#                 draw_info(frame, x1, y1, distance, dx, dy)              
 
#     end_time = time.time()
#     fps = 1 / (end_time - start_time)
#     cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


#     cv2.imshow("Frame", frame)

#     # Break the loop if 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#     elapsed_time = time.time() - start_time
#     if elapsed_time < 1./fps_limit:
#         time.sleep(1./fps_limit - elapsed_time)
#     start_time = time.time()



# cap.release()
# cv2.destroyAllWindows()









