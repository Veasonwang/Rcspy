import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
# -*- coding: ascii -*-
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAbstractItemView, QSizePolicy, QMessageBox, QWidget,QFileDialog
from util import *
from obspy import  UTCDateTime
from matplotlib.widgets import MultiCursor
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
        self.qmlcanvas.setRcs(self)
        self.qml = MplCanvas(self.qmlcanvas,dpi=100)
        self.fig=self.qml.fig
        self.statusbar.showMessage("Done")
        self.Files=Files(self)
        self.ondrawstations=[]
        self.dragydata=0
        self.dragxdata=0
        self.trname=""
        self.mousetime=""
        self.mousestarttime=""
        self.mouseydata=""
        self.setstaus()
        self.show()
        app.exec_()
    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
        self.actionexit.triggered.connect(self.onexit)
    def onfileopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './','*.seed')
        if filename!="":
            try:
                file=File(filename,parent=self)
                stream=read(filename)
                self.Files.addfile(file)
                stations = Stations(stream, file)
                file.appointstations(stations)
                self.initdrawstation()
                self.update_ondraw_stations()
                self.draw()
                self.connectevent()
                self._changebtn_cursor()
            except:
                pass
    def initdrawstation(self):
        if len(self.ondrawstations) == 0:
            for file in self.Files.files:
                for station in file.stations.stations:
                    self.ondrawstations.append(station)
                    station.setVisible(True)
                    break
                break
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
        self.qml.drawAxes(self.ondrawstations,self.VisibleChannel)
    def update_ondraw_stations(self):
        """
        To update the stations for self.qml.draw()
        :return:
        """
        self.ondrawstations=[]
        for file in self.Files.files:
            for station in file.stations:
                if station.visible==True:
                    self.ondrawstations.append(station)
    def _initStationTree(self):
        '''
        Setup stationtree :QTreeWidgetItem:
        '''
        self.stationTree.setColumnCount(3)
        self.stationTree.setColumnWidth(0, 60)
        self.stationTree.setColumnWidth(1, 100)
        self.stationTree.setColumnWidth(2, 150)
        self.stationTree.setExpandsOnDoubleClick(False)
        self.stationTree.setHeaderLabels([" "," "," "])
        self.stationTree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.stationTree.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.stationTree.setHeaderHidden(True)
        self.stationTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.stationTree.customContextMenuRequested.connect(self.poptreemenu)
    def poptreemenu(self):
        if len(self.stationTree.selectedItems())>0:
            if isinstance(self.stationTree.selectedItems()[-1].parent,File)==True:
                Menu = QMenu()
                ASI = Menu.addAction('All Stations Invisible')
                ASI.triggered.connect(lambda :self.Files.setstationsinvisible(self.stationTree.selectedItems()[-1].parent))
                Sortbyname=Menu.addAction('Sort by Name')
                Sortbyname.triggered.connect(lambda:self.Files.SortByName(self.stationTree.selectedItems()[-1].parent))
                Menu.exec_(QtGui.QCursor.pos())

            elif isinstance(self.stationTree.selectedItems()[-1].parent,Station)==True:
                Menu = QMenu()
                INV = Menu.addAction('Set Invisible')
                INV.triggered.connect(lambda :self.Set_selected_Invisible
                                                        (self.stationTree.selectedItems()))
                VIS=Menu.addAction('Set Visible')
                VIS.triggered.connect(lambda: self.Set_selected_Visible
                                                        (self.stationTree.selectedItems()))
                Menu.exec_(QtGui.QCursor.pos())

    def popqmlmenu(self):
        Menu=QMenu()
        ac=Menu.addAction('Function')
        Menu.exec_(QtGui.QCursor.pos())
    def Set_selected_Invisible(self,selectedList):
        for item in selectedList:
            if isinstance(item.parent,Station)==True:
                item.parent.setVisible(False)
        self.update_ondraw_stations()
        self.draw()
    def Set_selected_Visible(self,selectedList):
        for item in selectedList:
            if isinstance(item.parent,Station)==True:
                item.parent.setVisible(True)
        self.update_ondraw_stations()
        self.draw()
    def _initVistblebtn(self):
        self.VisibleChannel=ChannelVisible(self)
    def _changeStationVisibility(self):
        '''
        Change selected stations visibility

        ###performance update)###

        '''
        #for file in self.Files.files:
        #    for station in file.stations:
        #        if station.QStationItem.isSelected():
        #            station.setVisible(not station.visible)
        if isinstance(self.stationTree.selectedItems()[0].parent,Station)==True:
            station=self.stationTree.selectedItems()[0].parent
            station.setVisible(not station.visible)
        self.update_ondraw_stations()
        self.draw()
    def _changeSelectedChannel(self):
        '''
        Change plotted channel
        '''
        if self.ZCheckBox.isChecked():
            self.VisibleChannel.ZVisible=True
        else:
            self.VisibleChannel.ZVisible = False

        if self.NCheckBox.isChecked():
            self.VisibleChannel.NVisible=True
        else:
            self.VisibleChannel.NVisible = False

        if self.ECheckBox.isChecked():
            self.VisibleChannel.EVisible=True
        else:
            self.VisibleChannel.EVisible = False
        self.draw()
    def _changebtn_cursor(self):
        if self.cursor_switch.isChecked():
            self.set_MultiCursor()
        else:
            try:
                self.del_MultiCursor()
            except:
                pass
            pass
    def set_MultiCursor(self):
        try:
            self.multi = MultiCursor(self.qml.fig.canvas, self.qml.axes, color='r', lw=0.5, horizOn=False,
                                 vertOn=True,useblit=True)
            self.qml.fig.canvas.draw()
        except:
            pass
    def del_MultiCursor(self):
        del (self.multi)
        self.qml.fig.canvas.draw()
    def getchnbyaxes(self,ax):
        return self.qml.get_drawchnarray(self.qml.axes.index(ax))
    def connectevent(self):
        self.cid = self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        self.qml.mpl_connect('button_release_event', self.__mpl_mouseButtonReleaseEvent)
        self.qml.mpl_connect('button_press_event', self.__mpl_mouseButtonPressEvent)
        self.qml.mpl_connect('motion_notify_event', self.__mpl_motionNotifyEvent)
        self.qml.mpl_connect('axes_enter_event', self.enter_axes)
        self.qml.mpl_connect('axes_leave_event', self.leave_axes)
        self.qml.mpl_connect('scroll_event',self.onmouse_scroll)
        self.qml.mpl_connect('figure_leave_event',self.leave_figure)
        self.qml.mpl_connect('figure_enter_event', self.enter_figure)

    def onqwidghtsizechangeed(self,QRectevent):
        height=QRectevent.size().height()
        width=QRectevent.size().width()
        self.qml.resize(width,height)
    def onclick(self, event):
        print(event.button, event.x, event.y, event.xdata, event.ydata)
        if event.button==3:
            self.popqmlmenu()
    def __mpl_mouseButtonReleaseEvent(self,event):
        try:
            xmin, xmax = event.inaxes.get_xlim()
            xmin = (self.dragxdata - event.xdata) + xmin
            xmax = (self.dragxdata - event.xdata) + xmax
            self.dragxdata = event.xdata
            self.dragydata = event.ydata
            event.inaxes.set_xlim(xmin, xmax)

            event.canvas.draw()
        except:
            pass
    def __mpl_mouseButtonPressEvent(self,event):
        try:
            Qrect=self.qmlcanvas.geometry()
            print Qrect.height()
            print Qrect.width()
            self.dragxdata = event.xdata
            self.dragydata = event.ydata
        except:
            pass
    def __mpl_motionNotifyEvent(self,event):
        """
        bas performance
        :param event:
        :return:
        """
        try:
            x=int(event.xdata*100)
            self.mousetime = UTCDateTime(self.mousestarttime.timestamp+event.xdata)
            self.mouseydata = self.currentchn.tr.data[x]


        except:
            print "error"
            pass
        self.setstaus(self.trname,self.mousetime,self.mouseydata)
        pass
    def enter_axes(self,event):
        chn=self.getchnbyaxes(event.inaxes)
        self.currentchn=chn
        self.trname =chn.station.stats.network+"."+chn.station.stats.station+"."+chn.channel+"    "
        self.mousestarttime=UTCDateTime(self.getchnbyaxes(event.inaxes).starttime)

    def leave_axes(self,event):
        self.mousetime=""
        self.trname=""
    def enter_figure(self,event):
        self._changebtn_cursor()
    def leave_figure(self,event):
        try:
            self.del_MultiCursor()
            self.setstaus()
        except:
            pass
    def setstaus(self,trname="",mousetime="",mouseydata=""):
        if (trname,mousetime,mouseydata)==("","",""):
            self.statusbar.showMessage("Ready")
        else:
            #string = trname +"  time: "+str(mousetime.day)+"D"+str(mousetime.hour)+"h"+str(mousetime.minute)+"m"+str(mousetime.second)+"s"+" , Y:"+str(mouseydata)
            string=trname +"  UTCTime: "+str(mousetime)[0:-1]+"        Y:"+str(mouseydata)
            self.statusbar.showMessage(string)
            self.qmlcanvas.setToolTip(string)
            self.current_time.setText(str(mousetime)[0:-1])
    def onmouse_scroll(self,event):
        self.resetYlim(event)
        self.resetXlim(event)
        event.canvas.draw()
    def resetYlim(self,event):
        if event.button == 'down':
            ydata = event.ydata
            ymin, ymax = event.inaxes.get_ylim()
            upoffset = ymax - ydata
            downoffset = ydata - ymin
            upratio = upoffset / (upoffset + downoffset)
            downratio = downoffset / (upoffset + downoffset)
            ymin = ymin - (abs(ymax - ymin)) * 0.15 * downratio
            ymax = ymax + (abs(ymax - ymin)) * 0.15 * upratio
        if event.button=='up':
            ydata = event.ydata
            ymin, ymax = event.inaxes.get_ylim()
            upoffset = ymax - ydata
            downoffset = ydata - ymin
            upratio = upoffset / (upoffset + downoffset)
            downratio = downoffset / (upoffset + downoffset)
            ymin = ymin  + (abs(ymax-ymin))*0.15 * downratio
            ymax = ymax  - (abs(ymax-ymin))*0.15 * upratio
        event.inaxes.set_ylim(ymin, ymax)
    def resetXlim(self,event):
        if event.button == 'down':
            xdata = event.xdata
            xmin, xmax = event.inaxes.get_xlim()
            upoffset = xmax - xdata
            downoffset = xdata - xmin
            upratio = upoffset / (upoffset + downoffset)
            downratio = downoffset / (upoffset + downoffset)
            xmin = xmin - (abs(xmax - xmin)) * 0.15 * downratio
            xmax = xmax + (abs(xmax - xmin)) * 0.15 * upratio
        if event.button=='up':
            xdata = event.xdata
            xmin, xmax = event.inaxes.get_xlim()
            upoffset = xmax - xdata
            downoffset = xdata - xmin
            upratio = upoffset / (upoffset + downoffset)
            downratio = downoffset / (upoffset + downoffset)
            xmin = xmin + (abs(xmax - xmin)) * 0.15 * downratio
            xmax = xmax - (abs(xmax - xmin)) * 0.15 * upratio
        event.inaxes.set_xlim(xmin, xmax)
    def _Ampup(self):
        self.qml.limratio=self.qml.limratio*0.75
        self.update_ondraw_stations()
        self.draw()
    def _Ampdown(self):
        self.qml.limratio = self.qml.limratio *1.25
        self.update_ondraw_stations()
        self.draw()
    def _AmpReset(self):
        self.update_ondraw_stations()
        self.draw()
        pass

if __name__ == '__main__':
    Rcspy()



























