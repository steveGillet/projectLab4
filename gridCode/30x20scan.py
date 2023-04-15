import time
from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode


def waitfordrone():
    time.sleep(2)
    while tello.get_speed_x()>0 and tello.get_speed_y()>0 and tello.get_speed_z()>0:
        time.sleep(.01)

#set box position to 0,0
letter_positions = {'a': {'start': (0, 0), 'current': (0, 0)}, 'b': {'start': (0, 0), 'current': (0, 0)}, 'c': {'start': (0, 0), 'current': (0, 0)}, 'd': {'start': (0, 0), 'current': (0, 0)}, 'e': {'start': (0, 0), 'current': (0, 0)}, 'f': {'start': (0, 0), 'current': (0, 0)}}

# Create Tello object
tello = Tello()

# Connect to Tello drone
tello.connect()

# Make Drone takeoff
tello.takeoff()
waitfordrone()


# Define starting position
x = 0
y = 0

# Move forward (For efficiency)
tello.move_forward(76)
waitfordrone
y += 76
print("Current Position: {}, {}".format(x, y))

while True:
# Move forward in increments of 152 cm on Y axis
    while y < 836 and (x == 0 or x ==152 or x==304 or x==436):
        tello.move_forward(152)
        waitfordrone()
        y += 152
        print("Current Position: {}, {}".format(x, y))
        if y == 836:
            break
        
        
    # Move drone in X position
    if y == 836:
        tello.move_right(76)
        waitfordrone()
        x +=76
        print("Current Position: {}, {}".format(x, y))
        tello.move_back(152)
        waitfordrone()
        y -=152
        print("Current Position: {}, {}".format(x, y))
        
        

    if y == 76:
        tello.move_right(76)
        waitfordrone()
        x +=76
        print("Current Position: {}, {}".format(x, y))
        tello.move_forward(152)
        waitfordrone()
        y +=152
        print("Current Position: {}, {}".format(x, y))

    # Move backward in increments of 152 cm on Y axis
    while y > 76 and (x == 76 or x==228 or x==380 or x==532):
        tello.move_back(152)
        waitfordrone()
        y-=152
        print("Current Position: {}, {}".format(x, y))
        
        

    # Print final position
    # print("Final position: ({}, {})".format(x, y))

    # Disconnect from Tello drone
    # tello.land
