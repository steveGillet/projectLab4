import cv2
import numpy as np

def find_line(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        longest_line = max(lines, key=lambda line: np.linalg.norm(line.reshape(-1, 4)[:2] - line.reshape(-1, 4)[2:]))
        return longest_line
    else:
        return None

def draw_line(image, line, color=(0, 255, 0), thickness=2):
    if line is not None:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        line = find_line(frame)
        draw_line(frame, line)
        cv2.imshow('Webcam with Line', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
