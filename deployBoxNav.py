import tensorflow as tf
from tensorflow import keras
import cv2

def adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False):
    return tf.keras.optimizers.Adam(lr=lr, beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, decay=decay, amsgrad=amsgrad)

custom_objects = {'adam': adam}
model = keras.models.load_model('cnn_model.h5', custom_objects=custom_objects)

width=1280
height=720
flip=0 
camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap = cv2.VideoCapture(camSet)

while True:
    ret, frame = cap.read()
    
    # Preprocess the frame
    frame = cv2.resize(frame, (64, 64))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame / 255.0
    frame = frame.reshape(1, 64, 64, 3)
    
    # Make a prediction
    prediction = model.predict(frame)
    label = ['left', 'right', 'forward'][prediction.argmax()]
    
    # Display the label on the frame
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break