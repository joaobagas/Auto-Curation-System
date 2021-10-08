import tensorflow as tf

import argparse
import glob
import os
import sys
import time
import warnings
import humanfriendly
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageFile, ImageFont, ImageDraw
import statistics
from tqdm import tqdm
import tensorflow.compat.v1 as tf

from CameraTraps.detection.run_tf_detector import TFDetector
from CameraTraps.visualization.visualization_utils import load_image
from CameraTraps.ct_utils import truncate_float


def start():
    tf.disable_v2_behavior()
    warnings.filterwarnings('ignore', '(Possibly )?corrupt EXIF data', UserWarning)
    warnings.filterwarnings('ignore', 'Metadata warning', UserWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    print('TensorFlow version:', tf.__version__)
    print('Is GPU available? tf.test.is_gpu_available:', tf.test.is_gpu_available())

def detect_animal():
    image_file_names = ["test.jpeg"]
    model_file = "files/md_v4.1.0.pb"
    output_dir = "./result"

    detection_results = load_and_run_detector(model_file, image_file_names, output_dir, render_confidence_threshold=0.5)
    print("----Results----")
    print(detection_results)
    print("---------------")

    # size = (480,270)
    size = (1000, 676)
    im = Image.open("test.jpeg")
    im = im.resize(size)

    # Overwrite bbox
    draw_bboxs(detection_results[0]['detections'], im)

    # Show
    plt.imshow(im)
    plt.show()
    plt.title(f"image with bbox")

# From https://github.com/microsoft/CameraTraps/blob/master/detection/run_tf_detector.py
def load_and_run_detector(model_file, image_file_names, output_dir,
                          render_confidence_threshold=TFDetector.DEFAULT_RENDERING_CONFIDENCE_THRESHOLD):
    if len(image_file_names) == 0:
        print('Warning: no files available')
        return

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

    for im_file in tqdm(image_file_names):
        try:
            start_time = time.time()

            image = load_image(im_file)

            elapsed = time.time() - start_time
            time_load.append(elapsed)
            print(time_load)
        except Exception as e:
            print('Image {} cannot be loaded. Exception: {}'.format(im_file, e))
            result = {
                'file': im_file,
                'failure': TFDetector.FAILURE_IMAGE_OPEN
            }
            detection_results.append(result)
            continue

        try:
            start_time = time.time()

            result = tf_detector.generate_detections_one_image(image, im_file)

            # print("Detection result is:", result)

            detection_results.append(result)

            if result["detections"] == []:
                detection_categories.append(0)
            else:

                detection_categories.append(result["detections"][0]["category"])

            elapsed = time.time() - start_time
            time_infer.append(elapsed)
        except Exception as e:
            print('An error occurred while running the detector on image {}. Exception: {}'.format(im_file, e))
            # the error code and message is written by generate_detections_one_image,
            # which is wrapped in a big try catch
            continue

        try:
            # image is modified in place
            render_detection_bounding_boxes(result['detections'], image,
                                            label_map=TFDetector.DEFAULT_DETECTOR_LABEL_MAP,
                                            confidence_threshold=render_confidence_threshold)
            fn = os.path.basename(im_file).lower()
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
            print('Visualizing results on the image {} failed. Exception: {}'.format(im_file, e))
            continue

    ave_time_load = statistics.mean(time_load)
    ave_time_infer = statistics.mean(time_infer)
    if len(time_load) > 1 and len(time_infer) > 1:
        std_dev_time_load = humanfriendly.format_timespan(statistics.stdev(time_load))
        std_dev_time_infer = humanfriendly.format_timespan(statistics.stdev(time_infer))
    else:
        std_dev_time_load = 'not available'
        std_dev_time_infer = 'not available'
    print('On average, for each image,')
    print('- loading took {}, std dev is {}'.format(humanfriendly.format_timespan(ave_time_load),
                                                    std_dev_time_load))
    print('- inference took {}, std dev is {}'.format(humanfriendly.format_timespan(ave_time_infer),
                                                      std_dev_time_infer))

    return detection_results


def draw_bboxs(detections_list, im):
    """
    detections_list: list of set includes bbox.
    im: image read by Pillow.
    """

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

# This might not be used
# https://stackoverflow.com/questions/51278213/what-is-the-use-of-a-pb-file-in-tensorflow-and-how-does-it-work
def load_pb():
    with tf.io.gfile.GFile("files/md_v4.1.0.pb", "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')
        return graph
