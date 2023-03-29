import cv2
import numpy as np

# Load the ONNX model
net = cv2.dnn.readNetFromONNX("best.onnx")

# Enable OpenCL
cv2.ocl.setUseOpenCL(True)
if not cv2.ocl.haveOpenCL():
    print("OpenCL is not available on your system. Falling back to CPU.")
else:
    print("OpenCL is available on your system. Using GPU.")

# Prepare an input image
image = cv2.imread("input_image.jpg")
input_height, input_width = 224, 224  # Replace with the input dimensions of your model
image = cv2.resize(image, (input_width, input_height))
image = image.astype(np.float32) / 255.0
blob = cv2.dnn.blobFromImage(image)

# Set input and perform inference
net.setInput(blob)
output = net.forward()