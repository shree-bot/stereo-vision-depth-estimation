import sys
import cv2
import numpy as np
import time

def find_depth(circle_right, circle_left, frame_right, frame_left, basline, f, alpha):

    #Convert focal length f from [mm] to [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
    else:
        print('left and right camer do not have the same pixel width')

    x_right = circle_right[0]
    x_left = circle_left[0]

    #Calculate the disparity:
    disparity = x_left-x_right[0]                     #Displacement between left and right frames [pixels]

    #Calculate Depth z:
    zDepth = (basline*f_pixel)/disparity                #depth in [cm]

    return abs(zDepth)