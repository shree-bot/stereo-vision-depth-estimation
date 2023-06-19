import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt

#functions
import HSV_filter as hsv
import shape_recognition as shape
import triangulation as tri
#import calibration as calib

#open both cameras
cap_right= cv2.VideoCapture(3, cv2.CAP_DSHOW)
cap_left= cv2.VideoCapture(5, cv2.CAP_DSHOW)

framerate = 120  #camera frame rate (maximum at 120fps)

B = 12  #distance between the cameras [cm]
f = 6  #camera lense's focal length [mm]
alpha = 56.6  #camera field of view in the horisontal plane [degrees]

count = -1

while(True):
    count += 1

    ret_right, frame_right = cap_right.read()
    ret_left, frame_left = cap_left.read()

##################################### CALIBRATION ##################################################

    # frame_right, frame_left = calib.undistorted(frame_right, frame_left)

####################################################################################################
    #if cannot catch any frame, break
    if ret_right==False or ret_left==False:
        break
    else:
        #Applying HSV-FILTER:
        mask_right = hsv.add_HSV_filter(frame_right, 3)
        mask_left = hsv.add_HSV_filter(frame_left, 5)

        #result-frames after applying HSV-filter mask
        res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
        res_left = cv2.bitwwise_and(frame_left, frame_left, mask=mask_left)

        #applying shape recognition:
        Circles_right = shape.find_Circles(frame_right, mask_right)
        Circles_left = shape.find_Circles(frame_left, mask_left)

        #Hough Transform can be used aswell or some neural network to do object detection


         ############################### Calculating ball depth ##########################################

         # If no ball can be caught in one camera show text "Tracking Lost"
        if np.all(circles_right) == None or np.all(circles_left) == None:
             cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255), 2)
             cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255), 2)
        else:
             #FUnction to calculate depth of object. Outputs vectors of all depths in case of serval balls
             #All formulas used to find depth is in video presentaion
             depth = tri.find_depth(circles_right, circles_left, frame_right, frame_left, B, f, alpha)

             cv2.putText(frame_right, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255), 2)
             cv2.putText(frame_right, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255), 2)
             cv2.putText(frame_right, "Distance: " + str(round(depth,3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(124,252,0), 2)
             cv2.putText(frame_right, "Distance: " + str(round(depth,3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(124,252,0), 2)
             #Multiply compute value with 205.8 to get real-life depth in [cm]. The factor was found manually.
             print("Depth: ", depth)

         #show the frames
        cv2.imshow("frame right", frame_right)
        cv2.imshow("frame left", frame_left)
        cv2.imshow("mask right", mask_right)
        cv2.imshow("mask left", mask_left)

        #hit "g" to close the window
        if cv2.waitkey(1) & 0xFF == ord('q'):
            break

# release and destory all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()





