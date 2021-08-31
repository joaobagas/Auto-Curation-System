# This class holds all the methods to enhance the a give image.

from PIL import Image, ImageEnhance


class ImageEditor(object):
    def __init__(self, input_img):
        self.img = Image.open(input_img)

    def change_brightness(self, value):
        image_enhancer = ImageEnhance.Brightness(self.img)
        self.img = image_enhancer.enhance(value)

    def change_contrast(self, value):
        image_enhancer = ImageEnhance.Contrast(self.img)
        self.img = image_enhancer.enhance(value)

    def change_saturation(self, value):
        image_enhancer = ImageEnhance.Color(self.img)
        self.img = image_enhancer.enhance(value)

    def change_sharpness(self, value):
        image_enhancer = ImageEnhance.Sharpness(self.img)
        self.img = image_enhancer.enhance(value)

    def crop(self, left, top, right, bottom):
        self.img = self.img.crop((left, top, right, bottom))

    def save(self, title):
        self.img.save("img/observations/" + title + ".jpg")
