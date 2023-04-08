import cv2
from ultralytics import YOLO
import supervision as sv

def main():
    model = "tello.pt"

    box_annotator = sv.LineZoneAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5,
    )

    for result in model.track(source="0", show=True, stream=True):
        
        frame  = result.orig_img
        detections = sv.Detections.from_yolov8(result)
        frame = box_annotator.annotate(scene=frame, detections=detections)

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpu().astype(int)

        labels = [
            f"{tracker_id} {model.model.names[class_id]} {confidence:.2f}"
            for _, confidence, class_id, tracker_id
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
            )

        cv2.imshow("frame", frame)

        if (cv2.waitKey(30) == 27):
            break

if __name__ == "__main__":
    main()
