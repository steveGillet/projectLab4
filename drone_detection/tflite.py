import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter

# Load the TFLite model
interpreter = Interpreter(model_path="best_int8.tflite")
interpreter.allocate_tensors()

# Get the input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set the parameters for drawing bounding boxes
threshold = 0.2
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]  # Add more colors for different classes

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    # Preprocess the frame
    input_height, input_width = 640, 640 # Replace with the input dimensions of your model
    input_frame = cv2.resize(frame, (input_width, input_height))
    input_frame = input_frame.astype(np.float32) / 255.0
    input_frame = np.expand_dims(input_frame, axis=0)
    # Perform inference
    interpreter.set_tensor(input_details[0]['index'], input_frame)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Process the output data and draw bounding boxes
    height, width, _ = frame.shape
    # Assuming the detection vector has the format [x1, y1, x2, y2, score]
    for i in range(output_data.shape[2]):
        detection = output_data[0, :, i]

    if detection[4] > threshold:  # If the score is above the threshold
        x1, y1, x2, y2 = detection[:4]
        x1 = int(x1 * width)
        y1 = int(y1 * height)
        x2 = int(x2 * width)
        y2 = int(y2 * height)

        # Draw the bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the frame with the drawn bounding boxes
    cv2.imshow('Object Tracking', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()