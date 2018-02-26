# -*- coding: utf-8 -*-
import rcspy_Exportdialog
import rcspy_Preprocessdialog
import rcspy_Autopickdialog
import rcspy_Taupdialog
import obspy.core
from PyQt5.QtWidgets import QMessageBox,QProgressBar,QAbstractItemView,QFileDialog
from PyQt5.QtCore import QDir
from PyQt5 import  QtWidgets
from util import QListWidgetItem
from data_manager import *
class Exportdialog(rcspy_Exportdialog.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent):
        super(Exportdialog, self).__init__(parent)
        self.setupUi(self)
        self.File_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.channel_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()
        self.expath = ""
        self.radioMSEED.setChecked(True)
        self.radioSEED.setEnabled(False)
    def getFiles(self, Files):
        self.Files = Files
        for file in self.Files.files:
            listitem = QListWidgetItem(file)
            listitem.setText(file.name)
            self.File_list.addItem(listitem)
        print self.Files.files[0].stations[0].channels[0].tr.stats
    def connectevent(self):
        self.btnOK.clicked.connect(self.Onbtnok)
        self.btn_Cancel.clicked.connect(self.Onbtncancel)
        self.File_list.itemSelectionChanged.connect(self.OnFilelist_selectionchange)
        self.channel_list.itemSelectionChanged.connect(self.Onchannellist_selectionchange)
        self.allchannel_checkbox.stateChanged.connect(self.Onallchannel_change)
        self.btn_set_folder.clicked.connect(self.set_exfolder)

    def set_exfolder(self):
        foldername = QFileDialog.getExistingDirectory(self, 'save folder')
        if foldername != "":
            self.expath = foldername
            self.Exfolder_edit.setText(foldername)

    def Onallchannel_change(self):
        if self.allchannel_checkbox.isChecked() == True:
            self.channel_list.selectAll()
        else:
            self.channel_list.clearSelection()
            self.single_channel_checkbox.setEnabled(True)

    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems()) == 1:
            self.channel_list.setEnabled(True)
            self.allchannel_checkbox.setEnabled(True)
            file = self.File_list.selectedItems()[0].parent
            for station in file.stations:
                listitem = QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
        if len(self.File_list.selectedItems()) > 1:
            for item in self.File_list.selectedItems():
                file = item.parent
                for station in file.stations:
                    listitem = QListWidgetItem(station)
                    listitem.setText(station.name)
                    self.channel_list.addItem(listitem)
            self.channel_list.setEnabled(False)
            self.allchannel_checkbox.setChecked(True)
            self.allchannel_checkbox.setEnabled(False)
            self.radioMSEED.setChecked(True)

    def Onchannellist_selectionchange(self):
        count = self.channel_list.count()
        if len(self.channel_list.selectedItems()) == count:
            self.allchannel_checkbox.setChecked(True)
        else:
            self.allchannel_checkbox.setChecked(False)

    def Onbtncancel(self):
        self.close()

    def Onbtnok(self):
        if self.expath == "":
            QMessageBox.about(self, "tips", "please set export folder")

        elif len(self.File_list.selectedItems()) == 0:
            QMessageBox.about(self, "tips", "please set export files")
        else:
            self.dir = QDir()
            self.dir.cd(self.expath)
            self.pgb = QProgressBar(self)
            self.pgb.setWindowTitle("Exporting")
            self.pgb.setGeometry(140, 380, 260, 25)
            self.pgb.show()
            if self.radioMSEED.isChecked():
                self.Export2mseed()
            if self.radioASCII.isChecked():
                self.Export2Ascii()
            if self.radioSAC.isChecked():
                self.Export2sac()
            self.pgb.close()
            QMessageBox.about(self, "tips", "finished")

    def Export2mseed(self):
        self.allnum = len(self.File_list.selectedItems())
        self.currnum = 0
        if self.allnum == 1:
            self.allnum = len(self.channel_list.selectedItems()) * 3
            exstream = obspy.core.Stream()
            append = exstream.append
            for item in self.channel_list.selectedItems():
                for channel in item.parent.channels:
                    append(channel.tr)
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
                    self.currnum = self.currnum + 1
            file = self.File_list.selectedItems()[0].parent
            filesave = self.expath + "/" + str(file.ename) + ".mseed"
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked() == True:
                self.currnum = 0
                if self.dir.exists(file.ename) == False:
                    self.dir.mkdir(file.ename)
                filesave = self.expath + "/" + file.ename + "/"
                for tr in exstream:
                    tr.write(filesave + str(tr.id) + ".mseed", format='MSEED')
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
                    self.currnum = self.currnum + 1
            else:
                exstream.write(filesave, format='MSEED')
        else:
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked() == True:
                for item in self.File_list.selectedItems():
                    self.allnum = self.allnum + len(item.parent.stations.stations) * 3
                for item in self.File_list.selectedItems():
                    file = item.parent
                    if self.dir.exists(file.ename) == False:
                        self.dir.mkdir(file.ename)
                    filesave = self.expath + "/" + str(file.ename) + "/"
                    for tr in file.stream:
                        tr.write(filesave + str(tr.id) + ".mseed", format='MSEED')
                        self.currnum = self.currnum + 1
                        step = self.currnum * 100 / self.allnum
                        self.pgb.setValue(int(step))
            else:
                for item in self.File_list.selectedItems():
                    file = item.parent
                    filesave = self.expath + "/" + str(file.ename) + ".mseed"
                    file.stream.write(filesave, format='MSEED')
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))

    def Export2Ascii(self):
        self.allnum = len(self.File_list.selectedItems())
        self.currnum = 0
        if self.allnum == 1:
            self.allnum = len(self.channel_list.selectedItems()) * 3
            exstream = obspy.core.Stream()
            append = exstream.append
            for item in self.channel_list.selectedItems():
                for channel in item.parent.channels:
                    append(channel.tr)
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
            file = self.File_list.selectedItems()[0].parent
            filesave = self.expath + "/" + str(file.ename) + ".ascii"
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked() == True:
                if self.dir.exists(file.ename) == False:
                    self.dir.mkdir(file.ename)
                filesave = self.expath + "/" + file.ename + "/"
                for tr in exstream:
                    tr.write(filesave + str(tr.id) + ".ascii", format='SLIST')
            else:
                exstream.write(filesave, format='SLIST')
        else:
            '''
            single channel
            '''
            if self.single_channel_checkbox.isChecked() == True:
                for item in self.File_list.selectedItems():
                    self.allnum = self.allnum + len(item.parent.stations) * 3
                for item in self.File_list.selectedItems():
                    file = item.parent
                    if self.dir.exists(file.ename) == False:
                        self.dir.mkdir(file.ename)
                    filesave = self.expath + "/" + str(file.ename) + "/"
                    for tr in file.stream:
                        tr.write(filesave + str(tr.id) + ".ascii", format='SLIST')
                        self.currnum = self.currnum + 1
                        step = self.currnum * 100 / self.allnum
                        self.pgb.setValue(int(step))
            else:
                for item in self.File_list.selectedItems():
                    file = item.parent
                    filesave = self.expath + "/" + str(file.ename) + ".ascii"
                    file.stream.write(filesave, format='SLIST')
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))

    def Export2sac(self):
        self.allnum = len(self.File_list.selectedItems())
        self.currnum = 0
        if self.allnum == 1:
            self.allnum = len(self.channel_list.selectedItems()) * 3
            exstream = obspy.core.Stream()
            append = exstream.append
            for item in self.channel_list.selectedItems():
                for channel in item.parent.channels:
                    append(channel.tr)
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
            file = self.File_list.selectedItems()[0].parent
            if self.dir.exists(file.ename) == False:
                self.dir.mkdir(file.ename)
            for tr in exstream:
                filesave = self.expath + "/" + file.ename + "/" + str(tr.id) + ".SAC"
                tr.write(filesave, format='SAC')
        else:
            self.allnum = 0
            for item in self.File_list.selectedItems():
                self.allnum = self.allnum + len(item.parent.stations) * 3
            for item in self.File_list.selectedItems():
                if self.dir.exists(item.parent.ename) == False:
                    self.dir.mkdir(item.parent.ename)
                filedir = self.expath + "/" + item.parent.ename + "/"
                for tr in item.parent.stream:
                    filesave = filedir + tr.id + ".SAC"
                    tr.write(filesave, format='SAC')
                    self.currnum = self.currnum + 1
                    step = self.currnum * 100 / self.allnum
                    self.pgb.setValue(int(step))
class Preprocessdialog(rcspy_Preprocessdialog.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent):
        super(Preprocessdialog, self).__init__(parent)
        self.setupUi(self)
        self.Rcs = parent
        self.initList()
        self.Inv_test()
        self.File_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.channel_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()

    def Inv_test(self):
        current = 0
        for file in self.Files.files:
            if file.format != 'SEED':
                current = current + 1
            else:
                if file.Inv==None:
                    current=current-1
        if current != 0:
            QMessageBox.about(self, "warning", str(current) + "File(s) not set Inventory")

    def initList(self):
        self.Files = self.Rcs.Files
        for file in self.Files.files:
            listitem = QListWidgetItem(file)
            listitem.setText(file.name)
            self.File_list.addItem(listitem)

    def connectevent(self):
        self.File_list.itemSelectionChanged.connect(self.OnFilelist_selectionchange)
        self.channel_list.itemSelectionChanged.connect(self.Onchannellist_selectionchange)
        self.allchannel_checkbox.stateChanged.connect(self.Onallchannel_change)
        self.fminSlider.valueChanged.connect(self.OnfminSlider_valueChanged)
        self.fmaxSlider.valueChanged.connect(self.OnfmaxSlider_valueChanged)
        self.fminspin.valueChanged.connect(self.Onfminspin_valueChange)
        self.fmaxspin.valueChanged.connect(self.Onfmaxspin_valueChange)
        self.btnOK.clicked.connect(self.Onbtnok)
        self.btn_Cancel.clicked.connect(self.Onbtnback)

    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems()) == 1:
            self.channel_list.setEnabled(True)
            self.allchannel_checkbox.setEnabled(True)
            file = self.File_list.selectedItems()[0].parent
            for station in file.stations:
                listitem = QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
        if len(self.File_list.selectedItems()) > 1:
            for item in self.File_list.selectedItems():
                file = item.parent
                for station in file.stations:
                    listitem = QListWidgetItem(station)
                    listitem.setText(station.name)
                    self.channel_list.addItem(listitem)
            self.channel_list.setEnabled(False)
            self.allchannel_checkbox.setChecked(True)
            self.allchannel_checkbox.setEnabled(False)

    def Onchannellist_selectionchange(self):
        count = self.channel_list.count()
        if len(self.channel_list.selectedItems()) == count:
            self.allchannel_checkbox.setChecked(True)
        else:
            self.allchannel_checkbox.setChecked(False)

    def Onallchannel_change(self):
        if self.allchannel_checkbox.isChecked() == True:
            self.channel_list.selectAll()
        else:
            self.channel_list.clearSelection()

    def OnfminSlider_valueChanged(self):
        self.fminspin.setValue(float(self.fminSlider.value()) / 10.0)
        if self.fminSlider.value() > self.fmaxSlider.value():
            self.fmaxSlider.setValue(self.fminSlider.value())

    def OnfmaxSlider_valueChanged(self):
        self.fmaxspin.setValue(float(self.fmaxSlider.value()) / 10.0)
        if self.fminSlider.value() > self.fmaxSlider.value():
            self.fminSlider.setValue(self.fmaxSlider.value())

    def Onfminspin_valueChange(self):
        self.fminSlider.setValue(self.fminspin.value() * 10)

    def Onfmaxspin_valueChange(self):
        self.fmaxSlider.setValue(self.fmaxspin.value() * 10)

    def Onbtnok(self):
        self.errorcontrol = True
        if len(self.File_list.selectedItems()) == 0:
            QMessageBox.about(self, "tips", "please set export files")
        else:
            self.pgb = QProgressBar(self)
            self.pgb.setWindowTitle("Working")
            self.pgb.setGeometry(10, 5, 540, 20)
            self.pgb.show()
            if self.detrend_switch.isChecked():
                self.current_process.setText("detrend")
                self.detrend()
            if self.remove_response_switch.isChecked():
                self.current_process.setText("rm_response")
                self.remove_response()
            if self.bandpass_switch.isChecked():
                self.current_process.setText("bp_filter")
                self.bandpass_Filter()
            if self.lowpass_switch.isChecked():
                self.current_process.setText("lp_filter")
                self.lowpass_Filter()
            self.pgb.close()
            self.current_process.setText(" ")
            if self.errorcontrol == True:
                QMessageBox.about(self, "tips", "finished")
                self.Rcs.update_ondraw_stations()
                self.Rcs.draw()

    def Onbtnback(self):
        self.close()
        pass

    def detrend(self):
        currnum = 0
        if len(self.File_list.selectedItems()) == 1:
            for item in self.channel_list.selectedItems():
                allnum = len(self.channel_list.selectedItems())
                station = item.parent
                if self.radioConstant.isChecked():
                    station.detrend(type='constant')
                if self.radioLinear.isChecked():
                    station.detrend(type='linear')
                self.pgb.setValue(float(currnum * 100) / float(allnum))
                currnum = currnum + 1
            pass
        else:
            for item in self.File_list.selectedItems():
                allnum = len(self.File_list.selectedItems())
                file = item.parent
                if self.radioConstant.isChecked():
                    file.detrend(type='constant')
                if self.radioLinear.isChecked():
                    file.detrend(type='linear')
                self.pgb.setValue(float(currnum * 100) / float(allnum))
                currnum = currnum + 1

    def bandpass_Filter(self):
        currnum = 0
        try:
            if len(self.File_list.selectedItems()) == 1:
                for item in self.channel_list.selectedItems():
                    allnum = len(self.channel_list.selectedItems())
                    station = item.parent
                    station.Filter('bandpass',
                                     freqmin=float(self.fminspin.text()[0:-2]),
                                     freqmax=float(self.fmaxspin.text()[0:-2]), )
                    self.pgb.setValue(float(currnum * 100) / float(allnum))
                    currnum = currnum + 1
                pass
            else:
                '''calculate allnum'''
                for item in self.File_list.selectedItems():
                    allnum = len(item.parent.stations)
                for item in self.File_list.selectedItems():
                    file = item.parent
                    for station in file.stations:
                        station.Filter('bandpass',
                                         freqmin=float(self.fminspin.text()[0:-2]),
                                         freqmax=float(self.fmaxspin.text()[0:-2]), )
                        self.pgb.setValue(float(currnum * 100) / float(allnum))
                        currnum = currnum + 1
        except Exception, e:
            self.errorcontrol = False
            QMessageBox.about(self, "Error", str(e))
        pass

    def remove_response(self):
        currnum = 0
        try:
            error_str = "mismatch station:\n"
            allnum = len(self.File_list.selectedItems())
            for item in self.File_list.selectedItems():
                file = item.parent
                file.setInv()
                self.pgb.setValue(float(currnum * 100) / float(allnum))
                currnum = currnum + 1
            currnum = 0
            error = True
            if self.pre_filt_switch.isChecked():
                pre_filt = [self.f1_spin.value(),
                            self.f2_spin.value(),
                            self.f3_spin.value(),
                            self.f4_spin.value()]
            else:
                pre_filt = None
            if len(self.File_list.selectedItems()) == 1:
                for item in self.channel_list.selectedItems():
                    allnum = len(self.channel_list.selectedItems())
                    station = item.parent
                    try:
                        station.remove_response(inventory=station.parent.Inv,
                                                water_level=float(self.water_level_spin.text()),
                                                pre_filt=pre_filt)

                    except:
                        error = False
                        error_str = error_str + str(station.name) + "\n"
                    self.pgb.setValue(float(currnum * 100) / float(allnum))
                    currnum = currnum + 1

            else:
                '''calculate allnum'''
                for item in self.File_list.selectedItems():
                    allnum = len(item.parent.stations)
                for item in self.File_list.selectedItems():
                    file = item.parent
                    for station in file.stations:
                        try:
                            station.remove_response(inventory=station.parent.Inv,
                                                    water_level=float(self.water_level_spin.text()),
                                                    pre_filt=pre_filt)

                        except:
                            error = False
                            error_str = error_str + str(station.name) + "\n"
                        self.pgb.setValue(float(currnum * 100) / float(allnum))
                        currnum = currnum + 1
            if error == False:
                QMessageBox.about(self, "error", error_str)
        except Exception, e:
            self.errorcontrol = False
            QMessageBox.about(self, "Error", str(e))

    def lowpass_Filter(self):
        currnum = 0
        try:
            if len(self.File_list.selectedItems()) == 1:
                for item in self.channel_list.selectedItems():
                    allnum = len(self.channel_list.selectedItems())
                    station = item.parent
                    station.Filter('lowpass',
                                   freq=float(self.frqspin.text()[0:-2]),
                                   corners=int(self.lowpass_corners_spin.text()))
                    self.pgb.setValue(float(currnum * 100) / float(allnum))
                    currnum = currnum + 1
                pass
            else:
                '''calculate allnum'''
                for item in self.File_list.selectedItems():
                    allnum = len(item.parent.stations)
                for item in self.File_list.selectedItems():
                    file = item.parent
                    for station in file.stations:
                        station.Filter('lowpass',
                                       freq=float(self.frqspin.text()[0:-2]),
                                       corners=int(self.lowpass_corners_spin.text()))
                        self.pgb.setValue(float(currnum * 100) / float(allnum))
                        currnum = currnum + 1
        except Exception, e:
            self.errorcontrol = False
            QMessageBox.about(self, "Error", str(e))
        pass
class Autopickdialog(rcspy_Autopickdialog.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent):
        super(Autopickdialog, self).__init__(parent)
        self.setupUi(self)
        self.Rcs = parent
        self.initList()
        self.channel_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()

    def initList(self):
        self.Files = self.Rcs.Files
        for file in self.Files.files:
            listitem = QListWidgetItem(file)
            listitem.setText(file.name)
            self.File_list.addItem(listitem)

    def connectevent(self):
        self.File_list.itemSelectionChanged.connect(self.OnFilelist_selectionchange)
        self.channel_list.itemSelectionChanged.connect(self.Onchannellist_selectionchange)
        self.allchannel_checkbox.stateChanged.connect(self.Onallchannel_change)
        self.btnOK.clicked.connect(self.Onbtnok)
        self.btn_Cancel.clicked.connect(self.Onbtnback)
        pass

    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems()) == 1:
            self.channel_list.setEnabled(True)
            self.allchannel_checkbox.setEnabled(True)
            file = self.File_list.selectedItems()[0].parent
            for station in file.stations:
                listitem = QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
        if len(self.File_list.selectedItems()) > 1:
            for item in self.File_list.selectedItems():
                file = item.parent
                for station in file.stations:
                    listitem = QListWidgetItem(station)
                    listitem.setText(station.name)
                    self.channel_list.addItem(listitem)
            self.channel_list.setEnabled(False)
            self.allchannel_checkbox.setChecked(True)
            self.allchannel_checkbox.setEnabled(False)

    def Onchannellist_selectionchange(self):
        count = self.channel_list.count()
        if len(self.channel_list.selectedItems()) == count:
            self.allchannel_checkbox.setChecked(True)
        else:
            self.allchannel_checkbox.setChecked(False)

    def Onallchannel_change(self):
        if self.allchannel_checkbox.isChecked() == True:
            self.channel_list.selectAll()
        else:
            self.channel_list.clearSelection()

    def Onbtnok(self):
        if len(self.channel_list.selectedItems()) == 0:
            pass
        else:
            allnum = 0
            self.pgb = QProgressBar(self)
            self.pgb.setWindowTitle("Working")
            self.pgb.setGeometry(10, 5, 550, 28)
            self.pgb.show()
            for item in self.channel_list.selectedItems():
                station = item.parent
                if isinstance(station, Station):
                    allnum = allnum + 1
            currnum = 0
            for item in self.channel_list.selectedItems():
                station = item.parent
                if isinstance(station, Station):
                    f1 = self.low_frq.value()
                    f2 = self.upp_frq.value()
                    lta_p = self.lta_p.value()
                    sta_p = self.sta_p.value()
                    lta_s = self.lta_s.value()
                    sta_s = self.sta_s.value()
                    m_p = int(self.m_p.value())
                    m_s = int(self.m_s.value())
                    l_p = self.l_p.value()
                    l_s = self.l_s.value()
                    station.Ar_pick(f1, f2, lta_p, sta_p, lta_s, sta_s, m_p, m_s, l_p, l_s)
                    self.pgb.setValue(int(float(currnum) * 100 / allnum))
                    currnum = currnum + 1
                    # except Exception,e:
                    #    print e
            self.pgb.close()
            QMessageBox.about(self, "tip", "finished!")
            self.Rcs.draw()
        pass

    def Onbtnback(self):
        self.close()
        pass

class Traveltimedialog(rcspy_Taupdialog.Ui_Dialog,QtWidgets.QDialog):
    def __init__(self, parent):
        super(Traveltimedialog, self).__init__(parent)
        self.setupUi(self)
        self.Rcs = parent
        self.initList()
        #self.File_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connectevent()
    def setInv(self):
        for file in self.Files.files:
            file.setInv()
    def initList(self):
        self.Files = self.Rcs.Files
        for file in self.Files.files:
            listitem = QListWidgetItem(file)
            listitem.setText(file.name)
            self.File_list.addItem(listitem)
    def connectevent(self):
        self.File_list.itemSelectionChanged.connect(self.OnFilelist_selectionchange)
        self.channel_list.itemSelectionChanged.connect(self.Onchannellist_selectionchange)
        self.btnOK.clicked.connect(self.Onbtnok)
        self.btn_Cancel.clicked.connect(self.Onbtnback)
        self.btn_Inv.clicked.connect(self.OnbtnattachInv)
        self.btn_Event.clicked.connect(self.OnbtnattachEvent)
        pass
    def OnFilelist_selectionchange(self):
        self.channel_list.clear()
        if len(self.File_list.selectedItems()) == 1:
            file = self.File_list.selectedItems()[0].parent
            for station in file.stations:
                listitem = QListWidgetItem(station)
                listitem.setText(station.name)
                self.channel_list.addItem(listitem)
            if file.Invpath!=None:
                self.invdisplayer.setText(str(file.Invpath))
    def Onchannellist_selectionchange(self):
        station=self.channel_list.selectedItems()[0].parent
        if station.depth!=-1:
            self.stadepth.setText(str(station.depth))
        if station.longitude!=-1:
            self.stalongti.setText(str(station.longitude))
        if station.latitude!=-1:
            self.stalati.setText(str(station.latitude))
        pass
    def Onbtnok(self):
        if len(self.File_list.selectedItems())==1:
            source=self.get_source()
            if source!=None:
                list=[]
                if self.Pgchenkbox.isChecked():
                    list.append('P')
                if self.Sgchenkbox.isChecked():
                    list.append('S')
                if self.Pnchenkbox.isChecked():
                    list.append('Pn')
                if self.Snchenkbox.isChecked():
                    list.append('Sn')
                file=self.File_list.selectedItems()[0].parent
                self.pgb = QProgressBar(self)
                self.pgb.setWindowTitle("Working")
                self.pgb.setGeometry(10, 465, 520, 30)
                self.pgb.show()
                allnum=len(file.stations)
                currnum=0
                for station in file.stations:
                    self.pgb.setValue(float(currnum*100)/float(allnum))
                    station.get_travel_time(list)
                    currnum=currnum+1
                self.pgb.close()
                self.Rcs.draw()
                QMessageBox.about(self,'tips','finished')
            else:
                QMessageBox.about(self, 'tips', 'No source information')

    def Onbtnback(self):
        self.close()
        pass
    def OnbtnattachInv(self):
        if len(self.File_list.selectedItems())>0:
            filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './', '*.*')
            self.File_list.selectedItems()[0].parent.setInvbypath(filename)
            self.invdisplayer.setText(filename)
        pass
    def OnbtnattachEvent(self):
        pass
    def get_source(self):
        return None
        pass