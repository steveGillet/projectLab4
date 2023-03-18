import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration(main={"format": 'XRGB8888', "size": (3296, 2480)})
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()

i = 0
while True:
    input()
    picam.capture_file("leftpic{}.jpg".format(i))
    i+=1

picam.close()