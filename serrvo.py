import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
# kit.servo[15].set_pulse_width_range(500,2500)
# kit.servo[14].set_pulse_width_range(500,2500)

# kit.servo[0].angle = 180
# kit.continuous_servo[1].throttle = 1
# time.sleep(1)
# kit.continuous_servo[1].throttle = -1
# time.sleep(1)
# kit.servo[0].angle = 0
# kit.continuous_servo[1].throttle = 0

kit.servo[9].angle=90
kit.servo[8].angle=90
time.sleep(1)
# kit.servo[0].angle=180
# kit.servo[1].angle=0
# time.sleep(1)
# kit.servo[0].angle=0
# # kit.servo[1].angle=0
# time.sleep(1)
# kit.servo[0].angle=90
# kit.servo[1].angle=90
