# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'from_vdo.ui'
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
        Dialog.resize(790, 307)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 3, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.pano_tab = QtGui.QWidget()
        self.pano_tab.setObjectName(_fromUtf8("pano_tab"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.pano_tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 291, 41))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.checkBox_3 = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.gridLayout_3.addWidget(self.checkBox_3, 1, 2, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout_3.addWidget(self.checkBox_2, 1, 1, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_3.addWidget(self.checkBox, 1, 0, 1, 1)
        self.tabWidget.addTab(self.pano_tab, _fromUtf8(""))
        self.line_tab = QtGui.QWidget()
        self.line_tab.setObjectName(_fromUtf8("line_tab"))
        self.gridLayoutWidget_3 = QtGui.QWidget(self.line_tab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 391, 41))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.checkBox_7 = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.gridLayout_4.addWidget(self.checkBox_7, 1, 1, 1, 1)
        self.checkBox_4 = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.gridLayout_4.addWidget(self.checkBox_4, 1, 4, 1, 1)
        self.checkBox_5 = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.gridLayout_4.addWidget(self.checkBox_5, 1, 3, 1, 1)
        self.checkBox_6 = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.gridLayout_4.addWidget(self.checkBox_6, 1, 0, 1, 1)
        self.checkBox_8 = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        self.gridLayout_4.addWidget(self.checkBox_8, 1, 2, 1, 1)
        self.gridLayoutWidget_4 = QtGui.QWidget(self.line_tab)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 50, 391, 41))
        self.gridLayoutWidget_4.setObjectName(_fromUtf8("gridLayoutWidget_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.checkBox_9 = QtGui.QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))
        self.gridLayout_5.addWidget(self.checkBox_9, 1, 1, 1, 1)
        self.checkBox_10 = QtGui.QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_10.setObjectName(_fromUtf8("checkBox_10"))
        self.gridLayout_5.addWidget(self.checkBox_10, 1, 4, 1, 1)
        self.checkBox_11 = QtGui.QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_11.setObjectName(_fromUtf8("checkBox_11"))
        self.gridLayout_5.addWidget(self.checkBox_11, 1, 3, 1, 1)
        self.checkBox_12 = QtGui.QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_12.setObjectName(_fromUtf8("checkBox_12"))
        self.gridLayout_5.addWidget(self.checkBox_12, 1, 0, 1, 1)
        self.checkBox_13 = QtGui.QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_13.setObjectName(_fromUtf8("checkBox_13"))
        self.gridLayout_5.addWidget(self.checkBox_13, 1, 2, 1, 1)
        self.tabWidget.addTab(self.line_tab, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_5 = QtGui.QPushButton(Dialog)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_2.setChecked)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_3.setChecked)
        QtCore.QObject.connect(self.checkBox_6, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_7.setChecked)
        QtCore.QObject.connect(self.checkBox_6, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_8.setChecked)
        QtCore.QObject.connect(self.checkBox_6, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_5.setChecked)
        QtCore.QObject.connect(self.checkBox_6, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_4.setChecked)
        QtCore.QObject.connect(self.checkBox_12, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_9.setChecked)
        QtCore.QObject.connect(self.checkBox_12, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_13.setChecked)
        QtCore.QObject.connect(self.checkBox_12, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_11.setChecked)
        QtCore.QObject.connect(self.checkBox_12, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.checkBox_10.setChecked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "From VDO...", None))
        self.pushButton_2.setText(_translate("Dialog", "Browse...", None))
        self.label_2.setText(_translate("Dialog", "VDO Path:", None))
        self.pushButton_3.setText(_translate("Dialog", "Browse...", None))
        self.label_3.setText(_translate("Dialog", "Save Path:", None))
        self.pushButton.setText(_translate("Dialog", "Browse...", None))
        self.label.setText(_translate("Dialog", "LockBox Path:", None))
        self.checkBox_3.setText(_translate("Dialog", "c51", None))
        self.checkBox_2.setText(_translate("Dialog", "c50", None))
        self.checkBox.setText(_translate("Dialog", "pano_cam", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pano_tab), _translate("Dialog", "PANO_CAM", None))
        self.checkBox_7.setText(_translate("Dialog", "60", None))
        self.checkBox_4.setText(_translate("Dialog", "65", None))
        self.checkBox_5.setText(_translate("Dialog", "64", None))
        self.checkBox_6.setText(_translate("Dialog", "cam_6", None))
        self.checkBox_8.setText(_translate("Dialog", "61", None))
        self.checkBox_9.setText(_translate("Dialog", "70", None))
        self.checkBox_10.setText(_translate("Dialog", "75", None))
        self.checkBox_11.setText(_translate("Dialog", "74", None))
        self.checkBox_12.setText(_translate("Dialog", "cam_7", None))
        self.checkBox_13.setText(_translate("Dialog", "71", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.line_tab), _translate("Dialog", "LINE_CAM", None))
        self.pushButton_5.setText(_translate("Dialog", "Output Graph", None))
        self.pushButton_4.setText(_translate("Dialog", "Cancel", None))

