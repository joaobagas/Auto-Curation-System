import os


class ImageLoader(object):
    _instance = None
    observations = []  # Will store the observation names
    obs_pointer = -1
    images = []  # Will store all the images
    obs_images = []  # Will store all the images related to the current observation
    obs_images_pointer = -1

    current_observation = None
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
                strings = filename.split("-")
                if not strings[0] in self.observations:
                    self.observations.append(strings[0])
            else:
                continue
        self.load_obs()

    def load_obs(self):
        self.obs_images = []
        for filename in self.images:
            fn = filename.split("/")
            fn2 = fn[1]
            fn3 = fn2.split("-")
            root = fn3[0]
            if root == self.observations[self.obs_pointer]:
                self.obs_images.append(filename)

    def prev_obs(self):
        if self.observations != [] and self.obs_pointer == -1:
            self.obs_pointer = 0
            self.current_observation = self.observations[self.obs_pointer]
        elif self.observations != [] and self.obs_pointer > 0:
            self.obs_pointer -= 1
            self.current_observation = self.observations[self.obs_pointer]
        self.load_obs()

    def next_obs(self):
        if self.observations != [] and self.obs_pointer == -1:
            self.obs_pointer = 0
            self.current_observation = self.observations[self.obs_pointer]
        elif self.observations != [] and self.obs_pointer < len(self.observations) - 1:
            self.obs_pointer += 1
            self.current_observation = self.observations[self.obs_pointer]
        self.load_obs()

    def delete_obs(self):
        self.observations.pop(self.obs_pointer)
        os.remove(self.current_image)
        if self.obs_pointer > len(self.observations) - 1:
            self.obs_pointer -= 1
        if len(self.obs_pointer) == 0:
            self.obs_pointer = -1
            self.current_observation = None
        else:
            self.current_observation = self.observations[self.obs_pointer]
        return self.current_observation

    def prev_photo(self):
        if self.obs_images != [] and self.obs_images_pointer == -1:
            self.obs_images_pointer  = 0
            self.current_image = self.obs_images[self.obs_images_pointer]
        elif self.obs_images != [] and self.obs_images_pointer > 0:
            self.obs_images_pointer -= 1
            self.current_image = self.obs_images[self.obs_images_pointer]
        return self.current_image

    def next_photo(self):
        if self.obs_images != [] and self.obs_images_pointer  == -1:
            self.obs_images_pointer = 0
            self.current_image = self.obs_images[self.obs_images_pointer]
        elif self.obs_images != [] and self.obs_images_pointer  < len(self.obs_images) - 1:
            self.obs_images_pointer += 1
            self.current_image = self.obs_images[self.obs_images_pointer]
        return self.current_image

    def delete_photo(self):
        self.obs_images.pop(self.obs_images_pointer )
        os.remove(self.current_image)
        if self.obs_images_pointer > len(self.obs_images) - 1:
            self.obs_images_pointer -= 1
        if len(self.obs_images) == 0:
            self.obs_images_pointer = -1
            self.current_image = 'img/black_image.jpg'
        else:
            self.current_image = self.obs_images[self.obs_images_pointer]
        return self.current_image
