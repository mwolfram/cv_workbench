class ImageDisplay():
    def __init__(self, image, label, cmap_str):
        self.image = image
        self.label = label
        self.cmap_str = cmap_str

    def display6(image1, image2, image3, image4, image5, image6):
        image = np.concatenate((np.concatenate((image1, image2), axis=0),np.concatenate((image3, image4), axis=0)), axis=1)
        image = np.concatenate((np.concatenate((image5, image6), axis=0), image), axis=1)
        return image
