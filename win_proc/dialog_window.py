# coding: utf-8
from PyQt4 import QtGui
__author__ = 'gao.shulin'


class DialogWindow(QtGui.QDialog):
    # set common features used by QDialog

    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)

    def set_path(self, lineEdit_path):
        file_name = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        if file_name is not '':
            lineEdit_path.setText(file_name)

    def show_warning(self, message):
        QtGui.QMessageBox.critical(
            self, "Warning", message, QtGui.QMessageBox.Ok)

    def show_info(self, message):
        QtGui.QMessageBox.information(self, "Information!", message)
