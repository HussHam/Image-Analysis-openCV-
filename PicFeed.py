import cv2
import numpy as np
from NoiseReduction import ParentAnalysisMethods
# Wrapper class for Parent Analysis Methods
class PicFeed(ParentAnalysisMethods):

    # pic is the original image
    # forDispCont is displaying images created using contouring methods
    # forDisMser is a collection of images found via the mser nethod
    # firDispEdge is a collection of iamages created via edge mapping
    # YCrCb is the image converted to the YCrCb color space
    # threshImgs is a collection of thresholded images of the original image (potentially in different color spaces)
    # edgedMap is a edge map of the original image
    # grayImg is the image in black and white

    def __init__(self):
        self.pic = None
        self.forDispCont = []
        self.forDispMser = []
        self.forDispEdge = []
        self.YCrCb = None
        self.threshImgs = []
        self.edgedMap = None
        self.grayImg = []

    # creates new instance of the picfeed object
    # reads in image and converts it to YCrCb
    # Parameter: path to image location
    # Post-Condition: Image is read in, and converted to YCrCb

    def create(self, path):
        self.pic = ParentAnalysisMethods.imgIn(path)
        self.YCrCb = ParentAnalysisMethods.toChrom(self.pic)

    # Second createPic method
    # This one is for testing different methods and stuff
    # I had it set up for a while to test raw images, do what you may with this one

    def createPic(self, picIn):
        self.pic = picIn
        self.YCrCb = ParentAnalysisMethods.toChrom(self.pic)

    # Method that takes in image and YCrCb version
    # Parameter: none call it in on a object
    # Post-Condition: Saves thresholded images, edge map, y threshold, and gray scale image

    def filterNoise(self):
        arrCbCr = ParentAnalysisMethods.chromThresh(self.YCrCb)
        self.threshImgs.append(arrCbCr[0])
        self.threshImgs.append(arrCbCr[1])
        self.threshImgs.append(ParentAnalysisMethods.yThresh(self.YCrCb))
        self.edgedMap = ParentAnalysisMethods.edgeMap(self.pic)
        self.grayImg.append((cv2.cvtColor(self.pic, cv2.COLOR_BGR2GRAY)))

    # Method for finding targets
    # Parameter: none call it on an instance of this class
    # post-condition: targets are found using the different methods and saved object

    def getCountourID(self):
        result = ParentAnalysisMethods.contourId(self.threshImgs, self.pic)

        for crops in result:
                self.forDispCont.append(crops)
        result = ParentAnalysisMethods.detectionMSER(self.grayImg, self.pic)

        for crops in result:
            self.forDispMser.append(crops)

        result = ParentAnalysisMethods.contourId(self.edgedMap, self.pic)

        if(result != None):
            for crops in result:
                self.forDispEdge.append(crops)
        return True

    # Method saves targets to file
    # Parameter: Path you wish to save file too
    # Post-Condition: Saves file

    def saveCropsCont(self, path):
        i = 0
        print(str(len(self.forDispCont)) + " Cont ID's")
        for img in self.forDispCont:
            cv2.imwrite(path + "./res" + str(i) + ".png", img.getImg())
            i += 1

    def saveCropsMser(self, path):
        i = 0
        print(str(len(self.forDispMser)) + " Mser ID's")
        for img in self.forDispMser:
            cv2.imwrite(path + "./res" + str(i) + ".png", img.getImg())
            i += 1

    def saveCropsEdge(self, path):
        i = 0
        print(str(len(self.forDispEdge)) + " Edge ID's")
        for img in self.forDispEdge:
            cv2.imwrite(path + "./res" + str(i) + ".png", img.getImg())
            i += 1


