# import the necessary packages
import argparse
import os

import cv2
import sys

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="path to input image containing ArUCo tag")
# ap.add_argument("--folder", required=True,
#                 help="path to input images")
ap.add_argument("-t", "--type", type=str,
                default="DICT_ARUCO_ORIGINAL",
                help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

zeroes = []
ones = []
idx= 0
zeroindexes = []
oneindexes = []

def myFunc(e):
  return len(e)

lst = os.listdir("Images")
lst.sort(key=myFunc)
for image_name in lst:

    if image_name.endswith('.png'):
        # load the input image from disk and resize it
        # print("[INFO] loading image...")
        image_path = "Images/" + image_name
        print(image_path)
        # image = cv2.imread(args["image"])
        image = cv2.imread(image_path)
        # print(args["image"])
        # image = image_path
        # print(image)
        #image = imutils.resize(image, width=600)
        # verify that the supplied ArUCo tag exists and is supported by
        # OpenCV
        # if ARUCO_DICT.get(args["type"], None) is None:
        #     print("[INFO] ArUCo tag of '{}' is not supported".format(
        #         args["type"]))
        #     sys.exit(0)
        # load the ArUCo dictionary, grab the ArUCo parameters, and detect
        # the markers
        # print("[INFO] detecting '{}' tags...".format(args["type"]))
        arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
        arucoParams = cv2.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
                                                           parameters=arucoParams)
        # print(ids)
        if ids is not None:
            if (ids == [[0]]).all():
                zeroes.append(image_name)
                zeroindexes.append(idx)
            if (ids == [[1]]).all():
                ones.append(image_name)
                oneindexes.append(idx)
        idx += 1
# print(zeroes)
# print(zeroindexes)
# print(ones)
# print(oneindexes)

def longestConsecutive(s):
    # longest = 0
    # firstIdx = 0
    # lastIdx = 0
    # dummyIdx = 0
    # idx = 0
    # for i in x:
    #     if i - 1 not in x:
    #         current = i
    #         streak = 0
    #         firstIdx = idx
    #         dummyIdx = idx
    #         while i in x:
    #             i += 1
    #             dummyIdx += 1
    #             streak += 1
    #             # longest = max(longest, streak)
    #             if longest < streak:
    #                 longest = streak
    #                 lastIdx = dummyIdx
    #     idx += 1
    maxrun = -1
    rl = {}
    for x in s:
        run = rl[x] = rl.get(x - 1, 0) + 1
        print
        x - run + 1, 'to', x
        if run > maxrun:
            maxend, maxrun = x, run
    # print([maxend - maxrun + 1, maxend])
    # print(str(longest) + " longest")
    # print(str(firstIdx) + " firstIdx")
    # print(str(lastIdx) + "lastIdx")
    # print(x[firstIdx])
    # print(x[lastIdx])
    return [maxend - maxrun + 1, maxend]

rangezeroes = longestConsecutive(zeroindexes)
rangeones = longestConsecutive(oneindexes)

camera0 = (round((rangezeroes[1] - rangezeroes[0])/2)) + rangezeroes[0]
camera1 = (round((rangeones[1] - rangeones[0])/2)) + rangeones[0]

print("")
print("first Camera: frame" + str(camera0) + ".png")
print("second Camera: frame" + str(camera1) + ".png")

# print((ids == [[0]]).all())

# # verify *at least* one ArUco marker was detected
# if len(corners) > 0:
#     # flatten the ArUco IDs list
#     ids = ids.flatten()
#     # loop over the detected ArUCo corners
#     for (markerCorner, markerID) in zip(corners, ids):
#         # extract the marker corners (which are always returned in
#         # top-left, top-right, bottom-right, and bottom-left order)
#         corners = markerCorner.reshape((4, 2))
#         (topLeft, topRight, bottomRight, bottomLeft) = corners
#         # convert each of the (x, y)-coordinate pairs to integers
#         topRight = (int(topRight[0]), int(topRight[1]))
#         bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
#         bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
#         topLeft = (int(topLeft[0]), int(topLeft[1]))
#
#         # draw the bounding box of the ArUCo detection
#         cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
#         cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
#         cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
#         cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
#         # compute and draw the center (x, y)-coordinates of the ArUco
#         # marker
#         cX = int((topLeft[0] + bottomRight[0]) / 2.0)
#         cY = int((topLeft[1] + bottomRight[1]) / 2.0)
#         cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
#         # draw the ArUco marker ID on the image
#         cv2.putText(image, str(markerID),
#                     (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5, (0, 255, 0), 2)
#         print("[INFO] ArUco marker ID: {}".format(markerID))
#         # show the output image
#         cv2.imshow("Image", image)
#         cv2.waitKey(0)
#         #python detect_aruco_image.py --image Room_9/frame234.png --type DICT_4X4_250

