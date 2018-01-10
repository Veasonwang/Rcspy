from obspy.core import UTCDateTime, AttribDict
import os
from  PyQt5.QtWidgets import QTreeWidgetItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
from PyQt5 import QtGui
from PyQt5 import QtCore
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=18, height=10, dpi=100):
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
class Stations(object):
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

