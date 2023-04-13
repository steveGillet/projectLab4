import time 
from djitellopy import Tello

# Create Tello object
tello = Tello()

# Connect to Tello drone
tello.connect()

tello.takeoff()
# while tello.is_flying:
#     time.sleep(0.1)
#set box position to 0,0
letter_positions = {'a': {'start': (0, 0), 'current': (0, 0)}, 
                    'b': {'start': (0, 0), 'current': (0, 0)}, 
                    'c': {'start': (0, 0), 'current': (0, 0)}, 
                    'd': {'start': (0, 0), 'current': (0, 0)}, 
                    'e': {'start': (0, 0), 'current': (0, 0)}, 
                    'f': {'start': (0, 0), 'current': (0, 0)}}

# Define starting position
x = 0
y = 0
time.sleep(1)
tello.move_forward(76)
y += 76
# while tello.is_flying:
#     time.sleep(0.1)

# Move forward in increments of 152 cm
# while y<=152:
#     tello.move_forward(152)
#     y += 152
#     print('Current Position {x,y}')
#     #Wait for drone to complete movement
#     while tello.is_flying:
#         time.sleep(0.1)

    
  
time.sleep(2)

tello.move_right(76)
x +=76
print('Current Position {x,y}')
# while tello.is_flying:
#     time.sleep(0.1)
time.sleep(1)
while y >= 77:
    tello.move_back(152)
    y-=152
    while tello.is_flying:
        time.sleep(0.1)
    print('Current Position {x,y}')
    if y<=76:
        tello.move_right(76)
        while tello.is_flying:
            time.sleep(0.1)
        break
# Print final position
print("Final position: ({}, {})".format(x, y))

# Disconnect from Tello drone
tello.land()
