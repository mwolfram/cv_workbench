import numpy as np
import cv2
import glob
import math
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
from IPython.display import HTML
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

%matplotlib qt

DEFAULT_CONFIDENCE = 20
HISTORY_SIZE = 10
ksize=5
np.set_printoptions(precision=6, suppress=True)

def wAvg(val1, w1, val2, w2):
    return (val1 * w1 + val2 * w2) / 2.0

def mask(img, ml, mh):
    return cv2.inRange(img, ml, mh)

def get_histogram(binary_warped, ratio=2.0):
    histogram = np.sum(binary_warped[int(binary_warped.shape[0]/2.0):,:], axis=0)
    return histogram

def lane_offset(left_fit, right_fit, lane_img):
    lowestX_left = getLowestXPos(left_fit, lane_img)
    lowestX_right = getLowestXPos(right_fit, lane_img)
    avg = (lowestX_left + lowestX_right) / 2.0
    center = lane_img.shape[1]/2.0
    offset = avg - center
    return xToM(offset)

def xToM(x):
    xm_per_pix = 3.7/700 # meters per pixel in x dimension
    return x * xm_per_pix

def getLowestXPos(fit, img):

    # Fit new polynomials to x,y in world space
    ploty = np.linspace(0, img.shape[0]-1, img.shape[0] )

    # Generate x and y values for plotting
    fitx = fit[0]*ploty**2 + fit[1]*ploty + fit[2]

    return fitx[0]

def measure_curvature(fit, img):

    # measure curvature in pixel space
    y_eval = np.max(img.shape[0])
    px_curverad = ((1 + (2*fit[0]*y_eval + fit[1])**2)**1.5) / np.absolute(2*fit[0])

    # measure curvature in real world
    ym_per_pix = 30/720 # meters per pixel in y dimension
    xm_per_pix = 3.7/700 # meters per pixel in x dimension

    # Fit new polynomials to x,y in world space
    ploty = np.linspace(0, img.shape[0]-1, img.shape[0] )

    # Generate x and y values for plotting
    fitx = fit[0]*ploty**2 + fit[1]*ploty + fit[2]

    fit_cr = np.polyfit(ploty*ym_per_pix, fitx*xm_per_pix, 2)

    # Calculate the new radii of curvature
    world_curverad = ((1 + (2*fit_cr[0]*y_eval*ym_per_pix + fit_cr[1])**2)**1.5) / np.absolute(2*fit_cr[0])

    return px_curverad, world_curverad

def process_image_find_cspace(image):

    undistd = undist(image)
    persp = perspective_transform(undistd)

    #gradxH = abs_sobel_thresh(H(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))
    gradxL = abs_sobel_thresh(L(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))
    gradxS = abs_sobel_thresh(S(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))

    mix = np.zeros_like(gradxL)
    mix[(gradxL == 1) & (gradxS == 1)] = 1

    return concatenate_4_images(mix, Y(persp), U(persp), V(persp))

def compare_scaled(confident, candidate):
    return abs(abs(confident - candidate) / confident)

def cmp_num_to_str(num, tolerance):
    if num > tolerance:
        return '[%0.5f] ' % num
    else:
        return ' %0.5f  ' % num

def polynomials_within_tolerance(confident_fit, candidate_fit, tolerance):
    cmp0 = compare_scaled(confident_fit[0], candidate_fit[0])
    cmp1 = compare_scaled(confident_fit[1], candidate_fit[1])
    cmp2 = compare_scaled(confident_fit[2], candidate_fit[2])

    ok = cmp2 < tolerance
    return ok, cmp_num_to_str(cmp0, tolerance) + cmp_num_to_str(cmp1, tolerance) + cmp_num_to_str(cmp2, tolerance)


# Pipeline used for project_video
def process_image_video1(image):
    try:
        undistd = undist(image)
        persp = perspective_transform(undistd)

        thresholded_Y = thresh(Y(persp), thresh=(200, 255))
        thresholded_V = thresh(V(persp), thresh=(0, 100))

        #gradxH = abs_sobel_thresh(H(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))
        gradxL = abs_sobel_thresh(L(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))
        gradxS = abs_sobel_thresh(S(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))

        # AND Y and V thresholded channels
        mix_color = np.zeros_like(gradxL)
        mix_color[(thresholded_Y == 1) | (thresholded_V == 1)] = 1

        # AND L and S channels gradients in x direction
        mix_gradx = np.zeros_like(gradxL)
        mix_gradx[(gradxL == 1) & (gradxS == 1)] = 1

        # OR color channels and gradients, save as gradx for use in further pipeline
        gradx = np.zeros_like(gradxL)
        gradx[(mix_color == 1) | (mix_gradx == 1)] = 1

        #gradx = abs_sobel_thresh(L(persp), orient='x', sobel_kernel=ksize, thresh=(10, 100))

        global left_line, right_line
        left_fit = None
        right_fit = None

        if (left_line.detected and right_line.detected):
            result, left_fit, right_fit = detect_from_previous(gradx, left_line.best_fit, right_line.best_fit)

        else:
            result, left_fit, right_fit = sliding_window(gradx)
            left_line.detected = True
            right_line.detected = True

            # average best fit
            left_line.addToAverageBestFit(left_fit, result.shape)
            right_line.addToAverageBestFit(right_fit, result.shape)

        texts = []

        if left_line.detected and right_line.detected:

            left_px_curverad, left_world_curverad = measure_curvature(left_line.best_fit, gradx)
            left_line.radius_of_curvature = left_world_curverad

            right_px_curverad, right_world_curverad = measure_curvature(right_line.best_fit, gradx)
            right_line.radius_of_curvature = right_world_curverad

            left_px_cur_curverad, left_world_cur_curverad = measure_curvature(left_fit, gradx)
            right_px_cur_curverad, right_world_cur_curverad = measure_curvature(right_fit, gradx)

            #texts.append("Left / Right Cur Curverad: " + str(left_world_cur_curverad) + " | " + str(right_world_cur_curverad))
            texts.append("Left / Right Curverad: " + str(left_world_curverad) + " m   |   " + str(right_world_curverad) + " m")
            #texts.append("Left poly CUR: " + str(left_fit))
            #texts.append("Left poly AVG: " + str(left_line.best_fit))

            left_ok, left_cmp_str = polynomials_within_tolerance(left_line.best_fit, left_fit, 0.15)
            right_ok, right_cmp_str = polynomials_within_tolerance(right_line.best_fit, right_fit, 0.15)

            reset = False
            if not left_ok:
                left_line.confidence -= 1
                if (left_line.confidence <= 0):
                    reset = True
            else:
                left_line.confidence = DEFAULT_CONFIDENCE

            if not right_ok:
                right_line.confidence -= 1
                if (right_line.confidence <= 0):
                    reset = True
            else:
                right_line.confidence = DEFAULT_CONFIDENCE

            discard = ""
            if left_ok and right_ok:
                # average best fit
                left_line.addToAverageBestFit(left_fit, result.shape)
                right_line.addToAverageBestFit(right_fit, result.shape)
            else:
                discard = "DISCARD!"

            if reset:
                result, left_fit, right_fit = sliding_window(gradx)
                left_line.detected = True
                right_line.detected = True
                # average best fit
                left_line.addToAverageBestFit(left_fit, result.shape)
                right_line.addToAverageBestFit(right_fit, result.shape)
                discard = "RESET!"

            texts.append("Compare Left: " + str(left_cmp_str) + " Confidence: " + str(left_line.confidence))
            texts.append("Compare Right: " + str(right_cmp_str) + " Confidence: "+ str(right_line.confidence))

            offset = lane_offset(left_line.best_fit, right_line.best_fit, gradx)
            texts.append("Lane Offset: " + str(offset))

            texts.append(discard)

        result_warped = draw_lane_undistorted(undistd, left_line.best_fit, right_line.best_fit)
        result_warped = addText(result_warped, texts)

        return concatenate_4_images(image, gradx, result, result_warped)
        #return result_warped
    except:
        return concatenate_4_images(image, gradx, gradx, image)

    # Pipeline used for challenge_video
    def process_image_video2(image):
        try:
            undistd = undist(image)
            persp = perspective_transform(undistd)
            gradx = abs_sobel_thresh(L(persp), orient='x', sobel_kernel=ksize, thresh=(30, 100))

            left_lane_line = np.zeros_like(gradx)
            thresholded_L = thresh(L(persp), thresh=(130, 255))
            thresholded_S = thresh(S(persp), thresh=(15, 255))
            left_lane_line[(thresholded_L == 1) & (thresholded_S == 1)] = 1

            right_lane_line = thresh(L(persp), thresh=(180, 255))
            right_lane_line_strict = np.zeros_like(gradx)
            right_lane_line_strict[(right_lane_line == 1) & (gradx == 1)] = 1

            both_lane_lines = np.zeros_like(gradx)
            both_lane_lines[(left_lane_line == 1) | (right_lane_line_strict == 1)] = 1

            global left_line, right_line

            if (left_line.detected and right_line.detected):
                result, left_fit, right_fit = detect_from_previous(both_lane_lines, left_line.best_fit, right_line.best_fit)

                # average best fit
                left_line.addToAverageBestFit(left_fit, result.shape)
                right_line.addToAverageBestFit(right_fit, result.shape)

            else:
                histogram = get_histogram(both_lane_lines, ratio=1.4)
                result, left_fit, right_fit = sliding_window(both_lane_lines, histogram)

                left_line.detected = True
                right_line.detected = True

                # average best fit
                left_line.addToAverageBestFit(left_fit, result.shape)
                right_line.addToAverageBestFit(right_fit, result.shape)

            result_warped = draw_lane_undistorted(undistd, left_line.best_fit, right_line.best_fit)

            texts = []

            if left_line.detected:
                left_px_curverad, left_world_curverad = measure_curvature(left_line.best_fit, gradx)
                left_line.radius_of_curvature = left_world_curverad
                texts.append("Left World Curverad: " + str(left_world_curverad))
                texts.append("Left Px Curverad: " + str(left_px_curverad))

            if right_line.detected:
                right_px_curverad, right_world_curverad = measure_curvature(right_line.best_fit, gradx)
                right_line.radius_of_curvature = right_world_curverad
                texts.append("Right World Curverad: " + str(right_world_curverad))
                texts.append("Right Px Curverad: " + str(right_px_curverad))

            if left_line.detected and right_line.detected:
                offset = lane_offset(left_line.best_fit, right_line.best_fit, gradx)
                texts.append("Lane Offset: " + str(offset))

            result_warped = addText(result_warped, texts)
            ''
            return concatenate_4_images(left_lane_line, right_lane_line, result, result_warped)
            #return result_warped
        except:
            return concatenate_4_images(left_lane_line, right_lane_line, both_lane_lines, both_lane_lines)
            #return both_lane_lines
            #return undistd

def process_image(image):

    #image_o = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #cv2.imwrite("test_images/test_challenge_4.jpg", image_o)

    undistd = undist(image)
    persp = perspective_transform(undistd)
    #gradx = abs_sobel_thresh(Y(persp), orient='x', sobel_kernel=ksize, thresh=(50, 200)) # was 10,100

    #mag_L = mag_thresh(L(persp), thresh=(50, 200))
    #mag_Y = mag_thresh(Y(persp), thresh=None)
    #mag_U = mag_thresh(U(persp), thresh=(50, 200))
    #mag_S = mag_thresh(S(persp), thresh=(50, 200))

    thresholded_L = thresh(L(persp), thresh=(130, 255))
    left_lane_line = np.zeros_like(thresholded_L)
    thresholded_S = thresh(S(persp), thresh=(15, 255))
    left_lane_line[(thresholded_L == 1) & (thresholded_S == 1)] = 1
    thresholded_Y = thresh(Y(persp), thresh=(200, 255))
    thresholded_V = thresh(V(persp), thresh=(0, 100))
    thresholded_U = thresh(U(persp), thresh=(0, 100))
    thresholded_H = thresh(H(persp), thresh=(100, 102))
    #left_lane_line[(thresholded_L == 1) & (thresholded_S == 1)] = 1

    #right_lane_line = thresh(L(persp), thresh=(180, 255))
    #right_lane_line_strict = np.zeros_like(gradx)
    #right_lane_line_strict[(right_lane_line == 1) & (gradx == 1)] = 1



    #both_lane_lines = np.zeros_like(gradx)
    #both_lane_lines[(left_lane_line == 1) | (right_lane_line_strict == 1)] = 1

    #global left_line, right_line

    #result_sl, left_line, right_line = sliding_window(both_lane_lines, left_line, right_line)
    #if (left_line.detected and right_line.detected):
    #    result, left_line, right_line = detect_from_previous(both_lane_lines, left_line, right_line)

    return concatenate_4_images(thresholded_Y, left_lane_line, thresholded_U, thresholded_V)
