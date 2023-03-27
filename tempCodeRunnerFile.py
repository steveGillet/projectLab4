red_pixels = cv2.countNonZero(mask[y:y+h, x:x+w])
            # if red_pixels > 0.2 * w * h:
            #     cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
            