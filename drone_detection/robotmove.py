from adafruit_pca9685 import PCA9685
import time
import board
import busio
import digitalio

in1 = digitalio.DigitalInOut(board.D24)
in2 = digitalio.DigitalInOut(board.D15)
in3 = digitalio.DigitalInOut(board.D22)
in4 = digitalio.DigitalInOut(board.D23)

in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT
in3.direction = digitalio.Direction.OUTPUT
in4.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 60

ena = 2
enb = 3

def stop():
    in1.value = False
    in2.value = False
    in3.value = False
    in4.value = False
    pca.channels[ena].duty_cycle = 0x0000
    pca.channels[enb].duty_cycle = 0x0000

def turn_right():
    in1.value = True
    in2.value = False
    in3.value = False
    in4.value = True
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def turn_left():
    in1.value = False
    in2.value = True
    in3.value = True
    in4.value = False
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def move_backward():
    in1.value = True
    in2.value = False
    in3.value = True
    in4.value = False
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def move_forward():
    in1.value = False
    in2.value = True
    in3.value = False
    in4.value = True
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def move_to_position(coord):
    x, y = coord
    time_per_foot_x = 1
    time_per_foot_y = 1
    turn_time = 0.5

    if x > 0:
        move_forward()
    else:
        move_backward()

    time.sleep(abs(x) * time_per_foot_x)
    stop()

    if y > 0:
        turn_right()
    else:
        turn_left()

    time.sleep(turn_time)
    stop()

    if y > 0:
        move_forward()
    else:
        move_backward()

    time.sleep(abs(y) * time_per_foot_y)
    stop()

if __name__ == "__main__":
    try:
        move_to_position([5, 10])
    except KeyboardInterrupt:
        stop()
        pca.reset()
