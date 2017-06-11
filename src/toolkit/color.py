import cv2

class ColorTools():

    @staticmethod
    def gray(img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return gray

    @staticmethod
    def HLS(img):
        hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        return hls

    @staticmethod
    def YUV(img):
        yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        return yuv

    @staticmethod
    def H(img):
        hls = ColorTools.HLS(img)
        return hls[:,:,0]

    @staticmethod
    def L(img):
        hls = ColorTools.HLS(img)
        return hls[:,:,1]

    @staticmethod
    def S(img):
        hls = ColorTools.HLS(img)
        return hls[:,:,2]

    @staticmethod
    def Y(img):
        yuv = ColorTools.YUV(img)
        return yuv[:,:,0]

    @staticmethod
    def U(img):
        yuv = ColorTools.YUV(img)
        return yuv[:,:,1]

    @staticmethod
    def V(img):
        yuv = ColorTools.YUV(img)
        return yuv[:,:,2]

    @staticmethod
    def convert_color(img, src, tgt):
        return ColorTools.convert_from_RGB(img, tgt)

    @staticmethod
    def convert_from_RGB(img, tgt):
        if tgt == 'RGB':
            return np.copy(img)
        elif tgt == 'HSV':
            return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        elif tgt == 'LUV':
            return cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
        elif tgt == 'HLS':
            return ColorTools.HLS(img)
        elif tgt == 'YUV':
            return ColorTools.YUV(img)
        elif tgt == 'YCrCb':
            return cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        elif tgt == 'BGR':
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return np.copy(img)
