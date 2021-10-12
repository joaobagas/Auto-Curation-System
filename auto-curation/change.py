import cv2


def detect_change(img1, img2):
    pixel_change = 5
    threshold = 900

    img3 = cv2.subtract(img1, img2)
    img4 = cv2.subtract(img2, img1)

    count1 = 0
    for row in img3:
        for pixel in row:
            if pixel[0] > pixel_change and pixel[1] > pixel_change and pixel[2] > pixel_change:
                count1 += 1

    count2 = 0
    for row in img4:
        for pixel in row:
            if pixel[0] > pixel_change and pixel[1] > pixel_change and pixel[2] > pixel_change:
                count2 += 1

    if count1 > threshold and count2 > threshold:
        print("c1: " + str(count1) + " | c2: " + str(count2))
        return True
    return False
