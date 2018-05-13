README
===========================
该文件将告诉您如何配置运行本程序，告诉您如何基于本程序进行二次开发，此外，它还提供必要的类的成员变量和API的简介。

****
|Author|Veasonwang|
|---|---
|E-mail|wangwsong@foxmail.com

****
## 目录
* [开发环境](#开发环境)
* [使用QtDesigner](#使用QtDesigner)
* [源码文件结构](#源码文件结构)
* [主要类成员变量与API](#主要类成员变量与API)
* [二次开发示例](#二次开发示例)

****
### 开发环境
|系统|Windows/linux/mac均可，建议Ubuntu14.04/16.04LTS|
|---|---
|anaconda版本|4.4及以上，建议5.0.1。64位
|Python版本|2.7.x
|obspy|1.1.0
|IDE|JetBrains Pycharm 2018.03
|PyQt|5.6.0
|Matplotlib|2.0.2
-----------
#### 开发环境配置
1. 登录清华镜像站`https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/ `针对机器平台选择合适的镜像下载并安装。
2. 配置完成Anaconda环境后，执行`pip install obspy`安装obspy框架。
3. 安装pycharm ：登录`http://www.jetbrains.com/pycharm/download/ `选择合适的版本下载安装
4. 拉取源代码，登录`https://github.com/Veasonwang/Rcspy`下载源代码或者输入命令拉取源代码（需要安装git）
`git clone https://github.com/Veasonwang/Rcspy.git`
5. 打开pycharm，打开源代码文件夹。
6. 运行Rcspy.py
****
### 使用QtDesigner
1.	安装Qt，Windows平台登录 https://www.qt.io/ 下载Qt。Linux下运行`sudo apt-get install qtcreator` 命令完成安装。
2.	打开QtDesigner，创建一个新的窗口，另存为.ui文件。执行命令：`pyuic5 –o xxx.py xxx.ui` 可生成py源码文件
3.	将.py文件移动到main/ui_package中，在Sub_windows_support.py中添加`from ui_package import xxxx `即可完成该窗口类的导入
4.	定义该窗口对应的class，编写构造函数，需要继承创建的窗口类。
```python
class Exportdialog(rcspy_Exportdialog.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent):
        super(Exportdialog, self).__init__(parent)
        self.setupUi(self)
```
5.	调用。需要创建该窗口时，直接创建该类的实例即可
```python
self.exdialog = Exportdialog(self)
self.exdialog.exec_()
```
****
### 源码文件结构
1. 根目录。根目录下是GPL2.0开源协议、readme、以及版本信息。
2. main目录。该目录是程序主目录，源码位置在此，该目录下有四个源码文件。作用如下：
      * `Rcspy.py` 程序的入口，里面包含程序主窗口类——Rcspy类，负责程序启动、主窗口逻辑调用、变量初始化，是功能的入口。
      * `datamanager.py` 数据管理框架。包含Files、File、Station、Channel类。以及Source类、ChennelVisible类、Phasetime类等其他类。
      * `util.py` 主要是绘图模块（MplCanvas类），以及其他继承自Qt的控件类。
      * `Sub_windows_support.py` 所有的子窗口类在此文件中。
3. `main/icons` 存放各类图标
4. `main/ui` 存放qtdesigner的.ui文件
5. `main/ui_package` ui界面包，通过 `pyuic5 –o xxx.py xxx.ui` 命令生成的源码文件

****
### 主要类成员变量与API
#### Rcspy类
##### 成员变量
* `self.qml`：程序唯一MplCanvas类的变量，与QWidget控件绑定
* `self.qmlcanvas`：Rcspy的QWidget控件
* `self.fig`：qml变量唯一的figure，唯一画布。
* `self.zoomswi`：缩放开关
* `self.Files`：一般Files类实例
* `self.ondrawstations`：待绘制的台站
* `self.sac_files`：为了兼容绘图类的以三通道为单位的绘图接口，转为sac文件设置的files类，要求sac文件的输入数量必须是3的倍数，否则出错。
* `self.qmldrawswi`：左右拖动开关。

##### 成员函数
* `Eventconnect()`：连接在QtDesigner中未完成连接的事件
* `initdrawstation()`：当打开文件时，确保一开始有一个台站是可见的
* `draw()`：完成画布的更新。
* `update_ondraw_stations()`：同步待绘制台站。当更改台站是否可见属性后，需要执行此函数同步待绘制台站。
* `onqwidghtsizechangeed(QRectevent)`：保证qml的大小与qmlcanvas的大小一致
* `pick(event,phase)`：event是MplCanvas变量的鼠标事件，phase是一个字符。用于拾取震相。调用对应通道的getpick()方法完成震相的拾取，记录鼠标所在位置的时间和选择的震相完成。
* `_initStationTree()`：初始化列表树控件
* `poptreemenu()`：列表树菜单的弹出实现
* `Input_Source_info(items)`：为制定文件输入震源信息
* `Export_calculation_phase_file(items)`：输出指定文件的理论到时信息
* `Export_Pick_phase_file(items)`：输出指定文件拾取的震相
* `attach_event_file(items)`：为指定文件关联事件文件
* `export_xml(items)`：导出指定文件所包含的事件
* `Onstationtreeselectedchange()`：当列表树控件选定的项目改变时，改变状态栏的状态。
* `Set_selected_Invisible(selectedList)`：使选中的台站不可见
* `Set_selected_Visible(selectedList)`：使选中的台站不可见
* `_initVistblebtn()`：初始化可见的通道。
* `_changeStationVisibility()`：对选中的台站可见状态取反
* `connectevent()`: 连接matplotlib 事件
* `popqmlmenu()`: 画布右键菜单的实现
* `getchnbyaxes(ax)`：通过当前鼠标所在的axes，获取对应的channel的引用
* `getaxesbychn(chn)`：获取channel所对应的axes
------------------------------
#### MplCanvas类
* `self.axes[]：axes`：数组，按顺序保存每一个axes的引用
* `self.fig：MplCanvas`：唯一Figure变量，画布
* `self.signalheight`：单个通道的高度，单位像素。用以计算fig的总大小，以改变fig大小适应由单屏幕显示道数改变时带来的问题。
* `self.ondrawchn[]`：保存每一个axes对应的channel的引用。
* `self.labeloffset`：保存标签的放大倍数，实现标签同步放大缩小功能
* `self.Rcs`：MplCanvas类用以保存对Rcspy类的引用
* `drawAxes(stations,VisibleChn)`：给定需要绘制的stations列表和需要显示的N、E、Z的通道，将曲线绘制出来。该方法会把所有内容清除，再重新绘制。
* `drawIds()`：绘制每一个Axes的id标签
* `drawPicks()`：绘制所有拾取的震相
* `drawTraveltimes()`：绘制所有计算的理论到时
* `updateaxes（axes）`：仅重绘axes的曲线
* `updatePicks(axes)`：仅重绘axes拾取的震相
* `updateIds(axes)`：仅重绘axes的id标签
* `updateTravel_time(axes)`：仅绘制axes的走时
-------------------------------
#### Files类
* `self.files[]`：储存File类
* `addfile(file)`：添加将实例化的File添加进files[]中
* `setstationsinvisible(selecteditems)`：是的选中的文件的所有stations不可见。
* `exportxml（items）`：将选中的的文件导出。
-------------------------------
#### File类
* `self.path`：文件绝对路径
* `self.format`：记录文件类型
* `self.Inv`：文件Inventory类实例（仅seed文件支持）
* `self.stations[]`：一个文件所拥有的stations
* `update_event()`：更新当前文件的Event类，一个文件有一个Event实例，描述该文件对应的地震事件
* `attach_event(filename)`：为该文件关联对应的事件文件
* `setstationTree()`：列表树的初始化
* `setInv()`：调用read_inventory(path)方法获取inventory实例
* `detrend(type)`：去倾，type选择是常数型还是线性型
* `removestationTree（TreeItem）`：把指定的台站从列表树中移除
* `updatestats()`：更新每个台站的状态
-----------------------------------
#### Stations类
* `self.traveltime`：指地震波从产生到被台站接受时经过的时间
* `self.arriveltime`：指地震波到达时间
* `getchannelbyNZE（direction）`：通过方向获取该台站对应channel的实例
* `gettrbyNZE（direction）`：通过方向获取channel中的trace实例
* `get_travel_time(phase_list,source)`:获取走时信息
-------------------------------------
#### Channel类
* `self.datamean`：当前通道数据的平均值
* `self.tr_VEL`：速度曲线
* `self.tr_DISP`：位移曲线
* `self.tr_ACC`：加速度曲线
* `self.currentwaveform`：当前显示的曲线类型
* `setwaveform(type)`：修改当前显示的曲线类型。调用该接口后需要调用draw()函数重绘整个画布。
--------------------------------------
### 二次开发示例
接下来我将通过一个简单的例子讲解如何在本程序基础上进行二次开发。
#### 添加显示短时傅里叶变换功能
1. 通过obspy文档查询了解obspy的短时傅里叶变换接口`Trace.spectrogram(**kwargs)`，通过进一步查询的到接口参数的意义
Parameters:	
    `data` Input data
    `samp_rate (float)` Samplerate in Hz
    `per_lap (float) `Percentage of overlap of sliding window, ranging from 0 to 1. High overlaps take a long time to compute.
    `wlen (int or float) `Window length for fft in seconds. If this parameter is too small, the calculation will take forever. If None, it defaults to (samp_rate/100.0).
    `log (bool) `Logarithmic frequency axis if True, linear frequency axis otherwise.
    `outfile (str) `String for the filename of output file, if None interactive plotting is activated.
   ` fmt (str)` Format of image to save
    a`xes (matplotlib.axes.Axes) `Plot into given axes, this deactivates the fmt and outfile option.
    `dbscale (bool)` If True 10 * log10 of color values is taken, if False the sqrt is taken.
   ` mult (float)` Pad zeros to length mult * wlen. This will make the spectrogram smoother.
    `cmap (matplotlib.colors.Colormap)` Specify a custom colormap instance. If not specified, then the default ObsPy sequential colormap is used.
    `zorder (float) `Specify the zorder of the plot. Only of importance if other plots in the same axes are executed.
    `title (str) ` Set the plot title
    `show (bool)`  Do not call plt.show() at end of routine. That way, further modifications can be done to the figure before showing it.
   ` sphinx (bool)`  Internal flag used for API doc generation, default False
   ` clip ([float, float]) ` adjust colormap to clip at lower and/or upper end. The given percentages of the amplitude range (linear or logarithmic depending on option dbscale) are clipped.
2. 根据接口的参数表，结合我自己的需要。在datamanager.py 中的channel类建立新接口。
```python
    def spectrogram(self):
        self.tr.spectrogram(log=True,title=self.channel+str(self.starttime))
```
3. 在合适的时机调用它。比如我需要在画布上右键时，弹出菜单，选中该项后弹出一个窗口，显示对应的短时傅里叶变换图谱。则我需要在Rcspy类中修改popqmlmenu()函数：
```python
    def popqmlmenu(self,event):
        Menu=QMenu()
        Pg=Menu.addAction('PICK Pg')
        Sg = Menu.addAction('PICK Sg')
        Pn = Menu.addAction('PICK Pn')
        Sn = Menu.addAction('PICK Sn')
        ```diff
        +spectrogram=Menu.addAction("show spectrogram")
        ```
        Pg.triggered.connect(lambda:self.pick(event,'Pg'))
        Sg.triggered.connect(lambda:self.pick(event,'Sg'))
        Pn.triggered.connect(lambda:self.pick(event,'Pn'))
        Sn.triggered.connect(lambda:self.pick(event,'Sn'))
        ```diff
        +spectrogram.triggered.connect(lambda:self._Onspectrogram(event))
        ```
        Menu.exec_(QtGui.QCursor.pos())
```
4. 新增函数`self._Onspectrogram(event)`去响应菜单事件
```python
    def _Onspectrogram(self,event):
        chn=self.getchnbyaxes(event.inaxes)#获取channel实例
        chn.spectrogram()
```
5. 运行程序，大功告成。
