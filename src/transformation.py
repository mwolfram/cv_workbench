import cv2
import numpy as np

# TODO move to toolkit

# TODO configuration should really come from a config file and not from code

# Configuration
#SRC_TF = np.float32([ [262.0, 680.0], [1042.0, 680.0], [701.0, 460.0], [580.0, 460.0] ]) # for assignment
SRC_TF = np.float32([ [313.0, 481.0], [764.0, 481.0], [595.0, 308.0], [506.0, 308.0] ])
DST_TF = np.float32([ [262.0, 720.0], [1042.0, 720.0], [1042.0, 0.0], [262.0, 0.0] ])

def perspective_transform(img):
    M = cv2.getPerspectiveTransform(SRC_TF, DST_TF)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    return warped

def inverse_perspective_transform(img):
    Minv = cv2.getPerspectiveTransform(DST_TF, SRC_TF)
    warped = cv2.warpPerspective(img, Minv, (img.shape[1], img.shape[0]))
    return warped
