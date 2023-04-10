import cv2
from ultralytics import YOLO
import supervision as sv
import digitalio
import board
import busio
from simple_pid import PID
from adafruit_pca9685 import PCA9685

in1 = digitalio.DigitalInOut(board.D15)
in2 = digitalio.DigitalInOut(board.D24)
in3 = digitalio.DigitalInOut(board.D22)
in4 = digitalio.DigitalInOut(board.D23)
ena = 2
enb = 3

in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT
in3.direction = digitalio.Direction.OUTPUT
in4.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)

#Set the PWM frequency to 60hz
pca = PCA9685(i2c)
pca.frequency = 60


def forward():
    in1.value = False
    in2.value = True
    in3.value = False
    in4.value = True
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def backward():
    in1.value = True
    in2.value = False
    in3.value = True
    in4.value = False
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def stop():
    in1.value = False
    in2.value = False
    in3.value = False
    in4.value = False
    pca.channels[ena].duty_cycle = 0x0000
    pca.channels[enb].duty_cycle = 0x0000


def main():
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5,
    )
    
    model = YOLO("D:\downloads\\best.pt")
    
    for result in model.track(source="D:\downloads\IMG_0637.mov", show=False, stream=True, tracker="bytetrack.yaml"):
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
            #print(f"{distance:.2f} m")
            if distance > 1:
                forward()
            else:
                stop()

            if distance < 1:
                backward()
            else:
                stop()

        cv2.imshow("yolov8", frame)
        if (cv2.waitKey(30) == 27):
            break

if __name__ == "__main__":
    main()


