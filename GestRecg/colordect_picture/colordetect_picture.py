import cv2
import numpy as np
 
 
while(True):
 
    # 读取一帧
    frame = cv2.imread("picture1.jpg")
 
    # 把 BGR 转为 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # HSV中黑色范围
    lower_black = np.array([0,0,0]) 
    upper_black = np.array([180,255,46])
    # 把 BGR 转为 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # HSV中黑色范围
    lower_black = np.array([0,0,0]) 
    upper_black = np.array([180,255,45])
    lower_blue = np.array([100,43,46]) 
    upper_blue = np.array([124,255,255]) 
 
    # 获得黑色区域的mask
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
 
    # 和原始图片进行and操作，获得黑色区域
    res = cv2.bitwise_and(frame,frame, mask = mask_black)
    res2 = cv2.bitwise_and(frame,frame, mask = mask_blue)
 
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',frame)
    cv2.namedWindow('mask_black', cv2.WINDOW_NORMAL)
    cv2.imshow('mask_black',mask_black)
    cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    cv2.imshow('res',res)
    cv2.namedWindow('mask_blue', cv2.WINDOW_NORMAL)
    cv2.imshow('mask_blue',mask_blue)
    cv2.namedWindow('res2', cv2.WINDOW_NORMAL)
    cv2.imshow('res2',res2)
 
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
cv2.destroyAllWindows()


