import ntpath
from moviepy.editor import VideoFileClip

from toolkit.color import ColorTools
from toolkit.toolkit import FileTools
from toolkit.toolkit import ImageTools

class Video():

    def __init__(self, pathToVideo):
        self.pathToVideo = pathToVideo
        self.videoClip = VideoFileClip(self.pathToVideo)

    def videoToImages(self, targetFolder):
        counter = 0

        # get filename without extension
        videoFileName = ntpath.basename(self.pathToVideo)
        # TODO these go to tools
        videoFileName = os.path.splitext(videoFileName)[0]

        # concatenate to get target path and filename
        targetPath = FileTools.concatenatePaths(targetFolder, videoFileName)

        # iterate over all frames and write them to file with the frame number in the filename
        for frame in self.videoClip.iter_frames():
            ImageTools.writeImage(targetPath + "_" + str(counter) + ".jpg", ColorTools.convert_from_RGB(frame, "BGR"))
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
