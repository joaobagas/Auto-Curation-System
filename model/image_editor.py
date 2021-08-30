# This class holds all the methods to enhance the a give image.

from PIL import Image, ImageEnhance


class ImageEditor(object):
    def __init__(self, input_img):
        self.img = Image.open(input_img)

    def change_brightness(self, value):
        image_enhancer = ImageEnhance.Brightness(self.img)
        self.img = image_enhancer.enhance(value)
        self.img.show()

    def change_contrast(self, value):
        image_enhancer = ImageEnhance.Contrast(self.img)
        self.img = image_enhancer.enhance(value)
        self.img.show()

    def change_saturation(self, value):
        image_enhancer = ImageEnhance.Color(self.img)
        self.img = image_enhancer.enhance(value)
        self.img.show()

    def change_sharpness(self, value):
        image_enhancer = ImageEnhance.Sharpness(self.img)
        self.img = image_enhancer.enhance(value)
        self.img.show()

    def crop(self):
        # Opens a image in RGB mode
        im = Image.open(r"C:\Users\Admin\Pictures\geeks.png")

        # Size of the image in pixels (size of original image)
        width, height = im.size
        # Setting the points for cropped image
        left = 5
        top = height / 4
        right = 164
        bottom = 3 * height / 4
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))
        # Shows the image in image viewer
        im1.show()