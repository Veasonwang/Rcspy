import matplotlib
matplotlib.use("Qt5Agg")
from obspy import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# -*- coding: ascii -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget,QFileDialog
import copy
from numpy import arange, sin, pi
import n_rcsui
from matplotlib.figure import Figure
import sys
import random
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=18, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
class MyDynamicMplCanvas(MplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()
    def doing(self,filename):
        st = read(filename)
        tr = st[5]
        s = tr.data
        t = arange(1.0, len(s), 1)
        self.axes.cla()
        self.axes.plot(t,s[0:-1],'r')
        self.draw()


class Rcspy(n_rcsui.Ui_MainWindow,QMainWindow):

    def __init__(self,parent=None):
        app = QApplication(sys.argv)
        super(Rcspy,self).__init__()
        self.setupUi(self)

        self.menuconncect()
        #self.onfileopen()
        self.qml = MyDynamicMplCanvas(self.qmlcanvas, dpi=100)
        self.show()
        app.exec_()
        # print aw.qmlcanvas.width


    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
    def onfileopen(self):


        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.qml.doing(filename)
        #self.drawAxes(filename)
        #self.qmlcanvas.update()
        #self.listWidget.addItem(filename)
    def drawAxes(self,filename):
        #td1 = "C:\\Users\\v\\Desktop\\My_final_PC\\data_for_debug\\YN.201506152046.0002.seed"
        st = read(filename)
        self.qml.addaxs(6)
        #st=read(td1)
        tr = st[5]
        s = tr.data
        time = tr.stats.starttime
        t = arange(0.0, len(s), 1)

        print 6
        #self.qml.axes.cla()
        for i in range(0, self.qml.drawnum):
            tr = st[i]
            s = tr.data
            time1 = tr.stats.starttime
            # print time1
            time2 = tr.stats.endtime
            #print time2
            t = arange(1.0, 30000, 1)
            self.qml.tt.append(copy.deepcopy(t))
            self.qml.ss.append(copy.deepcopy(s))
            if i == 0:
                ax =self.qml.fig.add_subplot(self.qml.drawnum, 1, i + 1)
            else:
                ax =self.qml.fig.add_subplot(self.qml.drawnum, 1, i + 1, sharex=self.axes[0], sharey=self.axs[0])
            self.qml.axes.append(copy.copy(ax))
        print 5
        for i in range(0, self.qml.drawnum):
            self.qml.axes[i].plot(self.tt[i], self.qml.ss[i][0:-1])
        self.qml.draw()

if __name__ == '__main__':
    Rcspy()