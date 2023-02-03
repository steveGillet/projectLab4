import cv2
#print(cv2.__version__)
cam=cv2.VideoCapture('/dev/video1')
while True:
    _, frame = cam.read()
    cv2.imshow('mycam',frame)
    if cv2.waitKey(1)==ord('e'):
        break

cam.release()
cv2.destroyAllWindows    