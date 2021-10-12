import cv2

from change import *
# from detection import *
from enhancement import *


def auto_curation(mov):
    cap = cv2.VideoCapture(mov)
    c = 0
    a = 0
    # Motion Detection - Transforms the video into an array of frames with movement.
    if (cap.isOpened() == False):
        print("Error")
    frames_with_movement = []
    prev_frame = None
    while (cap.isOpened()):
        a += 1
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ret, frame = cap.read()
        if ret == True:
            print("Frame:" + str(a) + "/" + str(total))
            if prev_frame is not None:
                if detect_change(cv2.resize(frame, (300, 300)), cv2.resize(prev_frame, (300, 300))):
                    frames_with_movement.append(frame)
                    c += 1
                    print("Saved:" + str(c))
                    cv2.imshow(str(c), cv2.resize(frame, (400, 400)))
                    cv2.waitKey(0)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            prev_frame = frame
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    print(frames_with_movement)
    return None

    # Animal Detection - Checks the array of frames for animals and creates another array.
    frames_with_animals = []
    detect_animal(frames_with_movement)

    # Image Editing - Edits the images left in the array.
    for frame in frames_with_animals:
        enhance_brightness_and_contrast(frame)

    # Image selection - Here we are going to use the model's certainty to get the best photos.

auto_curation("camera_trap_2.mp4")