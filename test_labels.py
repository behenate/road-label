import numpy as np
import cv2 
import os
import copy
import pickle

labels_path = 'labels/'
labels_pahts = os.listdir(labels_path)
labels_pahts = sorted(labels_pahts)
cv2.namedWindow('test', cv2.WINDOW_KEEPRATIO)
cv2.resizeWindow('test', (1280,720))
def draw_points(img, left_lane, right_lane):
    for point in right_lane:
        cv2.circle(img, (point[0], point[1]), radius=3, thickness=3, color=(255,0,0))
    for point in left_lane:
        cv2.circle(img, (int(point[0]), int(point[1])), radius=3, thickness=3, color=(0,255,0))
    return img


for label in labels_pahts:
    if label.endswith(".p"):
        # print(label)
        label = pickle.load(open(labels_path + label, "rb"))
        img = label['img']
        left_lane = label['left_lane']
        right_lane = label['right_lane']

        # img = draw_points(img, left_lane, right_lane)
        cv2.imshow("test", img)
        key = cv2.waitKey(100)
        if key==ord('q'):
            break