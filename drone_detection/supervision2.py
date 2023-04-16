import cv2
from ultralytics import YOLO
import supervision as sv
import digitalio
import board
import busio
from simple_pid import PID
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
import numpy as np
import time

def supervision2():
    desired_distance = 0.5 # 1 meters
    pid_distance = PID(1, 0.1, 0.01, setpoint=desired_distance, output_limits=(-1, 1), sample_time=0.01)
    desired_distance = .5 # 1 meters
    pid_distance = PID(1, 0.01, 0.01, setpoint=desired_distance, output_limits=(-1, 1), sample_time=0.01)


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

    panPin = 15
    tiltPin = 14

    class cam:
        def __init__(self):
            self.panAngle = 90
            self.tiltAngle = 180
            kit.servo[panPin].angle=self.panAngle
            kit.servo[tiltPin].angle=self.tiltAngle
        def camLeft(self):
            self.panAngle = 180
            kit.servo[panPin].angle=self.panAngle
        def camRight(self):
            self.panAngle = 0
            kit.servo[panPin].angle=self.panAngle
        def camForward(self):
            self.panAngle = 90
            kit.servo[panPin].angle=self.panAngle

    def forward(speed):
        in1.value = False
        in2.value = True
        in3.value = False
        in4.value = True
        speed = int(speed * 0x7FFF)
        pca.channels[ena].duty_cycle = speed
        pca.channels[enb].duty_cycle = speed

    def backward(speed):
        in1.value = True
        in2.value = False
        in3.value = True
        in4.value = False
        speed = int(speed * 0x7FFF)
        pca.channels[ena].duty_cycle = speed
        pca.channels[enb].duty_cycle = speed

    def stop():
        in1.value = False
        in2.value = False
        in3.value = False
        in4.value = False
        pca.channels[ena].duty_cycle = 0x0000
        pca.channels[enb].duty_cycle = 0x0000

    kit = ServoKit(channels=16)
    kit.servo[panPin].set_pulse_width_range(500,2500)
    kit.servo[tiltPin].set_pulse_width_range(500,2500)

        # Create PID controllers for pan and tilt servos
    pan_pid = PID(0.01, 0, 0, setpoint=0)
    tilt_pid = PID(0.01, 0, 0, setpoint=0)

    # Update the adjust_pan_tilt_servos function to use the PID controller
    def adjust_pan_tilt_servos(dx, dy):
        # Calculate the pan and tilt output using the PID controller
        pan_output = pan_pid(dx)
        tilt_output = tilt_pid(dy)

        cam1.panAngle += pan_output
        cam1.tiltAngle -= tilt_output
        # if cam1.panAngle < 0 or cam1.tiltAngle > 180:
        #     turnRight()
        # elif cam1.panAngle > 180
        #     turnLeft()
        cam1.panAngle = np.clip(cam1.panAngle, 0, 180)
        cam1.tiltAngle = np.clip(cam1.tiltAngle, 0, 180)

        kit.servo[panPin].angle = cam1.panAngle
        kit.servo[tiltPin].angle = cam1.tiltAngle

    cam1 = cam()
    backward()
    time.sleep(2)
    stop()

    def main():
        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.5,
        )
        
        model = YOLO("best.onnx")
        
        for result in model.track(source="0", show=False, stream=True, tracker="bytetrack.yaml"):
            frame = result.orig_img
            detections = sv.Detections.from_yolov8(result)        

            if result.boxes.id is not None:
                detections.tracker_id = result.boxes.id.cpu().numpy() .astype(int)

            lables = [
                f"#{tracker_id}{class_id} {confidence:.2f}"
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
                # print(centerFrameX - centerX)
                # print(centerFrameY - centerY)
                dx = centerX - centerFrameX
                dy = centerY - centerFrameY 
                adjust_pan_tilt_servos(dx, dy)
            
                #Camera parameters
                focal_length = 730  # C920 webcam focal length 3.9mm??
                drone_real_width = 0.17  # Tello width

                drone_pixel_width = x2 - x1
                distance = (drone_real_width * focal_length) / drone_pixel_width
                error_distance = pid_distance(distance)
                print(f"{distance:.2f} m")
                print(error_distance)
                if error_distance < 0:
                    forward(abs(error_distance))
                elif error_distance > 0:
                    backward(abs(error_distance))
                else:
                    stop()

            cv2.imshow("yolov8", frame)
            if (cv2.waitKey(30) == 27):
                break

    if __name__ == "__main__":
        main()


