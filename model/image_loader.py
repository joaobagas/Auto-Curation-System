import os


class ImageLoader(object):
    _instance = None
    observations = []
    pointer = -1
    images = []
    current_image = 'img/black_image.jpg'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def load(self):
        directory = r'img\observations'
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                self.images.append(directory+"/"+filename)
            else:
                continue

    def prev_photo(self):
        if self.images != [] and self.pointer == -1:
            self.pointer = 0
            self.current_image = self.images[self.pointer]
        elif self.images != [] and self.pointer > 0:
            self.pointer -= 1
            self.current_image = self.images[self.pointer]
        return self.current_image

    def next_photo(self):
        if self.images != [] and self.pointer == -1:
            self.pointer = 0
            self.current_image = self.images[self.pointer]
        elif self.images != [] and self.pointer < len(self.images) - 1:
            self.pointer += 1
            self.current_image = self.images[self.pointer]
        print(self.current_image)
        return self.current_image

    def delete_photo(self):
        print("Photo deleted!")