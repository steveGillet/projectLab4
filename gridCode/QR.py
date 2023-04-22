import cv2
import numpy as np
from pyzbar.pyzbar import decode
from djitellopy import Tello
import time
#Initialize the Tello drone object
tello = Tello()
tello.connect()
time.sleep(1)
tello.streamon()
# time.sleep(2)
# tello.takeoff()
# time.sleep(2)
# height= tello.get_height()
# time.sleep(.5)
# Rheight=120-height
# tello.move_up(Rheight)


def QR_tello(tello):
    while True:
        # Get the Tello drone's camera feed
        frame = tello.get_frame_read().frame

        # If the frame is not None, decode barcodes and display the frame
        if frame is not None:
            gray_img = cv2.cvtColor(frame,0)
            barcode = decode(gray_img)

            for obj in barcode:
                points = obj.polygon
                (x,y,w,h) = obj.rect
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

                barcodeData = obj.data.decode("utf-8")
                barcodeType = obj.type
                string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
            
                cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                print("Barcode: "+barcodeData +" | Type: "+barcodeType)
            cv2.imshow('Image', frame)

        code = cv2.waitKey(10)
        if code == ord('q'):
            break

    tello.streamoff()
    cv2.destroyAllWindows()

QR_tello(tello)