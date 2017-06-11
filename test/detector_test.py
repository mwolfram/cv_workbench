import sys
sys.path.append('src')

import unittest
import numpy as np
import pickle

from detector import sliding_window
from detector import detect_from_previous

from toolkit.toolkit import FileTools
from toolkit.toolkit import ImageTools
from toolkit.toolkit import SerializationTools

from toolkit.color import ColorTools
from transformation import perspective_transform

class TestDetector(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.imagesFolder = "test-resources/image_series"
        self.expectedPickleData = "test-resources/expected_pickle_data"
        self.imageFileName = "test_0.jpg"

    def getBinaryTransformedImage(self, image):
        gray = ColorTools.Y(image)
        transformed = perspective_transform(gray)
        binary = np.zeros_like(transformed)
        binary[(transformed >= 150) & (transformed <= 250)] = 1
        return binary

    def testSlidingWindow(self):
        image = ImageTools.readImage(FileTools.concatenatePaths(self.imagesFolder, self.imageFileName))
        binary = self.getBinaryTransformedImage(image)
        detected_lines, left_fit, right_fit = sliding_window(binary)
        (exp_detected_lines, exp_left_fit, exp_right_fit) = SerializationTools.pickleLoadFromPath(FileTools.concatenatePaths(self.expectedPickleData, "sliding_window_result.pkl"))
        self.assertTrue(np.array_equal(exp_detected_lines, detected_lines))

    def testDetectFromPrevious(self):
        image = ImageTools.readImage(FileTools.concatenatePaths(self.imagesFolder, self.imageFileName))
        binary = self.getBinaryTransformedImage(image)
        (detected_lines, left_fit, right_fit) = SerializationTools.pickleLoadFromPath(FileTools.concatenatePaths(self.expectedPickleData, "sliding_window_result.pkl"))
        detect_from_previous(binary, left_fit, right_fit)

        # TODO assert

if __name__ == '__main__':
    unittest.main()
