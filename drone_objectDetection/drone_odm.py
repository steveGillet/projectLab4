import cv2
import numpy as np
import sys
import glob

import time
import torch



class YoloDetector():

    def _init_(self, model_name):

        self.model = self.load_model(model_name)
        self.classes = self.model.names
        #print(self.classes)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)


    def load_model(self, model_name):

        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            return model

    def score_frame(self, frame):

        self.model.to(self.device)
        downscale_factor = 2
        width = int(frame.shape[1] / downscale_factor)
        height = int(frame.shape[0] / downscale_factor)
        frame = cv2.resize(frame, (width, height))
        #frame = frame.to(self.device)

        results =self.model(frame)
        #print(results)

        labels, cord = results.xyxyn[0], results.xyxyn[0][:, :-1]
        #print(labels)

        return labels, cord
    
    def class_to_label(self, x):

        return self.classes[int(x)]
    
    def plot_boxes(self, frame, labels, height
