from jobs.parameter import Parameter
import numpy as np
from color import *

class ImageJob():

    def __init__(self, image):
        self.image = image
        self.parameters = dict()

    def execute(self):
        pass

    def addParameter(self, name, value, maximum):
        self.parameters[name] = Parameter(name, value, maximum)


class GreyscaleImageJob(ImageJob):

    def __init__(self, image):
        super(GreyscaleImageJob, self).__init__(image)
        self.initParameters()

    def initParameters(self):
        self.addParameter("minth", 120, 255)
        self.addParameter("maxth", 160, 255)
        self.addParameter("cch", 0, 5)

    def execute(self):
        minth = self.parameters["minth"].value
        maxth = self.parameters["maxth"].value
        cch = self.parameters["cch"].value

        if cch is 0:
            gray = H(self.image)
        if cch is 1:
            gray = L(self.image)
        if cch is 2:
            gray = S(self.image)
        if cch is 3:
            gray = Y(self.image)
        if cch is 4:
            gray = U(self.image)
        if cch is 5:
            gray = V(self.image)

        binary = np.zeros_like(gray)
        binary[(gray >= minth) & (gray <= maxth)] = 1
        return 255 * binary
