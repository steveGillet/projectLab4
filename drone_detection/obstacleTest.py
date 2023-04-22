import cv2

def process_frame(frame):
    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(blurred, 50, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def check_obstacle(frame, area_threshold=7500, distance_threshold=1000):
    # Process the frame and find contours
    contours = process_frame(frame)

    # Check if any of the contours are large enough and close enough to be considered obstacles
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > area_threshold:
            # Calculate the center of the contour
            moments = cv2.moments(contour)
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])

            # Check if the contour is close enough to be an obstacle
            if cY < distance_threshold:
                return True, contours

    return False, contours

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    obstacle_detected, contours = check_obstacle(frame)

    print(obstacle_detected)
    # Draw contours on the frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
