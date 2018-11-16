import cv2
import numpy as np
from PicFeed import PicFeed

test = PicFeed()
cap = cv2.VideoCapture("E:/droneclub/NeuralIDAlpha/Input/test.mp4")
(grab, frame) = cap.read()
test.createPic(frame)

while True:
    (grab, frame) = cap.read()
    test.createPic(frame)

    if not grab:
        break
    test.getCountourID()

test.saveCropsMser("E:/droneclub/NeuralIDAlpha/Output/MSER")
test.saveCropsCont("F:/droneclub/NeuralIDAlpha/Output/YCrCb")





'''
print("below ID")
test.saveCropsCont("F:/droneclub/NeuralIDAlpha/Output/YCrCb")
print("below cont")
test.saveCropsMser("F:/droneclub/NeuralIDAlpha/Output/MSER")
print("below mser")
test.saveCropsEdge("F:/droneclub/NeuralIDAlpha/Output/Edged")
print("below edge")
'''