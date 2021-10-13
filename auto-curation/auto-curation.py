import cv2

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
        if ret == True and saved_frames < 3:
            print("Frame: " + str(current_frame) + "/" + str(total) + " " + str(int(float(current_frame)*100.0/float(total))) + "%")
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
    start()
    frames_with_animals = []
    model_file = "files/md_v4.1.0.pb"
    output_dir = "result"
    translated_frames = translate_to_tf(frames_with_movement)
    detection_results = load_and_run_detector_on_video(model_file, translated_frames, output_dir, render_confidence_threshold=0.5)

    for result in detection_results:
        size = (400, 400)
        im = Image.open("test.jpeg")
        im = im.resize(size)

        draw_bboxs(detection_results[0]['detections'], im)

        plt.imshow(im)
        plt.show()
        plt.title(f"image with bbox")

    # Image Editing - Edits the images left in the array.

    for frame in frames_with_animals:
        enhance_brightness_and_contrast(frame)

    # Image selection - Here we are going to use the model's certainty to get the best photos.

auto_curation("camera_trap_2.mp4")