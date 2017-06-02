from moviepy.editor import VideoFileClip
import cv2

counter = 0

def saveImage(image):
    global counter

    image_o = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite("resources/calibration/set2/calibration_" + str(counter) + ".jpg", image_o)
    counter = counter + 1

    return image

def videoToImages():
    video = "/home/mwolfram/Videos/calibration"
    out = video + "_out_tmp.mp4"
    clip1 = VideoFileClip(video + ".mp4")
    white_clip = clip1.fl_image(saveImage)
    white_clip.write_videofile(out, audio=False)

videoToImages()
