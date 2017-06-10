import sys
sys.path.append('src')

import unittest
import pickle

from calibration import Calibration
from toolkit.toolkit import enumerateFilesWithExtension
from toolkit.toolkit import concatenatePaths
from toolkit.toolkit import readImage

class TestCalibration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.imagesFolder = "test-resources/calibration_images"
        self.extension = "jpg"

    def testCreate(self):
        calibration = Calibration()
        imageFileNames = enumerateFilesWithExtension(self.imagesFolder, self.extension)
        calibration.calibrate(9, 7, imageFileNames)
        self.assertIsNotNone(calibration.ret)
        self.assertIsNotNone(calibration.mtx)
        self.assertIsNotNone(calibration.dist)
        self.assertIsNotNone(calibration.rvecs)
        self.assertIsNotNone(calibration.tvecs)

    def testUndistort(self):
        calibration = Calibration()
        imageFileNames = enumerateFilesWithExtension(self.imagesFolder, self.extension)
        calibration.calibrate(9, 7, imageFileNames)
        undistortedImage = calibration.undistort(readImage(concatenatePaths(self.imagesFolder, "calibration_992.jpg")))

        # TODO assert

if __name__ == '__main__':
    unittest.main()
