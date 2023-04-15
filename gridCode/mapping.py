import time
from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import threading
import queue

def tellopath(x,y,tello):
    

    def waitfordrone():
        time.sleep(2)
    while tello.get_speed_x()>0 and tello.get_speed_y()>0 and tello.get_speed_z()>0:
        time.sleep(.01)


    # Make Drone takeoff
    tello.takeoff()
    waitfordrone()

    # Move forward (For efficiency)
    tello.move_forward(76)
    waitfordrone()
    y += 76
    
    print("Current Position: {}, {}".format(x, y))

    while True:
        # Move forward in increments of 152 cm on Y axis
        while y < 836 and (x == 0 or x ==152 or x==304 or x==436):
            tello.move_forward(152)
            waitfordrone()
            y += 152
            
            print("Current Position: {}, {}".format(x, y))
            if y == 836:
                break
            
            
        # Move drone in X position
        if y == 836:
            tello.move_right(76)
            waitfordrone()
            x +=76
            
            print("Current Position: {}, {}".format(x, y))
            tello.move_back(152)
            waitfordrone()
            y -=152
            
            print("Current Position: {}, {}".format(x, y))
            
            

        if y == 76:
            tello.move_right(76)
            waitfordrone()
            x +=76
            
            print("Current Position: {}, {}".format(x, y))
            tello.move_forward(152)
            waitfordrone()
            y +=152
            
            print("Current Position: {}, {}".format(x, y))

        # Move backward in increments of 152 cm on Y axis
        while y > 76 and (x == 76 or x==228 or x==380 or x==532):
            tello.move_back(152)
            waitfordrone()
            y-=152
            
            print("Current Position: {}, {}".format(x, y))
        
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
                bar.put(barcodeDataQRnumber= barcodeData)
                barcodeType = obj.type
                string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
            
                cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                print("Barcode: "+barcodeData +" | Type: "+barcodeType)
            cv2.imshow('Image', frame)

def run():
    tellopath(x,y,tello)
    QR_tello(tello)
#set box position to 0,0
box_positions = {'ABOX': (0, 0), 'BBOX': (0, 0), 'CBOX':(0,0), 'DBOX': (0,0), 'EBOX': (0,0), 'FBOX':(0,0)}

#Get QR value
bar = queue.Queue()

# Define starting position
x = 0
y = 0

# Create Tello object/ Connect
tello = Tello()
tello.connect()
time.sleep(1)
tello.streamon()
time.sleep(1)


t1 = threading.Thread(target=run)


t1.start()
