import tensorflow as tf
from tensorflow import keras
import cv2
from picamera2 import Picamera2
import time
import numpy as np

model = keras.models.load_model('cnn_model.h5')

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Loop over frames from the camera
while True:
    # Preprocess the image for the CNN model
    frame = picam2.capture_array()
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(frame.shape)
    print(frame.dtype)
    frame2 = cv2.resize(frame1, (64, 64))
    frame2 = frame2/ 255.0
    frame2 = np.reshape(frame2, (1, 64, 64, 3))

    # Run the CNN model on the preprocessed image
    predictions = model.predict(frame2)
    label = ['left', 'right', 'forward'][predictions.argmax()]
    print(label)

    # Display the image and predicted label in a window
    cv2.imshow("Image", frame1)
    cv2.waitKey(1)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up the camera and OpenCV resources
cv2.destroyAllWindows()
