import cv2

from change import detect_change
from detection import detect_animal
from enhancement import enhance_brightness_and_contrast


# https://learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
def auto_curation(mov):
    cap = cv2.VideoCapture()

    if (cap.isOpened() == False):
        print("Error")
    frames_with_movement = []
    prev_frame = None
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if prev_frame is not None:
                detect_change(frame, prev_frame, 20)
                cv2.imshow('Frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            prev_frame = frame
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    frames_with_animals = []
    for frame in frames_with_movement:
        detect_animal(frame)

    for frame in frames_with_animals:
        enhance_brightness_and_contrast(frame)
