import cv2 as cv
import numpy as np


def nothing(x):
    pass


# Create a black image, a window
video = cv.VideoCapture(0)
cv.namedWindow('image')

# create trackbars for color change
cv.createTrackbar('hue_min','image',0,179,nothing)
cv.createTrackbar('hue_max','image',179,179,nothing)
cv.createTrackbar('sat_min','image',0,255,nothing)
cv.createTrackbar('sat_max','image',255,255,nothing)
cv.createTrackbar('val_min','image',0,255,nothing)
cv.createTrackbar('val_max','image',255,255,nothing)


while True:

    success, img = video.read()
    if success:
        blurred = cv.GaussianBlur(img, (45,45),0,0,cv.BORDER_CONSTANT)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV) 
        # get current positions of four trackbars
        hue_min = cv.getTrackbarPos('hue_min','image')
        hue_max = cv.getTrackbarPos('hue_max','image')
        sat_min = cv.getTrackbarPos('sat_min','image')
        sat_max = cv.getTrackbarPos('sat_max','image')
        val_min = cv.getTrackbarPos('val_min','image')
        val_max = cv.getTrackbarPos('val_max','image')

        lower = np.array([hue_min,sat_min,val_min])
        upper = np.array([hue_max,sat_max,val_max])
        
        
        mask = cv.inRange(hsv, lower, upper)
        
        
        remove_noise = cv.morphologyEx(mask, cv.MORPH_OPEN, None, iterations = 2)
        
        contours, hierarchy = cv.findContours(remove_noise, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        
        
        for c in contours:
            area = cv.contourArea(c)
            if area > 3000:
                peri = cv.arcLength(c,True)
                approx = cv.approxPolyDP(c, 0.02 * peri, True)
                x, y, w, h = cv.boundingRect(c)
                cv.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
                cv.putText(img, "points: " + str(len(approx)), (x+w+20, y+h+20), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0))
            if len(approx) == 4:
                cv.putText(img, "RECTANGLE ", (x+w+20, y+h+20), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0))
        
        cv.imshow("orijinal image_mask", img)
        cv.imshow("blurred", blurred)
        #cv.imshow("hsv formati", hsv)
        
        cv.imshow("mask", mask)
        cv.imshow("remove noise", remove_noise)
            
   

    if cv.waitKey(1) == ord("q"):
        break
video.release()
cv.destroyAllWindows()
