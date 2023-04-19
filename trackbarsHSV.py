import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 145, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 97, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 90, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 222, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 100, 255, nothing)

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower_red_new = np.array([l_h, l_s, l_v])
    upper_red_new = np.array([u_h, u_s, u_v])

    lower_red_old = np.array([128, 122, 25])
    upper_red_old = np.array([179, 254, 122])

    mask_new = cv2.inRange(hsv, lower_red_new, upper_red_new)
    mask_old = cv2.inRange(hsv, lower_red_old, upper_red_old)

    mask = cv2.bitwise_or(mask_new, mask_old)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
