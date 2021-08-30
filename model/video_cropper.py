# This file holds the function which is used to crop frames off a video and save them.


def crop(location, obs, times):
    # The imports had to be placed inside of the function due to incompatibilities between PyQt5 and Open-CV
    from cv2 import VideoCapture, imwrite, destroyAllWindows

    cap = VideoCapture(location)

    # Set frame_no in range 0.0-1.0
    # In this example we have a video of 30 seconds having 25 frames per seconds, thus we have 750 frames.
    # The examined frame must get a value from 0 to 749.
    # time_length = 30.0
    # fps = 25
    # frame_seq = 749
    # time = (frame_seq / (time_length * fps))
    for time in times:
        cap.set(1, time)
        ret, frame = cap.read()
        if ret:
            imwrite("img/observations/" + obs + "-acs-" + str(time) + ".jpg", frame)
        else:
            print("There was an error loading the frame!")
    cap.release()
    destroyAllWindows()
