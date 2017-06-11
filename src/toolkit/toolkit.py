import os.path
import glob
import cv2
import numpy as np
import pickle


class FileTools():

    @staticmethod
    def concatenatePaths(path1, path2):
        return os.path.join(path1, path2)

    @staticmethod
    def enumerateFiles(pattern):
        return glob.glob(pattern)

    @staticmethod
    def enumerateFilesWithExtension(folder, extension):
        return FileTools.enumerateFiles(FileTools.concatenatePaths(folder, "*." + extension))


class ImageTools():

    @staticmethod
    def readImage(path):
        return cv2.imread(path)

    @staticmethod
    def writeImage(path, image):
        cv2.imwrite(path, image)

    @staticmethod
    def showImage(image, name="Image"):
        cv2.imshow(name, image)
        cv2.waitKey(10000)

    @staticmethod
    def meanSquaredErrorBetweenImages(imageA, imageB):
    	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    	err /= float(imageA.shape[0] * imageA.shape[1])
    	return err


class SerializationTools():

    @staticmethod
    def pickleDumpToPath(path, object):
        with open(path, "wb") as file:
            pickle.dump(file=file, obj=object)

    @staticmethod
    def pickleLoadFromPath(path):
        with open(path, "rb") as file:
            return pickle.load(file)
