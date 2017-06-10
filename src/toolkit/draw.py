import cv2
import numpy as np
from transformation import inverse_perspective_transform

def draw_polygon_with_margin_around_polynomial(out_img, polynomial, margin, color=(0, 255, 255)):
    if polynomial is None:
        return out_img

    window_img = np.zeros_like(out_img)

    # Generate x and y values for plotting
    ploty = np.linspace(0, out_img.shape[0]-1, out_img.shape[0] )
    plotx = polynomial[0]*ploty**2 + polynomial[1]*ploty + polynomial[2]

    # Generate a polygon to illustrate the search window area
    # And recast the x and y points into usable format for cv2.fillPoly()
    poly_window1 = np.array([np.transpose(np.vstack([plotx-margin, ploty]))])
    poly_window2 = np.array([np.flipud(np.transpose(np.vstack([plotx+margin, ploty])))])
    poly_pts = np.hstack((poly_window1, poly_window2))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(window_img, np.int_([poly_pts]), color)
    result = cv2.addWeighted(out_img, 1, window_img, 0.3, 0)

    return result

def draw_polygon_between_polynomials(out_img, left_fit, right_fit):
    if left_fit is None or right_fit is None:
        return out_img

    window_img = np.zeros_like(out_img)

    ploty = np.linspace(0, out_img.shape[0]-1, out_img.shape[0] )

    # Generate x and y values for plotting
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))
    cv2.fillPoly(window_img, np.int_([pts]), (255, 0, 0))

    result = cv2.addWeighted(out_img, 1, window_img, 0.8, 0)

    return result

def draw_lane_undistorted(undistd, left_fit, right_fit):

    # Create an image to draw the lines on
    #lane_zeros = np.zeros_like(undistd).astype(np.uint8)
    #lane_color = np.dstack((lane_zeros, lane_zeros, lane_zeros))
    lane_color = np.zeros_like(undistd)

    # draw the lane in top-down view, on the blank image
    lane_color = draw_polygon_between_polynomials(lane_color, left_fit, right_fit)

    # warp the lane back into the viewpoint of the car camera
    lane_color_warped = inverse_perspective_transform(lane_color)

    # Combine the result with the original image
    result = cv2.addWeighted(undistd, 1, lane_color_warped, 1, 0)

    return result

def addText(image, texts):
    y = 100
    y_offset = 50

    font = cv2.FONT_HERSHEY_SIMPLEX
    for text in texts:
        image = cv2.putText(image, text, (50, y), font, 1,(0,0,255),3)
        y += y_offset

    return image

def concatenate_4_images(image1, image2, image3, image4):
    image1 = grayToColor(image1)
    image2 = grayToColor(image2)
    image3 = grayToColor(image3)
    image4 = grayToColor(image4)

    left = np.concatenate((image1, image3), axis=0)
    right = np.concatenate((image2, image4), axis=0)
    return np.concatenate((left, right), axis=1)

def concatenate_6_images(image1, image2, image3, image4, image5, image6):
    image = np.concatenate((np.concatenate((image1, image2), axis=0),np.concatenate((image3, image4), axis=0)), axis=1)
    image = np.concatenate((np.concatenate((image5, image6), axis=0), image), axis=1)
    return image

def grayToColor(image):
    if (len(image.shape) < 3):
        return np.dstack((image, image, image))*255
    return image

def show_multiple(image_displays):
    fontsize = 10
    figsize = (20, 10)
    cols = 2

    rows = math.ceil(len(image_displays) / cols)
    print("image canvas with", cols, "cols and", rows, "rows")

    f, ( canvas ) = plt.subplots(rows, cols, figsize=figsize)

    for image_display_index in range(len(image_displays)):
        image_display = image_displays[image_display_index]

        if rows > 1:
            row = math.floor( float(image_display_index) / float(cols))
            col = image_display_index % cols
            print(image_display.label, "goes to", str(row), str(col))
            ax = canvas[row][col]
        else:
            ax = canvas[image_display_index]

        ax.imshow(image_display.image, cmap=image_display.cmap_str)
        ax.set_title(image_display.label, fontsize=fontsize)
