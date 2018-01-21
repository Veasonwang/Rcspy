import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
# -*- coding: ascii -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
import ctypes
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
        self.qml = MplCanvas(self.qmlcanvas,width=23,height=14,dpi=72)
        self.fig=self.qml.fig
        self.connectevent()
        self.statusbar.showMessage("Done")
        self.trname=""
        self.show()
        app.exec_()
        # print aw.qmlcanvas.width
    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
        self.actionexit.triggered.connect(self.onexit)
    def onfileopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './','*.seed')
        if filename!="":
            try:
                self.stream=read(filename)
                self.stations = Stations(self.stream, self)
                for i in range(3):
                    self.stations[i].setVisible(True)
                self.qml.getstream(self.stream)
                self.draw()
            except:
                pass
    def onexit(self):
        reply = QMessageBox.question(self,'Message', 'You sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os._exit(0)
            except:
                pass
        else:
            pass
    def draw(self):
        drawstations=self.stations.visibleStations()
        self.qml.drawAxes(drawstations,self.VisibleChannel)
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
    def gettracebyaxes(self,ax):
        return self.qml.get_drawarray(self.qml.axes.index(ax))
    def connectevent(self):
        self.cid = self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        self.qml.mpl_connect('button_release_event', self.__mpl_mouseButtonReleaseEvent)
        self.qml.mpl_connect('button_press_event', self.__mpl_mouseButtonPressEvent)
        self.qml.mpl_connect('motion_notify_event', self.__mpl_motionNotifyEvent)
        self.qml.mpl_connect('axes_enter_event', self.enter_axes)
        self.qml.mpl_connect('axes_leave_event', self.leave_axes)
    def onclick(self, event):
        print(event.button, event.x, event.y, event.xdata, event.ydata)
    def __mpl_mouseButtonReleaseEvent(self,event):
        pass
    def __mpl_mouseButtonPressEvent(self,event):
        pass
    def __mpl_motionNotifyEvent(self,event):
        self.setstaus(self.trname,event.xdata,event.ydata)
        pass
    def enter_axes(self,event):
        trace=self.gettracebyaxes(event.inaxes)
        self.trname =trace.station.stats.network+"."+trace.station.stats.station+"."+trace.channel+"    "
        event.inaxes.patch.set_facecolor('grey')
        event.canvas.draw()
    def leave_axes(self,event):
        event.inaxes.patch.set_facecolor('white')
        event.canvas.draw()
    def setstaus(self,trname,xdata,ydata):
        string=trname+" X:"+str(xdata)+" , Y:"+str(ydata)
        self.statusbar.showMessage(string)
if __name__ == '__main__':
    Rcspy()