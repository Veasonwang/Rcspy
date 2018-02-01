# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import QObject,QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAbstractItemView, QSizePolicy, QMessageBox, QWidget,QFileDialog
from util import *
from obspy import  UTCDateTime
from matplotlib.widgets import MultiCursor
import rcsui_Mainwindow
import sys
from UI_Container import *
class Rcspy(rcsui_Mainwindow.Ui_MainWindow,QMainWindow):
    def __init__(self,parent=None):
        app = QApplication(sys.argv)
        super(Rcspy,self).__init__()
        self.setupUi(self)
        self.Eventconncect()
        self._initStationTree()
        self._initVistblebtn()
        self._initvariable()
        self.show()
        app.exec_()
    def _initvariable(self):
        self.scrollArea.setRcs(self)
        self.qmlcanvas.setRcs(self)
        self.qml = MplCanvas(self.qmlcanvas, dpi=100)
        self.qml.setRcs(self)
        self.fig = self.qml.fig
        self.statusbar.showMessage("Done")
        self.zoomswi = self.zoomswitch.isChecked()
        self.Files = Files(self)
        self.xlimratio = 1
        self.ondrawstations = []
        self.dragydata = 0
        self.dragxdata = 0
        self.trname = ""
        self.mousetime = ""
        self.mousestarttime = ""
        self.mouseydata = ""
        self.qmldragswi=False
        self.setstaus()
    def Eventconncect(self):
        """
        Connection signal function
        :return:
        """
        self.actionRseed.triggered.connect(self.onRseed)
        self.actionRminiseed.triggered.connect(self.onRminiseed)
        self.actionexit.triggered.connect(self.onexit)
        self.actionexport.triggered.connect(self.Export)
        self.actiondetrend.triggered.connect(self.detrend)
        self.X_press.clicked.connect(self._OnbtnX_press_clicked)
        self.X_stretch.clicked.connect(self._OnbtnX_stretch_clicked)
        self.drawnumber_combobox.currentTextChanged.connect(self._Ondrawnumber_combobox_change)
        self.zoomswitch.stateChanged['int'].connect(self._Onzoomswitchchange)
        self.dragenable_switch.stateChanged.connect(self._Ondragenabeswitchchange)
    '''Drawing correlation function'''
    def initdrawstation(self):
        if len(self.ondrawstations) == 0:
            for file in self.Files.files:
                for station in file.stations.stations:
                    self.ondrawstations.append(station)
                    station.setVisible(True)
                    break
                break
    def draw(self):
        #if len(self.ondrawstations)>36:
        #    QMessageBox.about(self,"toomany","toomany stations draw,no more than 36")
        #    for station in self.ondrawstations:
        #        station.setVisible(False)
        #    self.ondrawstations=[]
        """

        :return:
        """
        ###calculate single channel height
        height=self.scrollArea.geometry().height()
        self.qml.signalheight = height / int(self.drawnumber_combobox.currentText())
        self.qml.drawAxes(self.ondrawstations,self.VisibleChannel)
        self.stationTree.clearSelection()
        self.statusbar.showMessage("Ready")
    def update_ondraw_stations(self):
        """
        To update the stations for self.qml.draw()
        :return:
        """
        currentnum=0
        self.statusbar.showMessage("updating station")
        self.ondrawstations=[]
        for file in self.Files.files:
            for station in file.stations:
                if station.visible==True:
                    self.statusbar.showMessage("updating station   "+str(currentnum))
                    currentnum=currentnum+1
                    self.ondrawstations.append(station)
        string="显示台站数："+str(len(self.ondrawstations))
        self.label_stationdrawnumber.setText(string)
    def onqwidghtsizechangeed(self,QRectevent):
        height=QRectevent.size().height()
        width=QRectevent.size().width()
        self.qml.resize(width,height)
    '''correlation functions of StationTree'''
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
        self.stationTree.itemSelectionChanged.connect(self._Onstationtreeselectedchange)
    def poptreemenu(self):
        if len(self.stationTree.selectedItems())>0:
            if isinstance(self.stationTree.selectedItems()[-1].parent,File)==True:
                Menu = QMenu()
                ASI = Menu.addAction('All Stations Invisible')
                ASI.triggered.connect(lambda :self.Files.setstationsinvisible(self.stationTree.selectedItems()))
                Sortbyname=Menu.addAction('Sort by Name')
                Sortbyname.triggered.connect(lambda:self.Files.SortByName(self.stationTree.selectedItems()))
                rmfile=Menu.addAction('remove file')
                rmfile.triggered.connect(lambda:self.Files.removeselectedfile(self.stationTree.selectedItems()))
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
    def _Onstationtreeselectedchange(self):
        selectednumber=len(self.stationTree.selectedItems())
        self.statusbar.showMessage(str(selectednumber)+" items selected")
    def Set_selected_Invisible(self,selectedList):
        for item in selectedList:
            if isinstance(item.parent,Station)==True:
                item.parent.setVisible(False)
        self.update_ondraw_stations()
        self.draw()
    def Set_selected_Visible(self,selectedList):
        self.update_ondraw_stations()
        if len(self.ondrawstations)+len(selectedList)>36:
            QMessageBox.about(self,"toomany","toomanystations,no more than 36")
        else:
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
    '''Canvas response function and support'''
    def connectevent(self):
        self.cid = self.fig.canvas.mpl_connect('button_press_event',self.onqmlclick)
        self.qml.mpl_connect('button_release_event', self.__mpl_mouseButtonReleaseEvent)
        self.qml.mpl_connect('button_press_event', self.__mpl_mouseButtonPressEvent)
        self.qml.mpl_connect('motion_notify_event', self.__mpl_motionNotifyEvent)
        self.qml.mpl_connect('axes_enter_event', self.enter_axes)
        self.qml.mpl_connect('axes_leave_event', self.leave_axes)
        self.qml.mpl_connect('figure_leave_event',self.leave_figure)
        self.qml.mpl_connect('figure_enter_event', self.enter_figure)
    def onqmlclick(self, event):
        if event.button==3:
            self.popqmlmenu()
        if event.button==1:
            print event
            event.inaxes.axvline(event.xdata,ymin=0,ymax=1)
            event.canvas.draw()
    def popqmlmenu(self):
        Menu=QMenu()
        ac=Menu.addAction('Function')
        Menu.exec_(QtGui.QCursor.pos())
    def __mpl_mouseButtonReleaseEvent(self,event):
        if self.qmldragswi==True:
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
        else:
            pass
    def __mpl_mouseButtonPressEvent(self,event):
        if self.qmldragswi == True:
            try:
                self.dragxdata = event.xdata
                self.dragydata = event.ydata
            except:
                pass
        else:
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
    def getchnbyaxes(self,ax):
        return self.qml.get_drawchnarray(self.qml.axes.index(ax))
    def setstaus(self,trname="",mousetime="",mouseydata=""):
        if (trname,mousetime,mouseydata)==("","",""):
            self.statusbar.showMessage("Ready")
        else:
            #string = trname +"  time: "+str(mousetime.day)+"D"+str(mousetime.hour)+"h"+str(mousetime.minute)+"m"+str(mousetime.second)+"s"+" , Y:"+str(mouseydata)
            string=trname +"  UTCTime: "+str(mousetime)[0:-1]+"        Y:"+str(mouseydata)
            self.statusbar.showMessage(string)
            self.qmlcanvas.setToolTip(string)
            self.current_time.setText(str(mousetime)[0:-1])

    '''three functions for Mouse scrolling zoom'''
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
    '''Menu bar response function'''
    def onRseed(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', './', '*.seed')

        if len(filenames) != 0:
            try:
                currentfile = 1
                allfile = len(filenames)
                for filename in filenames:
                    string = "Reading " + str(currentfile) + "  of" + str(allfile)
                    self.statusbar.showMessage(string)
                    currentfile = currentfile + 1
                    file = File(filename, parent=self, format='seed')
                    stream = read(filename)
                    self.Files.addfile(file)
                    stations = Stations(stream, file)
                    file.appointstations(stations)
                self.statusbar.showMessage("drawing")
                self.initdrawstation()
                self.update_ondraw_stations()
                self._changeSelectedChannel()
                self.connectevent()
                self._changebtn_cursor()
            except:
                pass
    def onRminiseed(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'file(*.mseed *.miniseed)')
        if filename != "":
            try:
                file = File(filename, parent=self, format='mseed')
                stream = read(filename)
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
        pass
    def Export(self):
        self.exdialog = Exportdialog(self)
        self.exdialog.getFiles(self.Files)
        self.exdialog.exec_()
    def onexit(self):
        reply = QMessageBox.question(self, 'Message', 'You sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os._exit(0)
            except:
                pass
        else:
            pass
    def detrend(self):
        for file in self.Files.files:
            for station in file.stations.stations:
                station.detrend()
        self.update_ondraw_stations()
        self.draw()
    '''Top operation bar response function'''
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
    def _Ampup(self):
        self.qml.ylimratio=self.qml.ylimratio*0.75
        self.update_ondraw_stations()
        self.draw()
    def _Ampdown(self):
        self.qml.ylimratio = self.qml.ylimratio *1.25
        self.update_ondraw_stations()
        self.draw()
    def _AmpReset(self):
        self.qml.ylimratio=1
        self.xlimratio=1
        width=self.scrollArea.geometry().width()
        self.qmlcanvas.setFixedWidth(width)
        self.update_ondraw_stations()
        self.draw()
        pass
    def _OnbtnX_press_clicked(self):
        if self.xlimratio >0.5:
            self.xlimratio=self.xlimratio*0.75
            if self.xlimratio<0.5:
                self.xlimratio=0.5
            width=self.scrollArea.geometry().width()
            self.qmlcanvas.setFixedWidth(width*self.xlimratio)
        pass
    def _OnbtnX_stretch_clicked(self):
        if self.xlimratio<7:
            if self.xlimratio>7:
                self.xlimratio=7
            self.xlimratio = self.xlimratio * 1.1
            width = self.scrollArea.geometry().width()
            self.qmlcanvas.setFixedWidth(width*self.xlimratio)
        pass
    def _Ondrawnumber_combobox_change(self):
        height=self.scrollArea.geometry().height()
        self.qml.signalheight=height/int(self.drawnumber_combobox.currentText())
        self.draw()
    def _Onzoomswitchchange(self):
        if self.zoomswitch.isChecked():
            self.zoomswi =True
            self.m_scroll_cid=self.qml.mpl_connect('scroll_event',self.onmouse_scroll)
        else:
            self.qml.mpl_disconnect(self.m_scroll_cid)
            self.zoomswi = False
    def _Ondragenabeswitchchange(self):
        if self.dragenable_switch.isChecked():
            if len(self.ondrawstations) > 12:
                QMessageBox.about(self, "会影响性能", "当前显示台站过多,开启拖动可能会影响性能")
                self.qmldragswi=True
            else:
                self.qmldragswi=True
        else:
            self.qmldragswi = False
            pass
if __name__ == '__main__':
    Rcspy()


















































