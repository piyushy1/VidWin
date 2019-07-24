# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

import cv2
import numpy as np,sys

A = cv2.imread('1_i_frame_0.jpg')

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    cv2.imwrite("G"+str(i)+".jpg",G)
    gpA.append(G)