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
                #ax.xaxis.set_ticks_position("top")

            #self.axes.append(ax)
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
            #xmin, xmax = self.axes[i].get_xlim()
            #xmin = xmin * self.xlimratio
            #xmax = xmax * self.xlimratio
            #if (ymax - mean) > (mean - ymin):
            #    ymin = ymin - (ymax + ymin - 2 * mean)
            #else:
            #    ymax = ymax + (2 * mean - ymax - ymin)
            #self.axes[i].set_ylim(ymin, ymax)
            string = "setting" + str(currentnum) + " of " + str(drawnumber)
            self.Rcs.statusbar.showMessage(string)
            currentnum=currentnum+1
        self.Rcs.statusbar.showMessage("drawing")
        self.drawIds()          #draw label
        self.drawPicks()
        self.fig.subplots_adjust(bottom=0.001, hspace=0.000, right=0.999, top=0.999, left=0.001)
        self.draw()
    def get_drawchnarray(self,index):
        return self.ondrawchn[index]
    def get_drawaxes(self,index):
        return self.axes[index]
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
        for axes, tr in zip(self.axes, self.ondrawchn):
            axes.text(x, y, tr.tr.id, color="k", transform=axes.transAxes,
                    bbox=bbox, **kwargs)

    def drawPicks(self):
        for axes,chn in zip(self.axes,self.ondrawchn):
            for pick in chn.picks:
                if pick!=None:
                    realtime=pick.time-chn.starttime
                    x=realtime
                    string=pick.phase_hint+str(pick.time)
                    ymin, ymax = axes.get_ylim()
                    if pick.phase_hint == 'Pg':
                        y = 0.9 * ymax
                        color='#FF00FF'
                    if pick.phase_hint == 'Sg':
                        y = 0.8 * ymax
                        color='#EEB422'
                    if pick.phase_hint == 'Pn':
                        y = 0.7 * ymax
                        color='#00868B'
                    if pick.phase_hint == 'Sn':
                        y = 0.6 * ymax
                        color='#27408B'
                    kwargs = dict(va="top", ha="left", fontsize=9 * self.labeloffset, family='monospace',
                                  zorder=10000)
                    axes.axvline(x, 0.2, 0.95,color=color)
                    axes.text(x,y,string,color=color,**kwargs)
            """
            if chn.pickPg !=None:
                realtime=chn.pickP.time-chn.starttime
                x=realtime
                ax.axvline(x,0,1,color='Y')
                print realtime
            if chn.pickSg !=None:
                realtime=chn.pickS.time-chn.starttime
                x=realtime
                ax.axvline(x,0,1,color='R')
                print realtime
            """
    def updateaxes(self,axes):
        i=self.axes.index(axes)
        ymin, ymax = self.axes[i].get_ylim()
        xmin, xmax = self.axes[i].get_xlim()
        axes.cla()
        axes.plot(self.tt[i], self.ss[i],'g')
        '''REset limratio'''
        '''not used
        ymin = ymin * self.ylimratio
        ymax = ymax * self.ylimratio
        if (ymax - mean) > (mean - ymin):
            ymin = ymin - (ymax + ymin - 2 * mean)
        else:
            ymax = ymax + (2 * mean - ymax - ymin)
        '''
        self.axes[i].set_ylim(ymin, ymax)
        self.axes[i].set_xlim(xmin,xmax)
        '''draw picks'''
        chn=self.ondrawchn[i]
        for pick in chn.picks:
            if pick != None:
                realtime = pick.time - chn.starttime
                x=realtime
                ymin, ymax = axes.get_ylim()
                '''draw pick_text'''
                if pick.phase_hint == 'Pg':
                    y = 0.9 * ymax
                    color = '#FF00FF'
                if pick.phase_hint == 'Sg':
                    y = 0.8 * ymax
                    color = '#EEB422'
                if pick.phase_hint == 'Pn':
                    y = 0.7 * ymax
                    color = '#00868B'
                if pick.phase_hint == 'Sn':
                    y = 0.6 * ymax
                    color = '#27408B'
                kwargs = dict(va="top", ha="left", fontsize=9 * self.labeloffset, family='monospace',
                              zorder=10000)
                string = pick.phase_hint +" "+ str(pick.time)
                axes.axvline(x, 0.2, 0.95,color=color)
                axes.text(x, y, string, color=color,  **kwargs)
        '''draw Ids'''
        self.drawIds()
        self.fig.canvas.draw()
