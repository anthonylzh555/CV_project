import cv2
import numpy as np

lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])

cam = cv2.VideoCapture(0)
kernalOpen = np.ones((5,5))
kernelClose=np.ones((20,20))

while True :
       ret, img = cam.read()
       img = cv2.resize(img,(400,300))

       #convert BGR to HSV
       imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
       # creat the mask
       mask = cv2. inRange(imgHSV,lowerBound,upperBound)
       # morphology
       maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernalOpen)
       maskClose = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalOpen)
       
       maskFinal  = maskClose
       _,conts,h = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       
       cv2.drawContours(img,conts,-1,(255,0,0),3)
       for i in range(len(conts)):
              x, y, w, h = cv2.boundingRect(conts[i])
              cv2.rectangle(img,(x,y),(x+w, y+h), (0,0,255), 2)
              cv2.putText(img, str(i+1),(x, y+h),cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,255))
       cv2.imshow("maskClose", maskClose)
       cv2.imshow("maskOpen", maskOpen)
       cv2.imshow("mask", mask)
       cv2.imshow("cam", img)
       if cv2.waitKey(10) &0xFF ==ord('q'):
                       cap.release()
                       cv2.destroyAllWindows()
                       break
l