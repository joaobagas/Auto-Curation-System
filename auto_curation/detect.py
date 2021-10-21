import cv2
import tensorflow as tf

# import argparse
# import glob
# import sys
# import numpy as np
# import pandas as pd
# import tensorflow.compat.v1 as tf
# from CameraTraps.ct_utils import truncate_float

import os
import time
import warnings
import humanfriendly
import matplotlib.pyplot as plt
from PIL import Image, ImageFile, ImageFont, ImageDraw
import statistics
from tqdm import tqdm

from CameraTraps.detection.run_tf_detector import TFDetector, ImagePathUtils
from CameraTraps.visualization.visualization_utils import load_image, render_detection_bounding_boxes
#tf.config.run_functions_eagerly(True)

# From https://github.com/microsoft/CameraTraps/blob/master/detection/run_tf_detector.py
def load_and_run_detector_on_video(model_file, images, output_dir,
                          render_confidence_threshold=TFDetector.DEFAULT_RENDERING_CONFIDENCE_THRESHOLD):
    if len(images) == 0:
        print('Warning: no files available')
        return

    index = 0
    # load and run detector on target images, and visualize the results
    start_time = time.time()
    tf_detector = TFDetector(model_file)
    elapsed = time.time() - start_time
    print('Loaded model in {}'.format(humanfriendly.format_timespan(elapsed)))

    detection_results = []
    time_load = []
    time_infer = []
    detection_categories = []

    # since we'll be writing a bunch of files to the same folder, rename
    # as necessary to avoid collisions
    output_file_names = {}

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
        """
        try:
            # image is modified in place
            render_detection_bounding_boxes(result['detections'], image,
                                            label_map=TFDetector.DEFAULT_DETECTOR_LABEL_MAP,
                                            confidence_threshold=render_confidence_threshold)
            fn = os.path.basename("Image: " + str(index)).lower()
            name, ext = os.path.splitext(fn)
            fn = '{}{}{}'.format(name, ImagePathUtils.DETECTION_FILENAME_INSERT, '.jpg')  # save all as JPG
            if fn in output_file_names:
                n_collisions = output_file_names[fn]  # if there were a collision, the count is at least 1
                fn = str(n_collisions) + '_' + fn
                output_file_names[fn] = n_collisions + 1
            else:
                output_file_names[fn] = 0

            output_full_path = os.path.join(output_dir, fn)
            image.save(output_full_path)
        except Exception as e:
            print('Visualizing results on the image {} failed. Exception: {}'.format("Image: " + str(index), e))
            continue

    ave_time_infer = statistics.mean(time_infer)
    if len(time_load) > 1 and len(time_infer) > 1:
        std_dev_time_infer = humanfriendly.format_timespan(statistics.stdev(time_infer))
    else:
        std_dev_time_infer = 'not available'
    print('On average, for each image,')
    print('- inference took {}, std dev is {}'.format(humanfriendly.format_timespan(ave_time_infer),
                                                      std_dev_time_infer))
    """
    return detection_results

def translate_to_tf(imgs):
    translated_imgs = []
    for img_bgr in imgs:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
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
