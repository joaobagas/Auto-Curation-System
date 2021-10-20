import cv2
import tensorflow as tf
from change import *
from detect import *
from enhancement import *


def auto_curation(mov):
    # Motion Detection - Transforms the video into an array of frames with movement.

    cap = cv2.VideoCapture(mov)
    saved_frames = 0
    current_frame = 0
    if (cap.isOpened() == False):
        print("Error")
    frames_with_movement = []
    prev_frame = None
    while (cap.isOpened()):
        current_frame += 1
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ret, frame = cap.read()
        if ret == True and saved_frames < 1:
            #print(str(int(float(current_frame)*100.0/float(total))) + "%")
            if prev_frame is not None:
                if detect_change(prev_frame, frame):
                    frames_with_movement.append(frame)
                    saved_frames += 1
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            prev_frame = frame
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Frames with motion: " + str(saved_frames))

    # Animal Detection - Checks the array of frames for animals and creates another array.

    frames_with_animals = []
    model_file = "files/md_v4.1.0.pb"
    output_dir = "files"
    translated_frames = translate_to_tf(frames_with_movement)
    detection_results = load_and_run_detector_on_video(model_file, translated_frames, output_dir, render_confidence_threshold=0.5)

    frame = 0
    for result in detection_results:
        for detection in result['detections']:
            if int(detection["category"]) == 2 and float(detection["conf"]) > 0.9: # This needs to be changed from 2 to 1
                frames_with_animals.append(frames_with_movement[frame])
        frame += 1

    # Image Editing - Edits the images left in the array.

    for frame in frames_with_animals:
        enhance_brightness_and_contrast(frame)
        cv2.imshow("", frame)
        cv2.waitKey(0)

    # Image selection - Here we are going to use the model's certainty to get the best photos.

    selected_frames = []

    # Return the images.

    return selected_frames

auto_curation("camera_trap_2.mp4")