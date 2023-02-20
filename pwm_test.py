import cv2
import RPi.GPIO as GPIO
import time
#print(cv2.__version__)

# width=800
# height=600
# flip=0

# camSet = 'v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
# cam=cv2.VideoCapture('/dev/video0')
def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32, GPIO.OUT)
    pwm1 = GPIO.PWM(32,60)
    pwm1.start(100)
    GPIO.setup(33, GPIO.OUT)
    pwm2 = GPIO.PWM(33,60)
    pwm2.start(100)
    time.sleep(30)
# pwm.ChangeDutyCycle(50)  

# while True:
#     _, frame = cam.read()
#     cv2.imshow('mycam',frame)\
#     #cv2.moveWindow('myCam',frame)
#     if cv2.waitKey(1)==ord('e'):
#         break

# cam.release()
    # cv2.destroyAllWindows() 

if __name__ == '__main__':
    main()


