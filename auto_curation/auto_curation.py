from auto_curation.change import *
from auto_curation.detect import *
from auto_curation.selection import *


def auto_curation(path, progress, status, is_video):

    progress.setMaximum(100)

    # Motion Detection - Transforms the video into an array of frames with movement.

    progress.setValue(0)
    status.setText("Status: 1/3 Running motion detection!")

    if is_video:
        observation_nums, frames_with_movement = load_from_video(path)
    else:
        observation_nums, frames_with_movement = load_from_folder(path)

    # Animal Detection - Checks the array of frames for animals and creates another array.

    progress.setValue(33)
    status.setText("Status: 2/3 Running animal detection!")

    frames_with_animals = []
    detections = []
    model_file = "auto_curation/files/md_v4.1.0.pb"
    output_dir = "auto_curation/files"
    translated_frames = translate_to_tf(frames_with_movement)
    detection_results = load_and_run_detector_on_video(model_file, translated_frames, output_dir, render_confidence_threshold=0.5)

    frame = 0
    for result in detection_results:
        for detection in result['detections']:
            if int(detection["category"]) == 1 and detection["conf"] > 0.900:  # 1 -> Animal | 2 -> Person
                frames_with_animals.append(frames_with_movement[frame])
                detections.append(detection)
                break
            else:
                observation_nums.pop(frame)
                frame -= 1
                break
        frame += 1
    del frames_with_movement, detection_results

    # Image Selection/Editing - Here we are going to get the best photos and edit the images left in the array.

    progress.setValue(67)
    status.setText("Status: 3/3 Selecting and editing the frames!")

    select(frames_with_animals, detections, observation_nums)

    # Return the images.

    progress.setValue(100)
    status.setText("Status: Process finished!")

def load_from_video(mov):
    cap = cv2.VideoCapture(mov)
    observation_nums = []
    saved_frames = 0
    current_frame = 0
    frames_skipped = 50
    observation = 0
    if cap.isOpened() is False:
        print("Error")
    frames_with_movement = []
    prev_frame = None
    while cap.isOpened():
        current_frame += 1
        ret, frame = cap.read()
        if ret is True:
            if prev_frame is not None:
                if detect_change(prev_frame, frame):
                    if frames_skipped > 50:
                        observation += 1
                    frames_with_movement.append(frame)
                    observation_nums.append(observation)
                    frames_skipped = 0
                    saved_frames += 1
                else:
                    frames_skipped += 1
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            prev_frame = frame
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

    return observation_nums, frames_with_movement


def load_from_folder(paths):
    images = []
    obs = []
    for path in paths:
        img = cv2.imread(path)
        if img is not None:
            images.append(img)
            obs.append(0)
    return obs, images
