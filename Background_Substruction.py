import cv2 as cv
import numpy as np


dilation_kernel = np.ones((20,20),np.uint8)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
fbgb = cv.createBackgroundSubtractorKNN()
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    print(frame.shape)
    frame = frame[100:frame.shape[0] -100,:frame.shape[1] - 100,:] #frame shapei değiştirdim.
    print(frame.shape)
    if ret:
        fgmask = fbgb.apply(frame)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
        dilation = cv.dilate(fgmask, dilation_kernel, iterations = 1)
        contours, hierarchy = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        for c in contours:
            area = cv.contourArea(c)
            if area > 3000:
                x,y,w,h = cv.boundingRect(c)
                rectangle = cv.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),2)
                #roi = frame[]
        cv.imshow("goruntu", frame)

        if cv.waitKey(1) == ord("q"):
            break
cap.release()
cv.destroyAllWindows()
