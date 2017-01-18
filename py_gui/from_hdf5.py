# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'from_hdf5.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(700, 136)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.out_graph_btn = QtGui.QPushButton(Dialog)
        self.out_graph_btn.setObjectName(_fromUtf8("out_graph_btn"))
        self.gridLayout_3.addWidget(self.out_graph_btn, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 1)
        self.cancel_btn = QtGui.QPushButton(Dialog)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.gridLayout_3.addWidget(self.cancel_btn, 3, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        self.stop_btn = QtGui.QPushButton(Dialog)
        self.stop_btn.setObjectName(_fromUtf8("stop_btn"))
        self.gridLayout_3.addWidget(self.stop_btn, 3, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.h5_browse_btn = QtGui.QPushButton(Dialog)
        self.h5_browse_btn.setObjectName(_fromUtf8("h5_browse_btn"))
        self.gridLayout.addWidget(self.h5_browse_btn, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lockbox_browse_btn = QtGui.QPushButton(Dialog)
        self.lockbox_browse_btn.setObjectName(_fromUtf8("lockbox_browse_btn"))
        self.gridLayout.addWidget(self.lockbox_browse_btn, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lockbox_path = QtGui.QLineEdit(Dialog)
        self.lockbox_path.setObjectName(_fromUtf8("lockbox_path"))
        self.gridLayout.addWidget(self.lockbox_path, 1, 1, 1, 1)
        self.h5_path = QtGui.QLineEdit(Dialog)
        self.h5_path.setObjectName(_fromUtf8("h5_path"))
        self.gridLayout.addWidget(self.h5_path, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "From HDF5", None))
        self.out_graph_btn.setText(_translate("Dialog", "Output Graph", None))
        self.cancel_btn.setText(_translate("Dialog", "Cancel", None))
        self.stop_btn.setText(_translate("Dialog", "Stop", None))
        self.h5_browse_btn.setText(_translate("Dialog", "Browse...", None))
        self.label_2.setText(_translate("Dialog", "HDF5 Path:", None))
        self.lockbox_browse_btn.setText(_translate("Dialog", "Browse...", None))
        self.label_3.setText(_translate("Dialog", "LockBox Path:", None))

