import cv2
import numpy as np

# Class for storing information about potential targets in an object
# cenX and cenY are the location of the center pixel of a target from the original image (tuples storing array location)
# img is a crop around the target
# spot is a identifier for the individual targets (1 would be the first target outputted, 2 is the 2nd ect.)
# get img simply returns the image
class Target:
    def __init__(self, cenX, cenY, img, spot):
        self.cenX = cenX
        self.cenY = cenY
        self.img = img
        self.spot = spot

    def getImg(self):
        return self.img

class ParentAnalysisMethods:

    # Parent Class for image analysis child class
    # Contains method for reading in images, filtering them, and finding unique shapes/targets within the image
    # Worked on by Hussein Hamdan
    # Uploaded 3/10/2018
    # Last worked on 6/30/2018

    # constants for calculations

    MIN_TARG_VAL = 1
    CHROM_RED_KTHRESH = 1.8
    CHROM_BLUE_KTHRESH = 1.8
    Y_KTHRESH = 1.1

    # Getter methods for constants used in calculations

    @staticmethod
    def getYK():
        return ParentAnalysisMethods.Y_KTHRESH

    @staticmethod
    def getMinTarg():
        return ParentAnalysisMethods.MIN_TARG_VAL

    @staticmethod
    def getBlueK():
        return ParentAnalysisMethods.CHROM_BLUE_KTHRESH

    @staticmethod
    def getRedK():
        return ParentAnalysisMethods.CHROM_RED_KTHRESH
    # Simple method for reading in images using openCv2 imRead
    # Parameter: file path fed in as a string, leading to a valid image file
    # Post-condition: Returns read in image as a openCV2 object (I think, it might be an numpy array)

    @staticmethod
    def imgIn(filepath):
        image = cv2.imread(filepath)
        return image

    # Method for creating an edgeMap out of an image, change values as needed depending on pic quality/camera used
    # Parameter: valid image passed in, preferably in color since I covert it to gray before creating the edge map
    # Post-condition: Returns edge map of original image

    @staticmethod
    def edgeMap(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gaussblur = cv2.GaussianBlur(gray, (7,7), 0)
        edged = cv2.Canny(gaussblur, 50, 120, 3)
        return edged

    # Simple method that coverts read in img from BGR 2 YCrCb
    # Parameter: BGR image passed in, as a numpy array
    # Post-condition : Returns the image as a Y Cr Cb picture/numpy array

    @staticmethod
    def toChrom(img):
        img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        return img_YCrCb

    # Method that takes in a YCrCb image and returns the Y thresholded image -> Shittiest working method! Testing only
    # [:,:,*] replacing with the * with a # 0-2 returns the corresponding Y Cr Cb layer (0 is Y, 1 is Cr, 2 is Cb)
    # Right now it is using the Y layer to do the chinese algorhthim
    # calculates min max and mean, and thresholds image
    # Parameter: image converted to YCrCb color space
    # Post-condition: returns a thresholded image of the y layer

    @staticmethod
    def yThresh(target):
        Y_channel = target[:, :, 0]
        avgLum = Y_channel.mean()
        maxLum = Y_channel.max()
        minLum = Y_channel.min()

        if(maxLum - avgLum) > 1:
            threshResultY = cv2.inRange(Y_channel, avgLum, 255)
            resultY = threshResultY
        else:
            print("Image cannot accurately be processed via Y analysis \n")
            print("Try lowering val of if statement or use a photo with more contrast \n")
            resultY = None;
        return resultY

    # Gathers the chrominance value from a YCrCb image and uses the info to thresh hold the image
    # currently uses the Cr layer
    # Parameter: A BGR image/numpy array, I handle converting to YCrCb in the method
    # Post-condition: Returns a thresholded image array, index 0 is Cb, index 1 is Cr

    @staticmethod
    def chromThresh(target):
        cr_channel = target[:, :, 1]
        maxCr = cr_channel.max()
        minCr = cr_channel.min()
        avgCr = cr_channel.mean()

        if(maxCr - avgCr) >ParentAnalysisMethods.getMinTarg():
            threshCr = maxCr-(maxCr - avgCr) * ParentAnalysisMethods.getRedK()
            threshedResultCr = cv2.inRange(cr_channel, threshCr, 255)
        else:
            print("Image cannot be accurately processed via Cr analysis \n")
            print("Try lowering MIN_TARG_VAL or using a less noisy photo \n")
            return None

        if(avgCr - minCr) > ParentAnalysisMethods.getMinTarg():
            threshCb = ((avgCr - minCr)*ParentAnalysisMethods.getBlueK()) + minCr
            threshedResultCb = cv2.inRange(cr_channel, threshCb, 255)
        else:
            print("Image cannot be accurately processed via Cb analysis \n")
            print("Try lowering MIN_TARG_VAL or using a less noisy photo \n")
            return None

        threshedResult = list()
        threshedResult.append(threshedResultCb)
        threshedResult.append(threshedResultCr)
        return threshedResult

    # feed in array of binarized/threshholded images and the original and this will find points of interest
    # and return an Target object containing the center points and a cropped img/numpy array around the target
    # Parameters: Array of binarized/thresholded images, original image that the threshold ones are based off of
    # Post condition: List of target objects containing center points of points of interest and image/np array cropped
    # around the point of interest from the original

    @staticmethod
    def contourId(arrayOfImg, ogImg):
        result = []
        i = 0
        for img in arrayOfImg:
            trashImg, countour, hier = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for count in countour:
                area = cv2.contourArea(count)
                perimeter = cv2.arcLength(count, True)
                aprox = cv2.approxPolyDP(count, perimeter*.1, True)
                (x, y, w, h) = cv2.boundingRect(aprox)
                if area < img.size/1000 and area > 350 and h > 50:
                    moment = cv2.moments(count)
                    cx = int(moment['m10']/moment['m00'])
                    cy = int(moment['m01']/moment['m00'])
                    amtY = int(cy/2)
                    amtX = int(cx/2)
                    ny = cy - amtY
                    nx = cx - amtX
                    crop = ogImg[ny:ny+(amtY*2), nx:nx+(amtX*2)]
                    id = Target(cx, cy, crop, i)
                    i += 1
                    result.append(id)
        return result
    # Feed in a gray scale image, and the MSER algorhtihim will look for a target.
    # Parameters: Array of grey scale images, threshed may work but is more finicky and prone to errors, original image
    # Post condition: Returns a list of target objects, containing center point of target and original image cropped
    # around it.

    @staticmethod
    def detectionMSER(arrayOfImg, ogImg):
        result = []
        i = 0
        mser = cv2.MSER_create()
        for img in arrayOfImg:
            hit, other = mser.detectRegions(img)
            for cnt in hit:
                area = cv2.contourArea(cnt)
                if area < img.size / 1000 and area > 350:
                    moment = cv2.moments(cnt)
                    cx = int(moment['m10'] / moment['m00'])
                    cy = int(moment['m01'] / moment['m00'])
                    amtY = int(cy / 2)
                    amtX = int(cx / 2)
                    ny = cy - amtY
                    nx = cx - amtX
                    crop = ogImg[ny:ny + (amtY * 2), nx:nx + (amtX * 2)]
                    id = Target(cx, cy, crop, i)
                    result.append(id)
                    i += 1
        return result


















