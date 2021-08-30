# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadTrainingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from model import training_manager


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(385, 123)
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
        self.cancelButton.setGeometry(QtCore.QRect(310, 90, 71, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.trainButton = QtWidgets.QPushButton(Dialog)
        self.trainButton.setGeometry(QtCore.QRect(230, 90, 71, 23))
        self.trainButton.setObjectName("trainButton")
        self.statusLabel = QtWidgets.QLabel(Dialog)
        self.statusLabel.setGeometry(QtCore.QRect(10, 70, 371, 16))
        self.statusLabel.setObjectName("statusLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.progressBar.setValue(0)
        self.browseButton.clicked.connect(self.on_click_browse)
        self.trainButton.clicked.connect(self.on_click_train)
        self.cancelButton.clicked.connect(Dialog.close)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Train"))
        self.browseButton.setText(_translate("Dialog", "Browse"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.trainButton.setText(_translate("Dialog", "Train"))
        self.statusLabel.setText(_translate("Dialog", "Status:"))

    def on_click_browse(self):
        fname = QFileDialog.getOpenFileName(None, "Open file")
        self.lineEdit.setText(fname[0])

    def on_click_train(self):
        self.progressBar.setMaximum(100)
        t = training_manager.TrainingManager()
        t.train(self.progressBar)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
