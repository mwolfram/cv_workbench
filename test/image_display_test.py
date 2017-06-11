import sys
sys.path.append('src')

import unittest

from image_display import ImageDisplay

class TestCalibration(unittest.TestCase):

    def testCreate(self):
        imageDisplay = ImageDisplay(None, "test", "hot")
        # TODO assert


if __name__ == '__main__':
    unittest.main()
