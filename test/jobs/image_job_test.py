import sys
sys.path.append('src')

import unittest
import numpy as np

from jobs.image_job import ImageJob
from jobs.image_job import GreyscaleImageJob
from calibration import Calibration

from toolkit.toolkit import FileTools
from toolkit.toolkit import ImageTools

#from toolkit.toolkit import readImage
#from toolkit.toolkit import writeImage
#from toolkit.toolkit import showImage
#from toolkit.toolkit import concatenatePaths
#from toolkit.toolkit import meanSquaredErrorBetweenImages

class TestImageJob(unittest.TestCase):

    def testExecute(self):
        imageJob = ImageJob()
        imageJob.execute()

    def testAddParameter(self):
        imageJob = ImageJob()
        imageJob.addParameter("testParam", 100, 255)
        self.assertIsNotNone(imageJob.parameters["testParam"])

class TestGreyscaleImageJob(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.imagesFolder = "test-resources/image_series"
        self.targetImageFolder = "test-resources/expected_images"
        self.imageFileName = "test"
        self.imageExtension = ".jpg"
        self.outImageExtension = ".png"

    def testCreate(self):
        greyscaleImageJob = GreyscaleImageJob(self.imagesFolder, self.imageFileName, self.imageExtension, Calibration())

    def testExecute(self):
        greyscaleImageJob = GreyscaleImageJob(self.imagesFolder, self.imageFileName, self.imageExtension, Calibration())
        image = greyscaleImageJob.execute()
        self.assertIsNotNone(image)

    def testExecuteWithAllColorChannels(self):
        greyscaleImageJob = GreyscaleImageJob(self.imagesFolder, self.imageFileName, self.imageExtension, Calibration())
        for i in range(6):
            greyscaleImageJob.parameters["cch"].value = i
            image = greyscaleImageJob.execute()
            expectedImagePath = FileTools.concatenatePaths(self.targetImageFolder, self.imageFileName + "_" + str(i) + self.outImageExtension)
            expectedImage = ImageTools.readImage(expectedImagePath)
            self.assertTrue(np.array_equal(expectedImage, image))

if __name__ == '__main__':
    unittest.main()
