import cv2

class FilterTools():

    @staticmethod
    def thresholdGrayscaleImage(gray, thresholdValues=(0, 255)):
        if thresholdValues is None:
            return gray
        binaryOutput = np.zeros_like(gray)
        binaryOutput[(gray >= thresh[0]) & (gray <= thresh[1])] = 1
        return binaryOutput

    @staticmethod
    def thresholdedSobel(gray, orient='x', sobelKernel=3, thresholdValues=(0, 255)):
        # Apply x or y gradient with the OpenCV Sobel() function
        # and take the absolute value
        if orient == 'x':
            absSobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobelKernel))
        if orient == 'y':
            absSobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobelKernel))
        # Rescale back to 8 bit integer
        scaledSobel = np.uint8(255*absSobel/np.max(absSobel))
        return thresholdGrayscaleImage(scaledSobel, thresholdValues)

    @staticmethod
    def thresholdedSobelMagnitude(gray, sobelKernel=3, thresholdValues=(0, 255)):
        # Take both Sobel x and y gradients
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobelKernel)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobelKernel)
        # Calculate the gradient magnitude
        gradmag = np.sqrt(sobelx**2 + sobely**2)
        # Rescale to 8 bit
        scaleFactor = np.max(gradmag)/255
        gradmag = (gradmag/scaleFactor).astype(np.uint8)
        return thresholdGrayscaleImage(gradmag, thresholdValues)

    @staticmethod
    def thresholdedSobelDirection(gray, sobelKernel=3, thresholdValues=(0, np.pi/2)):
        # Calculate the x and y gradients
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobelKernel)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobelKernel)
        # Take the absolute value of the gradient direction,
        # apply a threshold, and create a binary image result
        absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
        return thresholdGrayscaleImage(absgraddir, thresholdValues)
