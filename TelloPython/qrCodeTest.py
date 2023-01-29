import cv2

filename = "./../3.png"

img = cv2.imread(filename)

detector = cv2.QRCodeDetector()
data = detector.detectAndDecode(img)

print(data)