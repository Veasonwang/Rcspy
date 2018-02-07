'''
To handle gui events and draw cruve
'''

import rcspy_Exportdialog
import rcspy_Preprocessdialog
import os
from PyQt5.QtWidgets import QMenu,QMessageBox,QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import QDir
from util import QTreeWidgetItem,QListWidgetItem
from operator import attrgetter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView,QFileDialog
import obspy.core
from obspy import *
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
    def setstationsinvisible(self,selecteditems):
        for item in selecteditems:
            if isinstance(item.parent,File):
                file = item.parent
                file.setinvisible()
                self.parent.update_ondraw_stations()
                self.parent.draw()
    def SortByName(self,selecteditems):
        for item in selecteditems:
            if isinstance(item.parent,File):
                file=item.parent
                stations=file.stations
                stations.sort(key=attrgetter('stats.network','stats.station'))
                file.rebuildTreeview()
            else:
                pass

    def removeselectedfile(self,selecteditems):
        reply = QMessageBox.question(self.parent, 'Message', 'You sure to remove?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for item in selecteditems:
                if isinstance(item.parent,File):
                    file=item.parent
                    self.parent.stationTree.takeTopLevelItem(
                                                            self.parent.stationTree.indexOfTopLevelItem(
                                                            file.QStationItem))
                    self.removefile(file)
            lenth=len(self.parent.ondrawstations)
            self.parent.update_ondraw_stations()
            if lenth!=len(self.parent.ondrawstations):
                self.parent.draw()
        else:
            pass
    def removefile(self,file):
        self.parent.Files.files.remove(file)
    def removeselectedstation(self,items):
        reply = QMessageBox.question(self.parent, 'Message', 'You sure to remove?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            update=False
            for item in items:
                if isinstance(item.parent,Station):
                    station=item.parent
                    file=station.parent
                    st=file.stream.select(station=station.stats.station)
                    for tr in st:
                        file.stream.remove(tr)
                    file.stations.remove(station)
                    if station.visible==True:
                        update=True
                    file.removestationTree(station.QStationItem)
            if update==True:
                self.parent.update_ondraw_stations()
                self.parent.draw()
        else:
            pass
class File:
    """
    Represents a single file and hold the Stations()
    """
    def __init__(self,path,st,parent,fformat=''):
        self.path=path
        self.parent=parent
        self.stations=[]
        self.stream = st
        self.format=fformat
        self.setstationTree()
        self.setname()
        for stat in set([tr.stats.station for tr in st]):
            self.addStation(st=st.select(station=stat))
    def setstationTree(self):
        self.QStationItem = QTreeWidgetItem(self)
        self.QStationItem.setText(1, '%s' %
                                  (self.path.split('/')[-1]))
        self.QStationItem.setToolTip(1, self.path)
        self.QStationItem.setToolTip(2, self.path)
        self.parent.stationTree.addTopLevelItem(self.QStationItem)
    def setname(self):
        self.name = self.path.split('/')[-1]
        self.ename = ""
        for n in self.name.split('.')[0:-1]:
            self.ename=self.ename+n
    def addStation(self, st):
        '''
        Adds a station from
        :param st: obspy stream
        '''
        self.stations.append(Station(stream=st, parent=self))
        self.QStationItem.addChild(self.stations[-1].QStationItem)
    def setinvisible(self):
        for station in self.stations:
            station.setVisible(False)
    def setInv(self):
        self.Inv=read_inventory(self.path)
    def rebuildTreeview(self):
        for station in self.stations:
            self.QStationItem.removeChild(station.QStationItem)
        for station in self.stations:
            self.QStationItem.addChild(station.QStationItem)
    def detrend(self,type):
        for station in self.stations:
            for channel in station.channels:
                if type=='constant':
                    channel.tr=channel.tr.detrend(type='constant')
                if type=='linear':
                    channel.tr=channel.tr.detrend(type='linear')
    def visibleStations(self):
        '''
        Returns a list of all visible stations
        :return: list of Station()
        '''
        return [station for station in self.stations
                if station.visible]
    def removestationTree(self,TreeItem):
        self.QStationItem.removeChild(TreeItem)
        del(TreeItem)
    def __iter__(self):
        return iter(self.stations)

    def __getitem__(self, index):
        return self.stations[index]

    def __len__(self):
        return len(self.stations)
"""
It don't used now, including in class File
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
    def addStation(self, st):
        '''
        Adds a station from
        :param st: obspy stream
        '''
        self.stations.append(Station(stream=st, parent=self))
        self.parent.QStationItem.addChild(self.stations[-1].QStationItem)
    def visibleStations(self):
        '''
        Returns a list of all visible stations
        :return: list of Station()
        '''
        return [station for station in self.stations
                if station.visible]
    def __iter__(self):
        return iter(self.stations)

    def __getitem__(self, index):
        return self.stations[index]

    def __len__(self):
        return len(self.stations)
"""
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
        self.st = stream.merge()
        self.stats = self.st[0].stats.copy()
        self.stats.channel = None
        self.name=self.stats.network+"."+self.stats.station
        self.channels = []
        self.setstationTree()
        for tr in self.st:
            self.channels.append(Channel(tr, station=self))
        self.setVisible(False)
    def setstationTree(self):
        self.QStationItem = QTreeWidgetItem(self)
        self.QStationItem.setText(1, '%s.%s' %
                                  (self.stats.network,
                                   self.stats.station))
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
    def detrend(self,type):
        for channel in self.channels:
            if type == 'constant':
                channel.tr = channel.tr.detrend(type='constant')
            if type == 'linear':
                channel.tr = channel.tr.detrend(type='linear')
            channel.datamean=channel.tr.data.mean()
    def bandpass(self,type,**kwargs):
        for channel in self.channels:
            channel.tr=channel.tr.copy().filter(type=type,**kwargs)
            channel.datamean = channel.tr.data.mean()
    def remove_response(self,inventory=None,water_level=60,pre_filt=None):
        for channel in self.channels:
            channel.tr_VEL=channel.tr.copy().remove_response(inventory=inventory,output='VEL',water_level=water_level,
                                                        pre_filt=pre_filt)
            channel.tr_DISP = channel.tr.copy().remove_response(inventory=inventory, output='DISP', water_level=water_level,
                                                        pre_filt=pre_filt)
            channel.tr_ACC = channel.tr.copy().remove_response(inventory=inventory, output='ACC', water_level=water_level,
                                                        pre_filt=pre_filt)
            if isinstance(channel.tr_VEL,Trace):
                channel.tr=channel.tr_VEL.copy()
                channel.datamean = channel.tr.data.mean()
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
        self.origintr=tr.copy()
        self.station = station
        self.channel = tr.stats.channel
        self.starttime=tr.stats.starttime
        self.edntime=tr.stats.endtime
        self.setstationTree()
        self.datamean=self.tr.data.mean()
    def setstationTree(self):
        self.QChannelItem = QTreeWidgetItem(self)
        self.QChannelItem.setText(1, '%s @ %d Hz' %
                                  (self.tr.stats.channel,
                                   1. / self.tr.stats.delta))
        self.QChannelItem.setText(2, '%s\n%s' %
                                  (self.tr.stats.starttime,
                                   self.tr.stats.endtime))
        self.station.QStationItem.addChild(self.QChannelItem)
class Exportdialog(rcspy_Exportdialog.Ui_Dialog,QtWidgets.QDialog):
    def __init__(self,parent):
        super(Exportdialog, self).__init__(parent)
        self.setupUi(self)
        self.File_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.channel_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()
        self.expath=""
        self.radioMSEED.setChecked(True)
        self.radioSEED.setEnabled(False)
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
            self.single_channel_checkbox.setEnabled(True)
    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems())==1:
            self.channel_list.setEnabled(True)
            self.allchannel_checkbox.setEnabled(True)
            #self.radioSAC.setEnabled(True)
            file=self.File_list.selectedItems()[0].parent
            for station in file.stations:
                listitem=QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
        if len(self.File_list.selectedItems())>1:
            for item in self.File_list.selectedItems():
                file = item.parent
                for station in file.stations:
                    listitem = QListWidgetItem(station)
                    listitem.setText(station.name)
                    self.channel_list.addItem(listitem)
            self.channel_list.setEnabled(False)
            self.allchannel_checkbox.setChecked(True)
            self.allchannel_checkbox.setEnabled(False)
            self.radioMSEED.setChecked(True)
            #self.radioSAC.setEnabled(False)
    def Onchannellist_selectionchange(self):
        count=self.channel_list.count()
        if len(self.channel_list.selectedItems())==count:
            self.allchannel_checkbox.setChecked(True)
        else:
            self.allchannel_checkbox.setChecked(False)
    def Onbtncancel(self):
        self.close()
    def Onbtnok(self):
        if self.expath=="":
            QMessageBox.about(self,"tips","please set export folder")

        elif len(self.File_list.selectedItems())==0:
            QMessageBox.about(self, "tips", "please set export files")
        else:
            self.dir=QDir()
            self.dir.cd(self.expath)
            self.pgb = QProgressBar(self)
            self.pgb.setWindowTitle("Exporting")
            self.pgb.setGeometry(140, 380, 260, 25)
            self.pgb.show()
            if self.radioMSEED.isChecked():
                self.Export2mseed()
            if self.radioASCII.isChecked():
                self.Export2Ascii()
            if self.radioSAC.isChecked():
                self.Export2sac()
            self.pgb.close()
            QMessageBox.about(self, "tips", "finished")
    def Export2mseed(self):
        self.allnum = len(self.File_list.selectedItems())
        self.currnum = 0
        if self.allnum == 1:
            self.allnum = len(self.channel_list.selectedItems()) * 3
            exstream = obspy.core.Stream()
            append = exstream.append
            for item in self.channel_list.selectedItems():
                for channel in item.parent.channels:
                    append(channel.tr)
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
                    self.currnum = self.currnum + 1
            file = self.File_list.selectedItems()[0].parent
            filesave = self.expath + "/" + str(file.ename) + ".mseed"
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked() == True:
                self.currnum=0
                if self.dir.exists(file.ename) == False:
                    self.dir.mkdir(file.ename)
                filesave = self.expath + "/" + file.ename + "/"
                for tr in exstream:
                    tr.write(filesave + str(tr.id) + ".mseed", format='MSEED')
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
                    self.currnum = self.currnum + 1
            else:
                exstream.write(filesave, format='MSEED')
        else:
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked()== True:
                for item in self.File_list.selectedItems():
                    self.allnum = self.allnum + len(item.parent.stations.stations) * 3
                for item in self.File_list.selectedItems():
                    file = item.parent
                    if self.dir.exists(file.ename) == False:
                        self.dir.mkdir(file.ename)
                    filesave = self.expath + "/" + str(file.ename) + "/"
                    for tr in file.stream:
                        tr.write(filesave + str(tr.id) + ".mseed", format='MSEED')
                        self.currnum = self.currnum + 1
                        step = self.currnum * 100 / self.allnum
                        self.pgb.setValue(int(step))
            else:
                for item in self.File_list.selectedItems():
                    file = item.parent
                    filesave = self.expath + "/" + str(file.ename) + ".mseed"
                    file.stream.write(filesave, format='MSEED')
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
    def Export2Ascii(self):
        self.allnum = len(self.File_list.selectedItems())
        self.currnum = 0
        if self.allnum == 1:
            self.allnum = len(self.channel_list.selectedItems()) * 3
            exstream = obspy.core.Stream()
            append = exstream.append
            for item in self.channel_list.selectedItems():
                for channel in item.parent.channels:
                    append(channel.tr)
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
            file = self.File_list.selectedItems()[0].parent
            filesave = self.expath + "/" + str(file.ename) + ".ascii"
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked()== True:
                if self.dir.exists(file.ename) == False:
                    self.dir.mkdir(file.ename)
                filesave = self.expath + "/" + file.ename + "/"
                for tr in exstream:
                    tr.write(filesave + str(tr.id) + ".ascii", format='SLIST')
            else:
                exstream.write(filesave, format='SLIST')
        else:
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked()== True:
                for item in self.File_list.selectedItems():
                    self.allnum = self.allnum + len(item.parent.stations) * 3
                for item in self.File_list.selectedItems():
                    file = item.parent
                    if self.dir.exists(file.ename) == False:
                        self.dir.mkdir(file.ename)
                    filesave = self.expath + "/" + str(file.ename) + "/"
                    for tr in file.stream:
                        tr.write(filesave + str(tr.id) + ".ascii", format='SLIST')
                        self.currnum = self.currnum + 1
                        step = self.currnum * 100 / self.allnum
                        self.pgb.setValue(int(step))
            else:
                for item in self.File_list.selectedItems():
                    file = item.parent
                    filesave = self.expath + "/" + str(file.ename) + ".ascii"
                    file.stream.write(filesave, format='SLIST')
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
    def Export2sac(self):
        self.allnum = len(self.File_list.selectedItems())
        self.currnum = 0
        if self.allnum == 1:
            self.allnum = len(self.channel_list.selectedItems()) * 3
            exstream = obspy.core.Stream()
            append = exstream.append
            for item in self.channel_list.selectedItems():
                for channel in item.parent.channels:
                    append(channel.tr)
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
            file = self.File_list.selectedItems()[0].parent
            if self.dir.exists(file.ename) == False:
                self.dir.mkdir(file.ename)
            for tr in exstream:
                filesave = self.expath + "/"+file.ename+"/" + str(tr.id) + ".SAC"
                tr.write(filesave, format='SAC')
        else:
            self.allnum = 0
            for item in self.File_list.selectedItems():
                self.allnum = self.allnum + len(item.parent.stations) * 3
            for item in self.File_list.selectedItems():
                if self.dir.exists(item.parent.ename) == False:
                    self.dir.mkdir(item.parent.ename)
                filedir = self.expath + "/" + item.parent.ename + "/"
                for tr in item.parent.stream:
                    filesave = filedir + tr.id + ".SAC"
                    tr.write(filesave, format='SAC')
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
class Preprocessdialog(rcspy_Preprocessdialog.Ui_Dialog,QtWidgets.QDialog):
    def __init__(self,parent):
        super(Preprocessdialog, self).__init__(parent)
        self.setupUi(self)
        self.Rcs = parent
        self.initList()
        self.Inv_test()
        self.File_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.channel_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()
    def Inv_test(self):
        current=0
        for file in self.Files.files:
            if file.format!='SEED':
                current=current+1
        if current!=0:
            QMessageBox.about(self,"warning",str(current)+"File(s) not set Inventory")
    def initList(self):
        self.Files=self.Rcs.Files
        for file in self.Files.files:
            listitem=QListWidgetItem(file)
            listitem.setText(file.name)
            self.File_list.addItem(listitem)
    def connectevent(self):
        self.File_list.itemSelectionChanged.connect(self.OnFilelist_selectionchange)
        self.channel_list.itemSelectionChanged.connect(self.Onchannellist_selectionchange)
        self.allchannel_checkbox.stateChanged.connect(self.Onallchannel_change)
        self.fminSlider.valueChanged.connect(self.OnfminSlider_valueChanged)
        self.fmaxSlider.valueChanged.connect(self.OnfmaxSlider_valueChanged)
        self.fminspin.valueChanged.connect(self.Onfminspin_valueChange)
        self.fmaxspin.valueChanged.connect(self.Onfmaxspin_valueChange)
        self.btnOK.clicked.connect(self.Onbtnok)
        self.btn_Cancel.clicked.connect(self.Onbtnback)
    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems())==1:
            self.channel_list.setEnabled(True)
            self.allchannel_checkbox.setEnabled(True)
            file=self.File_list.selectedItems()[0].parent
            for station in file.stations:
                listitem=QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
        if len(self.File_list.selectedItems())>1:
            for item in self.File_list.selectedItems():
                file = item.parent
                for station in file.stations:
                    listitem = QListWidgetItem(station)
                    listitem.setText(station.name)
                    self.channel_list.addItem(listitem)
            self.channel_list.setEnabled(False)
            self.allchannel_checkbox.setChecked(True)
            self.allchannel_checkbox.setEnabled(False)
    def Onchannellist_selectionchange(self):
        count=self.channel_list.count()
        if len(self.channel_list.selectedItems())==count:
            self.allchannel_checkbox.setChecked(True)
        else:
            self.allchannel_checkbox.setChecked(False)
    def Onallchannel_change(self):
        if self.allchannel_checkbox.isChecked()==True:
            self.channel_list.selectAll()
        else:
            self.channel_list.clearSelection()
    """
    No use!!!!
    
    def Ondetrendswitch_change(self):
        if self.detrend_switch.isChecked():
            self.radioConstant.setEnabled(True)
            self.radioLinear.setEnabled(True)
        else:
            self.radioLinear.setEnabled(False)
            self.radioConstant.setEnabled(False)
    def Onremove_response_switch_change(self):
        if self.remove_respose_switch.isChecked():
            self.water_level_spin.setEnabled(True)
            self.pre_filt_switch.setEnabled(True)
            self.f1_spin.setEnabled(True)
            self.f2_spin.setEnabled(True)
            self.f3_spin.setEnabled(True)
            self.f4_spin.setEnabled(True)
            self.btn_setInv.setEnabled(True)
            self.apply_all_Inv_switch.setEnabled(True)
        else:
            self.water_level_spin.setEnabled(False)
            self.pre_filt_switch.setEnabled(False)
            self.f1_spin.setEnabled(False)
            self.f2_spin.setEnabled(False)
            self.f3_spin.setEnabled(False)
            self.f4_spin.setEnabled(False)
            self.btn_setInv.setEnabled(False)
            self.apply_all_Inv_switch.setEnabled(False)
    def Onbandpass_switch_change(self):
        if self.bandpass_switch.isChecked():
            self.fminspin.setEnabled(True)
            self.fmaxspin.setEnabled(True)
            self.fminSlider.setEnabled(True)
            self.fmaxSlider.setEnabled(True)
            self.corners_spin.setEnabled(True)
        else:
            self.fminspin.setEnabled(False)
            self.fmaxspin.setEnabled(False)
            self.fminSlider.setEnabled(False)
            self.fmaxSlider.setEnabled(False)
            self.corners_spin.setEnabled(False)
    """
    def OnfminSlider_valueChanged(self):
        self.fminspin.setValue(float(self.fminSlider.value())/10.0)
        if self.fminSlider.value()>self.fmaxSlider.value():
            self.fmaxSlider.setValue(self.fminSlider.value())
    def OnfmaxSlider_valueChanged(self):
        self.fmaxspin.setValue(float(self.fmaxSlider.value()) / 10.0)
        if self.fminSlider.value()>self.fmaxSlider.value():
            self.fminSlider.setValue(self.fmaxSlider.value())
    def Onfminspin_valueChange(self):
        self.fminSlider.setValue(self.fminspin.value()*10)
    def Onfmaxspin_valueChange(self):
        self.fmaxSlider.setValue(self.fmaxspin.value() * 10)
    def Onbtnok(self):
        self.errorcontrol=True
        if len(self.File_list.selectedItems())==0:
            QMessageBox.about(self, "tips", "please set export files")
        else:
            self.pgb = QProgressBar(self)
            self.pgb.setWindowTitle("Working")
            self.pgb.setGeometry(10, 5, 540, 20)
            self.pgb.show()
            if self.detrend_switch.isChecked():
                self.current_process.setText("detrend")
                self.detrend()
            if self.remove_response_switch.isChecked():
                self.current_process.setText("rm_response")
                self.remove_response()
            if self.bandpass_switch.isChecked():
                self.current_process.setText("bp_filter")
                self.bandpass()
            self.pgb.close()
            self.current_process.setText(" ")
            if self.errorcontrol==True:
                QMessageBox.about(self, "tips", "finished")
                self.Rcs.update_ondraw_stations()
                self.Rcs.draw()
    def Onbtnback(self):
        self.close()
        pass
    def detrend(self):
        currnum=0
        if len(self.File_list.selectedItems())==1:
            for item in self.channel_list.selectedItems():
                allnum=len(self.channel_list.selectedItems())
                station=item.parent
                if self.radioConstant.isChecked():
                    station.detrend(type='constant')
                if self.radioLinear.isChecked():
                    station.detrend(type='linear')
                self.pgb.setValue(float(currnum * 100) / float(allnum))
                currnum=currnum+1
            pass
        else:
            for item in self.File_list.selectedItems():
                allnum=len(self.File_list.selectedItems())
                file=item.parent
                if self.radioConstant.isChecked():
                    file.detrend(type='constant')
                if self.radioLinear.isChecked():
                    file.detrend(type='linear')
                self.pgb.setValue(float(currnum*100)/float(allnum))
                currnum = currnum + 1
    def bandpass(self):
        currnum = 0
        try:
            if len(self.File_list.selectedItems()) == 1:
                for item in self.channel_list.selectedItems():
                    allnum = len(self.channel_list.selectedItems())
                    station = item.parent
                    station.bandpass('bandpass',
                                     freqmin=float(self.fminspin.text()[0:-2]),
                                     freqmax=float(self.fmaxspin.text()[0:-2]),)
                    self.pgb.setValue(float(currnum * 100) / float(allnum))
                    currnum = currnum + 1
                pass
            else:
                '''calculate allnum'''
                for item in self.File_list.selectedItems():
                    allnum = len(item.parent.stations)
                for item in self.File_list.selectedItems():
                    file = item.parent
                    for station in file.stations:
                        station.bandpass('bandpass',
                                         freqmin=float(self.fminspin.text()[0:-2]),
                                         freqmax=float(self.fmaxspin.text()[0:-2]),)
                        self.pgb.setValue(float(currnum * 100) / float(allnum))
                        currnum = currnum + 1
        except Exception,e:
            self.errorcontrol = False
            QMessageBox.about(self,"Error",str(e))
        pass
    def remove_response(self):
        currnum = 0
        try:
            error_str="mismatch station:\n"
            allnum = len(self.File_list.selectedItems())
            for item in self.File_list.selectedItems():
                file=item.parent
                file.setInv()
                self.pgb.setValue(float(currnum * 100) / float(allnum))
                currnum = currnum + 1
            currnum=0
            error=True
            if self.pre_filt_switch.isChecked():
                pre_filt = [self.f1_spin.value(),
                            self.f2_spin.value(),
                            self.f3_spin.value(),
                            self.f4_spin.value()]
            else:
                pre_filt=None
            if len(self.File_list.selectedItems()) == 1:
                for item in self.channel_list.selectedItems():
                    allnum = len(self.channel_list.selectedItems())
                    station = item.parent
                    try:
                        station.remove_response(inventory=station.parent.Inv,
                                                water_level=float(self.water_level_spin.text()),
                                                pre_filt=pre_filt)

                    except :
                        error=False
                        error_str=error_str+str(station.name)+"\n"
                    self.pgb.setValue(float(currnum * 100) / float(allnum))
                    currnum = currnum + 1

            else:
                '''calculate allnum'''
                for item in self.File_list.selectedItems():
                    allnum = len(item.parent.stations)
                for item in self.File_list.selectedItems():
                    file = item.parent
                    for station in file.stations:
                        try:
                            station.remove_response(inventory=station.parent.Inv,
                                                    water_level=float(self.water_level_spin.text()),
                                                    pre_filt=pre_filt)

                        except:
                            error = False
                            error_str = error_str + str(station.name) + "\n"
                        self.pgb.setValue(float(currnum * 100) / float(allnum))
                        currnum = currnum + 1
            if error == False:
                QMessageBox.about(self, "error", error_str)
        except Exception, e:
            self.errorcontrol = False
            QMessageBox.about(self, "Error", str(e))