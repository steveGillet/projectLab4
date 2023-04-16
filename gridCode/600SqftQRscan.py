import time
from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import threading
import queue

def tellopath(x,y,tello):
    global bar

    def waitfordrone():
        time.sleep(2)
    while tello.get_speed_x()>0 and tello.get_speed_y()>0 and tello.get_speed_z()>0:
        time.sleep(.01)

    def getvalue():
        
        if bar.empty()== True:
            pass
        elif bar.empty() == False:
            QR = bar.get()
            if QR == 'A':
                box_positions['ABOX'] = (x, y)
                print(box_positions['ABOX'])
            elif QR == 'B':
                box_positions['BBOX'] = (x, y)
                print(box_positions['BBOX'])
            elif QR == 'C':
                box_positions['CBOX'] = (x, y)
                print(box_positions['CBOX'])
            elif QR == 'D':
                box_positions['DBOX'] = (x, y)
                print(box_positions['DBOX'])
            elif QR == 'E':
                box_positions['EBOX'] = (x, y)
                print(box_positions['EBOX'])
            elif QR == 'F':
                box_positions['FBOX'] = (x, y)
                print(box_positions['FBOX'])

    # Make Drone takeoff
    tello.takeoff()
    waitfordrone()
    time.sleep(1)
    height= tello.get_height()
    time.sleep(.5)
    Rheight=120-height
    tello.move_up(Rheight)
    time.sleep(1)
    # Move forward (For efficiency)
    tello.move_forward(38)
    waitfordrone()
    y += 38
    getvalue()
    print("Current Position: {}, {}".format(x, y))

    while True:
        # Move forward in increments of 152 cm on Y axis
        while y < 874 and (x == 0 or x ==244 or x==488):
            tello.move_forward(76)
            waitfordrone()
            y += 76
            getvalue()
            print("Current Position: {}, {}".format(x, y))
            if y == 874:
                break
            
            
        # Move drone in X position
        if y == 874:
            tello.move_right(122)
            waitfordrone()
            x +=122
            getvalue()
            print("Current Position: {}, {}".format(x, y))
            tello.move_back(76)
            waitfordrone()
            y -=76
            getvalue()
            print("Current Position: {}, {}".format(x, y))
            
            

        if y == 38:
            tello.move_right(122)
            waitfordrone()
            x +=122
            getvalue()
            print("Current Position: {}, {}".format(x, y))
            tello.move_forward(76)
            waitfordrone()
            y +=76
            getvalue()
            print("Current Position: {}, {}".format(x, y))

        # Move backward in increments of 152 cm on Y axis
        while y > 38 and (x == 122 or x==366):
            tello.move_back(76)
            waitfordrone()
            y-=76
            getvalue()
            print("Current Position: {}, {}".format(x, y))
        
def QR_tello(tello):
    global bar
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
                bar.put(barcodeData)
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


#set box position to 0,0
box_positions = {'ABOX': (0, 0), 'BBOX': (0, 0), 'CBOX':(0,0), 'DBOX': (0,0), 'EBOX': (0,0), 'FBOX':(0,0)}

#Get QR value
bar = queue.LifoQueue()

# Define starting position
x = 0
y = 0

# Create Tello object/ Connect
tello = Tello()
tello.connect()
time.sleep(1)
tello.streamon()
time.sleep(1)

t1 = threading.Thread(target=tellopath, args=(x, y, tello))
t2 = threading.Thread(target=QR_tello, args=(tello,))

t1.start()
t2.start()