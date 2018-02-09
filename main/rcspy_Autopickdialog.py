# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rcspy_Autopickdialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.setEnabled(True)
        Dialog.resize(600, 370)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(600, 370))
        Dialog.setMaximumSize(QtCore.QSize(600, 370))
        self.File_list = QtWidgets.QListWidget(Dialog)
        self.File_list.setGeometry(QtCore.QRect(10, 40, 201, 301))
        self.File_list.setObjectName("File_list")
        self.channel_list = QtWidgets.QListWidget(Dialog)
        self.channel_list.setGeometry(QtCore.QRect(220, 40, 111, 281))
        self.channel_list.setObjectName("channel_list")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(210, 20, 54, 12))
        self.label_4.setObjectName("label_4")
        self.btnOK = QtWidgets.QPushButton(Dialog)
        self.btnOK.setGeometry(QtCore.QRect(370, 300, 75, 23))
        self.btnOK.setObjectName("btnOK")
        self.btn_Cancel = QtWidgets.QPushButton(Dialog)
        self.btn_Cancel.setGeometry(QtCore.QRect(490, 300, 75, 23))
        self.btn_Cancel.setObjectName("btn_Cancel")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(340, 10, 251, 331))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 121, 31))
        self.label.setObjectName("label")
        self.low_frq = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.low_frq.setGeometry(QtCore.QRect(170, 30, 71, 31))
        self.low_frq.setDecimals(2)
        self.low_frq.setSingleStep(0.01)
        self.low_frq.setProperty("value", 1.0)
        self.low_frq.setObjectName("low_frq")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 121, 31))
        self.label_2.setObjectName("label_2")
        self.upp_frq = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.upp_frq.setGeometry(QtCore.QRect(170, 70, 71, 31))
        self.upp_frq.setDecimals(2)
        self.upp_frq.setMaximum(200.0)
        self.upp_frq.setSingleStep(0.01)
        self.upp_frq.setProperty("value", 20.0)
        self.upp_frq.setObjectName("upp_frq")
        self.lta_p = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.lta_p.setGeometry(QtCore.QRect(50, 110, 71, 31))
        self.lta_p.setMaximum(3600.0)
        self.lta_p.setSingleStep(0.1)
        self.lta_p.setProperty("value", 1.0)
        self.lta_p.setObjectName("lta_p")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 41, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 150, 41, 31))
        self.label_6.setObjectName("label_6")
        self.sta_p = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.sta_p.setGeometry(QtCore.QRect(50, 150, 71, 31))
        self.sta_p.setMaximum(3600.0)
        self.sta_p.setSingleStep(0.1)
        self.sta_p.setProperty("value", 0.1)
        self.sta_p.setObjectName("sta_p")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(130, 110, 41, 31))
        self.label_7.setObjectName("label_7")
        self.sta_s = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.sta_s.setGeometry(QtCore.QRect(170, 150, 71, 31))
        self.sta_s.setMaximum(3600.0)
        self.sta_s.setProperty("value", 1.0)
        self.sta_s.setObjectName("sta_s")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(130, 150, 41, 31))
        self.label_8.setObjectName("label_8")
        self.lta_s = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.lta_s.setGeometry(QtCore.QRect(170, 110, 71, 31))
        self.lta_s.setMaximum(3600.0)
        self.lta_s.setSingleStep(0.1)
        self.lta_s.setProperty("value", 4.0)
        self.lta_s.setObjectName("lta_s")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(130, 190, 41, 31))
        self.label_9.setObjectName("label_9")
        self.m_s = QtWidgets.QSpinBox(self.groupBox)
        self.m_s.setGeometry(QtCore.QRect(170, 190, 71, 31))
        self.m_s.setProperty("value", 8)
        self.m_s.setObjectName("m_s")
        self.m_p = QtWidgets.QSpinBox(self.groupBox)
        self.m_p.setGeometry(QtCore.QRect(50, 190, 71, 31))
        self.m_p.setProperty("value", 2)
        self.m_p.setObjectName("m_p")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 190, 41, 31))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(130, 230, 31, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 230, 31, 31))
        self.label_12.setObjectName("label_12")
        self.l_p = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.l_p.setGeometry(QtCore.QRect(50, 230, 71, 31))
        self.l_p.setMaximum(3600.0)
        self.l_p.setSingleStep(0.1)
        self.l_p.setProperty("value", 0.1)
        self.l_p.setObjectName("l_p")
        self.l_s = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.l_s.setGeometry(QtCore.QRect(170, 230, 71, 31))
        self.l_s.setMaximum(3600.0)
        self.l_s.setSingleStep(0.1)
        self.l_s.setProperty("value", 0.2)
        self.l_s.setObjectName("l_s")
        self.allchannel_checkbox = QtWidgets.QCheckBox(Dialog)
        self.allchannel_checkbox.setGeometry(QtCore.QRect(220, 320, 97, 31))
        self.allchannel_checkbox.setObjectName("allchannel_checkbox")
        self.groupBox.raise_()
        self.File_list.raise_()
        self.channel_list.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.btnOK.raise_()
        self.btn_Cancel.raise_()
        self.allchannel_checkbox.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "震相自动拾取"))
        self.label_3.setText(_translate("Dialog", "文件名"))
        self.label_4.setText(_translate("Dialog", "通道"))
        self.btnOK.setText(_translate("Dialog", "确认"))
        self.btn_Cancel.setText(_translate("Dialog", "取消"))
        self.groupBox.setTitle(_translate("Dialog", "ar_pick"))
        self.label.setToolTip(_translate("Dialog", "Frequency of the lower bandpass window."))
        self.label.setText(_translate("Dialog", "Lower frequency "))
        self.low_frq.setToolTip(_translate("Dialog", "Frequency of the lower bandpass window."))
        self.label_2.setToolTip(_translate("Dialog", "Frequency of the upper .andpass window."))
        self.label_2.setText(_translate("Dialog", "Upper frequency "))
        self.upp_frq.setToolTip(_translate("Dialog", "Frequency of the upper .andpass window."))
        self.lta_p.setToolTip(_translate("Dialog", "Length of LTA for the P arrival in seconds."))
        self.label_5.setToolTip(_translate("Dialog", "Length of LTA for the P arrival in seconds."))
        self.label_5.setText(_translate("Dialog", "lta_p"))
        self.label_6.setToolTip(_translate("Dialog", "Length of STA for the P arrival in seconds."))
        self.label_6.setText(_translate("Dialog", "sta_p"))
        self.sta_p.setToolTip(_translate("Dialog", "Length of STA for the P arrival in seconds."))
        self.label_7.setToolTip(_translate("Dialog", "Length of LTA for the S arrival in seconds."))
        self.label_7.setText(_translate("Dialog", "lta_s"))
        self.sta_s.setToolTip(_translate("Dialog", "Length of STA for the S arrival in seconds."))
        self.label_8.setToolTip(_translate("Dialog", "Length of STA for the S arrival in seconds."))
        self.label_8.setText(_translate("Dialog", "sta_s"))
        self.lta_s.setToolTip(_translate("Dialog", "Length of LTA for the S arrival in seconds."))
        self.label_9.setToolTip(_translate("Dialog", "Number of AR coefficients for the S arrival."))
        self.label_9.setText(_translate("Dialog", "m_s"))
        self.m_s.setToolTip(_translate("Dialog", "Number of AR coefficients for the S arrival."))
        self.m_p.setToolTip(_translate("Dialog", "Number of AR coefficients for the P arrival."))
        self.label_10.setToolTip(_translate("Dialog", "Number of AR coefficients for the P arrival."))
        self.label_10.setText(_translate("Dialog", "m_p"))
        self.label_11.setToolTip(_translate("Dialog", "Length of variance window for the S arrival in seconds."))
        self.label_11.setText(_translate("Dialog", "l_s"))
        self.label_12.setToolTip(_translate("Dialog", "Length of variance window for the P arrival in seconds."))
        self.label_12.setText(_translate("Dialog", "l_p"))
        self.l_p.setToolTip(_translate("Dialog", "Length of variance window for the P arrival in seconds."))
        self.l_s.setToolTip(_translate("Dialog", "Length of variance window for the S arrival in seconds."))
        self.allchannel_checkbox.setText(_translate("Dialog", "所有通道"))

