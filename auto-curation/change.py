import cv2


def detect_change(img1, img2, threshold):
    img3 = cv2.subtract(img1, img2)
    img4 = cv2.subtract(img2, img1)
    count1 = 0
    for pixel in img3:
        if pixel[0] > 0 or pixel[1] > 0 or pixel[2] > 0:
            count1 += 1
    count2 = 0
    for pixel in img4:
        if pixel[0] > 0 or pixel[1] > 0 or pixel[2] > 0:
            count2 += 1
    if count1 > threshold or count2 > threshold:
        return True
    return False
