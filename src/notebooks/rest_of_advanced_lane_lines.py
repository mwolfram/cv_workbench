# Undistort
%matplotlib inline
image = cv2.imread("camera_cal2/resized/20170523_181342A.jpg")
plt.imshow(undist(image))
cv2.imwrite("output_images/undistorted_20170523_181342A.jpg.jpg", undist(image))

# Undistort
#%matplotlib inline
#image = cv2.imread("test_images/straight_lines1.jpg")
#plt.imshow(undist(image))
#cv2.imwrite("output_images/undistorted_straight_lines1.jpg", undist(image))


# Undistort and perspective
%matplotlib inline
image = cv2.imread("test_images/straight_lines_hart.png")
plt.imshow(perspective_transform(undist(image)))
#cv2.imwrite("output_images/undistorted_20170523_181342A.jpg.jpg", undist(image))


image = cv2.imread("test_images/straight_lines1.jpg")
undistd = undist(image)
gradx = abs_sobel_thresh(L(undistd), orient='x', sobel_kernel=ksize, thresh=(10, 100))
out_img = np.dstack((gradx, gradx, gradx))*255
cv2.imwrite("output_images/straight_lines1_sobel.jpg", out_img)

image = cv2.imread("test_images/straight_lines1.jpg")
undistd = undist(image)
thresholded_L = thresh(L(undistd), thresh=(180, 255))
out_img = np.dstack((thresholded_L, thresholded_L, thresholded_L))*255
cv2.imwrite("output_images/straight_lines1_thresholdedL.jpg", out_img)

image = cv2.imread("test_images/straight_lines1.jpg")
undistd = undist(image)
persp = perspective_transform(undistd)
cv2.imwrite("output_images/straight_lines1_persp.jpg", persp)

thresholded_L = thresh(L(persp), thresh=(180, 255))
out_img = np.dstack((thresholded_L, thresholded_L, thresholded_L))*255
cv2.imwrite("output_images/straight_lines1_persp_thresholdedL.jpg", out_img)

thresholded_S = thresh(S(persp), thresh=(180, 255))
out_img = np.dstack((thresholded_S, thresholded_S, thresholded_S))*255
cv2.imwrite("output_images/straight_lines1_persp_thresholdedS.jpg", out_img)

thresholded_Y = thresh(L(persp), thresh=(200, 255))
out_img = np.dstack((thresholded_Y, thresholded_Y, thresholded_Y))*255
cv2.imwrite("output_images/straight_lines1_persp_thresholdedY.jpg", out_img)

thresholded_V = thresh(V(persp), thresh=(155, 255))
out_img = np.dstack((thresholded_V, thresholded_V, thresholded_V))*255
cv2.imwrite("output_images/straight_lines1_persp_thresholdedV.jpg", out_img)

thresholded_Y = thresh(Y(persp), thresh=(200, 255))
thresholded_V = thresh(V(persp), thresh=(155, 255))

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

out_img = np.dstack((gradx, gradx, gradx))*255
cv2.imwrite("output_images/straight_lines1_persp_combined.jpg", out_img)

left_line = None
right_line = None
image = cv2.imread("test_images/test2.jpg")
undistd = undist(image)
persp = perspective_transform(undistd)

thresholded_Y = thresh(Y(persp), thresh=(200, 255))
thresholded_V = thresh(V(persp), thresh=(155, 255))

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
result, left_fit, right_fit = sliding_window(gradx)
cv2.imwrite("output_images/test2_sliding_window.jpg", result)
result, left_fit, right_fit = detect_from_previous(gradx, left_fit, right_fit)
cv2.imwrite("output_images/test2_detect_from_previous.jpg", result)
lane_img = draw_lane_undistorted(undistd, left_fit, right_fit)
cv2.imwrite("output_images/test2_lane_orig.jpg", lane_img)
lane_offset(left_fit, right_fit, lane_img)

%matplotlib inline

left_line = Line()
right_line = Line()

image_displays=[]

image = cv2.imread("test_images/test6.jpg")
#plt.imshow(process_image(image))'
#plt.imshow(process_image(image))

#undistd = undist(image)
#persp = perspective_transform(undistd)
#gradx = abs_sobel_thresh(Y(persp), orient='x', sobel_kernel=ksize, thresh=(50, 200)) # was 10,100#

#mag_L = mag_thresh(L(persp), thresh=(50, 200))
#mag_Y = mag_thresh(Y(persp), thresh=None)
#mag_U = mag_thresh(U(persp), thresh=(50, 200))
#mag_S = mag_thresh(S(persp), thresh=(50, 200))

#left_lane_line = np.zeros_like(gradx)
#thresholded_L = thresh(L(persp), thresh=(130, 255))
thresholded_U = thresh(U(undist(image)), thresh=(0, 255))
thresholded_V = thresh(V(undist(image)), thresh=(0, 255))
#thresholded_L = thresh(L(persp), thresh=(180, 255))

image_displays.append(ImageDisplay(process_image(image), "processed", "gray"))
image_displays.append(ImageDisplay(thresholded_U, "th U", "gray"))
image_displays.append(ImageDisplay(thresholded_V, "th V", "gray"))
image_displays.append(ImageDisplay(V(undist(image)), "original V", "gray"))
image_displays.append(ImageDisplay(H(undist(image)), "original H", "gray"))
image_displays.append(ImageDisplay(L(undist(image)), "original L", "gray"))
image_displays.append(ImageDisplay(S(undist(image)), "original S", "gray"))


image_displays.append(ImageDisplay(process_image_video1(image), "processed", "gray"))
#image_displays.append(ImageDisplay(process_image(image), "processed_again", "gray"))

# display all images
show_multiple(image_displays)



#image = cv2.imread("test_images/straight_lines2.jpg")

# Choose a Sobel kernel size
#ksize = 5 # Choose a larger odd number to smooth gradient measurements

# Apply each of the thresholding functions
#gradx = abs_sobel_thresh(S(image), orient='x', sobel_kernel=ksize, thresh=(10, 100))
#grady = abs_sobel_thresh(S(image), orient='y', sobel_kernel=ksize, thresh=(10, 100))
#mag_binary = mag_thresh(S(image), sobel_kernel=ksize, mag_thresh=(10, 100))
#dir_binary = dir_threshold(L(image), sobel_kernel=ksize, thresh=(0.1, 0.3))

#histogram = np.sum(gradx[int(gradx.shape[0]/2):,:], axis=0)
#plt.plot(histogram)

#return sliding_window(gradx)

#combined = np.zeros_like(dir_binary)
#combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1
#combined[(gradx == 1) & (grady == 1)] = 1

%matplotlib inline

left_line = Line()
right_line = Line()

#video = "project_video"
#video = "project_video_fin"
#video = "challenge_video"
#video = "harder_challenge_video"
video = "own_ll_2"

mode = "debug"
#mode = "with_pipeline_1"

white_output = video + "_" + mode + "_out.mp4"
clip1 = VideoFileClip(video + ".mp4")

# choose pipeline
white_clip = clip1.fl_image(process_image_video1)
#white_clip = clip1.fl_image(process_image_video2)
#white_clip = clip1.fl_image(process_image)
#white_clip = clip1.fl_image(process_image_find_cspace)

%time white_clip.write_videofile(white_output, audio=False)
