# -*- coding: utf-8 -*-
'''
Core data framework
'''
from obspy.signal.trigger import ar_pick
from obspy.core.event.base import *
from obspy.core.event.origin import Pick
from obspy.core.event.event import Event
from obspy.taup.tau import TauPyModel
from obspy.geodetics.base import *
from obspy import *
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from util import QTreeWidgetItem
from operator import attrgetter
from obspy.core.inventory import Inventory
from obspy.core.event.origin import Origin
class Source:
    '''
    TO hold source info
    '''
    def __init__(self,longitude,latitude,depth,time):
        self.longitude=longitude
        self.latitude=latitude
        self.depth=depth
        self.time=time
class ChannelVisible:
    def __init__(self,parent=None):
        self.parent=parent
        self.ZVisible=True
        self.NVisible=False
        self.EVisible=False
class Phasetime:
    def __init__(self,phasename,traveltime):
        self.phasename=phasename
        self.time=traveltime
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
    def updatestats(self):
        for file in self.files:
            file.updatestats()
    def exportxml(self,items):
        for item in items:
            item.parent.exportQuakeml()
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
        self.source=None
        self.Inv=None
        self.Invpath=None
        self.origin = Origin()
        for stat in set([tr.stats.station for tr in st]):
            self.addStation(st=st.select(station=stat))
        self.setInv()
    '''
    def init_event(self):
        self.picks=[]
        for station in self.stations:
            for pick in station.picks:
                if pick != None:
                    self.picks.append(pick)
        self.origin=Origin()
        self.origins=[]
        self.origins.append(self.origin)
        self.event = Event(picks=self.picks,origins=self.origins)
    '''
    def addStation(self, st):
        '''
        Adds a station from
        :param st: obspy stream
        '''
        self.stations.append(Station(stream=st, parent=self))
        self.QStationItem.addChild(self.stations[-1].QStationItem)
    def update_event(self):
        self.picks = []
        for station in self.stations:
            for pick in station.picks:
                if pick != None:
                    self.picks.append(pick)
        self.origins = []
        self.origins.append(self.origin)
        self.event = Event(picks=self.picks, origins=self.origins)
    def export_event(self,filename):
        self.update_event()
        self.event.write(filename,format='QUAKEML')
    def Export_calculation_phase_file(self,filename):
        head1=' \tUTCTIME\tTimeError\tLatitude\tLatitude_Error\tLongitude_Error\tDepth\tDepth_Error'
        head2='\tStationNumber\tTraveltime\tPhase\n'
        head=head1+head2
        wf=open(filename,'w')
        wf.write(unicode(head))
        source_info="#\t"+str(self.source.time.year)+" "+str(self.source.time.month)+" "\
                         +str(self.source.time.day)+" "+str(self.source.time.hour)+" "\
                         +str(self.source.time.minute)+" "+str(self.source.time.second)
        source_info+="\ttimeerror"
        source_info+="\t"+str(self.source.latitude)+"\tlatierror"
        source_info+="\t"+str(self.source.longitude)+"\tlongierror"
        source_info+="\t"+str(self.source.depth)+"\tdeptherror"
        for station in self.stations:
            station_info="\t"+station.name
            for phase in station.traveltime:
                phase_info="\t"+str(phase.time)+"\t"+phase.phasename+"\n"
                line=source_info+station_info+phase_info
                wf.write(unicode(line))
    def Export_Pick_phase_file(self,filename):
        head1 = ' \tUTCTIME\tTimeError\tLatitude\tLatitude_Error\tLongitude_Error\tDepth\tDepth_Error'
        head2 = '\tStationNumber\tTraveltime\tPhase\n'
        head = head1 + head2
        wf = open(filename, 'w')
        wf.write(unicode(head))
        source_info = "#\t" + str(self.source.time.year) + " " + str(self.source.time.month) + " " \
                      + str(self.source.time.day) + " " + str(self.source.time.hour) + " " \
                      + str(self.source.time.minute) + " " + str(self.source.time.second)
        source_info += "\ttimeerror"
        source_info += "\t" + str(self.source.latitude) + "\tlatierror"
        source_info += "\t" + str(self.source.longitude) + "\tlongierror"
        source_info += "\t" + str(self.source.depth) + "\tdeptherror"
        for station in self.stations:
            station_info = "\t" + station.name
            for pick in station.picks:
                if pick!=None:
                    pick_info = "\t" + str(pick.time) + "\t" + pick.phase_hint+ "\n"
                    line = source_info + station_info + pick_info
                    wf.write(unicode(line))
    def attach_event(self,filename):
        try:
            catalog=read_events(filename)
        except Exception, e :
            QMessageBox.about(self.parent,"tips",e)
        self.event=catalog.events[0]
        event=self.event
        self.origin=self.event.origins[0]
        try:
            self.source=Source(self.origin.longitude,self.origin.latitude,
                            self.origin.depth,self.origin.time)
        except:
            self.source=None
        for pick in event.picks:
            for station in self.stations:
                for channel in station.channels:
                    if pick.waveform_id.__eq__(channel.stream_ID):
                        if pick.phase_hint=='Pg':
                            channel.picks[0]=pick.copy()
                        if pick.phase_hint=='Sg':
                            channel.picks[1]=pick.copy()
                        if pick.phase_hint=='Pn':
                            channel.picks[2]=pick.copy()
                        if pick.phase_hint=='Sn':
                            channel.picks[3]=pick.copy()
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

    def setinvisible(self):
        for station in self.stations:
            station.setVisible(False)
    def setInv(self):
        if self.format=='SEED':
            if not isinstance(self.Inv,Inventory):
                try:
                    self.Inv=read_inventory(self.path)
                    self.Invpath = self.path
                    self.get_station_info()
                except Exception,e:
                    self.Inv=None
                    self.Invpath=None
                    self.clear_station_info()
                    print e
    def setInvbypath(self,path):
        try:
            Inv=read_inventory(path)
            self.Inv=Inv
            self.Invpath=path
            self.get_station_info()
        except Exception,e:
            self.Inv = None
            self.Invpath = None
            self.clear_station_info()
            QMessageBox.about(self.parent,'Error',str(e))
    def clear_station_info(self):
        for station in self.stations:
            station.depth = -1
            station.longitude = -1
            station.latitude = -1
    def get_station_info(self):
        try:
            for station in self.stations:
                for network in self.Inv:
                    if station.network == network.code:
                        for sta in network:
                            if station.stationname == sta.code:
                                station.latitude = sta.latitude
                                station.longitude = sta.longitude
                                station.depth = sta[0].depth
                                break
                        break
        except Exception,e:
            print e
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
    def updatestats(self):
        for station in self.stations:
            station.updatestats()
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
        self._initvariable()
        self.setstationTree()
        for tr in self.st:
            self.channels.append(Channel(tr, station=self))
        self.setVisible(False)
    def _initvariable(self):
        self.picks = []
        self.starttime=self.stats.starttime
        self.traveltime = [Phasetime('P',0),Phasetime('S',0),Phasetime('Pn',0),Phasetime('Sn',0)]
        self.arriveltime = [Phasetime('P',0),Phasetime('S',0),Phasetime('Pn',0),Phasetime('Sn',0)]
        self.stats.channel = None
        self.network = self.stats.network
        self.stationname = self.stats.station
        self.depth = -1
        self.longitude = -1
        self.latitude = -1
        self.name = self.stats.network + "." + self.stats.station
        self.channels = []
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
            channel.origintr = channel.tr.copy()
    def Filter(self,type,**kwargs):
        for channel in self.channels:
            channel.tr=channel.tr.copy().filter(type=type,**kwargs)
            channel.origintr=channel.tr.copy()
            channel.datamean = channel.tr.data.mean()
    def remove_response(self,inventory=None,water_level=60,pre_filt=None):
        for channel in self.channels:
            channel.tr_VEL=channel.tr.copy().remove_response(inventory=inventory,output='VEL',water_level=water_level,
                                                        pre_filt=pre_filt)
            #channel.tr_DISP = channel.tr.copy().remove_response(inventory=inventory, output='DISP', water_level=water_level,
            #                                            pre_filt=pre_filt)
            #channel.tr_ACC = channel.tr.copy().remove_response(inventory=inventory, output='ACC', water_level=water_level,
            #                                            pre_filt=pre_filt)
            channel.tr_DISP=channel.tr_VEL.copy().integrate()
            channel.tr_ACC=channel.tr_VEL.copy().differentiate()
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
        print 1
        for chn in self.channels:
            #chn.clearpicks()
            chn.getpick(pg_time,'Pg')
            chn.getpick(sg_time,'Sg')
    def setwaveform(self,type):
        for channel in self.channels:
            channel.setwaveform(type)
    def clearpicks(self):
        for channel in self.channels:
            channel.clearpicks()
    def updatestats(self):
        for channel in self.channels:
            channel.update_stats()
    def get_travel_time(self,phase_list,source):
        taup=TauPyModel()
        degree=locations2degrees(source.latitude,source.longitude,self.latitude,self.longitude)
        if self.depth !=-1:
            arrivals=taup.get_travel_times(source.depth/1000,degree,phase_list,self.depth)
            for phasetime in arrivals:
                if phasetime.name=='P':
                    self.traveltime[0]=Phasetime('P',phasetime.time)
                    self.arriveltime[0]=Phasetime('P',self.parent.source.time+phasetime.time-UTCDateTime(self.starttime))
                if phasetime.name=='S':
                    self.traveltime[1] = Phasetime('S', phasetime.time)
                    self.arriveltime[1]=Phasetime('S',self.parent.source.time+phasetime.time-UTCDateTime(self.starttime))
                if phasetime.name=='Pn':
                    self.traveltime[2] =Phasetime('Pn', phasetime.time)
                    self.arriveltime[2]=Phasetime('Pn',self.parent.source.time+phasetime.time-UTCDateTime(self.starttime))
                if phasetime.name=='Sn':
                    self.traveltime[3] = Phasetime('Sn', phasetime.time)
                    self.arriveltime[3]=Phasetime('Sn',self.parent.source.time+phasetime.time-UTCDateTime(self.starttime))
            for channel in self.channels:
                channel.arriveltime=self.arriveltime
                channel.traveltime=self.traveltime
            print self.arriveltime[0].time
            print self.traveltime[0].time
    def get_source_info(self):
        pass
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
        self.stats=tr.stats.copy()
        self.origintr=tr.copy()
        self.stream_ID = WaveformStreamID(network_code=self.stats.network,
                                     station_code=self.stats.station,
                                     location_code=self.stats.location,
                                     channel_code=self.stats.channel)
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
        self.station.picks=self.picks
        self.traveltime=[]
        self.arriveltime=[]
    def getpick(self,time,phase):
        if phase=='Pg':
            self.pickPg=Pick(time=time,waveform_id=self.stream_ID,phase_hint=phase)
            self.picks[0]=self.pickPg
            self.stats.Pg=time
        if phase=='Sg':
            self.pickSg=Pick(time=time,waveform_id=self.stream_ID,phase_hint=phase)
            self.picks[1] = self.pickSg
            self.stats.Sg = time
        if phase=='Pn':
            self.pickPn=Pick(time=time,waveform_id=self.stream_ID,phase_hint=phase)
            self.picks[2] = self.pickPn
            self.stats.Pn = time
        if phase=='Sn':
            self.pickSn=Pick(time=time,waveform_id=self.stream_ID,phase_hint=phase)
            self.picks[3] = self.pickSn
            self.stats.Sn = time
    def clearpick(self,phase):
        for pick in self.picks:
            i=self.picks.index(pick)
            if pick!=None:
                if pick.phase_hint==phase:
                    self.picks[i]=None
                    delattr(self.stats,phase)
    def clearpicks(self):
        for i in range(len(self.picks)):
            self.picks[i]=None
            delattr(self.stats, 'Pg')
            delattr(self.stats, 'Sg')
            delattr(self.stats, 'Pn')
            delattr(self.stats, 'Sg')
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
    def update_stats(self):
        self.tr.stats=self.stats
    def spectrogram(self):
        self.tr.spectrogram(log=True,title=self.station.name+"."+self.channel+"."+str(self.starttime))
    '''
    def readpicks(self):
        if hasattr(self.stats,'Pg'):
            self.getpick(self.stats.Pg,'Pg')
        if hasattr(self.stats,'Sg'):
            self.getpick(self.stats.Sg,'Sg')
        if hasattr(self.stats,'Pn'):
            self.getpick(self.stats.Pn,'Pn')
        if hasattr(self.stats,'Sn'):
            self.getpick(self.stats.Sn,'Sn')
    '''

















