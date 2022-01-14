import cv2


# This function subtracts a 50x50 image by the previous one and vice-versa,
# then it checks if the result has 50 or more pixels that have a value higher than 5 in the RGB channels.
def detect_change(img1, img2):
    pixel_change = 5
    threshold = 50
    x_size = 50
    y_size = 50

    img1 = cv2.resize(img1, (x_size, y_size))
    img2 = cv2.resize(img2, (x_size, y_size))
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
        return True
    return False
