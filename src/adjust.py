import cv2

class TrackbarWrapper():

    def __init__(self, parameter, windowName, notificationFunction):
        self.parameter = parameter
        self.notificationFunction = notificationFunction
        cv2.createTrackbar(parameter.name, windowName, parameter.value, parameter.maximum, self.valueChanged)

    def valueChanged(self, value):
        self.parameter.value = value
        self.notificationFunction()


class Adjust():

    def __init__(self, job, windowName="Adjust"):
        self.job = job
        self.trackbarWrappers = []
        self.windowName = windowName
        self.createWindow()
        self.updateWindow()
        self.waitOnWindow()

    def waitOnWindow(self):
        while cv2.getWindowProperty(self.windowName, 0) >= 0:
            keyCode = cv2.waitKey(1000)

    def createWindow(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        for key, parameter in self.job.parameters.items():
            self.trackbarWrappers.append(TrackbarWrapper(parameter, self.windowName, self.updateWindow))

    def updateWindow(self):
        cv2.imshow(self.windowName, self.job.execute())
