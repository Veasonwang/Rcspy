'''
To handle gui events and draw cruve
'''

import rcspy_Exportdialog
import os
from PyQt5.QtWidgets import QMenu,QMessageBox,QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont,QIcon
from util import QTreeWidgetItem,QListWidgetItem
from operator import attrgetter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView,QFileDialog
from numpy import mean
class ChannelVisible:
    def __init__(self,parent=None):
        self.parent=parent
        self.ZVisible=True
        self.NVisible=False
        self.EVisible=False

class Files:
    """
    File() container object
    """
    def __init__(self,parent):
        self.files=[]
        self.parent=parent
    def addfile(self,file):
        self.files.append(file)
    def setstationsinvisible(self,File):
        File.setinvisible()
        self.parent.update_ondraw_stations()
        self.parent.draw()
    def SortByName(self,File):
        stations=File.stations.stations
        stations.sort(key=attrgetter('stats.network','stats.station'))
        File.rebuildTreeview()

class File:
    """
    Represents a single file and hold the Stations()
    """
    def __init__(self,path,parent,format=''):
        self.path=path
        self.parent=parent
        self.stations=[]
        self.QStationItem = QTreeWidgetItem(self)
        self.QStationItem.setText(1, '%s' %
                                  (self.path.split('/')[-1]))
        self.QStationItem.setToolTip(1,self.path)
        self.QStationItem.setToolTip(2, self.path)
        self.name=self.path.split('/')[-1]
        self.ename=""
        for n in self.name.split('.')[0:-1]:
            self.ename=self.ename+n
        self.parent.stationTree.addTopLevelItem(self.QStationItem)
    def appointstations(self,stations):
        """
        add childstations
        :param stations:
        :return:
        """
        self.stations=stations
        self.stream=self.stations.stream
    def setinvisible(self):
        for station in self.stations.stations:
            station.setVisible(False)
    def rebuildTreeview(self):
        for station in self.stations.stations:
            self.QStationItem.removeChild(station.QStationItem)
        for station in self.stations.stations:
            self.QStationItem.addChild(station.QStationItem)


class Stations:
    '''
    Station() container object
    '''
    def __init__(self, st, parent):
        '''
        Inits with

        :parent: grapePicker QtGui.QMainWindow
        '''
        self.parent = parent
        self.stream = st
        self.stations = []
        for stat in set([tr.stats.station for tr in st]):
            self.addStation(st=st.select(station=stat))
        self.sorted_by = None
    def addStation(self, st):
        '''
        Adds a station from
        :param st: obspy stream
        '''
        self.stations.append(Station(stream=st, parent=self))
        #self.parent.stationTree.addTopLevelItem(
        #    self.stations[-1].QStationItem)
        self.parent.QStationItem.addChild(self.stations[-1].QStationItem)
    def visibleStations(self):
        '''
        Returns a list of all visible stations
        :return: list of Station()
        '''
        return [station for station in self.stations
                if station.visible]
    def showQMenu(self):
        '''
        Sort Menu for the QTreeWidget
        '''
        T_menu = QMenu()
        T_menu.setFont(QFont('', 9))
        allinvi = T_menu.addAction('Sort by attribute')
        allinvi.setEnabled(False)
        allinvi.setFont(QFont('', 8, QFont.Bold))
    def sortByAttrib(self, key):
        '''
        Sort station by attribute key
        '''
        from operator import attrgetter
        self.stations = sorted(self.stations, key=attrgetter('stats.%s' % key))
        self.sorted_by = key
        self._sortStationsOnGUI()
    def __iter__(self):
        return iter(self.stations)

    def __getitem__(self, index):
        return self.stations[index]

    def __len__(self):
        return len(self.stations)
class Station(object):
    '''
    Represents a single Station and hold the channel
    '''
    def __init__(self, stream, parent):
        '''
        Object is initiated with a obspy Stream object and the parent mainDialog

        :stream: obspy.core.Stream()
        '''
        self.parent = parent
        self.plotItem = None

        self.st = stream.merge()
        self.stats = self.st[0].stats.copy()
        self.stats.channel = None
        self.channel_components = set([tr.stats.channel for tr in self.st])

        self.QStationItem = QTreeWidgetItem(self)
        self.QStationItem.setText(1, '%s.%s' %
                                  (self.stats.network,
                                   self.stats.station))
        self.name=self.stats.network+"."+self.stats.station
        #self.QStationItem.setText(2, '%.3f N, %.3f E' %
        #                              (self.getCoordinates()[0],
        #                               self.getCoordinates()[1]))

        self.picks = []
        self.station_events = []

        self.channels = []
        for tr in self.st:
            self.channels.append(Channel(tr, station=self))
        self.setVisible(False)
    def setVisible(self, visible=True):
        '''
        Sets wheather the station is visible in the plot view
        '''
        basedir = os.path.dirname(__file__)

        self.visible = visible
        if visible:
            self.QStationItem.setIcon(0,
                                      QIcon(os.path.join(basedir,
                                            'icons/eye-24.png')))
        else:
            self.QStationItem.setIcon(0,
                                      QIcon(os.path.join(basedir,
                                            'icons/eye-hidden-24.png')))
    def getchannelbyNZE(self,direction):
        for chann in self.channels:
            if chann.channel[-1]==direction:
                return chann
    def gettrbyNZE(self,direction):
        for chann in self.channels:
            if chann.channel[-1]==direction:
                return chann.tr
class Channel(object):
    '''
    Channel Container Object handels an individual channel,obspy.core.trace

    self.QChannelItem represents the QTreeWidgetItem
    '''
    def __init__(self, tr, station):
        '''
        init the channel with parent Station() and obspy trace
        :param tr: obspy.core.trace of the channel
        :param station: Station()
        '''
        self.tr = tr
        self.station = station
        self.channel = tr.stats.channel
        self.starttime=tr.stats.starttime
        self.edntime=tr.stats.endtime
        self.QChannelItem = QTreeWidgetItem(self)
        self.QChannelItem.setText(1, '%s @ %d Hz' %
                                  (self.tr.stats.channel,
                                   1./self.tr.stats.delta))
        self.QChannelItem.setText(2, '%s\n%s' %
                                  (self.tr.stats.starttime,
                                   self.tr.stats.endtime))
        self.station.QStationItem.addChild(self.QChannelItem)
        self.datamean=self.tr.data.mean()


class Exportdialog(rcspy_Exportdialog.Ui_Dialog,QtWidgets.QDialog):
    def __init__(self,parent):
        super(Exportdialog, self).__init__(parent)
        self.setupUi(self)
        self.File_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.channel_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()
        self.expath=""
    def getFiles(self,Files):
        self.Files=Files
        for file in self.Files.files:
            listitem=QListWidgetItem(file)
            listitem.setText(file.name)
            self.File_list.addItem(listitem)

    def connectevent(self):
        self.btnOK.clicked.connect(self.Onbtnok)
        self.btn_Cancel.clicked.connect(self.Onbtncancel)
        self.File_list.itemSelectionChanged.connect(self.OnFilelist_selectionchange)
        self.channel_list.itemSelectionChanged.connect(self.Onchannellist_selectionchange)
        self.allchannel_checkbox.stateChanged.connect(self.Onallchannel_change)
        self.btn_set_folder.clicked.connect(self.set_exfolder)
    def set_exfolder(self):
        foldername=QFileDialog.getExistingDirectory(self,'save folder')
        if foldername !="":
            self.expath=foldername
            self.Exfolder_edit.setText(foldername)
    def Onallchannel_change(self):
        if self.allchannel_checkbox.isChecked()==True:
            self.channel_list.selectAll()
        else:
            self.channel_list.clearSelection()
    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems())==1:
            self.channel_list.setEnabled(True)
            self.allchannel_checkbox.setEnabled(True)

            self.radioSAC.setEnabled(True)
            stations=self.File_list.selectedItems()[0].parent.stations
            for station in stations.stations:
                listitem=QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
        if len(self.File_list.selectedItems())>1:
            for item in self.File_list.selectedItems():
                stations = item.parent.stations
                for station in stations.stations:
                    listitem = QListWidgetItem(station)
                    listitem.setText(station.name)
                    self.channel_list.addItem(listitem)
            self.channel_list.setEnabled(False)
            self.allchannel_checkbox.setChecked(True)
            self.allchannel_checkbox.setEnabled(False)
            self.radioMSEED.setChecked(True)
            self.radioSAC.setEnabled(False)
    def Onchannellist_selectionchange(self):
        count=self.channel_list.count()
        if len(self.channel_list.selectedItems())==count:
            self.allchannel_checkbox.setChecked(True)
        else:
            self.allchannel_checkbox.setChecked(False)
    def Onbtnok(self):
        if self.expath=="":
            QMessageBox.about(self,"tips","please set export folder")

        elif len(self.File_list.selectedItems())==0:
            QMessageBox.about(self, "tips", "please set export files")

        else:
            if self.radioMSEED.isChecked():
                self.pgb = QProgressBar(self)
                self.pgb.setWindowTitle("Exporting")
                self.pgb.setGeometry(160, 380, 200, 25)
                self.pgb.show()
                step=0
                allnum=len(self.File_list.selectedItems())
                currnum=0
                for item in self.File_list.selectedItems():
                    file=item.parent
                    filesave=self.expath+"/"+str(file.ename)+".mseed"
                    file.stream.write(filesave,format='MSEED',reclen=256)
                    currnum=currnum+1
                    step=currnum*100/allnum
                    self.pgb.setValue(int(step))
                self.pgb.close()
                QMessageBox.about(self,"tips","finished")

    def Onbtncancel(self):
        self.close()




























































