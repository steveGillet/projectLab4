import cv2

img = cv2.imread('image.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        pixel = hsv[y, x]
        print(f'H:{pixel[0]} S:{pixel[1]} V:{pixel[2]}')

cv2.namedWindow('image')

cv2.setMouseCallback('image', mouse_callback)

cv2.imshow('image', img)
cv2.waitKey(0)

cv2.destroyAllWindows()