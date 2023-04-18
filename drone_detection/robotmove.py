from adafruit_pca9685 import PCA9685
import time
import board
import busio
import digitalio

# in1 = digitalio.DigitalInOut(board.D24)
# in2 = digitalio.DigitalInOut(board.D15)
# in3 = digitalio.DigitalInOut(board.D22)
# in4 = digitalio.DigitalInOut(board.D23)

# in1.direction = digitalio.Direction.OUTPUT
# in2.direction = digitalio.Direction.OUTPUT
# in3.direction = digitalio.Direction.OUTPUT
# in4.direction = digitalio.Direction.OUTPUT

# i2c = busio.I2C(board.SCL, board.SDA)

# pca = PCA9685(i2c)
# pca.frequency = 60

# ena = 2
# enb = 3

# def stop():
#     in1.value = False
#     in2.value = False
#     in3.value = False
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x0000
#     pca.channels[enb].duty_cycle = 0x0000

# def turn_right():
#     in1.value = True
#     in2.value = False
#     in3.value = False
#     in4.value = True
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def turn_left():
#     in1.value = False
#     in2.value = True
#     in3.value = True
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def move_backward():
#     in1.value = True
#     in2.value = False
#     in3.value = True
#     in4.value = False
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

# def move_forward():
#     in1.value = False
#     in2.value = True
#     in3.value = False
#     in4.value = True
#     pca.channels[ena].duty_cycle = 0x7FFF
#     pca.channels[enb].duty_cycle = 0x7FFF

def moveToPosition(groundBot, coord):
    x, y = coord

    time_per_cm_x = 0.033
    time_per_cm_y = 0.033

    if x > 0:
        while groundBot.yaw > -0.019:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()
    elif x < 0:
        while groundBot.yaw < 0.019:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()

    if x > 0:
        groundBot.forward()
    elif x < 0:
        groundBot.backward()

    time.sleep(abs(x) * time_per_cm_x)
    groundBot.stop()

    if x > 0 and y > 0:
        while groundBot.yaw < 0.000:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()
    elif x > 0 and y < 0:
        while groundBot.yaw > 0.000:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()
    elif x < 0 and y > 0:
        while groundBot.yaw < 0.000:
            groundBot.turnLeft()
            time.sleep(0.1)
        groundBot.stop()
    elif x < 0 and y < 0:
        while groundBot.yaw > 0.000:
            groundBot.turnRight()
            time.sleep(0.1)
        groundBot.stop()

    if y > 0:
        groundBot.forward()
    elif y < 0:
        groundBot.backward()

    time.sleep(abs(y) * time_per_cm_y)
    groundBot.stop()


# if __name__ == "__main__":
#     try:
#         move_to_position([10, 40])
#     except KeyboardInterrupt:
#         stop()
#         pca.reset()
