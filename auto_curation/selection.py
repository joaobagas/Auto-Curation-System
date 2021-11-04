from datetime import datetime

import cv2
from PIL import Image, ImageEnhance


def select(enhanced_frames, results, observation_nums):
    score = []
    # Use the blur method to get the sharpest images.
    for frame in enhanced_frames:
        score.append(blur_selection(frame))

    # Use the confidence method to get the easier to detect images and the bbox method to get the biggest images.
    i = 0
    for result in results:
        score[i] += int(result["conf"] * 100)
        score[i] += int(bbox_selection(result))
        i += 1

    indexes = select_highest_values(score)
    save(enhanced_frames, indexes, observation_nums)


def blur_selection(img1):
    pixel_change = 5
    img2 = cv2.blur(img1, (10, 10))
    img3 = cv2.subtract(img1, img2)

    count1 = 0
    for row in img3:
        for pixel in row:
            if pixel[0] > pixel_change and pixel[1] > pixel_change and pixel[2] > pixel_change:
                count1 += 1
    return count1


def bbox_selection(detection):
    bbox = detection['bbox']
    x = abs(bbox[3] - bbox[1])
    y = abs(bbox[2] - bbox[0])
    return x * y * 100


def select_highest_values(array):
    highest = 0
    index = 0
    indexes = []
    for val in array:
        if val > (highest + 0.001):
            indexes.clear()
            indexes.append(index)
        elif val < (highest - 0.001):
            pass
        else:
            indexes.append(index)
    return indexes


def save(enhanced_frames, indexes, observation_nums):
    now = datetime.now()
    timestamp = now.strftime("%d%m%Y%H%M%S")
    count = 0
    for frame in enhanced_frames:
        if count in indexes:
            im_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im_cvt)
            im.save(
                "img/observations/" + timestamp + "obs" + str(observation_nums[count]) + "-ACS-" + str(count) + ".jpeg")
        count += 1