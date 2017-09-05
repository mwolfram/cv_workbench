#!/usr/bin/python

from calibration import Calibration
import glob
import pickle
from adjust import Adjust
from jobs.image_job import GreyscaleImageJob
from jobs.image_job import TrafficLightsImageJob
import cv2
from video import Video

# Calibrate
def calibrate():
    images = glob.glob('resources/calibration/set2/selected/*.jpg')
    calibration = Calibration()
    calibration.calibrate(9, 7, images)
    outfile = open('resources/calibration/set2_calibrated.pkl', 'wb')
    pickle.dump(calibration, outfile)
    outfile.close()

def useAdjust():
    calibrationFile = open('resources/calibration/set2_calibrated.pkl', 'rb')
    calibration = pickle.load(calibrationFile)
    adjust = Adjust(GreyscaleImageJob("resources/hart1","hart1",".jpg",calibration))

def trafficLights():
    adjust = Adjust(TrafficLightsImageJob("resources/red","left0",".jpg"))

trafficLights()
#calibrate()


def doAdjustJob():
    outfile = open('resources/calibration/set2_calibrated.pkl', 'rb')
    calibrate = pickle.load(outfile)
    outfile.close()
    image = cv2.imread("./resources/test_images/straight_lines_hart.png")
    #image = cv2.imread("./resources/calibration/set2/selected/calibration_0.jpg")
    undistorted = calibrate.undistort(image)
    cv2.imshow("img", undistorted)
    adjust = Adjust(GreyscaleImageJob(undistorted))
    #cv2.waitKey(10000)

def videoTest():
    video = Video("resources/videos/hart1.mp4")
    video.videoToImages("resources/hart1")

#videoTest()
