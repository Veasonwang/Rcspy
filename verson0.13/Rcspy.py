import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
# -*- coding: ascii -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
import rcsui
import sys
from UI_Container import *


class Rcspy(rcsui.Ui_MainWindow,QMainWindow):
    def __init__(self,parent=None):
        app = QApplication(sys.argv)
        super(Rcspy,self).__init__()
        self.setupUi(self)
        self.menuconncect()
        self. _initStationTree()
        self.qml = MplCanvas(self.qmlcanvas, dpi=100)

        self.show()
        app.exec_()
        # print aw.qmlcanvas.width
    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
    def onfileopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.stream=read(filename)
        self.stations = Stations(self.stream, self)
        self.Fdebug()
        self.draw()
    def draw(self):
        drawstations=self.stations.visibleStations()
        self.qml.drawStations(drawstations,'N')

    def Fdebug(self):
        for i in range(6):
            self.stations[i].setVisible(True)

    def redraw(self):
        self.qml.drawAxes(self.stream, 3)

    def testgit(self):
        pass

    def _initStationTree(self):
        '''
                Setup stationtree :QTreeWidgetItem:
                '''
        self.stationTree.setColumnCount(3)
        self.stationTree.setColumnWidth(0, 40)
        self.stationTree.setColumnWidth(1, 90)
        self.stationTree.setColumnWidth(2, 150)
        #self.stationTree.setExpandsOnDoubleClick(False)
        #self.stationTree.itemDoubleClicked.connect(self._changeStationVisibility)
        #self.stationTree.setContextMenuPolicy(Qt.CustomContextMenu)          #add menu
        #self.stationTree.customContextMenuRequested.connect(self.stations.showSortQMenu)
if __name__ == '__main__':
    Rcspy()