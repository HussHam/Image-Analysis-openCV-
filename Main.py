import cv2
import numpy as np
from PicFeed import PicFeed

# Main method for testing the program, last tested with gopro footage from a test flight of my teams UAV

test = PicFeed()
cap = cv2.VideoCapture("E:/droneclub/ID/Input/test.mp4")
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




# How the code was being ran beforehand when using single images as test data
# Not shown: the actual loading in and creation of test object with singular picture
'''
print("below ID")
test.saveCropsCont("F:/droneclub/IDAlpha/Output/YCrCb")
print("below cont")
test.saveCropsMser("F:/droneclub/IDAlpha/Output/MSER")
print("below mser")
test.saveCropsEdge("F:/droneclub/IDAlpha/Output/Edged")
print("below edge")
'''
