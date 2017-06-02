import cv2
import os
import numpy as np

class Calibration():

    def __init__(self):
        self.ret = None
        self.mtx = None
        self.dist = None
        self.rvecs = None
        self.tvecs = None

    def calibrate(self, nx, ny, images):

        objpoints = []
        imgpoints = []

        for idx, fname in enumerate(images):

            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            objp = np.zeros((nx*ny, 3), np.float32)
            objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2) # x, y coordinates

            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

            if ret is False:
                print(fname + ": DELETE")
                os.remove(fname)
            else:
                print(fname + ": keep")

            #if ret == True: # meaning that we found chessboard corners
            #    imgpoints.append(corners)
            #    objpoints.append(objp)
            #    cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
            #    cv2.imwrite("/home/mwolfram/udacity/sdcnd/cv_workbench/resources/calibration/set3")
            #    cv2.waitKey(500)

        #cv2.destroyAllWindows()

        #ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        #return ret, mtx, dist, rvecs, tvecs

    def undistort(self, image):
        return cv2.undistort(self.image, self.mtx, self.dist, None, self.mtx)
