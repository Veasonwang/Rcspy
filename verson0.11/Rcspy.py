import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# -*- coding: ascii -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
import copy
import obspy.core.trace as tc
from numpy import arange, sin, pi
import n_rcsui
from matplotlib.figure import Figure
import sys
import random
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
            self.axes[i].plot(self.tt[i],self.ss[i],'r')
        self.draw()

class Rcspy(n_rcsui.Ui_MainWindow,QMainWindow):


    def __init__(self,parent=None):
        app = QApplication(sys.argv)
        super(Rcspy,self).__init__()
        self.setupUi(self)
        self.menuconncect()
        self.qml = MplCanvas(self.qmlcanvas, dpi=100)
        self.show()
        app.exec_()
        # print aw.qmlcanvas.width
    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
    def onfileopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.steam=read(filename)
        self.qml.drawAxes(self.steam,3)
        self.listivew_additem(self.steam)
    def listivew_additem(self,steam):
        for tr in steam:
            print tr.stats
            self.listWidget.addItem(tr.stats.network+"/"+tr.stats.station+"/"+tr.stats.location+"/"+tr.stats.channel)

    def testgit(self):
        pass


if __name__ == '__main__':
    Rcspy()