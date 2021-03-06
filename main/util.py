# -*- coding: utf-8 -*-
"""
class Inheriting from Pyqt5 and Matplotlib
"""

from PyQt5.QtWidgets import QListWidgetItem as QLWI
from  PyQt5.QtWidgets import QTreeWidgetItem as QTWI
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import   QSizePolicy,QWidget
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QScrollArea as QSLA
import math
import matplotlib
class Qcwidget(QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
    def resizeEvent(self, QResizeEvent):
        self.Rcs.onqwidghtsizechangeed(QResizeEvent)
    def setRcs(self,Rcs):
        self.Rcs=Rcs
class QcScrollArea(QSLA):
    def __init__(self,parent):
        QSLA.__init__(self,parent)
    def setRcs(self,Rcs):
        self.Rcs=Rcs
    def wheelEvent(self,event):
        if self.Rcs.zoomswi==True:
            pass
        else:
            QSLA.wheelEvent(self, event)
        pass
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
        self.ylimratio=1
        self.xlimratio=1
        FigureCanvas.__init__(self, fig)
        self.signalheight=300
        self.setParent(parent)
        self.parent=parent
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        self.ondrawchn=[]             #To write down the channel order
        self.labeloffset = 1         #offset label offset
        FigureCanvas.updateGeometry(self)
        matplotlib.rcParams['xtick.direction'] = 'in'
        matplotlib.rcParams['ytick.direction'] = 'in'
    def setRcs(self,Rcs):
        self.Rcs=Rcs
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
            string = "clearing axes " + str(i) + " of " + str(len(self.axes))
            self.Rcs.statusbar.showMessage(string)
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
        height=self.signalheight*drawnumber
        self.parent.setFixedHeight(height)
        width=self.parent.geometry().width()
        self.resize(width,height)
        self.fig.clear()

        """
        setting label offset
        """
        singledrawnumber=int(self.Rcs.drawnumber_combobox.currentText())
        self.labeloffset=(1.8/(float(math.sqrt(float(singledrawnumber)))+0.1))+0.25
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
            string = "ready axes "+str(i)+" of "+str(drawnumber)
            self.Rcs.statusbar.showMessage(string)
            if i == 0:
                ax = self.fig.add_subplot(drawnumber, 1, 1)
            else:
                ax = self.fig.add_subplot(drawnumber, 1, i + 1)

            """
            high performance
            """
            axappend(ax)
        currentnum=0
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
            currentnum=currentnum+1
            string = "ready station" + str(currentnum) + " of " + str(drawnumber)
            self.Rcs.statusbar.showMessage(string)
        currentnum=0
        for i in range(len(self.axes)):
            self.axes[i].cla()
            self.axes[i].xaxis.set_tick_params(direction='in')
            self.axes[i].plot(self.tt[i], self.ss[i],'g')

            '''set Ylimratio'''
            mean=self.ondrawchn[i].datamean
            ymin,ymax=self.axes[i].get_ylim()
            ymin=ymin*self.ylimratio
            ymax=ymax*self.ylimratio
            if (ymax-mean)>(mean-ymin):
                ymin=ymin-(ymax+ymin-2*mean)
            else:
                ymax=ymax+(2*mean-ymax-ymin)
            self.axes[i].set_ylim(ymin,ymax)
            '''set Xlimratio'''
            string = "setting" + str(currentnum) + " of " + str(drawnumber)
            self.Rcs.statusbar.showMessage(string)
            currentnum=currentnum+1
        self.Rcs.statusbar.showMessage("drawing")
        self.fig.subplots_adjust(bottom=0.001, hspace=0.000, right=0.999, top=0.999, left=0.001)
    def get_drawchnarray(self,index):
        return self.ondrawchn[index]
    def get_drawaxes(self,index):
        return self.axes[index]
    def drawIds(self):
        """
        draws the trace ids plotted as text into each axes.
        """
        x = 0.01
        y = 0.9
        bbox = dict(boxstyle="round,pad=0.4", fc="w", ec="k", lw=1.2, alpha=1.0)
        # labeloffset to adjust the size of the label in case of too large plotted number
        kwargs = dict(va="top", ha="left", fontsize=16*self.labeloffset, family='monospace',
                      zorder=10000)
        for axes, tr  in zip(self.axes, self.ondrawchn):
            axes.text(x, y, tr.tr.id, color="k", transform=axes.transAxes,
                    bbox=bbox, **kwargs)
            axes.text(0.85,0.85,tr.currentwaveform,color='r',fontsize=9,transform=axes.transAxes)
    def drawTraveltimes(self):
        for axes,chn in zip(self.axes,self.ondrawchn):
            for pick in chn.arriveltime:
                if pick!=0:
                    x=pick.time
                    string=pick.phasename+str(pick.time)
                    xmin,xmax=axes.get_xlim()
                    if x>(xmax-xmin):
                        pass
                    else:
                        ymin, ymax = axes.get_ylim()
                        y=0.5*ymax
                        '''draw pick_text'''
                        if pick.phasename == 'P':
                            y = 0.85 * ymax
                        if pick.phasename == 'S':
                            y = 0.75 * ymax
                        if pick.phasename == 'Pn':
                            y = 0.65 * ymax
                        if pick.phasename == 'Sn':
                            y = 0.55 * ymax
                        axes.axvline(x, 0.2, 0.95,color='r')
                        axes.text(x,y,string,color='r',fontsize=10)
    def drawPicks(self):
        for axes,chn in zip(self.axes,self.ondrawchn):
            for pick in chn.picks:
                if pick != None:
                    x = pick.time - chn.starttime
                    ymin, ymax = axes.get_ylim()
                    '''draw pick_text'''
                    if pick.phase_hint == 'Pg':
                        y = 0.85 * ymax
                        color = '#FF00FF'
                    if pick.phase_hint == 'Sg':
                        y = 0.75 * ymax
                        color = '#EEB422'
                    if pick.phase_hint == 'Pn':
                        y = 0.65 * ymax
                        color = '#00868B'
                    if pick.phase_hint == 'Sn':
                        y = 0.55 * ymax
                        color = '#27408B'
                    string = pick.phase_hint + " " + str(pick.time)
                    axes.axvline(x, 0.2, 0.95, color=color)
                    axes.text(x, y, string, color=color, fontsize=10)
    def updateaxes(self,axes):
        i=self.axes.index(axes)
        ymin, ymax = self.axes[i].get_ylim()
        xmin, xmax = self.axes[i].get_xlim()
        axes.cla()
        axes.plot(self.tt[i], self.ss[i],'g')
        self.axes[i].set_ylim(ymin, ymax)
        self.axes[i].set_xlim(xmin,xmax)
        '''draw picks'''
        if self.Rcs.pick_phase_checkbox.isChecked():
            self.updatePicks(axes)
        '''draw Ids'''
        self.updateIds(axes)
        '''draw Travel_time'''
        if self.Rcs.traveltime_checkBox.isChecked():
            self.updateTravel_time(axes)
        self.fig.canvas.draw()
    def updatePicks(self,axes):
        i = self.axes.index(axes)
        chn = self.ondrawchn[i]
        for pick in chn.picks:
            if pick != None:
                x = pick.time - chn.starttime
                ymin, ymax = axes.get_ylim()
                '''draw pick_text'''
                if pick.phase_hint == 'Pg':
                    y = 0.85 * ymax
                    color = '#FF00FF'
                if pick.phase_hint == 'Sg':
                    y = 0.75 * ymax
                    color = '#EEB422'
                if pick.phase_hint == 'Pn':
                    y = 0.65 * ymax
                    color = '#00868B'
                if pick.phase_hint == 'Sn':
                    y = 0.55 * ymax
                    color = '#27408B'
                string = pick.phase_hint + " " + str(pick.time)
                axes.axvline(x, 0.2, 0.95, color=color)
                axes.text(x, y, string, color=color, fontsize=10)

    def updateIds(self,axes):
        i = self.axes.index(axes)
        chn = self.ondrawchn[i]
        bbox = dict(boxstyle="round,pad=0.4", fc="w", ec="k", lw=1.2, alpha=1.0)
        kwargs = dict(va="top", ha="left", fontsize=16 * self.labeloffset, family='monospace',
                      zorder=10000)
        axes.text(0.01, 0.9, chn.tr.id, color="k", transform=axes.transAxes,
                  bbox=bbox, **kwargs)
        axes.text(0.05, 0.78, chn.currentwaveform, color='r', fontsize=9, transform=axes.transAxes)

    def updateTravel_time(self,axes):
        chn = self.get_drawchnarray(self.axes.index(axes))
        for arrive in chn.arriveltime:
            if arrive != 0:
                x = arrive.time
                string = arrive.phasename + str(arrive.time)
                xmin, xmax = axes.get_xlim()
                if x > (xmax - xmin):
                    pass
                else:
                    ymin, ymax = axes.get_ylim()
                    y = 0.5 * ymax
                    '''draw pick_text'''
                    if arrive.phasename == 'P':
                        y = 0.85 * ymax

                    if arrive.phasename == 'S':
                        y = 0.75 * ymax

                    if arrive.phasename == 'Pn':
                        y = 0.65 * ymax

                    if arrive.phasename == 'Sn':
                        y = 0.55 * ymax

                    axes.axvline(x, 0.2, 0.95, color='r')
                    axes.text(x, y, string, color='r', fontsize=10)





























