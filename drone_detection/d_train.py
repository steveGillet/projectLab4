from ultralytics import YOLO

# load model

model = YOLO("yolov8n.pt")

#Train the model

model.train(data="D:\downloads\\newTello", epochs=100, imgsz=640, device="0")