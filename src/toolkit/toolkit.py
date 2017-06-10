import cv2
import numpy as np
import os.path
import pickle

def concatenatePaths(path1, path2):
    return os.path.join(path1, path2)

def readImage(path):
    return cv2.imread(path)

def writeImage(path, image):
    cv2.imwrite(path, image)

def showImage(image, name="Image"):
    cv2.imshow(name, image)
    cv2.waitKey(10000)

def meanSquaredErrorBetweenImages(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def pickleDumpToPath(path, object):
    with open(path, "wb") as file:
        pickle.dump(file=file, obj=object)

def pickleLoadFromPath(path):
    with open(path, "rb") as file:
        return pickle.load(file)
