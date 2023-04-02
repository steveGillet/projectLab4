<<<<<<< HEAD
=======
# import board
# import digitalio
# import busio
# from adafruit_pca9685 import PCA9685
# import time
# from adafruit_servokit import ServoKit

# # kit=ServoKit(channels=16)
 
# # tilt=90
# # pan=90
# # dTilt=10
# # dPan=1
 
# # kit.servo[0].angle=pan
# # kit.servo[1].angle=tilt

# in1 = digitalio.DigitalInOut(board.D15)
# in2 = digitalio.DigitalInOut(board.D24)
# in3 = digitalio.DigitalInOut(board.D22)
# in4 = digitalio.DigitalInOut(board.D23)

# in1.direction = digitalio.Direction.OUTPUT
# in2.direction = digitalio.Direction.OUTPUT
# in3.direction = digitalio.Direction.OUTPUT
# in4.direction = digitalio.Direction.OUTPUT

# i2c = busio.I2C(board.SCL, board.SDA)

# pca = PCA9685(i2c)

# # Set the PWM frequency to 60hz.
# pca.frequency = 60

# # Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# # but the PCA9685 will only actually give 12 bits of resolution.
# ena = 2
# enb = 3

# def stop():
#     in1.value = False
#     in2.value = False
#     in3.value = False
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x0000
#     pca.channels[enb].duty_cycle = 0x0000

# def turnRight():
#     in1.value = True
#     in2.value = False
#     in3.value = False
#     in4.value = True
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def turnLeft():
#     in1.value = False
#     in2.value = True
#     in3.value = True
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def backward():
#     in1.value = True
#     in2.value = False
#     in3.value = True
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def forward():
#     in1.value = False
#     in2.value = True
#     in3.value = False
#     in4.value = True
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963
# import cv2
# from ultralytics import YOLO
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor

# model = YOLO("best_full_integer_quant_edgetpu.tflite")

# results = model.track(source="0",show=True, tracker="bytetrack.yaml") #stream=True) 

import cv2
from ultralytics import YOLO
import time
<<<<<<< HEAD


# Load the YOLOv8 model
model = YOLO("D:\downloads\\best.pt")
=======
import board
import digitalio
from adafruit_servokit import ServoKit
import numpy as np
# import onnxruntime as ort

kit=ServoKit(channels=16)

# Load the YOLOv8 model
model = YOLO("best.onnx")
# session = ort.InferenceSession('best.onnx')
# input_name = session.get_inputs()[0].name
>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963

# desired distance between the ground robot and the drone

desired_distance = 0.75

# Camera parameters
focal_length = 730  # C920 webcam focal length 3.9mm??
drone_real_width = 0.17  # Tello width

# Open the video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
<<<<<<< HEAD
frame_center_x = 320
frame_center_y = 240
=======
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_center_x = frame_width // 2
frame_center_y = frame_height // 2
>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963

pan_angle = 90
tilt_angle = 90
kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle

def adjust_pan_tilt_servos(dx, dy):
    global pan_angle
    global tilt_angle
    changeSpeed = 2
    pan_angle -= changeSpeed * np.sign(dx)
    tilt_angle -= changeSpeed * np.sign(dy)  # Reverse the sign of dy
    # Clamp the angles to avoid exceeding the servo limits
    pan_angle = np.clip(pan_angle, 0, 180)
    tilt_angle = np.clip(tilt_angle, 0, 180)

<<<<<<< HEAD
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
=======
    # Set the new angles for the servos
    kit.servo[0].angle = pan_angle
    kit.servo[1].angle = tilt_angle

# def adjust_robot_movement(distance):
#     if distance < desired_distance:
#         backward()

#     elif distance > desired_distance:
#         forward()
>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963

#     else:
#         stop()

<<<<<<< HEAD
# while cap.isOpened():
#     ret, frame = cap.read()
=======
fps_limit = 5
start_time = time.time()
>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963

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

    scale_factor = 0.5
    frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

    frame_center_x = int(frame_width * scale_factor) // 2
    frame_center_y = int(frame_height * scale_factor) // 2

    # Detect objects and track using YOLOv8 and ByteTrack
<<<<<<< HEAD
    results = model.track(frame, show=False, device="0", tracker="botsort.yaml")
=======
    results = model.track(frame, show=False, tracker="bytetrack.yaml")
    # Preprocess the input frame
    input_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # input_frame = cv2.resize(input_frame, (640, 640))
    # input_frame = input_frame.transpose(2, 0, 1)
    # input_frame = np.expand_dims(input_frame, axis=0)
    # input_frame = input_frame.astype(np.float32) / 255
>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963

    # Perform object detection using the ONNX model
    # results = session.run(None, {input_name: input_frame})
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

<<<<<<< HEAD
                draw_info(frame, x1, y1, distance, dx, dy)              
 
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
=======
                # adjust_robot_movement(distance)

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"Distance: {distance:.2f}m", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                

                # Show the dx and dy values on the video feed
                cv2.putText(frame, f"dx: {dx:.2f}", (int(x1), int(y1) - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, f"dy: {dy:.2f}", (int(x1), int(y1) - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
>>>>>>> b582798ee65d8f46487494bf8abd3aae3ab23963


    cv2.imshow("Frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    elapsed_time = time.time() - start_time
    if elapsed_time < 1./fps_limit:
        time.sleep(1./fps_limit - elapsed_time)
    start_time = time.time()



cap.release()
cv2.destroyAllWindows()









