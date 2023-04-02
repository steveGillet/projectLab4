import cv2
import numpy as np

# Load the model
model = cv2.dnn.readNetFromTensorflow('best.pb')

# Load an image
image = cv2.VideoCapture(0)
ret, image = image.read()

# Preprocess the image
blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)

# Set the input for the model
model.setInput(blob)

# Run the model
output = model.forward()

# Extract the detection results
detections = output[0, 0, :, :]

# Set a confidence threshold
confidence_threshold = 0.5

# Loop through the detections
for detection in detections:
    confidence = detection[2]
    
    # If the confidence is above the threshold, draw a bounding box around the detected object
    if confidence > confidence_threshold:
        x1, y1, x2, y2 = (detection[3:7] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])).astype(int)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Show the resulting image
cv2.imshow('Output', image)
cv2.waitKey(0)
cv2.destroyAllWindows()