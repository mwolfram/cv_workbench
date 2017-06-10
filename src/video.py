import ntpath
from moviepy.editor import VideoFileClip

from toolkit.color import convert_from_RGB
from toolkit.toolkit import concatenatePaths
from toolkit.toolkit import writeImage

class Video():

    def __init__(self, pathToVideo):
        self.pathToVideo = pathToVideo
        self.videoClip = VideoFileClip(self.pathToVideo)

    def videoToImages(self, targetFolder):
        counter = 0

        # get filename without extension
        videoFileName = ntpath.basename(self.pathToVideo)
        videoFileName = os.path.splitext(videoFileName)[0]

        # concatenate to get target path and filename
        targetPath = concatenatePaths(targetFolder, videoFileName)

        # iterate over all frames and write them to file with the frame number in the filename
        for frame in self.videoClip.iter_frames():
            writeImage(targetPath + "_" + str(counter) + ".jpg", convert_from_RGB(frame, "BGR"))
            counter = counter + 1

    def getFrame(self, frameNumber):
        currentFrame = 0
        for frame in self.videoClip.iter_frames():
            if currentFrame is frameNumber:
                return frame
            currentFrame = currentFrame + 1
        return None

    def getNumberOfFrames(self):
        currentFrame = 0
        for frame in self.videoClip.iter_frames():
            currentFrame = currentFrame + 1
        return currentFrame
