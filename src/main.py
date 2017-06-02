#!/usr/bin/python

from calibration import Calibration
import glob
import pickle
from adjust import Adjust
from jobs.image_job import GreyscaleImageJob
import cv2

# Calibrate
#images = glob.glob('resources/calibration/set2/*.jpg')
#calibration = Calibration()
#calibration.calibrate(9, 7, images)
#outfile = open('resources/calibration/set2_calibrated.pkl', 'wb')
#pickle.dump(calibration, outfile)

def useAdjust():
    image = cv2.imread("./resources/test_images/straight_lines_hart.png")
    adjust = Adjust(GreyscaleImageJob(image))

useAdjust()
