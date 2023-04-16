import time
from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import threading
import queue


def tellopath(tello):
    global xp, yp
    def waitfordrone():
        time.sleep(2)
    while tello.get_speed_x()>0 and tello.get_speed_y()>0 and tello.get_speed_z()>0:
        time.sleep(.01)

 

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
    yp += 38
    
    print("Current Position: {}, {}".format(xp, yp))

    while True:
        # Move forward in increments of 152 cm on yp axpis
        while yp < 874 and (xp == 0 or xp ==244 or xp==488):
            tello.move_forward(76)
            waitfordrone()
            yp += 76
            
            print("Current Position: {}, {}".format(xp, yp))
            if yp == 874:
                break
            
            
        # Move drone in xp position
        if yp == 874:
            tello.move_right(122)
            waitfordrone()
            xp +=122
            
            print("Current Position: {}, {}".format(xp, yp))
            tello.move_back(76)
            waitfordrone()
            yp -=76
            
            print("Current Position: {}, {}".format(xp, yp))
            
            

        if yp == 38:
            tello.move_right(122)
            waitfordrone()
            xp +=122
            
            print("Current Position: {}, {}".format(xp, yp))
            tello.move_forward(76)
            waitfordrone()
            yp +=76
            
            print("Current Position: {}, {}".format(xp, yp))

        # Move backward in increments of 152 cm on yp axpis
        while yp > 38 and (xp == 122 or xp==366):
            tello.move_back(76)
            waitfordrone()
            yp-=76
            
            print("Current Position: {}, {}".format(xp, yp))
        
def QR_tello(tello):
    global xp, yp, box_positions
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
                if barcodeData == 'A':
                    box_positions['ABOX'] = (xp, yp)
                    print(box_positions['ABOX'])
                elif barcodeData == 'B':
                    box_positions['BBOX'] = (xp, yp)
                    print(box_positions['BBOX'])
                elif barcodeData == 'C':
                    box_positions['CBOX'] = (xp, yp)
                    print(box_positions['CBOX'])
                elif barcodeData == 'D':
                    box_positions['DBOX'] = (xp, yp)
                    print(box_positions['DBOX'])
                elif barcodeData == 'E':
                    box_positions['EBOX'] = (xp, yp)
                    print(box_positions['EBOX'])
                elif barcodeData == 'F':
                    box_positions['FBOX'] = (xp, yp)
                    print(box_positions['FBOX'])
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
xp = 0
yp = 0

# Create Tello object/ Connect
tello = Tello()
tello.connect()
time.sleep(1)
tello.streamon()
time.sleep(1)

t1 = threading.Thread(target=tellopath, args=(tello,))
t2 = threading.Thread(target=QR_tello, args=(tello,))

t1.start()
t2.start()

