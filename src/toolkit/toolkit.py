import cv2
import os.path

def concatenatePaths(path1, path2):
    return os.path.join(path1, path2)

def readImage(path):
    return cv2.imread(path)

def writeImage(path, image):
    cv2.imwrite(path, image)

def showImage(image, name="Image"):
    cv2.imshow(name, image)
