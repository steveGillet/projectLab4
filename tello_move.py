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

    field_width = 9
    field_length = 6
    increment = 1  # 1 meter increment

    drone_x, drone_y = 0,0

    boxes = []
    found_boxes = 0
    total_boxes = 7

    # Starting position
    drone_x, drone_y = 0, 0

    # Lawnmower pattern
    for x in range(0, field_width, increment):
        for y in range(0, field_length, increment):

            # update the drone position
            drone_x += x
            drone_y += y

            # Move to next position
            drone.move_to(drone_x + x, drone_y + y, drone.get_height())
            time.sleep(1)


            print(drone_x)
            print(drone_y)

            # Capture frame
            frame = drone.get_frame_read().frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect QR codes
            decoded_objects = detect_qr_code(frame)

            for obj in decoded_objects:
                box_id = obj.data.decode('utf-8')
                if box_id in {'a', 'b', 'c', 'd', 'e', 'f'}:
                    box = get_coordinates(drone, box_id)
                    boxes.append(box)
                    found_boxes += 1

            if found_boxes == total_boxes:
                break

        # Reverse direction
        increment = -increment

    drone.streamoff()
    drone.end()

    print("Found boxes:", boxes)

if __name__ == "__main__":
    main()
