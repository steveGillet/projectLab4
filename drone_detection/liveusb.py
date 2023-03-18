from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
model = YOLO("tello.pt")


model.predict(source="0",show=True,conf=0.5)

#results = model.track(source="0", show=True, tracker="customTrack.yaml") 
