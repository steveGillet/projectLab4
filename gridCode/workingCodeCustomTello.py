import time
import cv2
import numpy as np
import threading
from pyzbar.pyzbar import decode
from tello import Tello
import queue

def droneGrid(groundBot):
    def waitfordrone():
        time.sleep(5)
        # while tello.get_speed_x() > 0 and tello.get_speed_y() > 0 and tello.get_speed_z() > 0:

    def tellopath(tello):
        tello.send_command("takeoff")
        time.sleep(7)
        tello.send_command("speed 10")
        # height = tello.get_height()
        # Rheight = 40
        tello.send_command(f"up 80")
        tello.send_command("forward 38")
        waitfordrone()
        groundBot.yp += 38
        
        print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))

        while True:
            # Move forward in increments of 76 cm on the groundBot.yp axis
            while groundBot.yp < 342 and (groundBot.xp == 0 or groundBot.xp == 152 or groundBot.xp == 304 or groundBot.xp == 456 or groundBot.xp == 608 or groundBot.xp == 760):
                tello.send_command("forward 76")
                waitfordrone()
                groundBot.yp += 76

                print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))
                if groundBot.yp == 342:
                    break

            # Move drone in groundBot.xp position
            if groundBot.yp == 342:
                tello.send_command("right 76")
                waitfordrone()
                groundBot.xp += 76

                print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))
                tello.send_command("back 76")
                waitfordrone()
                groundBot.yp -= 76

                print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))

            if groundBot.yp == 38:
                tello.send_command("right 76")
                waitfordrone()
                groundBot.xp += 76

                print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))
                tello.send_command("forward 76")
                waitfordrone()
                groundBot.yp += 76

                print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))

            # Move backward in increments of 76 cm on the groundBot.yp axis
            while groundBot.yp > 38 and (groundBot.xp == 76 or groundBot.xp == 228 or groundBot.xp == 380 or groundBot.xp == 532 or groundBot.xp == 684 or groundBot.xp == 836):
                tello.send_command("back 76")
                waitfordrone()
                groundBot.yp -= 76

                print("Current Position: {}, {}".format(groundBot.xp, groundBot.yp))
                if groundBot.yp == 38:
                    break

            
    def QR_tello(tello):
        while True:
            # Get the Tello drone's camera feed
            frame = tello.frame

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
                        groundBot.box_positions['A'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['A'])
                    elif barcodeData == 'B':
                        groundBot.box_positions['B'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['B'])
                    elif barcodeData == 'C':
                        groundBot.box_positions['C'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['C'])
                    elif barcodeData == 'D':
                        groundBot.box_positions['D'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['D'])
                    elif barcodeData == 'E':
                        groundBot.box_positions['E'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['E'])
                    elif barcodeData == 'F':
                        groundBot.box_positions['F'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['F'])
                    elif barcodeData == 'DONE':
                        groundBot.box_positions['DONE'] = (groundBot.xp, groundBot.yp)
                        print(groundBot.box_positions['DONE'])
                    barcodeType = obj.type
                    string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
                
                    # cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                    print("Barcode: "+barcodeData +" | Type: "+barcodeType)
                # cv2.imshow('Image', frame)
        #     code = cv2.waitKey(10)
        #     if code == ord('q'):
        #         break

        # tello.send_command("streamoff")
        # cv2.destroyAllWindows()

    #Get QR value
    bar = queue.LifoQueue()

    tello = Tello()
    tello.send_command("command")
    tello.send_command("streamon")
    t1 = threading.Thread(target=tellopath, args=(tello,))
    t2 = threading.Thread(target=QR_tello, args=(tello,))

    t1.start()
    t2.start()

