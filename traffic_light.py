import cv2
import numpy as np
import argparse
from opencv_traffic_light import file_read as fr
from matplotlib.patches import YAArrow

cap = cv2.VideoCapture(fr.resource)
# 프레임 넓이, 높이
width = int(cap.get(3) / 3)
height = int(cap.get(4) / 3)

num = 1
detect = 0
x = 0
y = 0
w = 0
h = 0
W=0
H=0
# 감지되었을 때의 좌표
detect_x = 0
detect_y = 0
detect_w = 0
detect_h = 0

X_light=1000
Y_light=1000
W_light =0
H_light=0
# COLOR_MIN_RED = np.array([161, 155, 84], np.uint8)
# COLOR_MAX_RED = np.array([179, 255, 255], np.uint8)

COLOR_MIN_RED = np.array([170, 120, 70], np.uint8)
COLOR_MAX_RED = np.array([180, 255, 255], np.uint8)

COLOR_MIN_BLUE = np.array([94, 80, 2], np.uint8)
COLOR_MAX_BLUE = np.array([126, 255, 255], np.uint8)

COLOR_MIN_GREEN = np.array([25, 52, 72], np.uint8)
COLOR_MAX_GREEN = np.array([102, 255, 255], np.uint8)

COLOR_MIN_YELLOW = np.array([20, 100, 100], np.uint8)
COLOR_MAX_YELLOW = np.array([30, 255, 255], np.uint8)

chk2 = 0


flag=1

while (cap.isOpened()):
    _, frame = cap.read()
    if frame is None:
        break

    # 영상 높이를 1/3로 조절
    W = cap.get(3)
    H = cap.get(4)

    # _, frame = cap.read()
    if frame is None:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    frame_threshed = cv2.inRange(hsv_frame, COLOR_MIN_RED, COLOR_MAX_RED)


    ret, thresh = cv2.threshold(frame_threshed, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    if chk2<300: #check the video about 3secs to find red light
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 3 and h > 3:
                detect_x = x
                detect_y = y
                detect_w = w
                detect_h = h
                if detect_y < Y_light: #find the red light , if it is red light location of the light is the smallest
                    X_light = detect_x
                    Y_light = detect_y
                    W_light = detect_w
                    H_light = detect_h

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                detect = 1
        chk2 +=1
    else:

    #crop_frame = frame[ (detect_y):(detect_y + detect_h) , (detect_x + detect_w):-1]
        crop_frame = frame[(Y_light):(Y_light + H_light), (X_light):X_light+int(W_light*4.3)]
        cv2.imshow("crop_frame", crop_frame)
        crop_hsv_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2HSV)
        crop_frame_threshed = cv2.inRange(crop_hsv_frame, COLOR_MIN_GREEN, COLOR_MAX_GREEN)

        crop_ret, crop_thresh = cv2.threshold(crop_frame_threshed, 127, 255, 0)
        crop_contours, crop_hierarchy = cv2.findContours(crop_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in crop_contours:
            x1, y1, w1, h1 = cv2.boundingRect(cnt)
            if w1 > 1 and h1 > 1:
                print("GREEN")
                cv2.rectangle(crop_frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                cv2.imshow("crop_frame", crop_frame)
                flag=0
                break
    if flag==0:
        break







    cv2.imshow("final", frame)

    # 빨간색 detection



    key = cv2.waitKey(1)
    if key == 27:
        break

print(X_light,Y_light)