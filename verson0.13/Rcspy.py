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
        self._initStationTree()
        self._initVistblebtn()
        self.qml = MplCanvas(self.qmlcanvas,dpi=100)
        self.show()
        app.exec_()
        # print aw.qmlcanvas.width
    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
    def onfileopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.stream=read(filename)
        self.stations = Stations(self.stream, self)
        for i in range(3):
            self.stations[i].setVisible(True)
        self.draw()
    def draw(self):
        drawstations=self.stations.visibleStations()
        self.qml.drawStations(drawstations,self.VisibleChannel)
    def _initStationTree(self):
        '''
        Setup stationtree :QTreeWidgetItem:
        '''
        self.stationTree.setColumnCount(3)
        self.stationTree.setColumnWidth(0, 40)
        self.stationTree.setColumnWidth(1, 90)
        self.stationTree.setColumnWidth(2, 150)
        self.stationTree.setExpandsOnDoubleClick(False)
        self.stationTree.setHeaderHidden(True)
    def _initVistblebtn(self):
        self.VisibleChannel=ChannelVisible(self)
    def _changeStationVisibility(self, item):
        '''
        Change selected stations visibility
        '''
        for station in self.stations:
            if station.QStationItem.isSelected():
                station.setVisible(not station.visible)
        self.draw()
    def _changeSelectedChannel(self):
        '''
        Change plotted channel
        '''
        if self.ZButton.isChecked():
            self.VisibleChannel.ZVisible=True
        else:
            self.VisibleChannel.ZVisible = False

        if self.NButton.isChecked():
            self.VisibleChannel.NVisible=True
        else:
            self.VisibleChannel.NVisible = False

        if self.EButton.isChecked():
            self.VisibleChannel.EVisible=True
        else:
            self.VisibleChannel.EVisible = False
        self.draw()
if __name__ == '__main__':
    Rcspy()