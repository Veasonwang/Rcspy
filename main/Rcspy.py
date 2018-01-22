import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
# -*- coding: ascii -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
import ctypes
from util import *
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
                self._changebtn_cursor()
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
    def _changeStationVisibility(self):
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
    def _changebtn_cursor(self):
        if self.btn_cursor.isChecked():
            self.set_MultiCursor()
        else:
            try:
                del(self.multi)
                self.qml.fig.canvas.draw()
            except:
                pass
            pass
    def gettracebyaxes(self,ax):
        return self.qml.get_drawarray(self.qml.axes.index(ax))
    def set_MultiCursor(self):
        self.multi = MultiCursor(self.qml.fig.canvas, self.qml.axes, color='r', lw=0.5, horizOn=False,
                                 vertOn=True,useblit=True)
        self.qml.fig.canvas.draw()
    def connectevent(self):
        self.cid = self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        self.qml.mpl_connect('button_release_event', self.__mpl_mouseButtonReleaseEvent)
        self.qml.mpl_connect('button_press_event', self.__mpl_mouseButtonPressEvent)
        self.qml.mpl_connect('motion_notify_event', self.__mpl_motionNotifyEvent)
        self.qml.mpl_connect('axes_enter_event', self.enter_axes)
        self.qml.mpl_connect('axes_leave_event', self.leave_axes)
        self.qml.mpl_connect('scroll_event',self.onmouse_scroll)

    def onclick(self, event):
        print(event.button, event.x, event.y, event.xdata, event.ydata)
    def __mpl_mouseButtonReleaseEvent(self,event):
        event.inaxes.patch.set_facecolor('white')
        event.canvas.draw()
        pass
    def __mpl_mouseButtonPressEvent(self,event):
        event.inaxes.patch.set_facecolor('grey')
        event.canvas.draw()
        pass
    def __mpl_motionNotifyEvent(self,event):
        """
        bas performance
        :param event:
        :return:
        """
        #self.draw()
        #for ax in self.qml.axes:
        #    ax.axvline(x=event.xdata, ymin=0, ymax=1)
        #event.canvas.draw()

        self.setstaus(self.trname,event.xdata,event.ydata)
        pass
    def enter_axes(self,event):
        trace=self.gettracebyaxes(event.inaxes)
        self.trname =trace.station.stats.network+"."+trace.station.stats.station+"."+trace.channel+"    "

    def leave_axes(self,event):
        self.trname=""

    def setstaus(self,trname,xdata,ydata):
        string=trname+" X:"+str(xdata)+" , Y:"+str(ydata)
        self.statusbar.showMessage(string)
    def onmouse_scroll(self,event):
        if event.button=='down':
            print 1
        if event.button=='up':
            print 2
    def scrolldown(self):
        pass
    def scrollup(self):
        pass
if __name__ == '__main__':
    Rcspy()