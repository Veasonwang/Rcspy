# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rcsui_Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1117, 868)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.current_time = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_time.sizePolicy().hasHeightForWidth())
        self.current_time.setSizePolicy(sizePolicy)
        self.current_time.setMinimumSize(QtCore.QSize(200, 0))
        self.current_time.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.current_time.setAlignment(QtCore.Qt.AlignCenter)
        self.current_time.setReadOnly(True)
        self.current_time.setObjectName("current_time")
        self.gridLayout_2.addWidget(self.current_time, 0, 13, 1, 1)
        self.zoomswitch = QtWidgets.QCheckBox(self.centralwidget)
        self.zoomswitch.setObjectName("zoomswitch")
        self.gridLayout_2.addWidget(self.zoomswitch, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 18, 1, 1)
        self.cursor_switch = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cursor_switch.sizePolicy().hasHeightForWidth())
        self.cursor_switch.setSizePolicy(sizePolicy)
        self.cursor_switch.setChecked(False)
        self.cursor_switch.setObjectName("cursor_switch")
        self.gridLayout_2.addWidget(self.cursor_switch, 0, 3, 1, 1)
        self.AmpUP = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AmpUP.sizePolicy().hasHeightForWidth())
        self.AmpUP.setSizePolicy(sizePolicy)
        self.AmpUP.setMaximumSize(QtCore.QSize(30, 16777215))
        self.AmpUP.setObjectName("AmpUP")
        self.gridLayout_2.addWidget(self.AmpUP, 0, 7, 1, 1)
        self.ZCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZCheckBox.sizePolicy().hasHeightForWidth())
        self.ZCheckBox.setSizePolicy(sizePolicy)
        self.ZCheckBox.setChecked(True)
        self.ZCheckBox.setObjectName("ZCheckBox")
        self.gridLayout_2.addWidget(self.ZCheckBox, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 15, 1, 1)
        self.X_press = QtWidgets.QPushButton(self.centralwidget)
        self.X_press.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.X_press.setFont(font)
        self.X_press.setObjectName("X_press")
        self.gridLayout_2.addWidget(self.X_press, 0, 11, 1, 1)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)
        self.reset.setMaximumSize(QtCore.QSize(50, 16777215))
        self.reset.setObjectName("reset")
        self.gridLayout_2.addWidget(self.reset, 0, 10, 1, 1)
        self.ECheckBox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ECheckBox.sizePolicy().hasHeightForWidth())
        self.ECheckBox.setSizePolicy(sizePolicy)
        self.ECheckBox.setChecked(True)
        self.ECheckBox.setObjectName("ECheckBox")
        self.gridLayout_2.addWidget(self.ECheckBox, 0, 6, 1, 1)
        self.Amp_display = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Amp_display.sizePolicy().hasHeightForWidth())
        self.Amp_display.setSizePolicy(sizePolicy)
        self.Amp_display.setMinimumSize(QtCore.QSize(80, 0))
        self.Amp_display.setMaximumSize(QtCore.QSize(80, 16777215))
        self.Amp_display.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.Amp_display.setAlignment(QtCore.Qt.AlignCenter)
        self.Amp_display.setReadOnly(True)
        self.Amp_display.setObjectName("Amp_display")
        self.gridLayout_2.addWidget(self.Amp_display, 0, 14, 1, 1)
        self.X_stretch = QtWidgets.QPushButton(self.centralwidget)
        self.X_stretch.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.X_stretch.setFont(font)
        self.X_stretch.setObjectName("X_stretch")
        self.gridLayout_2.addWidget(self.X_stretch, 0, 12, 1, 1)
        self.Ampdown = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Ampdown.sizePolicy().hasHeightForWidth())
        self.Ampdown.setSizePolicy(sizePolicy)
        self.Ampdown.setMaximumSize(QtCore.QSize(30, 16777215))
        self.Ampdown.setObjectName("Ampdown")
        self.gridLayout_2.addWidget(self.Ampdown, 0, 9, 1, 1)
        self.NCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NCheckBox.sizePolicy().hasHeightForWidth())
        self.NCheckBox.setSizePolicy(sizePolicy)
        self.NCheckBox.setChecked(True)
        self.NCheckBox.setObjectName("NCheckBox")
        self.gridLayout_2.addWidget(self.NCheckBox, 0, 5, 1, 1)
        self.drawnumber_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.drawnumber_combobox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.drawnumber_combobox.setObjectName("drawnumber_combobox")
        self.drawnumber_combobox.addItem("")
        self.drawnumber_combobox.addItem("")
        self.drawnumber_combobox.addItem("")
        self.drawnumber_combobox.addItem("")
        self.drawnumber_combobox.addItem("")
        self.gridLayout_2.addWidget(self.drawnumber_combobox, 0, 16, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(550, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.label_stationdrawnumber = QtWidgets.QLabel(self.centralwidget)
        self.label_stationdrawnumber.setObjectName("label_stationdrawnumber")
        self.gridLayout_2.addWidget(self.label_stationdrawnumber, 0, 17, 1, 1)
        self.dragenable_switch = QtWidgets.QCheckBox(self.centralwidget)
        self.dragenable_switch.setObjectName("dragenable_switch")
        self.gridLayout_2.addWidget(self.dragenable_switch, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.stationTree = QtWidgets.QTreeWidget(self.splitter)
        self.stationTree.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stationTree.sizePolicy().hasHeightForWidth())
        self.stationTree.setSizePolicy(sizePolicy)
        self.stationTree.setMaximumSize(QtCore.QSize(320, 16777215))
        self.stationTree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stationTree.setColumnCount(0)
        self.stationTree.setObjectName("stationTree")
        self.scrollArea = QcScrollArea(self.splitter)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.qmlcanvas = Qcwidget()
        self.qmlcanvas.setGeometry(QtCore.QRect(0, 0, 755, 755))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qmlcanvas.sizePolicy().hasHeightForWidth())
        self.qmlcanvas.setSizePolicy(sizePolicy)
        self.qmlcanvas.setObjectName("qmlcanvas")
        self.scrollArea.setWidget(self.qmlcanvas)
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 23))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menu_2 = QtWidgets.QMenu(self.menufile)
        self.menu_2.setObjectName("menu_2")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionEmseed = QtWidgets.QAction(MainWindow)
        self.actionEmseed.setObjectName("actionEmseed")
        self.actionEsac = QtWidgets.QAction(MainWindow)
        self.actionEsac.setObjectName("actionEsac")
        self.actionEseed = QtWidgets.QAction(MainWindow)
        self.actionEseed.setObjectName("actionEseed")
        self.actionRseed = QtWidgets.QAction(MainWindow)
        self.actionRseed.setObjectName("actionRseed")
        self.actionRminiseed = QtWidgets.QAction(MainWindow)
        self.actionRminiseed.setObjectName("actionRminiseed")
        self.actionRsac = QtWidgets.QAction(MainWindow)
        self.actionRsac.setObjectName("actionRsac")
        self.actionexport = QtWidgets.QAction(MainWindow)
        self.actionexport.setObjectName("actionexport")
        self.actionfiltering = QtWidgets.QAction(MainWindow)
        self.actionfiltering.setObjectName("actionfiltering")
        self.actionRInstrument_response = QtWidgets.QAction(MainWindow)
        self.actionRInstrument_response.setObjectName("actionRInstrument_response")
        self.actiondetrend = QtWidgets.QAction(MainWindow)
        self.actiondetrend.setObjectName("actiondetrend")
        self.menu_2.addAction(self.actionRseed)
        self.menu_2.addAction(self.actionRminiseed)
        self.menu_2.addAction(self.actionRsac)
        self.menufile.addAction(self.menu_2.menuAction())
        self.menufile.addAction(self.actionexport)
        self.menufile.addAction(self.actionexit)
        self.menu.addAction(self.actionfiltering)
        self.menu.addAction(self.actionRInstrument_response)
        self.menu.addAction(self.actiondetrend)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.stationTree.itemDoubleClicked['QTreeWidgetItem*','int'].connect(MainWindow._changeStationVisibility)
        self.cursor_switch.stateChanged['int'].connect(MainWindow._changebtn_cursor)
        self.ZCheckBox.stateChanged['int'].connect(MainWindow._changeSelectedChannel)
        self.NCheckBox.stateChanged['int'].connect(MainWindow._changeSelectedChannel)
        self.ECheckBox.stateChanged['int'].connect(MainWindow._changeSelectedChannel)
        self.AmpUP.clicked.connect(MainWindow._Ampup)
        self.Ampdown.clicked['bool'].connect(MainWindow._Ampdown)
        self.reset.clicked.connect(MainWindow._AmpReset)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rcspy"))
        self.current_time.setText(_translate("MainWindow", "YY-MM-DD hh-mm-ss.SSS"))
        self.zoomswitch.setText(_translate("MainWindow", "滚轮缩放"))
        self.cursor_switch.setText(_translate("MainWindow", "光标"))
        self.AmpUP.setText(_translate("MainWindow", "▲"))
        self.ZCheckBox.setText(_translate("MainWindow", "Z"))
        self.label_2.setText(_translate("MainWindow", "单屏道数"))
        self.X_press.setText(_translate("MainWindow", ">  <"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.ECheckBox.setText(_translate("MainWindow", "E"))
        self.Amp_display.setText(_translate("MainWindow", "μm/s"))
        self.X_stretch.setText(_translate("MainWindow", "<  >"))
        self.Ampdown.setText(_translate("MainWindow", "▼"))
        self.NCheckBox.setText(_translate("MainWindow", "N"))
        self.drawnumber_combobox.setItemText(0, _translate("MainWindow", "3"))
        self.drawnumber_combobox.setItemText(1, _translate("MainWindow", "6"))
        self.drawnumber_combobox.setItemText(2, _translate("MainWindow", "9"))
        self.drawnumber_combobox.setItemText(3, _translate("MainWindow", "12"))
        self.drawnumber_combobox.setItemText(4, _translate("MainWindow", "24"))
        self.label_stationdrawnumber.setText(_translate("MainWindow", "显示台站数：0"))
        self.dragenable_switch.setText(_translate("MainWindow", "左右拖动"))
        self.menufile.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "打开"))
        self.menu.setTitle(_translate("MainWindow", "预处理"))
        self.actionexit.setText(_translate("MainWindow", "退出"))
        self.actionEmseed.setText(_translate("MainWindow", ".mseed"))
        self.actionEsac.setText(_translate("MainWindow", ".sac"))
        self.actionEseed.setText(_translate("MainWindow", ".seed"))
        self.actionRseed.setText(_translate("MainWindow", "seed"))
        self.actionRminiseed.setText(_translate("MainWindow", "miniseed"))
        self.actionRsac.setText(_translate("MainWindow", "sac"))
        self.actionexport.setText(_translate("MainWindow", "导出"))
        self.actionfiltering.setText(_translate("MainWindow", "滤波"))
        self.actionRInstrument_response.setText(_translate("MainWindow", "去仪器响应"))
        self.actiondetrend.setText(_translate("MainWindow", "去倾"))

from util import QcScrollArea, Qcwidget
