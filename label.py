#%%
import numpy as np 
import matplotlib.pyplot as plt 
import cv2 
import copy
import pickle

#%%
vid_name = 'test.mp4'
vid_path = 'test.mp4'
img_scale = 4

cv2.namedWindow("test_image", cv2.WINDOW_KEEPRATIO)
cap = cv2.VideoCapture(vid_path)
# Create necessary global variables for working with the mouse callback
global top, bottom
global right_lane, left_lane
global click_count
click_count = 0
global img_edit
global frame_num


frame_num = 0

#%%
def set_points(event, x, y,flags, param):
    global click_count
    global img_edit
    global img_scale
    global lane_img
    global right_lane
    global left_lane
    if event == cv2.EVENT_MOUSEMOVE:
        if click_count > 1:
            if click_count in range (2,8):
                img_edit = copy.deepcopy(lane_img)
                cv2.circle(img_edit, (x, left_lane[click_count-2][1]), radius=3, thickness=3, color=(0,255,0))
            if click_count in range (8,14):
                img_edit = copy.deepcopy(lane_img)
                cv2.circle(img_edit, (x, right_lane[click_count-8][1]), radius=3, thickness=3, color=(255,0,0))
    if(event == cv2.EVENT_LBUTTONDOWN):
        if click_count == 0:
            global bottom
            bottom = img_edit.shape[0] - 50
        elif click_count == 1:
            global top
            top = y
            arr = np.geomspace(top, bottom, 6)
            for val in arr:
                val = int(val)
                left_lane.append([0, val])
                right_lane.append([0, val])
                cv2.line(img_edit, (0, val), (img_edit.shape[1], val), color=(0,0,255), thickness=2)
            lane_img = copy.deepcopy(img_edit)
        elif click_count in range (2,8):
            left_lane[click_count-2][0] = x
            cv2.circle(lane_img, (x, left_lane[click_count-2][1]), radius=3, thickness=6, color=(0,255,0))
        elif click_count in range (8,14):
            right_lane[click_count-8][0] = x
            cv2.circle(lane_img, (x, right_lane[click_count-8][1]), radius=3, thickness=3, color=(255,0,0))
        click_count+=1

def save_label(left_lane, right_lane, frame_num, vid_path, vid_name):
    global img_scale
    global cap
    cap.set(1, frame_num)

    _, img = cap.read()
    print(img.shape)
    img = cv2.resize(img, (int(img.shape[1]/img_scale), int(img.shape[0]/img_scale)))
    left_lane = np.array(left_lane)
    right_lane = np.array(right_lane)
    left_lane = left_lane/img_scale
    right_lane = right_lane/img_scale
    left_lane = left_lane.astype(int)
    right_lane = right_lane.astype(int)
    label = {
        'img': img,
        'left_lane': left_lane,
        'right_lane': right_lane
    }
    pickle.dump(label, open(f"labels/{vid_name}-{frame_num}.p", "wb"))
#%%
def label(vid_path, vid_name):
    # Use global variables
    global top, bottom
    global right_lane, left_lane
    global click_count
    global img_edit
    global frame_num
    global cap
    top, bottom = 0,0
    right_lane, left_lane = [], []
    click_count = 0


    cap.set(1, frame_num)

    # load the image
    ret,img = cap.read() 
    if not ret:
        return 0
    # Assign the img to img
    img_edit = img
    # Create window, assign callback
    cv2.setMouseCallback("test_image", set_points)
    while True:
        cv2.imshow("test_image",img_edit)
        key = cv2.waitKey(33)
        #skip desired number of frames and label next img
        if key == ord('d'):
            frame_num += 10
            break
        elif key == ord('f'):
            frame_num += 100
            break
        elif key == ord('g'):
            frame_num += 1000
            break
        elif key == ord('s'):
            break
        elif key == ord('q'):
            cv2.destroyAllWindows()
            return 0
    #   Check if image is labeled correctly, 
    if(len(right_lane) == 6 and right_lane[5][0] is not 0):
        print('saving!')
        save_label(left_lane, right_lane, frame_num, vid_path, vid_name)
    del top, bottom, right_lane, left_lane, img_edit
    label(vid_path, vid_name)

    return 0

#%%
label(vid_path, vid_name)
#%%
