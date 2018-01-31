import cv2
import numpy as np
import argparse
#camera_port = 0
#ramp_up = 30
#camera = cv2.VideoCapture(camera_port)

pic = cv2.imread("C:/Users/Hussie Bae/Desktop/pictures/pic7Realtest.jpg")
im = cv2.imread("C:/Users/Hussie Bae/Desktop/pictures/pic7Realtest.jpg", 0)
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)













#def get_image():
#    return camera.read()[1]


#for i in range(ramp_up):
 #   temp = get_image()


print("Getting picture")
#take_pic = get_image()
#cv2.imwrite(r"C:/Users/suna/Desktop/Image Practice/Pic/test_pic.png", take_pic)
#test = cv2.imread(r"C:/Users/suna/Desktop/Image Practice/testimages/pic1.jpg", 0)
let = cv2.namedWindow('eh', cv2.WINDOW_NORMAL)
pic = cv2.imread("C:/Users/Hussie Bae/Desktop/pictures/pic7Realtest.jpg")
gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 50, 120, 3)
##cv2.imshow('eh', edged)
##cv2.waitKey(0)
##cv2.destroyAllWindows()

img1 = cv2.convertScaleAbs(edged)


shapes, _, n = cv2.findContours(img1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


while(True):
    for j in _:
        perimeter = .1*cv2.arcLength(j, True)
        approximation = cv2.approxPolyDP(j, perimeter*.1, True)

        if len(approximation) >=3 and len(approximation) <= 10:
            (x, y, w, h) = cv2.boundingRect(approximation)
            aspect = w/float(h)
            area = cv2.contourArea(j)
            areaHull = cv2.contourArea(cv2.convexHull(j))
            solid = area/float(areaHull)

            if w > 3 and h > 3 and solid > .3 and aspect >= .2 and aspect <= 3.9:
                b = 3
                cv2.drawContours(pic, [approximation], -1, (0, 0, 255), 4)
                weDidIt = "We found us a shape"

                M = cv2.moments(approximation)
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                cv2.line(pic, (startX, cY), (endX, cY), (0, 0, 155), 3)
                cv2.line(pic, (cX, startY), (cX, endY), (0, 0, 155), 3)
                cv2.putText(pic, str(b), (startX, cY), cv2.FONT_HERSHEY_TRIPLEX, .75, (0, 0, 93), 2)

    # draw the status text on the frame
                cv2.putText(pic, weDidIt, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # show the frame and record if a key is pressed
    print("did we get down here?")
    cv2.imshow("eh", pic)
    key = cv2.waitKey(1) & 0xFF


    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
#del camera