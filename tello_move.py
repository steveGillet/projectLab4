import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from djitellopy import Tello
import time

def detect_qr_code(image):
    decoded_objects = pyzbar.decode(image)
    return decoded_objects

def get_coordinates(drone, box_id):
    x, y = drone.get_current_position()
    return {'id': box_id, 'x': x, 'y': y}

def main():
    # Connect to the DJI Tello drone
    drone = Tello()
    drone.connect()
    drone.streamon()

    field_width = 300
    field_length = 200
    increment = 50  # 1 meter increment (Tello uses centimeters)

    boxes = []
    found_boxes = 0
    total_boxes = 7

    # Starting position
    drone_x, drone_y = 0, 0

    # Lawnmower pattern
    for x in range(0, field_width, increment):
        for y in range(0, field_length, increment):
            # Move to next position
            if x != drone_x:
                delta_x = x - drone_x
                if delta_x > 0:
                    drone.move_right(delta_x)
                else:
                    drone.move_left(-delta_x)
                drone_x = x
                time.sleep(1)

            if y != drone_y:
                delta_y = y - drone_y
                if delta_y > 0:
                    drone.move_forward(delta_y)
                else:
                    drone.move_back(-delta_y)
                drone_y = y
                time.sleep(1)

            # Capture frame
            frame = drone.get_frame_read().frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect QR codes
            decoded_objects = detect_qr_code(frame)

            for obj in decoded_objects:
                box_id = obj.data.decode('utf-8')
                if box_id in {'a', 'b', 'c', 'd', 'e', 'f'}:
                    box = get_coordinates(drone_x, drone_y, box_id)
                    boxes.append(box)
                    found_boxes += 1

            if found_boxes == total_boxes:
                break

        # Reverse direction
        increment = -increment

    drone.streamoff()
    drone.end()

    print("Found boxes:", boxes)

def get_coordinates(drone_x, drone_y, box_id):
    return {'id': box_id, 'x': drone_x/100, 'y': drone_y/100}

if __name__ == "__main__":
    main()
