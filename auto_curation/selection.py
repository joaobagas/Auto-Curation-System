import cv2
from PIL import Image, ImageEnhance

def blur_selection(img1):
    pixel_change = 5
    threshold = 200

    image_enhancer = ImageEnhance.Sharpness(img1)
    img2 = image_enhancer.enhance(-30)

    img3 = cv2.subtract(img1, img2)

    count1 = 0
    for row in img3:
        for pixel in row:
            if pixel[0] > pixel_change and pixel[1] > pixel_change and pixel[2] > pixel_change:
                count1 += 1

    if count1 > threshold:
        return True
    return False

def bbox_selection(bboxes):
    values = []
    for bbox in bboxes:
        x = abs(bbox[3] - bbox[1])
        y = abs(bbox[2] - bbox[0])
        values.append(x*y)
    highest = 0
    index = 0
    indexes = []
    for val in values:
        if val > (highest + 0.001):
            indexes.clear()
            indexes.append(index)
        elif val < (highest - 0.001):
            pass
        else:
            indexes.append(index)
    return indexes

