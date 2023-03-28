import board
import digitalio
import busio
from adafruit_pca9685 import PCA9685

print("Hello blinka!")

# Try to great a Digital input
pin = digitalio.DigitalInOut(board.D7)
print("Digital IO ok!")

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

pca = PCA9685(i2c)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
pca.channels[2].duty_cycle = 0xFFFF

# Try to create an SPI device
# spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
# print("SPI ok!")

print("done!")