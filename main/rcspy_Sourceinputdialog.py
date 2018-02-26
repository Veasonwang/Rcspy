# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rcspy_Sourceinputdialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(220, 185)
        Dialog.setMaximumSize(QtCore.QSize(220, 185))
        self.btn_ok = QtWidgets.QPushButton(Dialog)
        self.btn_ok.setGeometry(QtCore.QRect(44, 140, 51, 23))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_back = QtWidgets.QPushButton(Dialog)
        self.btn_back.setGeometry(QtCore.QRect(130, 140, 51, 23))
        self.btn_back.setObjectName("btn_back")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 51, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 100, 51, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(20, 60, 51, 17))
        self.label_8.setObjectName("label_8")
        self.longitude = QtWidgets.QLineEdit(Dialog)
        self.longitude.setGeometry(QtCore.QRect(80, 20, 111, 20))
        self.longitude.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.longitude.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.longitude.setAlignment(QtCore.Qt.AlignCenter)
        self.longitude.setObjectName("longitude")
        self.latitude = QtWidgets.QLineEdit(Dialog)
        self.latitude.setGeometry(QtCore.QRect(80, 60, 111, 20))
        self.latitude.setAlignment(QtCore.Qt.AlignCenter)
        self.latitude.setObjectName("latitude")
        self.depth = QtWidgets.QLineEdit(Dialog)
        self.depth.setGeometry(QtCore.QRect(80, 100, 111, 20))
        self.depth.setFrame(True)
        self.depth.setAlignment(QtCore.Qt.AlignCenter)
        self.depth.setObjectName("depth")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "震源输入"))
        self.btn_ok.setText(_translate("Dialog", "OK"))
        self.btn_back.setText(_translate("Dialog", "Back"))
        self.label_6.setText(_translate("Dialog", "经度(度)"))
        self.label_7.setText(_translate("Dialog", "深度(km)"))
        self.label_8.setText(_translate("Dialog", "纬度(度)"))

