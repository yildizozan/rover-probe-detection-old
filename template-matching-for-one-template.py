import os
import cv2

class TemplateMatch:
    def __init__(self, templates):
        self.cam = cv2.VideoCapture(0)
        
        self.w = templates.shape[1]
        self.h = templates.shape[0]
        
        self.templates = templates

    def detect(self, frame, templates, w, h):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(frame, self.templates, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        top_left = max_loc
        bottom_right = (top_left[0] + self.w, top_left[1] + self.h)

        return (max_val, top_left, bottom_right)

    def run(self):
        while True:
            _, image = self.cam.read()

    
            result = self.detect(image, self.templates,self.w, self.h)
            if result[0] >= 0.6:
                label = '{:.2f}%'.format( result[0] * 100)

                cv2.putText(image, label, (result[1][0], result[1][1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.rectangle(image, *result[1:], (32, 32, 32), 2)

            else:
                print('{:.2f}%'.format(result[0] * 100))

            cv2.imshow('temp match', image)

            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = TemplateMatch(cv2.imread("C:/Users/Muhammed/Desktop/OpenCV/Udemy/templates/template-152.jpeg",0)) # location of template image
    app.run()
print(-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------)

import os
import cv2


templates = cv2.imread("C:/Users/Muhammed/Desktop/OpenCV/Udemy/templates/template-152.jpeg",0)
cam = cv2.VideoCapture(0)

w = templates.shape[1]
h = templates.shape[0]


while True:
    _, image = cam.read()
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(frame, templates, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if max_val >= 0.6:
        label = '{:.2f}%'.format( max_val * 100)

        cv2.putText(image, label, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(image, top_left,bottom_right, (32, 32, 32), 2)

    else:
        print('{:.2f}%'.format(max_val * 100))

    cv2.imshow('temp match', image)

    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
