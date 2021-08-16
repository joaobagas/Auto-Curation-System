import cv2


def crop(location, obs, times):
    cap = cv2.VideoCapture(location)

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
            cv2.imshow("frame", frame)
            cv2.waitKey()
            cv2.imwrite("img/observations/" + obs + "-acs-" + str(time) + ".jpg", frame)
        else:
            print("There was an error loading the frame!")
    cap.release()
    cv2.destroyAllWindows()