import cv2
#print(cv2.__version__)

width=800
height=600
flip=0

camSet = 'v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
cam=cv2.VideoCapture('/dev/video1')
while True:
    _, frame = cam.read()
    cv2.imshow('mycam',frame)\
    #cv2.moveWindow('myCam',frame)
    if cv2.waitKey(1)==ord('e'):
        break

cam.release()
cv2.destroyAllWindows() 