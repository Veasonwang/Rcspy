"""
class Inheriting from Pyqt5 and Matplotlib
"""

from PyQt5.QtWidgets import QListWidgetItem as QLWI
from  PyQt5.QtWidgets import QTreeWidgetItem as QTWI
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import  QMenu, QSizePolicy,QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import math
class Qcwidget(QWidget):
    def __init__(self,arg):
        QtWidgets.QWidget.__init__(self,arg)
    def resizeEvent(self, QResizeEvent):
        self.Rcs.onqwidghtsizechangeed(QResizeEvent)
    def setRcs(self,Rcs):
        self.Rcs=Rcs
class QListWidgetItem(QLWI):
    def __init__(self,parent):
        QLWI.__init__(self)
        self.parent=parent


class QTreeWidgetItem(QTWI):
    def __init__(self,parent):
        QTWI.__init__(self)
        self.parent=parent
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=23, height=28, dpi=72):

        fig = Figure(figsize=(width, height), dpi=72,linewidth=1)
        self.axes = []
        self.fig=fig
        self.limratio=1
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        self.ondrawchn=[]             #To write down the channel order
        self.labeloffset = 1         #offset label offset
        FigureCanvas.updateGeometry(self)
    def drawAxes(self,stations,VisibleChn):
        """
        final drawing function
        draw stations on the figure
        :param stations:
        :param VisibleChn:
        :return:
        """
        self.ondrawchn=[]
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

        """
        cauculate the drawnumber to create axes
        """
        drawnumber=len(stations)*visnum
        self.fig.clear()


        """
        setting label offset
        """
        self.labeloffset=(1.8/(float(math.sqrt(float(drawnumber)))+0.1))+0.25
        if self.labeloffset>1:
            self.labeloffset=1
        """
        high performance
        """
        axappend=self.axes.append
        tappend=t.append
        sappend=s.append
        ondrawchnappend=self.ondrawchn.append
        for i in range(drawnumber):
            if i == 0:
                ax = self.fig.add_subplot(drawnumber, 1, 1)
            else:
                ax = self.fig.add_subplot(drawnumber, 1, i + 1)
                #ax.xaxis.set_ticks_position("top")

            #self.axes.append(ax)
            """
            high performance
            """
            axappend(ax)
        for station in stations:
            if(VisibleChn.ZVisible==True):
                tappend(station.getchannelbyNZE('Z').tr.times().copy())
                sappend(station.getchannelbyNZE('Z').tr.data.copy())
                ondrawchnappend(station.getchannelbyNZE('Z'))
            if (VisibleChn.NVisible == True):
                tappend(station.getchannelbyNZE('N').tr.times().copy())
                sappend(station.getchannelbyNZE('N').tr.data.copy())
                ondrawchnappend(station.getchannelbyNZE('N'))
            if (VisibleChn.EVisible == True):
                tappend(station.getchannelbyNZE('E').tr.times().copy())
                sappend(station.getchannelbyNZE('E').tr.data.copy())
                ondrawchnappend(station.getchannelbyNZE('E'))
        for i in range(len(self.axes)):
            self.axes[i].cla()
            self.axes[i].plot(self.tt[i], self.ss[i], 'g')
            mean=self.ondrawchn[i].datamean
            ymin,ymax=self.axes[i].get_ylim()
            ymin=ymin*self.limratio
            ymax=ymax*self.limratio
            if (ymax-mean)>(mean-ymin):
                ymin=ymin-(ymax+ymin-2*mean)
            else:
                ymax=ymax+(2*mean-ymax-ymin)
            self.axes[i].set_ylim(ymin,ymax)

        self.drawIds()          #draw label
        self.fig.subplots_adjust(bottom=0.001, hspace=0.000, right=0.999, top=0.999, left=0.001)
        self.draw()
    def get_drawchnarray(self,index):
        return self.ondrawchn[index]
    def drawIds(self):
        """
        draws the trace ids plotted as text into each axes.
        """
        x = 0.01
        y = 0.92
        bbox = dict(boxstyle="round,pad=0.4", fc="w", ec="k", lw=1.2, alpha=1.0)

        # labeloffset to adjust the size of the label in case of too large plotted number

        kwargs = dict(va="top", ha="left", fontsize=16*self.labeloffset, family='monospace',
                      zorder=10000)
        for ax, tr in zip(self.axes, self.ondrawchn):
            ax.text(x, y, tr.tr.id, color="k", transform=ax.transAxes,
                    bbox=bbox, **kwargs)


