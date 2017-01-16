# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resolution_analyse.ui'
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
        Dialog.resize(406, 83)
        Dialog.setMinimumSize(QtCore.QSize(406, 83))
        Dialog.setMaximumSize(QtCore.QSize(406, 83))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.from_vdo_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.from_vdo_btn.sizePolicy().hasHeightForWidth())
        self.from_vdo_btn.setSizePolicy(sizePolicy)
        self.from_vdo_btn.setObjectName(_fromUtf8("from_vdo_btn"))
        self.verticalLayout_2.addWidget(self.from_vdo_btn)
        self.from_hdf5_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.from_hdf5_btn.sizePolicy().hasHeightForWidth())
        self.from_hdf5_btn.setSizePolicy(sizePolicy)
        self.from_hdf5_btn.setObjectName(_fromUtf8("from_hdf5_btn"))
        self.verticalLayout_2.addWidget(self.from_hdf5_btn)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "RESOLUTION ANALYSE", None))
        self.from_vdo_btn.setText(_translate("Dialog", "From VDO...", None))
        self.from_hdf5_btn.setText(_translate("Dialog", "From HDF5...", None))

