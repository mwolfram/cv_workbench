import cv2
import numpy as np

from toolkit.color import ColorTools
from toolkit.toolkit import FileTools
from detector import sliding_window
from jobs.parameter import Parameter
from transformation import perspective_transform
from toolkit.draw import draw_lane_undistorted
from toolkit.draw import concatenate_4_images


class ImageJob():

    def __init__(self):
        self.parameters = dict()

    def execute(self):
        pass

    def addParameter(self, name, value, maximum):
        self.parameters[name] = Parameter(name, value, maximum)


class GreyscaleImageJob(ImageJob):

    def __init__(self, imagesFolder, imageFileName, imageExtension, calibration):
        super(GreyscaleImageJob, self).__init__()
        self.imagesFolder = imagesFolder
        self.imageFileName = imageFileName
        self.imageExtension = imageExtension
        self.calibration = calibration
        self.initParameters()

    def initParameters(self):
        self.addParameter("videopos", 0, 1000)
        self.addParameter("minth", 179, 255)
        self.addParameter("maxth", 222, 255)
        self.addParameter("cch", 3, 5)

    def execute(self):
        videopos = self.parameters["videopos"].value
        minth = self.parameters["minth"].value
        maxth = self.parameters["maxth"].value
        cch = self.parameters["cch"].value

        imagePath = FileTools.concatenatePaths(self.imagesFolder, self.imageFileName)
        imagePath = imagePath + "_" + str(videopos) + self.imageExtension
        image = cv2.imread(imagePath)
        image = self.calibration.undistort(image)

        if cch is 0:
            gray = ColorTools.H(image)
        if cch is 1:
            gray = ColorTools.L(image)
        if cch is 2:
            gray = ColorTools.S(image)
        if cch is 3:
            gray = ColorTools.Y(image)
        if cch is 4:
            gray = ColorTools.U(image)
        if cch is 5:
            gray = ColorTools.V(image)

        transformed = perspective_transform(gray)

        binary = np.zeros_like(transformed)
        binary[(transformed >= minth) & (transformed <= maxth)] = 1
        #normalized_binary = 255 * binary

        detected_lines, left_fit, right_fit = sliding_window(binary)

        image_with_lanes = draw_lane_undistorted(image, left_fit, right_fit)

        return concatenate_4_images(image_with_lanes, detected_lines, image_with_lanes, detected_lines)

        #return image_with_lanes
