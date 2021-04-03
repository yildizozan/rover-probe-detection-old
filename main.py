import numpy as np
import cv2 as cv

cap = cv.VideoCapture("test_vids/IMG_9350.MOV")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    dst = cv.equalizeHist(gray)
    temp = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    blur = cv.GaussianBlur(temp, (5, 5), 0)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, (25, 100, 100), (100, 255, 255))

    kernel = np.ones((7, 7), np.uint8)
    green_mask = cv.dilate(mask, kernel)
    res_green = cv.bitwise_and(frame, frame, mask=green_mask)

    # Display the resulting frame
    result = cv.resize(res_green, (640, 480))
    frame = cv.resize(frame, (640, 480))
    cv.imshow('Result', result)
    cv.imshow('Original', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
