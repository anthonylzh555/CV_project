import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse = Controller()
app = wx.App(False)
sx,sy = wx.GetDisplaySize()
(camx, camy) = (400,300)

"""
#RED
lowerBound = np.array([0,80,40])
upperBound = np.array([25,255,255])
"""
"""
#YELLOW
lowerBound = np.array([7,80,80])
upperBound = np.array([43,255,255])
"""

#GREEN
lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])


cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)
kernalOpen = np.ones((5,5))
kernelClose=np.ones((20,20))

mLoc0ld = np.array([0,0])
mouseLoc = np.array([0,0])
DamplingFactor = 2   #should be between > 1

pinchFlag = 0
openx,openy,openw,openh = (0,0,0,0)

#mouseLoc = mLoc0ld + (targetLoc - mLoc0ld)/DamplingFactor

while True :
       ret, img = cam.read()
       #mg = cv2.resize(img,(340,240))

       #convert BGR to HSV
       imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
       # creat the mask
       mask = cv2. inRange(imgHSV,lowerBound,upperBound)
       # morphology
       maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernalOpen)
       maskClose = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalOpen)
       
       maskFinal  = maskClose
       _,conts,h = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       
       if (len(conts) == 2) :
              if (pinchFlag == 1) :
                     pinchFlag = 0
                     mouse.release(Button.left)
              mouse.release(Button.left)
              x1,y1,w1,h1 = cv2.boundingRect(conts[0])
              x2,y2,w2,h2 = cv2.boundingRect(conts[1])
              cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
              cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
              cx1=x1+w1/2
              cy1=y1+h1/2
              cx2=x2+w2/2
              cy2=y2+h2/2
              cx = (cx1 + cx2)/2
              cy = (cy2 + cy2)/2
              cv2.line(img, (int(cx1),int(cy1)),(int(cx2),int(cy2)),(255,0,0),2)
              cv2.circle(img, (int(cx),int(cy)),2,(0,0,255),2)
              mouseLoc = mLoc0ld + ( (int(cx),int(cy)) - mLoc0ld)/DamplingFactor
              mouse.position =  (sx-int(mouseLoc[0]*sx/camx),int(mouseLoc[1]*sy/camy))     
              while mouse.position != (sx-int(mouseLoc[0]*sx/camx),int(mouseLoc[1]*sy/camy)) :
                     pass
              mLoc0ld = mouseLoc
              openx,openy,openw,openh=cv2.boundingRect(np.array([[[x1,y1],[x1+w1,y1+h1],[x2,y2],[x2+w2, y2+h2]]]))
              #cv2.rectangle(img,(openx,openy),(openx+openw,openy+openh),(255,0,0),2)

              
       elif (len(conts)==1):
              x,y,w,h = cv2.boundingRect(conts[0])
              if (pinchFlag == 0) :
                     if (abs((w*h - openw*openh)*100/(w*h))<20) :
                            pinchFlag = 1
                            mouse.press(Button.left)
                            openx,openy,openw,openh = (0,0,0,0)
              else :
                     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                     cx = x + w/2
                     cy = y + h/2
                     cv2.circle(img, (int(cx),int(cy)),int((w+h)/4),(0,0,255),2)
                     mouseLoc = mLoc0ld + ( (int(cx),int(cy)) - mLoc0ld)/DamplingFactor
                     mouse.position =  (sx-int(mouseLoc[0]*sx/camx),int(mouseLoc[1]*sy/camy))     
                     while mouse.position != (sx-int(mouseLoc[0]*sx/camx),int(mouseLoc[1]*sy/camy)) :
                                   pass
                     mLoc0ld = mouseLoc
              
       #cv2.imshow("maskClose", maskClose)
       #cv2.imshow("maskOpen", maskOpen)
       #cv2.imshow("mask", mask)
       cv2.imshow("cam", img)
       if cv2.waitKey(10) &0xFF ==ord('q'):
              cap.release()
              cv2.destroyAllWindows()
              break
       
