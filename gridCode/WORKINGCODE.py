import time
from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import threading
import queue

def droneGrid(groundBot):
    def tellopath(tello, xp, yp):
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
            # Move forward in increments of 76 cm on the yp axis
            while yp < 174 and (xp == 0):
                tello.move_forward(68)
                waitfordrone()
                yp += 68
                
                print("Current Position: {}, {}".format(xp, yp))
                if yp == 174:
                    break
                
                
            # Move drone in xp position
            if yp == 174:
                tello.move_right(122)
                waitfordrone()
                xp +=122
                
                print("Current Position: {}, {}".format(xp, yp))
                tello.move_back(68)
                waitfordrone()
                yp -=68
                
                print("Current Position: {}, {}".format(xp, yp))
                
                

            # if yp == 38 :
            #     tello.move_right(122)
            #     waitfordrone()
            #     xp +=122
                
            #     print("Current Position: {}, {}".format(xp, yp))
            #     tello.move_forward(68)
            #     waitfordrone()
            #     yp +=68
                
            #     print("Current Position: {}, {}".format(xp, yp))

            # Move backward in increments of 68 cm on the yp axis
            while yp > 38 and (xp == 122):
                tello.move_back(68)
                waitfordrone()
                yp-=68
                
                print("Current Position: {}, {}".format(xp, yp))
                if yp == 38
                    break
            
    def QR_tello(tello, xp, yp):
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
                        groundBot.box_positions['A'] = (xp, yp)
                        print(groundBot.box_positions['A'])
                    elif barcodeData == 'B':
                        groundBot.box_positions['B'] = (xp, yp)
                        print(groundBot.box_positions['B'])
                    elif barcodeData == 'C':
                        groundBot.box_positions['C'] = (xp, yp)
                        print(groundBot.box_positions['C'])
                    elif barcodeData == 'D':
                        groundBot.box_positions['D'] = (xp, yp)
                        print(groundBot.box_positions['D'])
                    elif barcodeData == 'E':
                        groundBot.box_positions['E'] = (xp, yp)
                        print(groundBot.box_positions['E'])
                    elif barcodeData == 'F':
                        groundBot.box_positions['F'] = (xp, yp)
                        print(groundBot.box_positions['F'])
                    elif barcodeData == 'DONE':
                        groundBot.box_positions['DONE'] = (xp, yp)
                        print(groundBot.box_positions['DONE'])
                    barcodeType = obj.type
                    string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
                
                #     cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                #     print("Barcode: "+barcodeData +" | Type: "+barcodeType)
                # cv2.imshow('Image', frame)
            # code = cv2.waitKey(10)
            # if code == ord('q'):
            #     break

        tello.streamoff()
        cv2.destroyAllWindows()

    #Get QR value
    bar = queue.LifoQueue()

    # Define starting position
    xp = 1
    yp = 1

    # Create Tello object/ Connect
    tello = Tello()
    tello.connect()
    time.sleep(1)
    tello.streamon()
    time.sleep(1)

    t1 = threading.Thread(target=tellopath, args=(tello, xp, yp))
    t2 = threading.Thread(target=QR_tello, args=(tello, xp, yp))

    t1.start()
    t2.start()

