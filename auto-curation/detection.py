import tensorflow as tf

# https://github.com/microsoft/CameraTraps
def detect_animal(img):
    print(load_pb())

# https://stackoverflow.com/questions/51278213/what-is-the-use-of-a-pb-file-in-tensorflow-and-how-does-it-work
def load_pb():
    with tf.gfile.GFile("auto-curation/files/md_v4.1.0.pb", "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')
        return graph
