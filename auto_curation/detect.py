import cv2
import tensorflow as tf
import time
import humanfriendly
from PIL import ImageDraw
from matplotlib import pyplot as plt

from CameraTraps.detection.run_tf_detector import TFDetector


# From https://github.com/microsoft/CameraTraps/blob/master/detection/run_tf_detector.py
def load_and_run_detector_on_video(model_file, images, output_dir,
                          render_confidence_threshold=TFDetector.DEFAULT_RENDERING_CONFIDENCE_THRESHOLD):
    if len(images) == 0:
        print('Warning: no files available')
        return

    index = 0
    start_time = time.time()
    tf_detector = TFDetector(model_file)
    elapsed = time.time() - start_time
    print('Loaded model in {}'.format(humanfriendly.format_timespan(elapsed)))

    detection_results = []
    time_infer = []
    detection_categories = []

    for image in images:
        index += 1
        try:
            start_time = time.time()
            result = tf_detector.generate_detections_one_image(image, "Image: " + str(index))
            print("Detection result is:", result)
            detection_results.append(result)
            if result["detections"] == []:
                detection_categories.append(0)
            else:
                detection_categories.append(result["detections"][0]["category"])

            elapsed = time.time() - start_time
            time_infer.append(elapsed)
        except Exception as e:
            print('An error occurred while running the detector on image {}. Exception: {}'.format("Image: " + str(index), e))
            # the error code and message is written by generate_detections_one_image,
            # which is wrapped in a big try catch
            continue
    return detection_results

def translate_to_tf(imgs):
    translated_imgs = []
    for img_bgr in imgs:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (500, 500))
        img_tensor = tf.convert_to_tensor(img_rgb, dtype=tf.float32)
        translated_imgs.append(img_tensor)
    return translated_imgs

def draw_bboxs(detections_list, im):
    for detection in detections_list:
        x1, y1, w_box, h_box = detection["bbox"]
        ymin, xmin, ymax, xmax = y1, x1, y1 + h_box, x1 + w_box
        draw = ImageDraw.Draw(im)

        imageWidth = im.size[0]
        imageHeight = im.size[1]
        (left, right, top, bottom) = (xmin * imageWidth, xmax * imageWidth,
                                      ymin * imageHeight, ymax * imageHeight)
        draw.line([(left, top), (left, bottom), (right, bottom),
                   (right, top), (left, top)], width=4, fill='Red')
