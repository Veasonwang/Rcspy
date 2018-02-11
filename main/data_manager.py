# -*- coding: utf-8 -*-
'''
Core data framework
'''
from obspy.signal.trigger import ar_pick
from obspy.core.event.base import *
from obspy.core.event.origin import Pick
from obspy import *
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from util import QTreeWidgetItem
from operator import attrgetter
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
    def clear_selected_station_picks(self,items):
        reply = QMessageBox.question(self.parent, 'Message', 'You sure to remove?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            update = False
            for item in items:
                if isinstance(item.parent, Station):
                    station = item.parent
                    station.clearpicks()
                    update=True
            if update == True:
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
        if len(self.channels)==3:
            self.visible = visible
            if visible:
                self.QStationItem.setIcon(0,
                                          QIcon(os.path.join(basedir,
                                                'icons/eye-24.png')))
            else:
                self.QStationItem.setIcon(0,
                                          QIcon(os.path.join(basedir,
                                                'icons/eye-hidden-24.png')))
        else:
            self.visible=False
            self.QStationItem.setIcon(0,
                                      QIcon(os.path.join(basedir,
                                                         'icons/eye-hidden-24.png')))
            pass
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
    def Filter(self,type,**kwargs):
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
    def Ar_pick(self,f1,f2,lta_p,sta_p,lta_s,sta_s,m_p,m_s,l_p,l_s):
        Z=self.getchannelbyNZE('Z')
        N=self.getchannelbyNZE('N')
        E=self.getchannelbyNZE('E')
        df=self.stats.sampling_rate
        pg_pick,sg_pick=ar_pick(Z.origintr.data, N.origintr.data, E.origintr.data, df,f1,f2,lta_p,sta_p,lta_s,sta_s,m_p,m_s,l_p,l_s,s_pick=True)
        #pg_pick, sg_pick = ar_pick(Z.tr.data, N.tr.data, E.tr.data, df, 1, 20, 1, 0.1, 4, 1, 2, 8,
        #                           0.1, 0.2, s_pick=True)
        starttime=self.stats.starttime
        pg_time=starttime+pg_pick
        sg_time=starttime+sg_pick
        for chn in self.channels:
            chn.getpick(pg_time,'Pg')
            chn.getpick(sg_time,'Sg')
    def setwaveform(self,type):
        for channel in self.channels:
            channel.setwaveform(type)
    def clearpicks(self):
        for channel in self.channels:
            channel.clearpicks()

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
        self.stats=tr.stats
        self.origintr=tr.copy()
        self.station = station
        self.channel = tr.stats.channel
        self.starttime=tr.stats.starttime
        self.edntime=tr.stats.endtime
        self.setstationTree()
        self.datamean=self.tr.data.mean()
        self.tr_VEL=self.tr.copy()
        self.tr_DISP=None
        self.tr_ACC=None
        self.currentwaveform='VEL'
        self._initpicks()
    def _initpicks(self):
        self.pickPg=None
        self.pickSg=None
        self.pickPn = None
        self.pickSn = None
        self.picks=[]
        self.picks.append(self.pickPg)
        self.picks.append(self.pickSg)
        self.picks.append(self.pickPn)
        self.picks.append(self.pickSn)
    def getpick(self,time,phase):
        if phase=='Pg':
            stream_ID=WaveformStreamID(network_code=self.stats.network,
                                       station_code=self.stats.station,
                                       location_code=self.stats.location,
                                       channel_code=self.stats.channel)
            self.pickPg=Pick(time=time,waveform_id=stream_ID,phase_hint=phase)
            self.picks[0]=self.pickPg
        if phase=='Sg':
            stream_ID=WaveformStreamID(network_code=self.stats.network,
                                       station_code=self.stats.station,
                                       location_code=self.stats.location,
                                       channel_code=self.stats.channel)
            self.pickSg=Pick(time=time,waveform_id=stream_ID,phase_hint=phase)
            self.picks[1] = self.pickSg
        if phase=='Pn':
            stream_ID=WaveformStreamID(network_code=self.stats.network,
                                       station_code=self.stats.station,
                                       location_code=self.stats.location,
                                       channel_code=self.stats.channel)
            self.pickPn=Pick(time=time,waveform_id=stream_ID,phase_hint=phase)
            self.picks[2] = self.pickPn
        if phase=='Sn':
            stream_ID=WaveformStreamID(network_code=self.stats.network,
                                       station_code=self.stats.station,
                                       location_code=self.stats.location,
                                       channel_code=self.stats.channel)
            self.pickSn=Pick(time=time,waveform_id=stream_ID,phase_hint=phase)
            self.picks[3] = self.pickSn
    def clearpick(self,phase):
        for pick in self.picks:
            i=self.picks.index(pick)
            if pick!=None:
                if pick.phase_hint==phase:
                    self.picks[i]=None
    def clearpicks(self):
        for i in range(len(self.picks)):
            self.picks[i]=None
    def setstationTree(self):
        self.QChannelItem = QTreeWidgetItem(self)
        self.QChannelItem.setText(1, '%s @ %d Hz' %
                                  (self.tr.stats.channel,
                                   1. / self.tr.stats.delta))
        self.QChannelItem.setText(2, '%s\n%s' %
                                  (self.tr.stats.starttime,
                                   self.tr.stats.endtime))
        self.station.QStationItem.addChild(self.QChannelItem)
    def setwaveform(self,type):
        if type=='VEL':
            if self.tr_VEL!=None:
                self.tr=self.tr_VEL
                self.currentwaveform='VEL'
        if type=='DISP':
            if self.tr_DISP!=None:
                self.tr=self.tr_DISP
                self.currentwaveform='DISP'
        if type=='ACC':
            if self.tr_ACC!=None:
                self.tr=self.tr_ACC
                self.currentwaveform='ACC'

















