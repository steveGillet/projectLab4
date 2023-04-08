import cv2
# from getkey import getkey, keys

width=1280
height=720
flip=0
# camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
cap=cv2.VideoCapture(0)

ret, frame = cap.read()

i = 0

while True:
    _, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Show the image
    cv2.imshow("Red, square door frame detection", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    elif key == ord('f'):
        cv2.imwrite('box{}.jpg'.format(i), frame)
        i += 1

cap.release()
cv2.destroyAllWindows()