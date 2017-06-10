import sys
sys.path.append('src')

import unittest
from jobs.image_job import ImageJob
from jobs.image_job import GreyscaleImageJob
from calibration import Calibration

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
        self.imageFileName = "test"
        self.imageExtension = ".jpg"

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
            self.assertIsNotNone(image)

if __name__ == '__main__':
    unittest.main()
