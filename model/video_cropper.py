# This file holds the function which is used to crop frames off a video and save them.
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def crop(location, obs, times):
    # The imports had to be placed inside of the function due to incompatibilities between PyQt5 and Open-CV
    from cv2 import VideoCapture, imwrite, destroyAllWindows

    cap = VideoCapture(location)

    for time in times:
        cap.set(1, time)
        ret, frame = cap.read()
        if ret:
            imwrite("img/observations/" + obs + "-acs-" + str(time) + ".jpg", frame)
        else:
            print("There was an error loading the frame!")
    cap.release()
    destroyAllWindows()


def trim(video, start, end, title):
    # End and start are displayed in seconds
    path = title + ".mp4"
    ffmpeg_extract_subclip(video, start, end, targetname=path)
