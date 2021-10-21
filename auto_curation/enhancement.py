import cv2


# https://answers.opencv.org/question/75510/how-to-make-auto-adjustmentsbrightness-and-contrast-for-image-android-opencv-image-correction/
def enhance_brightness_and_contrast(img):
    alow = img.min()
    ahigh = img.max()
    amax = 255
    amin = 0

    # calculate alpha, beta
    alpha = ((amax - amin) / (ahigh - alow))
    beta = amin - alow * alpha
    # perform the operation g(x,y)= α * f(x,y)+ β
    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # return [new_img, alpha, beta]
    return new_img
