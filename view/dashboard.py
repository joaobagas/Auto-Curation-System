# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboard.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from model import image_loader
from view import load_training_dialog, load_video_dialog, upload_dialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 490)
        MainWindow.setFixedWidth(690)
        MainWindow.setFixedHeight(490)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imageView = QtWidgets.QLabel(self.centralwidget)
        self.imageView.setGeometry(QtCore.QRect(10, 10, 671, 361))
        self.imageView.setText("")
        self.imageView.setPixmap(QtGui.QPixmap("img/black_image.jpg"))
        self.imageView.setObjectName("imageView")
        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(10, 410, 71, 23))
        self.trainButton.setObjectName("trainButton")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(10, 440, 71, 23))
        self.runButton.setObjectName("runButton")
        self.nameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLineEdit.setGeometry(QtCore.QRect(10, 380, 671, 20))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.forwardArrowButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardArrowButton.setGeometry(QtCore.QRect(430, 440, 81, 23))
        self.forwardArrowButton.setObjectName("forwardArrowButton")
        self.backArrowButton = QtWidgets.QPushButton(self.centralwidget)
        self.backArrowButton.setGeometry(QtCore.QRect(180, 440, 81, 23))
        self.backArrowButton.setObjectName("backArrowButton")
        self.deleteImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteImageButton.setGeometry(QtCore.QRect(270, 440, 151, 23))
        self.deleteImageButton.setObjectName("deleteImageButton")
        self.nextObsButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextObsButton.setGeometry(QtCore.QRect(430, 410, 81, 23))
        self.nextObsButton.setObjectName("nextObsButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(610, 440, 71, 23))
        self.exitButton.setObjectName("exitButton")
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(270, 410, 71, 23))
        self.uploadButton.setObjectName("uploadButton")
        self.previousObsButton = QtWidgets.QPushButton(self.centralwidget)
        self.previousObsButton.setGeometry(QtCore.QRect(180, 410, 81, 23))
        self.previousObsButton.setObjectName("previousObsButton")
        self.rejectButton = QtWidgets.QPushButton(self.centralwidget)
        self.rejectButton.setGeometry(QtCore.QRect(350, 410, 71, 23))
        self.rejectButton.setObjectName("rejectButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.exitButton.clicked.connect(exit)
        self.trainButton.clicked.connect(self.on_click_train)
        self.runButton.clicked.connect(self.on_click_run)
        self.uploadButton.clicked.connect(self.on_click_upload)

        self.previousObsButton.clicked.connect(self.on_click_previousObsButton)
        self.nextObsButton.clicked.connect(self.on_click_nextObsButton)
        self.backArrowButton.clicked.connect(self.on_click_backArrowButton)
        self.forwardArrowButton.clicked.connect(self.on_click_forwardArrowButton)

        self.rejectButton.clicked.connect(self.on_click_rejectButton)
        self.deleteImageButton.clicked.connect(self.on_click_deleteImageButton)

        image_loader.ImageLoader.__new__(image_loader.ImageLoader).load()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.trainButton.setText(_translate("MainWindow", "Train"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.forwardArrowButton.setText(_translate("MainWindow", "-->"))
        self.backArrowButton.setText(_translate("MainWindow", "<--"))
        self.deleteImageButton.setText(_translate("MainWindow", "Delete Image"))
        self.nextObsButton.setText(_translate("MainWindow", "Next obs."))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.uploadButton.setText(_translate("MainWindow", "Upload"))
        self.previousObsButton.setText(_translate("MainWindow", "Previous obs."))
        self.rejectButton.setText(_translate("MainWindow", "Reject"))

    def on_click_train(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = load_training_dialog.Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def on_click_run(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = load_video_dialog.Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def on_click_upload(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = upload_dialog.Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def on_click_previousObsButton(self):
        self.imageView.setPixmap(QtGui.QPixmap(image_loader.ImageLoader.__new__(image_loader.ImageLoader).prev_obs()))
        self.nameLineEdit.setText(image_loader.ImageLoader.__new__(image_loader.ImageLoader).get_obs())

    def on_click_nextObsButton(self):
        self.imageView.setPixmap(QtGui.QPixmap(image_loader.ImageLoader.__new__(image_loader.ImageLoader).next_obs()))
        self.nameLineEdit.setText(image_loader.ImageLoader.__new__(image_loader.ImageLoader).get_obs())

    def on_click_backArrowButton(self):
        self.imageView.setPixmap(QtGui.QPixmap(image_loader.ImageLoader.__new__(image_loader.ImageLoader).prev_photo()))

    def on_click_forwardArrowButton(self):
        self.imageView.setPixmap(QtGui.QPixmap(image_loader.ImageLoader.__new__(image_loader.ImageLoader).next_photo()))

    def on_click_rejectButton(self):
        image_loader.ImageLoader.__new__(image_loader.ImageLoader).delete_obs()

    def on_click_deleteImageButton(self):
        self.imageView.setPixmap(QtGui.QPixmap(image_loader.ImageLoader.__new__(image_loader.ImageLoader).delete_photo()))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
