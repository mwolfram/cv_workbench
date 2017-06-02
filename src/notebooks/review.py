# Detect yellow and white lines sep.

    b = np.zeros((img.shape[0],img.shape[1]))

    def thresh(img, thresh_min, thresh_max):
        ret = np.zeros_like(img)
        ret[(img >= thresh_min) & (img <= thresh_max)] = 1
        return ret

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    H = hsv[:,:,0]
    S = hsv[:,:,1]
    V = hsv[:,:,2]

    R = img[:,:,0]
    G = img[:,:,1]
    B = img[:,:,2]

    t_yellow_H = thresh(H,10,30)
    t_yellow_S = thresh(S,50,255)
    t_yellow_V = thresh(V,150,255)

    t_white_R = thresh(R,225,255)
    t_white_V = thresh(V,230,255)

    b[(t_yellow_H==1) & (t_yellow_S==1) & (t_yellow_V==1)] = 1
    b[(t_white_R==1)|(t_white_V==1)] = 1

def smooth(self, prev, curr, coeficient = 0.4):
        '''
         exponential smoothing
        :param prev: old value
        :param curr: new value
        :param coeficient: smoothing coef.
        :return:
        '''
        return curr*coeficient + prev*(1-coeficient)
