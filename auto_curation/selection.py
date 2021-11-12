from datetime import datetime
from auto_curation.enhancement import enhance_brightness_and_contrast

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
        # scores[i] += int(bbox_selection(result))
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
    now = datetime.now()
    timestamp = now.strftime("%d%m%Y%H%M%S")
    count = 0
    for frame in enhanced_frames:
        if count in indexes:
            draw_bounding_box(frame, results[count])
            frame = enhance_brightness_and_contrast(frame)
            im_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im_cvt)
            im.save(
                "img/observations/" + timestamp + "obs" + str(observation_nums[count]) + "-ACS-" + str(count) + ".jpeg")
        count += 1

def draw_bounding_box(image, result):
    bbox = result['bbox']
    height, width, channels = image.shape
    p1 = (int(bbox[0]*width), int(bbox[1]*height))
    p2 = (int(bbox[2]*width), int(bbox[3]*height))
    cv2.rectangle(image, p1, p2, (0, 0, 255), 2)