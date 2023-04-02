import cv2
import onnxruntime as ort
import numpy as np
from adafruit_servokit import ServoKit
import os

os.environ['ONNXRT_NPU_ENABLE'] = '1'
# Constants
ONNX_MODEL_PATH = 'best.onnx'
VIDEO_SOURCE = 0  # 0 for the first connected camera
PAN_SERVO_CHANNEL = 0
TILT_SERVO_CHANNEL = 1
PAN_SPEED = 1
TILT_SPEED = 1
MIN_CONFIDENCE = 0.5

# Load ONNX model
import onnxruntime as ort

# Create an InferenceSession with ACL execution provider
session = ort.InferenceSession("best.onnx")
# options = ort.SessionOptions()
# options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
# options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
# options.execution_order = [":NPU"]
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

cap = cv2.VideoCapture(VIDEO_SOURCE)

while True:
    ret, frame1 = cap.read()
    if not ret:
        break

    # Preprocess the frame
    frame = np.resize(frame1, (640,640,3))
    frame = frame.astype(np.float32)
    frame = np.expand_dims(frame, axis=0)
    frame = np.transpose(frame, (0, 3, 2, 1))

    # Run object detection
    detections = session.run([output_name], {input_name: frame})[0]
    print("Detections: ", detections)
    # Find the highest confidence detection
    max_confidence = 0
    best_detection = None
    for detection in detections:
        confidence = detection[-1]
        if (confidence.any() > MIN_CONFIDENCE) and (confidence.any() > max_confidence):
            max_confidence = confidence
            best_detection = detection

    if best_detection is not None:
        print("Best Detection: ", best_detection)
        # Get the coordinates of the detected object
        x, y, w, h = [coord.item() for coord in best_detection[:-1]]
        x1 = int(x * frame1.shape[1])
        y1 = int(y * frame1.shape[0])
        x2 = int((x + w) * frame1.shape[1])
        y2 = int((y + h) * frame1.shape[0])

        # Calculate the pan and tilt angles required to center the camera on the detected object
        center_x, center_y = (x + w / 2, y + h / 2)
        frame_height, frame_width, _, _ = frame.shape
        dx, dy = (center_x - frame_width / 2, center_y - frame_height / 2)

    #     # Update the pan and tilt angles based on the object's position
    #     pan_angle += PAN_SPEED * np.sign(dx)
    #     tilt_angle += TILT_SPEED * np.sign(dy)
    # # Clamp the angles to avoid exceeding the servo limits
    # pan_angle = np.clip(pan_angle, 0, 180)
    # tilt_angle = np.clip(tilt_angle, 0, 180)

    # Set the new angles for the servos
    # kit.servo[PAN_SERVO_CHANNEL].angle = pan_angle
    # kit.servo[TILT_SERVO_CHANNEL].angle = tilt_angle

    # Draw a bounding box around the detected object
    cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Object Tracking', frame1)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break