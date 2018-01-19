'''
To handle gui events and draw cruve
'''


from obspy.core import UTCDateTime, AttribDict
import os
from  PyQt5.QtWidgets import QTreeWidgetItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
from PyQt5.QtGui import QFont,QIcon
import copy
import math
from PyQt5 import QtGui
from PyQt5 import QtCore
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=23, height=14, dpi=72):

        fig = Figure(figsize=(width, height), dpi=72,linewidth=1)
        self.axes = []
        self.fig=fig
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        self.ondrawtr=[]             #To writr down the trace order
        self.labeloffset = 1         #offset label offset
        FigureCanvas.updateGeometry(self)
        #self.connectevent()         #connect to recive the mouse event

    def getstream(self,stream):
        self.stream=stream
    def drawAxes(self,stations,VisibleChn):
        self.ondrawtr=[]
        self.fig.clear()
        axes=[]
        s=[]
        t=[]
        self.ss=s
        self.tt=t
        for i in range(len(self.axes)):
            self.axes[i].cla()
        self.axes=axes
        visnum=0
        if VisibleChn.ZVisible==True:
            visnum=visnum+1
        if VisibleChn.NVisible==True:
            visnum=visnum+1
        if VisibleChn.EVisible==True:
            visnum=visnum+1

        drawnumber=len(stations)*visnum
        self.fig.clear()
        self.labeloffset=2.0/(float(math.sqrt(float(drawnumber)))+0.1)
        if self.labeloffset>1:
            self.labeloffset=1
        for i in range(drawnumber):
            if i == 0:
                ax = self.fig.add_subplot(drawnumber, 1, 1)
            else:
                ax = self.fig.add_subplot(drawnumber, 1, i + 1)
                #ax.xaxis.set_ticks_position("top")
            axes.append(ax)
        for station in stations:
            if(VisibleChn.ZVisible==True):
                t.append(station.getchannelbyNZE('Z').times().copy())
                s.append(copy.deepcopy(station.getchannelbyNZE('Z').data.copy()))
                self.ondrawtr.append(copy.deepcopy(station.getchannelbyNZE('Z')))
            if (VisibleChn.NVisible == True):
                t.append(station.getchannelbyNZE('N').times().copy())
                s.append(copy.deepcopy(station.getchannelbyNZE('N').data.copy()))
                self.ondrawtr.append(copy.deepcopy(station.getchannelbyNZE('N')))
            if (VisibleChn.EVisible == True):
                t.append(station.getchannelbyNZE('E').times().copy())
                s.append(copy.deepcopy(station.getchannelbyNZE('E').data.copy()))
                self.ondrawtr.append(copy.deepcopy(station.getchannelbyNZE('E')))

        for i in range(len(self.axes)):
            self.axes[i].cla()
            self.axes[i].plot(self.tt[i], self.ss[i], 'g')
        self.drawIds()
        self.fig.subplots_adjust(bottom=0.001, hspace=0.000, right=0.999, top=0.999, left=0.001)
        self.draw()





    def drawIds(self):
        """
        draws the trace ids plotted as text into each axes.
        """
        x = 0.01
        y = 0.92
        bbox = dict(boxstyle="round,pad=0.4", fc="w", ec="k", lw=1.2, alpha=1.0)

        # labeloffset to adjust the size of the label in case of too many plotted number

        kwargs = dict(va="top", ha="left", fontsize=16*self.labeloffset, family='monospace',
                      zorder=10000)
        for ax, tr in zip(self.axes, self.ondrawtr):
            ax.text(x, y, tr.id, color="k", transform=ax.transAxes,
                    bbox=bbox, **kwargs)
class ChannelVisible:
    def __init__(self,parent=None):
        self.parent=parent
        self.ZVisible=True
        self.NVisible=False
        self.EVisible=False
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
        self.parent.stationTree.addTopLevelItem(
            self.stations[-1].QStationItem)

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

        self.QStationItem = QTreeWidgetItem()
        self.QStationItem.setText(1, '%s.%s' %
                                  (self.stats.network,
                                   self.stats.station))
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
        for channel in self.channels:
            if channel.channel[-1]==direction:
                return channel.tr
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
        self.QChannelItem = QTreeWidgetItem()
        self.QChannelItem.setText(1, '%s @ %d Hz' %
                                  (self.tr.stats.channel,
                                   1./self.tr.stats.delta))
        self.QChannelItem.setText(2, '%s\n%s' %
                                  (self.tr.stats.starttime,
                                   self.tr.stats.endtime))
        self.station.QStationItem.addChild(self.QChannelItem)

