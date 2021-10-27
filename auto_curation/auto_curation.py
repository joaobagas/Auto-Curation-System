import cv2
import numpy as np
import tensorflow as tf
from pyqt5_plugins.examplebuttonplugin import QtGui
from PIL import Image

from auto_curation.change import *
from auto_curation.detect import *
from auto_curation.enhancement import *


def auto_curation(mov, progress, status):

    progress.setMaximum(100)

    # Motion Detection - Transforms the video into an array of frames with movement.

    progress.setValue(0)
    status.setText("Status: 1/4 Running motion detection!")

    cap = cv2.VideoCapture(mov)
    saved_frames = 0
    current_frame = 0
    if (cap.isOpened() == False):
        print("Error")
    frames_with_movement = []
    prev_frame = None
    while (cap.isOpened()):
        current_frame += 1
        ret, frame = cap.read()
        if ret == True:
            if prev_frame is not None and saved_frames < 5:
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

    progress.setValue(25)
    status.setText("Status: 2/4 Running animal detection!")

    frames_with_animals = []
    detections = []
    model_file = "auto_curation/files/md_v4.1.0.pb"
    output_dir = "auto_curation/files"
    translated_frames = translate_to_tf(frames_with_movement)
    detection_results = load_and_run_detector_on_video(model_file, translated_frames, output_dir, render_confidence_threshold=0.5)

    frame = 0
    for result in detection_results:
        for detection in result['detections']:
            if int(detection["category"]) == 2 and float(detection["conf"]) > 0.900: #Test it should be 1
                frames_with_animals.append(frames_with_movement[frame])
                detections.append(detection)
        frame += 1
    del frames_with_movement, detection_results

    # Image Editing - Edits the images left in the array.

    progress.setValue(50)
    status.setText("Status: 3/4 editing images!")

    enhanced_frames = []
    for frame in frames_with_animals:
        enhanced_frames.append(enhance_brightness_and_contrast(frame))
    del frames_with_animals

    # Image selection - Here we are going to use the model's certainty to get the best photos.

    progress.setValue(75)
    status.setText("Status: 4/4 Selecting the frames!")

    selected_frames = []
    count = 0
    for frame in enhanced_frames:
        if detections[count]["conf"] > 0.998:
            im_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im_cvt)
            im.save("img/observations/test-ACS-" + str(count) + ".jpeg")
        count += 1
    del enhanced_frames
    
    # Return the images.

    progress.setValue(100)
    status.setText("Status: Process finished!")

    return selected_frames