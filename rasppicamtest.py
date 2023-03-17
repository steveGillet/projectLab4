import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()

i = 0
while True:
    input()
    picam.capture_file("right4{}.jpg".format(i))
    i+=1

picam.close()