import cv2

def gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray

def HLS(img):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    return hls

def YUV(img):
    yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    return yuv

def H(img):
    hls = HLS(img)
    return hls[:,:,0]

def L(img):
    hls = HLS(img)
    return hls[:,:,1]

def S(img):
    hls = HLS(img)
    return hls[:,:,2]

def Y(img):
    yuv = YUV(img)
    return yuv[:,:,0]

def U(img):
    yuv = YUV(img)
    return yuv[:,:,1]

def V(img):
    yuv = YUV(img)
    return yuv[:,:,2]

def convert_color(img, src, tgt):
    return convert_from_RGB(img, tgt)

def convert_from_RGB(img, tgt):
    if tgt != 'RGB':
        if tgt == 'HSV':
            return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        elif tgt == 'LUV':
            return cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
        elif tgt == 'HLS':
            return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        elif tgt == 'YUV':
            return cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        elif tgt == 'YCrCb':
            return cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        elif tgt == 'BGR':
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        return np.copy(img)

    return None
