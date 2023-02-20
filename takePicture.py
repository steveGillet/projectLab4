import cv2

width=1280
height=720
flip=0
camSet='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=24/1 ! videoconvert ! appsink'
cap=cv2.VideoCapture(camSet)

ret, frame = cap.read()

cv2.imwrite("image.jpg", frame)
cap.release()
cv2.destroyAllWindows()