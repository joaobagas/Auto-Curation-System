import cv2

from change import *
from detection import *
from enhancement import *


def auto_curation(mov):
    cap = cv2.VideoCapture()

    # Motion Detection - Transforms the video into an array of frames.
    if (cap.isOpened() == False):
        print("Error")
    frames_with_movement = []
    prev_frame = None
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if prev_frame is not None:
                detect_change(frame, prev_frame, 20)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            prev_frame = frame
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

    # Animal Detection - Checks the array of frames for animals and creates another array.
    frames_with_animals = []
    for frame in frames_with_movement:
        detect_animal(frame)

    # Image Editing - Edits the images left in the array.
    for frame in frames_with_animals:
        enhance_brightness_and_contrast(frame)

    # Image selection - Here we are going to use the model's certainty to get the best photos.
