import sys
import cv2
import numpy as np
import time
import imutils

def find_Circles(frame, mask):

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    #Only proceed if at least one contour was found
    if len(contours) > 0:
        # Find the largest contours in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        C = max(contours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(C)
        M = cv2.moments(C)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius is greater than a minimum value
        if radius > 10:
            # draw the circle and centroid on the frame
            # then update the list of trated points
           cv2.circle(frame, int(x), int(y), int(radius), (0, 255, 255), 2)
           cv2.circle(frame, center, 5, (0,0,0), -1)

    return center

