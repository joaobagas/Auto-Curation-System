from datetime import datetime
import numpy
from acll_cnn.run import run_cnn
import cv2
from PIL import Image


def select(enhanced_frames, results, observation_nums):
    scores = []

    # Use the blur method to get the sharpest images.
    for frame in enhanced_frames:
        scores.append(blur_selection(frame))

    # Use the confidence method to get the easier to detect images and the bbox method to get the biggest images.
    # Max score 5 000

    i = 0
    for result in results:
        scores[i] += int(result["conf"]) * 5000
        i += 1

    indexes = select_highest_values(scores)
    save(enhanced_frames, indexes, observation_nums, results)


# Max score = 2 500
def blur_selection(img1):
    pixel_change = 5
    img1 = cv2.resize(img1, (500, 500))
    img2 = cv2.blur(img1, (10, 10))
    img3 = cv2.subtract(img1, img2)

    count1 = 0
    for row in img3:
        for pixel in row:
            if pixel[0] > pixel_change and pixel[1] > pixel_change and pixel[2] > pixel_change:
                count1 += 1
    return count1 / 100


# Max score 2 500 there is a bug in the bbox
def bbox_selection(detection):
    bbox = detection['bbox']
    x = abs(bbox[3] - bbox[0])
    y = abs(bbox[2] - bbox[1])
    return x * y * 2500


def select_highest_values(array):
    highest = max(array)
    index = 0
    indexes = []
    for val in array:
        if val >= (highest - 500):
            indexes.append(index)
        index += 1
    return indexes


def save(enhanced_frames, indexes, observation_nums, results):

    # Because of bugs in the neural network it comes disabled by default.
    # You can use enable it here!
    use_network = False

    now = datetime.now()
    timestamp = now.strftime("%d%m%Y%H%M%S")
    count = 0

    if use_network:
        enhanced_frames = run_cnn(enhanced_frames)
    else:
        enhanced_frames = enhance_brightness_and_contrast(enhanced_frames)

    for frame in enhanced_frames:
        if count in indexes:
            if use_network:
                frame = numpy.array(frame)
            im_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im_cvt)
            im.save(
                "img/observations/" + timestamp + "obs" + str(observation_nums[count]) + "-ACS-" + str(count) + ".jpeg")
        count += 1

# https://answers.opencv.org/question/75510/how-to-make-auto-adjustmentsbrightness-and-contrast-for-image-android-opencv-image-correction/
def enhance_brightness_and_contrast(imgs):
    new_imgs = []
    for img in imgs:
        alow = img.min()
        ahigh = img.max()
        amax = 255
        amin = 0

        # calculate alpha, beta
        alpha = ((amax - amin) / (ahigh - alow))
        beta = amin - alow * alpha

        # perform the operation g(x,y)= α * f(x,y)+ β
        new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        new_imgs.append(new_img)

    return new_imgs