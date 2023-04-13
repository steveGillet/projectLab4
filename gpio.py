import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685
import time

#green, blue, orange, yellow
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

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
ena = 2
enb = 3

def stop():
    in1.value = False
    in2.value = False
    in3.value = False
    in4.value = False
    pca.channels[ena].duty_cycle = 0x0000
    pca.channels[enb].duty_cycle = 0x0000

def turnRight():
    in1.value = True
    in2.value = False
    in3.value = False
    in4.value = True
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def turnLeft():
    in1.value = False
    in2.value = True
    in3.value = True
    in4.value = False
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def backward():
    in1.value = True
    in2.value = False
    in3.value = True
    in4.value = False
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

def forward():
    in1.value = False
    in2.value = True
    in3.value = False
    in4.value = True
    pca.channels[ena].duty_cycle = 0x7FFF
    pca.channels[enb].duty_cycle = 0x7FFF

turnLeft()
time.sleep(1)
turnRight()
time.sleep(1)
forward()
time.sleep(1)
backward()
time.sleep(1)
stop()