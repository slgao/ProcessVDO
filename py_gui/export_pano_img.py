# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_pano_img.ui'
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
        Dialog.resize(830, 265)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.vdo_browse_btn = QtGui.QPushButton(Dialog)
        self.vdo_browse_btn.setObjectName(_fromUtf8("vdo_browse_btn"))
        self.gridLayout.addWidget(self.vdo_browse_btn, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.img_save_browse_btn = QtGui.QPushButton(Dialog)
        self.img_save_browse_btn.setObjectName(_fromUtf8("img_save_browse_btn"))
        self.gridLayout.addWidget(self.img_save_browse_btn, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.img_save_path = QtGui.QLineEdit(Dialog)
        self.img_save_path.setObjectName(_fromUtf8("img_save_path"))
        self.gridLayout.addWidget(self.img_save_path, 1, 1, 1, 1)
        self.vdo_path = QtGui.QLineEdit(Dialog)
        self.vdo_path.setObjectName(_fromUtf8("vdo_path"))
        self.gridLayout.addWidget(self.vdo_path, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dpc_img_csv_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dpc_img_csv_btn.sizePolicy().hasHeightForWidth())
        self.dpc_img_csv_btn.setSizePolicy(sizePolicy)
        self.dpc_img_csv_btn.setObjectName(_fromUtf8("dpc_img_csv_btn"))
        self.horizontalLayout.addWidget(self.dpc_img_csv_btn)
        self.out_pano_img_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.out_pano_img_btn.sizePolicy().hasHeightForWidth())
        self.out_pano_img_btn.setSizePolicy(sizePolicy)
        self.out_pano_img_btn.setObjectName(_fromUtf8("out_pano_img_btn"))
        self.horizontalLayout.addWidget(self.out_pano_img_btn)
        self.cancel_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_btn.sizePolicy().hasHeightForWidth())
        self.cancel_btn.setSizePolicy(sizePolicy)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 8, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 7, 0, 1, 1)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 40, 291, 41))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.checkBox_c51 = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_c51.setObjectName(_fromUtf8("checkBox_c51"))
        self.gridLayout_3.addWidget(self.checkBox_c51, 1, 2, 1, 1)
        self.checkBox_c50 = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_c50.setObjectName(_fromUtf8("checkBox_c50"))
        self.gridLayout_3.addWidget(self.checkBox_c50, 1, 1, 1, 1)
        self.checkBox_pano_cam = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_pano_cam.setObjectName(_fromUtf8("checkBox_pano_cam"))
        self.gridLayout_3.addWidget(self.checkBox_pano_cam, 1, 0, 1, 1)
        self.gridLayoutWidget_3 = QtGui.QWidget(self.frame)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 0, 231, 41))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.checkBox_img_export = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_img_export.setObjectName(_fromUtf8("checkBox_img_export"))
        self.gridLayout_4.addWidget(self.checkBox_img_export, 1, 0, 1, 1)
        self.checkBox_multi_folder = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_multi_folder.setObjectName(_fromUtf8("checkBox_multi_folder"))
        self.gridLayout_4.addWidget(self.checkBox_multi_folder, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.checkBox_pano_cam, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_c50.setChecked)
        QtCore.QObject.connect(self.checkBox_pano_cam, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_c51.setChecked)
        QtCore.QObject.connect(self.cancel_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "EXPORT PANO IMG", None))
        self.vdo_browse_btn.setText(_translate("Dialog", "Browse...", None))
        self.label_2.setText(_translate("Dialog", "VDO Path:", None))
        self.img_save_browse_btn.setText(_translate("Dialog", "Browse...", None))
        self.label_3.setText(_translate("Dialog", "Img Save Path:", None))
        self.dpc_img_csv_btn.setText(_translate("Dialog", "DPC Img CSV", None))
        self.out_pano_img_btn.setText(_translate("Dialog", "Output Pano Img", None))
        self.cancel_btn.setText(_translate("Dialog", "Cancel", None))
        self.checkBox_c51.setText(_translate("Dialog", "c51", None))
        self.checkBox_c50.setText(_translate("Dialog", "c50", None))
        self.checkBox_pano_cam.setText(_translate("Dialog", "pano_cam", None))
        self.checkBox_img_export.setText(_translate("Dialog", "img_export", None))
        self.checkBox_multi_folder.setText(_translate("Dialog", "multi_folder(run_day)", None))

