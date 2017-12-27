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

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=300):
        self.fig = Figure(figsize=(16,9),dpi=dpi)
        #self.axes.hold(False)
        self.compute_initial_figure()
        #
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass
class Rcspy(n_rcsui.Ui_MainWindow,QMainWindow):

    def __init__(self,parent=None):
        app = QApplication(sys.argv)
        super(Rcspy,self).__init__()
        self.setupUi(self)

        self.initqml()
        self.menuconncect()
        self.show()
        app.exec_()
        # print aw.qmlcanvas.width

    def initqml(self):
        self.qml = MplCanvas(self.qmlcanvas, dpi=100)

    def menuconncect(self):
        self.actionopen.triggered.connect(self.onfileopen)
    def onfileopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.drawAxes(self,filename)
        print filename
    def drawAxes(self,filename):
        #td1 = "C:\\Users\\v\\Desktop\\My_final_PC\\data_for_debug\\YN.201506152046.0002.seed"
        st = read(filename)
        #st=read(td1)
        tr = st[5]
        s = tr.data
        time = tr.stats.starttime
        t = arange(0.0, len(s), 1)
        tt = []
        ss = []
        axs = []
        print 6
        drawnum=6
        for i in range(0, drawnum):
            tr = st[i]
            s = tr.data
            time1 = tr.stats.starttime
           # print time1
            time2 = tr.stats.endtime
            #print time2
            t = arange(1.0, 30000, 1)
            tt.append(copy.deepcopy(t))
            ss.append(copy.deepcopy(s))
            if i == 0:
                ax =self.qml.fig.add_subplot(drawnum, 1, i + 1)
            else:
                ax =self.qml.fig.add_subplot(drawnum, 1, i + 1, sharex=axs[0], sharey=axs[0])
            axs.append(copy.copy(ax))
        print 5
        for i in range(0, drawnum):
            axs[i].plot(tt[i], ss[i][0:-1])
if __name__ == '__main__':
    Rcspy()