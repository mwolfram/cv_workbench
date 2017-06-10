import sys
sys.path.append('src')

import unittest
from adjust import TrackbarWrapper
from jobs.parameter import Parameter

class TestTrackbarWrapper(unittest.TestCase):

    def notificationFunction(self):
        self.notificationFunctionCalled = True

    def testCreate(self):
        parameter = Parameter("testParam", 100, 255)
        trackbarWrapper = TrackbarWrapper(parameter, "windowName", self.notificationFunction)

    def testValueChanged(self):
        parameter = Parameter("testParam", 100, 255)
        self.notificationFunctionCalled = False
        trackbarWrapper = TrackbarWrapper(parameter, "windowName", self.notificationFunction)
        self.assertFalse(self.notificationFunctionCalled)
        trackbarWrapper.valueChanged(200)
        self.assertTrue(self.notificationFunctionCalled)


if __name__ == '__main__':
    unittest.main()
