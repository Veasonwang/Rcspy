from obspy.core import UTCDateTime, AttribDict
import os
from  PyQt5.QtWidgets import QTreeWidgetItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
from PyQt5.QtGui import QFont,QIcon
import copy
from PyQt5 import QtGui
from PyQt5 import QtCore
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=17, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = []
        self.fig=fig
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
    def drawAxes(self,steam,drawnumber):
        self.fig.clear()
        axes=[]
        st = steam
        s=[]
        t=[]
        self.ss=s
        self.tt=t
        self.axes=axes
        for i in range(drawnumber):
            if i==0:
                ax=self.fig.add_subplot(drawnumber,1,1)
            else:
                ax = self.fig.add_subplot(drawnumber, 1, i + 1)
            axes.append(ax)
            t.append(st[i].times())
            s.append(st[i].data)
        for i in range(drawnumber):
            self.axes[i].cla()
        for i in range(drawnumber):
            self.axes[i].plot(self.tt[i],self.ss[i],'g')
        self.draw()
    def drawStations(self,stations,drawtype):
        self.fig.clear()
        axes=[]
        s=[]
        t=[]
        self.ss=s
        self.tt=t
        for i in range(len(self.axes)):
            self.axes[i].cla()
        self.axes=axes
        drawnumber=len(stations)
        self.fig.clear()
        for i in range(drawnumber):
            if i == 0:
                ax = self.fig.add_subplot(drawnumber, 1, 1)
            else:
                ax = self.fig.add_subplot(drawnumber, 1, i + 1)
                #ax.xaxis.set_ticks_position("top")
            axes.append(ax)
        for station in stations:
            if(drawtype=='N'):
                t.append(station.channels[0].tr.times().copy())
                s.append(copy.deepcopy(station.channels[0].tr.data.copy()))
        for i in range(len(self.axes)):
            self.axes[i].cla()
            self.axes[i].plot(self.tt[i], self.ss[i], 'g')
        self.draw()


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
    Represents a single Station and hold the plotItem in the layout
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

class Channel(object):
    '''
    Channel Container Object handels an individual channel

    self.QChannelItem represents the QTreeWidgetItem
    self.traceItem is the inherited pyqtgraph.PlotCurveItem
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
        #self.QChannelItem.setFont(1, QFont('', 7))
        #self.QChannelItem.setFont(2, QFont('', 7))
        self.station.QStationItem.addChild(self.QChannelItem)

    def plotTraceItem(self):
        '''
        Plots the pg.PlotCurveItem into self.station.plotItem
        '''
        self.plotTrace = self.tr.copy()
        # Filter if necessary
        if self.station.parent.parent.filterArgs is not None:
            self.plotTrace.filter('bandpass',
                                  **self.station.parent.parent.filterArgs)
        self.traceItem.setData(y=self.plotTrace.data, antialias=True)
        self.station.plotItem.getAxis('bottom').setScale(self.tr.stats.delta)

