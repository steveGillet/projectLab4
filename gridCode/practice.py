import time
from djitellopy import Tello

# Create Tello object

tello = Tello()

# Connect to Tello drone
tello.connect()
time.sleep(2)
tello.takeoff
time.sleep(5)

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
tello.move_forward(20)
y += 20
print('Current Position {x,y}')

# Move forward in increments of 152 cm
while y<=110:
    tello.move_forward(30)
    y += 30
    print('Current Position {x,y}')
    time.sleep(2)  # Wait for drone to complete movement

    
  


tello.move_left(40)
x +=40
print('Current Position {x,y}')
time.sleep(5)
while y >= 21:
    tello.move_back(30)
    y-=30
    print('Current Position {x,y}')
    if y<=20:
        tello.land()
        break
# Print final position
print("Final position: ({}, {})".format(x, y))

# Disconnect from Tello drone
tello.land
