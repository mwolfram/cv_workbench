import cv2
import numpy as np

from toolkit.color import ColorTools
from toolkit.toolkit import FileTools
from toolkit.detector import DetectorTools
from jobs.parameter import Parameter
from transformation import perspective_transform

from toolkit.draw import DrawTools
#from toolkit.draw import draw_lane_undistorted
#from toolkit.draw import concatenate_4_images


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

        detected_lines, left_fit, right_fit = DetectorTools.sliding_window(binary)

        image_with_lanes = DrawTools.draw_lane_undistorted(image, left_fit, right_fit)

        return DrawTools.concatenate_4_images(image_with_lanes, detected_lines, image_with_lanes, detected_lines)

        #return image_with_lanes

class TrafficLightsImageJob(ImageJob):

    def __init__(self, imagesFolder, imageFileName, imageExtension, calibration=None):
        super(TrafficLightsImageJob, self).__init__()
        self.imagesFolder = imagesFolder
        self.imageFileName = imageFileName
        self.imageExtension = imageExtension
        self.calibration = calibration
        self.initParameters()

    def initParameters(self):
        self.addParameter("img_number", 357, 500)
        self.addParameter("hue_lo", 26, 255)
        self.addParameter("hue_hi", 35, 255)
        self.addParameter("lum_lo", 0, 1000)
        self.addParameter("lum_hi", 1000, 1000)
        self.addParameter("cch", 5, 5)

    def execute(self):
        img_number = self.parameters["img_number"].value
        hue_lo = self.parameters["hue_lo"].value
        hue_hi = self.parameters["hue_hi"].value
        lum_lo = self.parameters["lum_lo"].value
        lum_hi = self.parameters["lum_hi"].value
        cch = self.parameters["cch"].value

        imagePath = FileTools.concatenatePaths(self.imagesFolder, self.imageFileName)
        imagePath = imagePath + str(img_number) + self.imageExtension
        image = cv2.imread(imagePath)

        if self.calibration is not None:
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

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        luminosity = hsv[:,:,2]
        hue = hsv[:,:,0]

        output = image.copy()

        # detect circles in the image
        # int method, double dp, double minDist, double param1=100, double param2=100, int minRadius=0, int maxRadius=0
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=30, param2=20, minRadius=5, maxRadius=30) # TODO adjustable

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                if (luminosity[y,x]<lum_hi and luminosity[y,x]>lum_lo):
                    if (hue[y,x]<hue_hi and hue[y,x]>hue_lo):
                        cv2.circle(output, (x, y), r, (255, 0, 0), 3)

        return output
