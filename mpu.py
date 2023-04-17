import time
import math
import board
import busio
import adafruit_mpu6050
from Kalman import KalmanAngle

# Initialize the MPU6050 sensor and the Kalman filter
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
kalmanX = KalmanAngle()
kalmanY = KalmanAngle()

# Set the roll and pitch angles to 0
roll = 0
pitch = 0

# Loop to read the sensor data and stabilize the robot's orientation
while True:
    # Read the raw sensor data
    accel_x, accel_y, accel_z = mpu.acceleration
    gyro_x, gyro_y, gyro_z = mpu.gyro

    # Calculate the roll and pitch angles from the raw sensor data
    roll = math.atan2(accel_y, accel_z) * 57.29578
    pitch = math.atan2(-accel_x, math.sqrt(accel_y * accel_y + accel_z * accel_z)) * 57.29578

    # Apply the Kalman filter to the roll and pitch angles
    kalAngleX = kalmanX.getAngle(roll, gyro_x / 131, 0.005)
    kalAngleY = kalmanY.getAngle(pitch, gyro_y / 131, 0.005)

    # Calculate the motor outputs based on the stabilized angles
    print(kalAngleY)
    print(kalAngleX)

    # Apply the motor outputs to the robot to bring it back to its original orientation
    # (you will need to implement the code to control the robot)
    # control_robot(motor1, motor2, motor3, motor4)

    # Wait for a short time to stabilize the readings and reduce the load on the processor
    time.sleep(0.01)
