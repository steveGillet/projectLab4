import cv2
from ultralytics import YOLO
import supervision as sv

def main():
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5,
    )
    
    model = YOLO("best.pt")
    
    for result in model.track(source=0, show=False, stream=True, tracker="bytetrack.yaml"):
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)        

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy() .astype(int)

        lables = [
            f"#{tracker_id}{model.model.names[class_id]} {confidence:.2f}"
            for xyxy, confidence, class_id, tracker_id
            in detections
        ]
        frame = box_annotator.annotate(scene=frame, detections=detections, labels=lables)

        if detections.xyxy.any():
            [x1, y1, x2, y2] = detections.xyxy[0]
            centerX = x1 + (x2 - x1) / 2
            centerY = y1 + (y2 - y1) / 2
            centerFrameX = 320
            centerFrameY = 240
            print(centerFrameX - centerX)
            print(centerFrameY - centerY)
        
            #Camera parameters
            focal_length = 730  # C920 webcam focal length 3.9mm??
            drone_real_width = 0.17  # Tello width

            drone_pixel_width = x2 - x1
            distance = (drone_real_width * focal_length) / drone_pixel_width
            print(f"{distance:.2f}")

        cv2.imshow("yolov8", frame)
        if (cv2.waitKey(30) == 27):
            break

if __name__ == "__main__":
    main()


