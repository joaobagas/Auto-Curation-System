from PyQt5.QtWidgets import QMessageBox


def warning(error):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error: " + error)
    msg.setWindowTitle("Error")
    msg.exec_()