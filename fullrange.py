from adafruit_servokit import ServoKit
import time

# Initialize PCA9685 and ServoKit
pca = ServoKit(channels=16)
servo = 0  # Set the servo channel to 0

# Define the pulse range for the SG90
servo_min = 150  # Minimum pulse length in microseconds
servo_max = 600  # Maximum pulse length in microseconds

# Loop through the full range of motion
while True:
    # Move the servo from minimum to maximum position
    for i in range(servo_min, servo_max):
        pca.servo[0].duty_cycle= int(i * 65535 / 20000)
        time.sleep(0.005)  # Wait for the servo to move

    # Move the servo from maximum to minimum position
    for i in range(servo_max, servo_min, -1):
        pca.servo[0].duty_cycle = int(i * 65535 / 20000)
        time.sleep(0.005)  # Wait for the servo to move