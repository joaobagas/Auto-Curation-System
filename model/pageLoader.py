import sys

from pyqt5_plugins.examplebutton import QtWidgets

from view import dashboard


def load_dashboard():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = dashboard.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


def load_training_dialog():
    print("Training loaded!")


def load_video_dialog():
    print("Video dialog loaded!")


def load_upload_dialog():
    print("Upload dialog loaded!")