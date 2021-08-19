# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadVideoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from model import video_cropper
from model.image_loader import ImageLoader


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(385, 111)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 291, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.browseButton = QtWidgets.QPushButton(Dialog)
        self.browseButton.setGeometry(QtCore.QRect(310, 10, 71, 23))
        self.browseButton.setObjectName("browseButton")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 361, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(310, 80, 71, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(230, 80, 71, 23))
        self.runButton.setObjectName("runButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.browseButton.clicked.connect(self.browse)
        self.runButton.clicked.connect(self.run)
        self.cancelButton.clicked.connect(Dialog.close)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.browseButton.setText(_translate("Dialog", "Browse"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.runButton.setText(_translate("Dialog", "Run"))

    def browse(self):
        fname = QFileDialog.getOpenFileName(None, "Open file", r"C:\Users\joaob\OneDrive\Documents\Downloads")
        self.lineEdit.setText(fname[0])

    def run(self):
        video_cropper.crop(self.lineEdit.text(), "Test", [1000, 1005])
        ImageLoader.__new__(ImageLoader).load()
        self.cancelButton.click()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
