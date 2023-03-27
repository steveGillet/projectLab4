from adafruit_servokit import ServoKit
import time 
myKit=ServoKit(channels=16)
myKit.servo[0].set_pulse_width_range(500,2500)
myKit.servo[1].set_pulse_width_range(500,2500)

try:
    while True:
              myKit.servo[0].angle=0
              myKit.servo[1].angle=180
              time.sleep(1)
              myKit.servo[0].angle=90
              myKit.servo[1].angle=90
              time.sleep(1)
              myKit.servo[0].angle=180
              myKit.servo[1].angle=0
              time.sleep(1)
            
except: KeyboardInterrupt
print("/nDone")
