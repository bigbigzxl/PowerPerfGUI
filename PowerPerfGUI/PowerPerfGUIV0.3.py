# coding=utf-8
from __future__ import unicode_literals
from aqua.qsshelper import QSSHelper

import sys,os
import numpy as np
import  Queue
import threading
from multiprocessing import Process

# 注：由于matplotlib嵌入pyqt4这个功能库本身存在某些BUG，因此请勿轻易调整包的import顺序。
from matplotlib.backends import qt_compat
import matplotlib.pyplot as plt


use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
import matplotlib.font_manager as fm
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4.QtCore import *
from PyQt4.QtGui import *
progname = os.path.basename(sys.argv[0])
progversion = "0.1"

from filter import Filter_thread
from dispatch import dispatch_thread
from server_control import Server_control
from server_communicate import ServerCommunicator
from pmu_raw_events import PMU_RAW_EVENTS
from conv_kernel_operators import *
##############################PowerPerfGUIv0.2##################################
# 1. add tab in window.
#     2018.11.29 add 33 items show.
#
# @2018.12.5 by zxl
# 2. 新增动态Perf、交互显示功能；
#     之前的V0.1版本只能被动地显示输出数据，也就是我编译一次运行一次只能出一次perf结果，不能做到编译一次无限次运行的效果；
#     同时，由于一次只能测6个事件，因此会出现无法全局观看事件的问题，因此修改后，在PC端跟手机端分别搭建一个server，PC端处理事件的
#      发送，移动端的解析事件然后通过JNI让底层的test pattern再一次以某些特定的参数运行，从而实现动态perf的功能；
#
# 3. 新增adb控制接口可实现对手机的几乎任意操作，获取权限、安装软件、打电话、听歌、关机...等。
#
# TODO:
#     1. 返回数据通过adb socket方式稳定高效返回，而非log方式低效抓取；
#     2. kernel自动调优平台；+
#        2.1 linux端自动编译；
#        2.2 windows端自动编译；
#        2.3 按照一定策略文本修改kernnel汇编代码；
#        2.4 APK安装运行并获取perf结果及显示；
#        2.4 集成测试；
#        2.4 调研机器学习算法并设计优化策略，最终实现kernel自动调优（有限空间内）；
#
##############################PowerPerfGUIv0.3####################################
#
#
#
#
#
#
#
#
#

def magic_thread_show(names, lines, boosts):
    fig_s = plt.figure(figsize=(8, 6), dpi=80)
    fig_s.set_facecolor('gray')

    axe_s = fig_s.add_subplot(111)
    # axe_s.patch.set_facecolor("k")
    # axe_s.patch.set_alpha(0.5)

    for i, name in enumerate(names):
        axe_s.plot(lines[i], '--o', linewidth=1.0, label=name + "(Boost=%.1f%%)" % boosts[i])

    # plt.tight_layout() #只有在全屏显示时效果才好，否则会有些区域看不到。
    myfont = fm.FontProperties(fname="C:/Windows/Fonts/simkai.ttf", size=14)
    plt.legend(loc="best", prop=myfont, shadow=True)

    plt.xlabel("counter", fontsize=16)
    plt.ylabel("value", fontsize=16)

    plt.title("".join(["Analysis Mode: ", "muti-Process"]),
              fontsize=18, fontweight='bold', fontstyle='italic',
              backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))
    plt.grid()
    plt.show()

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.fig.set_facecolor('gray')
        # fig.set_alpha(0.99)
        # plt.rcParams['axes.facecolor'] = 'gray'

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        # 解决中文乱码问题
        self.myfont = fm.FontProperties(fname="C:/Windows/Fonts/simkai.ttf", size=14)
        plt.legend(loc="best", prop=self.myfont, shadow=True)

        self.axes = self.fig.add_subplot(111)
        self.axes.patch.set_facecolor("k")
        self.axes.patch.set_alpha(0.75)

        self.axes.set_title("ARM(V7/V8) HARDWARE PMU RAW EVENT", fontsize=14, fontweight='bold', fontstyle='italic',
                  backgroundcolor="green", bbox=dict(facecolor='g', edgecolor='black', alpha=0.9))
        # self.axes.set_title("ARM(V7/V8) HARDWARE PMU RAW EVENT", fontsize=12)
        self.axes.set_xlabel("counts", fontsize=12)
        self.axes.set_ylabel("Raw Events", fontsize=12)

        # # 右轴专门显示CPU CYCLES的
        # self.axe_R = self.axes.twinx()
        # # self.axe_R.plot(month, ctr, '-or')
        # self.axe_R.set_ylabel('CPU_CYCLES', fontsize=12)
        # # DISPATCH_DICTS["CPU_CYCLES"]["Line"], = self.axe_R.plot([],  "r--o", linewidth=2.0, label= "CPU_CYCLES" )
        # self.line, = self.axe_R.plot([],  "r--o", linewidth=2.0, label= "CPU_CYCLES" )

        # unit test.
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(30)

    def compute_initial_figure(self):
        pass

    def background(self):
        self.axes.patch.set_facecolor("k")
        self.axes.patch.set_alpha(0.75)
        self.axes.set_title("ARM(V7/V8) HARDWARE PMU RAW EVENT", fontsize=14, fontweight='bold', fontstyle='italic',
                            backgroundcolor="green", bbox=dict(facecolor='g', edgecolor='black', alpha=0.9))
        # self.axes.set_title("ARM(V7/V8) HARDWARE PMU RAW EVENT", fontsize=12)
        self.axes.set_xlabel("counts", fontsize=12)
        self.axes.set_ylabel("Raw Events", fontsize=12)

        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(handles[::-1], labels[::-1])
        legend = self.axes.legend(loc='upper left', shadow=True)#, fontsize='x-large'

    def update_figure(self):
        global CURRENT_LINE
        global DISPATCH_DICTS
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        self.axes.cla()

        # print CURRENT_LINE, DISPATCH_DICTS

        for event_line in CURRENT_LINE:
            # 这个是为以后优化准备的，此处因为数据是不是新的都不重要，我每次都把axe给清了，你总得不断画吧！
            # 但是以后优化了只更新line就有用了，我只在有数据更新的时候才把line给重画一次
            if  DISPATCH_DICTS[event_line]["NEW_DATA"]:

                self.axes.plot(DISPATCH_DICTS[event_line]["Line_Y"], '--o', linewidth=1.0, label= event_line+"(Boost=%.1f%%)"%DISPATCH_DICTS[event_line]["Boost"])#+ "(Jitter:%.1f%%)"%jitter

        self.background()
        self.draw()

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # 1. checkable pushbutton--left
        self.pushbutton_checkable_C = QtGui.QPushButton('clear')  # synchronizing
        self.pushbutton_checkable_R = QtGui.QPushButton('Run')  # synchronizing
        # self.pushbutton_checkable_C.setCheckable(True)
        # self.pushbutton_checkable_R.setCheckable(True)
        # self.pushbutton_checkable_C.setChecked(True)
        # self.pushbutton_checkable_R.setChecked(True)
        self.pushbutton_checkable_C.clicked.connect(lambda: self.pushbutton_clear_recall(self.pushbutton_checkable_C))
        self.pushbutton_checkable_R.clicked.connect(lambda: self.pushbutton_Run_recall(self.pushbutton_checkable_R))


        # 2. checkable groupbox --left
        self.PMU_EVENT_NAME_LayoutInit()

        # 3. layer size
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        # font.setWeight(75)
        self.LayerSize_label = QtGui.QLabel('AddLayerSzie=H:W:Cin:Cout')
        self.LayerSize_label.setAlignment(Qt.AlignLeft)
        self.LayerSize_label.setFont(font)
        self.LayerSize_combobox_editable = QtGui.QComboBox()
        self.LayerSize_combobox_editable.setEditable(True)
        self.LayerSize_combobox_editable.addItems([
                                                   "16:16:64:1024",
                                                   "16:16:1024:64",
                                                   "16:16:256:256",
                                                   "64:64:16:256",
                                                   "64:64:256:16",
                                                   "64:64:64:64",
                                                   "128:128:16:64",
                                                   "128:128:64:16",
                                                   "128:128:32:32",
                                                   "256:256:16:16"
                                                   ])
        # print (self.LayerSize_combobox_editable.currentIndex())
        # print (self.LayerSize_combobox_editable.currentText())

        # 4. run times, 每次发送前来这读一次数据即可
        self.spinbox_label = QtGui.QLabel('Run times:')
        self.spinbox_label.setAlignment(Qt.AlignLeft)
        self.spinbox_label.setFont(font)
        self.spinbox = QtGui.QSpinBox()
        self.spinbox.setMaximum(127)
        self.spinbox.setMinimum(1)
        self.spinbox.setValue(1)

        # 5. layer operators
        self.conv1x1s1_LayoutInit()
        self.conv3x3s1_LayoutInit()
        self.conv3x3s2_LayoutInit()

        self.ConvType_label = QtGui.QLabel('Convlution Kernel type:')
        self.ConvType_label.setAlignment(Qt.AlignLeft)
        self.ConvType_label.setFont(font)
        self.toolbox = QtGui.QToolBox()
        self.toolbox.addItem(self.conv1x1s1_scroll, 'Convolution_1x1s1')
        self.toolbox.addItem(self.conv3x3s1_scroll, 'Convolution_3x3s1')
        self.toolbox.addItem(self.conv3x3s2_scroll, 'Convolution_3x3s2')

        self.pushbutton_checkable_magic = QtGui.QPushButton('Analysis Mode')  # synchronizing
        self.pushbutton_checkable_magic.clicked.connect(lambda: self.pushbutton_magic_recall())


        # self.toolbox.addItem(self.conv3x3s1_scroll, 'conv3x3s1')
        # self.toolbox.addItem(self.conv3x3s2_scroll, 'conv3x3s2')


        # canvas--right
        self.canvas_widget =  QtGui.QWidget(self)
        canvas = MyDynamicMplCanvas(self.canvas_widget, width=300, height=300, dpi=100)


        # vertical spacer on the left
        vspacer_left = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)

        # vertical spacer on the right
        vspacer_right = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)

        self.adbSocket_state_label = QtGui.QLabel('Adb Socket State:')

        # vertical layout on the left
        vlayout_left = QtGui.QVBoxLayout()
        vlayout_left.addWidget(self.pushbutton_checkable_R)
        vlayout_left.addWidget(self.pushbutton_checkable_C)
        vlayout_left.addWidget(self.pushbutton_checkable_magic)
        vlayout_left.addWidget(self.scrollarea)
        vlayout_left.addWidget(self.LayerSize_label)
        vlayout_left.addWidget(self.LayerSize_combobox_editable)
        vlayout_left.addWidget(self.spinbox_label)
        vlayout_left.addWidget(self.spinbox)
        vlayout_left.addWidget(self.ConvType_label)
        vlayout_left.addWidget(self.toolbox)

        vlayout_left.addSpacerItem(vspacer_left)
        vlayout_left.setMargin(10)

        # vertical layout on the right
        vlayout_right = QtGui.QVBoxLayout()
        vlayout_right.addWidget(canvas)
        vlayout_right.addWidget(self.adbSocket_state_label)

        # horizontal layout
        hlayout = QtGui.QHBoxLayout()
        hlayout.addLayout(vlayout_left)
        hlayout.addLayout(vlayout_right)

        # central widget
        central = QtGui.QWidget()
        central.setLayout(hlayout)
        self.setCentralWidget(central)

        # server control & communicator Initial part.
        self.communicateor = ServerCommunicator()
        self.controller    = Server_control()


    #在class的初始化那里继承父类加一个QtGui.QWidget： class Window(QtGui.QMainWindow, QtGui.QWidget)，然后直接重载keyPressEvent就好了
    #更新，发现不需要继承QtGui.QWidget，估计是QtGui.QMainWindow里面已经包括了；
    # 键盘监听函数，继承了父类，这里重写
    def keyPressEvent(self, event):
        key = event.key()

        #按下D
        if key == QtCore.Qt.black:
            self.pushbutton_Run_recall()

        #按ESC键，则退出程序
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def pushbutton_magic_recall(self):
        # 线程会把界面给卡死, 很正常啊，你两个主界面死循环肯定会出现一山不容二虎的局面。
        # temp_thread = threading.Thread(target=magic_thread_show)
        # temp_thread.start()
        names  = []
        lines  = []
        boosts = []
        for event_line in CURRENT_LINE:
            names.append(event_line)
            lines.append(DISPATCH_DICTS[event_line]["Line_Y"])
            boosts.append(DISPATCH_DICTS[event_line]["Boost"])

        if len(names) == len(lines) == len(boosts):
            p = Process(target=magic_thread_show, args=(names, lines, boosts))
            p.start()
        else:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "ERROR!!!",
                                 self.tr("当前界面你现实的数据，长度不匹配（name,Line_Y,Boost）"))
            # 驳回，此次申请无效；
            return


    def PMU_EVENT_NAME_LayoutInit(self):
        self.checkbox1  = QtGui.QCheckBox('CPU_CYCLES')
        self.checkbox2  = QtGui.QCheckBox('INST_RETIRED')

        self.checkbox3  = QtGui.QCheckBox('LD_RETIRED')
        self.checkbox4  = QtGui.QCheckBox('ST_RETIRED')

        self.checkbox5  = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox6  = QtGui.QCheckBox('L1D_CACHE_REFILL')
        self.checkbox7  = QtGui.QCheckBox('L1D_CACHE_WB')
        self.checkbox8  = QtGui.QCheckBox('L1D_CACHE_ALLOCATE')
        self.checkbox9  = QtGui.QCheckBox('L1D_TLB')
        self.checkbox10 = QtGui.QCheckBox('L1D_TLB_REFILL')

        self.checkbox11 = QtGui.QCheckBox('L2D_CACHE')
        self.checkbox12 = QtGui.QCheckBox('L2D_CACHE_REFILL')
        self.checkbox13 = QtGui.QCheckBox('L2D_CACHE_WB')
        self.checkbox14 = QtGui.QCheckBox('L2D_CACHE_ALLOCATE')
        self.checkbox15 = QtGui.QCheckBox('L2D_TLB')
        self.checkbox16 = QtGui.QCheckBox('L2D_TLB_REFILL')

        self.checkbox17 = QtGui.QCheckBox('L1I_CACHE')
        self.checkbox18 = QtGui.QCheckBox('L1I_TLB_REFILL')
        self.checkbox19 = QtGui.QCheckBox('L1I_CACHE_REFILL')
        self.checkbox20 = QtGui.QCheckBox('L1I_TLB')

        self.checkbox21 = QtGui.QCheckBox('BUS_CYCLES')
        self.checkbox22 = QtGui.QCheckBox('BUS_ACCESS')
        self.checkbox23 = QtGui.QCheckBox('MEM_ACCESS')
        self.checkbox24 = QtGui.QCheckBox('MEMORY_ERROR')
        self.checkbox25 = QtGui.QCheckBox('UNALIGNED_LDST_RETIRED')

        self.checkbox26 = QtGui.QCheckBox('BR_PRED')
        self.checkbox27 = QtGui.QCheckBox('BR_MIS_PRED')
        self.checkbox28 = QtGui.QCheckBox('BR_IMMED_RETIRED')
        self.checkbox29 = QtGui.QCheckBox('BR_RETURN_RETIRED')

        self.checkbox30 = QtGui.QCheckBox('INST_SPEC')
        self.checkbox31 = QtGui.QCheckBox('EXC_TAKEN')
        self.checkbox32 = QtGui.QCheckBox('EXC_RETURN')
        self.checkbox33 = QtGui.QCheckBox('CID_WRITE_RETIRED')
        self.checkbox34 = QtGui.QCheckBox('PC_WRITE_RETIRED')
        self.checkbox35 = QtGui.QCheckBox('TTBR_WRITE_RETIRED')
        self.checkbox36 = QtGui.QCheckBox('CHAIN')

        # self.check_boxs = [self.checkbox1 ,self.checkbox2 ,self.checkbox3 ,self.checkbox4 ,self.checkbox5 ,
        #                    self.checkbox6 ,self.checkbox7 ,self.checkbox8 ,self.checkbox9 ,self.checkbox10,
        #                    self.checkbox11,self.checkbox12,self.checkbox13,self.checkbox14,self.checkbox15,
        #                    self.checkbox16,self.checkbox17,self.checkbox18,self.checkbox19,self.checkbox20,
        #                    self.checkbox21,self.checkbox22,self.checkbox23,self.checkbox24,self.checkbox25,
        #                    self.checkbox26,self.checkbox27,self.checkbox28,self.checkbox29,self.checkbox30,
        #                    self.checkbox31,self.checkbox32,self.checkbox33]

        font      = "Times New Roman"
        font_size = 12
        # for box in self.check_boxs:
        #     box.setFont( QFont(font, font_size))
        #     box.toggled.connect(lambda: self.checkboxRecall(box))


        self.checkbox1.setFont( QFont(font, font_size))
        self.checkbox2.setFont( QFont(font, font_size))
        self.checkbox3.setFont( QFont(font, font_size))
        self.checkbox4.setFont( QFont(font, font_size))
        self.checkbox5.setFont( QFont(font, font_size))
        self.checkbox6.setFont( QFont(font, font_size))
        self.checkbox7.setFont( QFont(font, font_size))
        self.checkbox8.setFont( QFont(font, font_size))
        self.checkbox9.setFont( QFont(font, font_size))
        self.checkbox10.setFont( QFont(font, font_size))
        self.checkbox11.setFont( QFont(font, font_size))
        self.checkbox12.setFont( QFont(font, font_size))
        self.checkbox13.setFont( QFont(font, font_size))
        self.checkbox14.setFont( QFont(font, font_size))
        self.checkbox15.setFont( QFont(font, font_size))
        self.checkbox16.setFont( QFont(font, font_size))
        self.checkbox17.setFont( QFont(font, font_size))
        self.checkbox18.setFont( QFont(font, font_size))
        self.checkbox19.setFont( QFont(font, font_size))
        self.checkbox20.setFont( QFont(font, font_size))
        self.checkbox21.setFont( QFont(font, font_size))
        self.checkbox22.setFont( QFont(font, font_size))
        self.checkbox23.setFont( QFont(font, font_size))
        self.checkbox24.setFont( QFont(font, font_size))
        self.checkbox25.setFont( QFont(font, font_size))
        self.checkbox26.setFont( QFont(font, font_size))
        self.checkbox27.setFont( QFont(font, font_size))
        self.checkbox28.setFont( QFont(font, font_size))
        self.checkbox29.setFont( QFont(font, font_size))
        self.checkbox30.setFont( QFont(font, font_size))
        self.checkbox31.setFont( QFont(font, font_size))
        self.checkbox32.setFont( QFont(font, font_size))
        self.checkbox33.setFont( QFont(font, font_size))
        self.checkbox34.setFont( QFont(font, font_size))
        self.checkbox35.setFont( QFont(font, font_size))
        self.checkbox36.setFont( QFont(font, font_size))

        # bug来的，用循环 的方式会导致只有一个事件被绑定的异常
        self.checkbox1.toggled.connect(lambda: self.checkboxRecall(self.checkbox1))
        self.checkbox2.toggled.connect(lambda: self.checkboxRecall(self.checkbox2))
        self.checkbox3.toggled.connect(lambda: self.checkboxRecall(self.checkbox3))
        self.checkbox4.toggled.connect(lambda: self.checkboxRecall(self.checkbox4))
        self.checkbox5.toggled.connect(lambda: self.checkboxRecall(self.checkbox5))
        self.checkbox6.toggled.connect(lambda: self.checkboxRecall(self.checkbox6))
        self.checkbox7.toggled.connect(lambda: self.checkboxRecall(self.checkbox7))
        self.checkbox8.toggled.connect(lambda: self.checkboxRecall(self.checkbox8))
        self.checkbox9.toggled.connect(lambda: self.checkboxRecall(self.checkbox9))
        self.checkbox10.toggled.connect(lambda: self.checkboxRecall(self.checkbox10))
        self.checkbox11.toggled.connect(lambda: self.checkboxRecall(self.checkbox11))
        self.checkbox12.toggled.connect(lambda: self.checkboxRecall(self.checkbox12))
        self.checkbox13.toggled.connect(lambda: self.checkboxRecall(self.checkbox13))
        self.checkbox14.toggled.connect(lambda: self.checkboxRecall(self.checkbox14))
        self.checkbox15.toggled.connect(lambda: self.checkboxRecall(self.checkbox15))
        self.checkbox16.toggled.connect(lambda: self.checkboxRecall(self.checkbox16))
        self.checkbox17.toggled.connect(lambda: self.checkboxRecall(self.checkbox17))
        self.checkbox18.toggled.connect(lambda: self.checkboxRecall(self.checkbox18))
        self.checkbox19.toggled.connect(lambda: self.checkboxRecall(self.checkbox19))
        self.checkbox20.toggled.connect(lambda: self.checkboxRecall(self.checkbox20))
        self.checkbox21.toggled.connect(lambda: self.checkboxRecall(self.checkbox21))
        self.checkbox22.toggled.connect(lambda: self.checkboxRecall(self.checkbox22))
        self.checkbox23.toggled.connect(lambda: self.checkboxRecall(self.checkbox23))
        self.checkbox24.toggled.connect(lambda: self.checkboxRecall(self.checkbox24))
        self.checkbox25.toggled.connect(lambda: self.checkboxRecall(self.checkbox25))
        self.checkbox26.toggled.connect(lambda: self.checkboxRecall(self.checkbox26))
        self.checkbox27.toggled.connect(lambda: self.checkboxRecall(self.checkbox27))
        self.checkbox28.toggled.connect(lambda: self.checkboxRecall(self.checkbox28))
        self.checkbox29.toggled.connect(lambda: self.checkboxRecall(self.checkbox29))
        self.checkbox30.toggled.connect(lambda: self.checkboxRecall(self.checkbox30))
        self.checkbox31.toggled.connect(lambda: self.checkboxRecall(self.checkbox31))
        self.checkbox32.toggled.connect(lambda: self.checkboxRecall(self.checkbox32))
        self.checkbox33.toggled.connect(lambda: self.checkboxRecall(self.checkbox33))
        self.checkbox34.toggled.connect(lambda: self.checkboxRecall(self.checkbox34))
        self.checkbox35.toggled.connect(lambda: self.checkboxRecall(self.checkbox35))
        self.checkbox36.toggled.connect(lambda: self.checkboxRecall(self.checkbox36))


        groupbox_checkable_layout = QtGui.QVBoxLayout()
        # for box in self.check_boxs:
        #     groupbox_checkable_layout.addWidget(box)
        groupbox_checkable_layout.addWidget(self.checkbox1)
        groupbox_checkable_layout.addWidget(self.checkbox2)
        groupbox_checkable_layout.addWidget(self.checkbox3)
        groupbox_checkable_layout.addWidget(self.checkbox4)
        groupbox_checkable_layout.addWidget(self.checkbox5)
        groupbox_checkable_layout.addWidget(self.checkbox6)
        groupbox_checkable_layout.addWidget(self.checkbox7)
        groupbox_checkable_layout.addWidget(self.checkbox8)
        groupbox_checkable_layout.addWidget(self.checkbox9)
        groupbox_checkable_layout.addWidget(self.checkbox10)
        groupbox_checkable_layout.addWidget(self.checkbox11)
        groupbox_checkable_layout.addWidget(self.checkbox12)
        groupbox_checkable_layout.addWidget(self.checkbox13)
        groupbox_checkable_layout.addWidget(self.checkbox14)
        groupbox_checkable_layout.addWidget(self.checkbox15)
        groupbox_checkable_layout.addWidget(self.checkbox16)
        groupbox_checkable_layout.addWidget(self.checkbox17)
        groupbox_checkable_layout.addWidget(self.checkbox18)
        groupbox_checkable_layout.addWidget(self.checkbox19)
        groupbox_checkable_layout.addWidget(self.checkbox20)
        groupbox_checkable_layout.addWidget(self.checkbox21)
        groupbox_checkable_layout.addWidget(self.checkbox22)
        groupbox_checkable_layout.addWidget(self.checkbox23)
        groupbox_checkable_layout.addWidget(self.checkbox24)
        groupbox_checkable_layout.addWidget(self.checkbox25)
        groupbox_checkable_layout.addWidget(self.checkbox26)
        groupbox_checkable_layout.addWidget(self.checkbox27)
        groupbox_checkable_layout.addWidget(self.checkbox28)
        groupbox_checkable_layout.addWidget(self.checkbox29)
        groupbox_checkable_layout.addWidget(self.checkbox30)
        groupbox_checkable_layout.addWidget(self.checkbox31)
        groupbox_checkable_layout.addWidget(self.checkbox32)
        groupbox_checkable_layout.addWidget(self.checkbox33)
        groupbox_checkable_layout.addWidget(self.checkbox34)
        groupbox_checkable_layout.addWidget(self.checkbox35)
        groupbox_checkable_layout.addWidget(self.checkbox36)


        self.groupbox_checkable = QtGui.QGroupBox('PMU RAW EVENT')
        self.groupbox_checkable.setFont(QFont("Arial Black", 24))
        self.groupbox_checkable.setLayout(groupbox_checkable_layout)
        self.groupbox_checkable.setCheckable(False)

        self.scrollarea = QtGui.QScrollArea()
        self.scrollarea.setWidget(self.groupbox_checkable)

        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setFixedHeight(400)
        self.scrollarea.setFixedWidth(220)
        self.scrollarea.setAlignment(Qt.AlignCenter)

    def conv1x1s1_LayoutInit(self):
        self.conv1x1s1_mygroupbox = QtGui.QGroupBox('Convolution_1x1s1')
        self.conv1x1s1_myform = QtGui.QFormLayout()
        # self.conv1x1s1_labellist    = []
        self.conv1x1s1_checkboxlist   = []
        self.temp = 0

        for i, name in enumerate(Conv1x1s1Operators.operators_name):
            # self.conv1x1s1_labellist.append(QtGui.QLabel(str(i) + ":"))
            # must use slef.temp , not just temp;
            self.temp = QtGui.QCheckBox(name.replace("Convolution", ""))
            self.conv1x1s1_checkboxlist.append(self.temp)
            # self.conv1x1s1_myform.addRow(self.conv1x1s1_labellist[i], self.conv1x1s1_checkboxlist[i])
            self.conv1x1s1_myform.addRow(self.conv1x1s1_checkboxlist[i])

        # size = len(self.combolist)
        # for i in range(size):
        #     self.combolist[i].toggled.connect(lambda: self.checkboxRecall(self.combolist[i]))
        # you must do it like this not above;
        print ("conv1x1s1_checkboxlist size = ", len(self.conv1x1s1_checkboxlist))
        self.conv1x1s1_checkboxlist[0].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[0]))
        self.conv1x1s1_checkboxlist[1].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[1]))
        self.conv1x1s1_checkboxlist[2].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[2]))
        self.conv1x1s1_checkboxlist[3].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[3]))
        self.conv1x1s1_checkboxlist[4].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[4]))
        self.conv1x1s1_checkboxlist[5].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[5]))
        self.conv1x1s1_checkboxlist[6].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[6]))
        self.conv1x1s1_checkboxlist[7].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[7]))
        self.conv1x1s1_checkboxlist[8].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[8]))
        self.conv1x1s1_checkboxlist[9].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[9]))

        self.conv1x1s1_checkboxlist[10].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[10]))
        self.conv1x1s1_checkboxlist[11].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[11]))
        self.conv1x1s1_checkboxlist[12].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[12]))
        self.conv1x1s1_checkboxlist[13].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[13]))
        self.conv1x1s1_checkboxlist[14].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[14]))
        self.conv1x1s1_checkboxlist[15].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[15]))
        self.conv1x1s1_checkboxlist[16].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[16]))
        self.conv1x1s1_checkboxlist[17].toggled.connect(
            lambda: self.Conv1x1s1Operator_checkboxRecall(self.conv1x1s1_checkboxlist[17]))

        self.conv1x1s1_mygroupbox.setLayout(self.conv1x1s1_myform)
        self.conv1x1s1_mygroupbox.setFont(QFont("Times New Roman", 12))
        self.conv1x1s1_scroll = QtGui.QScrollArea()
        self.conv1x1s1_scroll.setWidget(self.conv1x1s1_mygroupbox)
        self.conv1x1s1_scroll.setWidgetResizable(True)
        # self.conv1x1s1_scroll.setFixedHeight(350) #固定高度后会出现“双下巴”
        self.conv1x1s1_scroll.setAlignment(Qt.AlignRight)

    def conv3x3s1_LayoutInit(self):
        self.conv3x3s1_mygroupbox = QtGui.QGroupBox('Convolution_3x3s1')
        self.conv3x3s1_myform = QtGui.QFormLayout()
        # self.conv3x3s1_labellist    = []
        self.conv3x3s1_checkboxlist = []
        self.temp = 0

        for i, name in enumerate(Conv3x3s1Operators.operators_name):
            # self.conv3x3s1_labellist.append(QtGui.QLabel(str(i) + ":"))
            # must use slef.temp , not just temp;
            self.temp = QtGui.QCheckBox(name.replace("Convolution", ""))
            self.conv3x3s1_checkboxlist.append(self.temp)
            # self.conv3x3s1_myform.addRow(self.conv3x3s1_labellist[i], self.conv3x3s1_checkboxlist[i])
            self.conv3x3s1_myform.addRow(self.conv3x3s1_checkboxlist[i])

        # size = len(self.combolist)
        # for i in range(size):
        #     self.combolist[i].toggled.connect(lambda: self.checkboxRecall(self.combolist[i]))
        # you must do it like this not above;
        print ("conv3x3s1_checkboxlist size = ", len(self.conv3x3s1_checkboxlist))
        self.conv3x3s1_checkboxlist[0].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[0]))
        self.conv3x3s1_checkboxlist[1].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[1]))
        self.conv3x3s1_checkboxlist[2].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[2]))
        self.conv3x3s1_checkboxlist[3].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[3]))
        self.conv3x3s1_checkboxlist[4].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[4]))
        self.conv3x3s1_checkboxlist[5].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[5]))
        self.conv3x3s1_checkboxlist[6].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[6]))
        self.conv3x3s1_checkboxlist[7].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[7]))
        self.conv3x3s1_checkboxlist[8].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[8]))
        self.conv3x3s1_checkboxlist[9].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[9]))

        self.conv3x3s1_checkboxlist[10].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[10]))
        self.conv3x3s1_checkboxlist[11].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[11]))
        self.conv3x3s1_checkboxlist[12].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[12]))
        self.conv3x3s1_checkboxlist[13].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[13]))
        self.conv3x3s1_checkboxlist[14].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[14]))
        self.conv3x3s1_checkboxlist[15].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[15]))
        self.conv3x3s1_checkboxlist[16].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[16]))
        self.conv3x3s1_checkboxlist[17].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[17]))
        self.conv3x3s1_checkboxlist[18].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[18]))
        self.conv3x3s1_checkboxlist[19].toggled.connect(
            lambda: self.Conv3x3s1Operator_checkboxRecall(self.conv3x3s1_checkboxlist[19]))

        self.conv3x3s1_mygroupbox.setLayout(self.conv3x3s1_myform)
        self.conv3x3s1_mygroupbox.setFont(QFont("Times New Roman", 12))
        self.conv3x3s1_scroll = QtGui.QScrollArea()
        self.conv3x3s1_scroll.setWidget(self.conv3x3s1_mygroupbox)
        self.conv3x3s1_scroll.setWidgetResizable(True)
        # self.conv3x3s1_scroll.setFixedHeight(350)
        self.conv3x3s1_scroll.setAlignment(Qt.AlignRight)

    def conv3x3s2_LayoutInit(self):
        self.conv3x3s2_mygroupbox = QtGui.QGroupBox('Convolution_3x3s1')
        self.conv3x3s2_myform = QtGui.QFormLayout()
        # self.conv3x3s2_labellist    = []
        self.conv3x3s2_checkboxlist = []
        self.temp = 0

        for i, name in enumerate(Conv3x3s2Operators.operators_name):
            # self.conv3x3s2_labellist.append(QtGui.QLabel(str(i) + ":"))
            # must use slef.temp , not just temp;
            self.temp = QtGui.QCheckBox(name.replace("Convolution", ""))
            self.conv3x3s2_checkboxlist.append(self.temp)
            # self.conv3x3s2_myform.addRow(self.conv3x3s2_labellist[i], self.conv3x3s2_checkboxlist[i])
            self.conv3x3s2_myform.addRow(self.conv3x3s2_checkboxlist[i])

        # size = len(self.combolist)
        # for i in range(size):
        #     self.combolist[i].toggled.connect(lambda: self.checkboxRecall(self.combolist[i]))
        # you must do it like this not above;
        print ("conv3x3s2_checkboxlist size = ", len(self.conv3x3s2_checkboxlist))
        self.conv3x3s2_checkboxlist[0].toggled.connect(
            lambda: self.Conv3x3s2Operator_checkboxRecall(self.conv3x3s2_checkboxlist[0]))
        self.conv3x3s2_checkboxlist[1].toggled.connect(
            lambda: self.Conv3x3s2Operator_checkboxRecall(self.conv3x3s2_checkboxlist[1]))


        self.conv3x3s2_mygroupbox.setLayout(self.conv3x3s2_myform)
        self.conv3x3s2_mygroupbox.setFont(QFont("Times New Roman", 12))
        self.conv3x3s2_scroll = QtGui.QScrollArea()
        self.conv3x3s2_scroll.setWidget(self.conv3x3s2_mygroupbox)
        self.conv3x3s2_scroll.setWidgetResizable(True)
        # self.conv3x3s2_scroll.setFixedHeight(350)
        self.conv3x3s2_scroll.setAlignment(Qt.AlignRight)

    def Conv1x1s1Operator_checkboxRecall(self, cbx):
        # 进来就获取type值，获取错误的话我的配置文件可能异常了
        ops_name = "Convolution" + str(cbx.text())
        ops_type = -1
        for i,keyword in enumerate(ConvOperators.OperatorTypeKeyWord):
            if keyword in ops_name:
                ops_type = i
        if ops_type == -1:
            print("ERROR!!!! operators type not support yet! type = %d"%ops_type)
            cbx.setChecked(False)
            return

        if cbx.isChecked():
            # 非第一次进来时的冲突检查，跟当前的CURRENT_KERNEL["typeNo"]进行比较，不一致则提示并退出，同时取消checkbox的选中
            if CURRENT_KERNEL["typeNo"] > -1 and ops_type != CURRENT_KERNEL["typeNo"]:
                cbx.setChecked(False)
                # 当前kernel数组不空，同时我选择的kernel type不同，则报警。
                QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
                QMessageBox.critical(self, "ERROR!!!",
                                     self.tr("目前只支持同一种类型的Operator啊~"))
                return

            if CURRENT_KERNEL["typeNo"] < -1 and CURRENT_KERNEL["typeNo"] > 1000:
                cbx.setChecked(False)
                QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
                QMessageBox.critical(self, "ERROR!!!",
                                     self.tr("CURRENT_KERNEL[\"typeNo\"]=%d, 这个里面的参数产生了未知异常！"%CURRENT_KERNEL["typeNo"]))
                return

            if CURRENT_KERNEL["typeNo"] == -1:#表示是第一个kernel，直接赋值就完事了。其他情况都是正常情况。
                CURRENT_KERNEL["typeNo"] = ops_type

            # 找到对应的ops后，就将值映射值存储进set集合中，同时进行了去重操作
            flag = 0
            for i,operator_name in enumerate(Conv1x1s1Operators.operators_name):
                if ops_name == operator_name:
                    CURRENT_KERNEL["operators"].add(i)
                    flag += 1
            print(CURRENT_KERNEL["operators"], flag)
            #加入这里出现某种异常，导致加不进去呢？
            if flag != 1:
                cbx.setChecked(False)
                QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
                QMessageBox.critical(self, "ERROR!!!",
                                     self.tr("%s kernel在conv_kernel_operator.Conv1x1s1Operators中重复了"%ops_name))
                return

        else:
            # 删除操作，因为添加操作的时候就会判断是否kernnel冲突了，因此这里就不需要继续监测了；
            flag = 0
            for i,operator_name in enumerate(Conv1x1s1Operators.operators_name):
                if ops_name == operator_name:
                    current_kernel_id = i
                    flag += 1

            if flag != 1:
                cbx.setChecked(False)
                QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
                QMessageBox.critical(self, "ERROR!!!",
                                     self.tr("%s kernel在conv_kernel_operator.Conv1x1s1Operators中找不到"%ops_name))
                return
            else:
                if current_kernel_id in CURRENT_KERNEL["operators"]:
                    # 这里用discard而不用remove是因为，假如不存在而你去remove时会报错，而discard则不会。
                    CURRENT_KERNEL["operators"].discard(current_kernel_id)

            print("CURRENT_KERNEL: ", CURRENT_KERNEL["operators"])

    def Conv3x3s1Operator_checkboxRecall(self, cbx):
        event_name = str(cbx.text())
        if cbx.isChecked():
            print(event_name)
        else:
            pass

    def Conv3x3s2Operator_checkboxRecall(self, cbx):
        event_name = str(cbx.text())
        if cbx.isChecked():
            print(event_name)
        else:
            pass

    def checkboxRecall(self, cbx):

        event_name = str(cbx.text())
        if cbx.isChecked():
            if not DISPATCH_DICTS.get(event_name):# 没打开过的, 则创建这么一个位置；
                DISPATCH_DICTS[event_name] = {"Line_Y": [], "NEW_DATA": False, "Line": None}
            # 已经打开过的，有存在的因此直接添加标志位就好了；
            CURRENT_LINE.add(event_name)
        else:
            # 取消显示的话，我们清空数组，并把之从CURRENT_LINE当前显示line中去掉；
            CURRENT_LINE.remove(event_name)

    def pushbutton_Run_recall(self, pbc_r):
        if not self.controller.get_perf_author():
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "ERROR!!!",
                                 self.tr("无法打开手机perf权限（root了吗？adb打开了吗？）"))
            # 驳回，此次申请无效；
            return
        # 1. CURRENT LINE是否超过6个（不包括CPU cycles）
        cmd_length = len(CURRENT_LINE)
        if "CPU_CYCLES" in CURRENT_LINE:
            illegal = (cmd_length > 7)
        else:
            illegal = (cmd_length > 6)

        if illegal:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "ERROR!!!",
                                 self.tr("不要勾选超过6(%d)个呀！(CPU CYCLES是VIP，没办法！)"%cmd_length))
            return

        # 2. 假如操作合理的话，就该发送指令了，个人感觉这里该改写为线程，因为socket通信假如阻塞了呢？
        #     这样，主界面可就是会出现卡顿的呀！对追求如丝般顺滑流畅的我来说，还是难以忍受的吧！
        #     2.1 需要重定向端口
        if not self.communicateor.redirect_port():
            # 重连5次
            for i in range(5):
                if self.communicateor.redirect_port():
                     break

            # 最后的确认
            if not self.communicateor.is_redirected():
                pe = QPalette()
                pe.setColor(QPalette.WindowText, Qt.darkRed)
                self.adbSocket_state_label.setText("Adb Socket State: can't redirect port.")
                self.adbSocket_state_label.setFont(QFont("Roman times", 10, QFont.Bold))
                self.adbSocket_state_label.setPalette(pe)
                return
            else:
                pe = QPalette()
                pe.setColor(QPalette.WindowText, Qt.darkYellow)
                self.adbSocket_state_label.setText("Adb Socket State: redirect port successed.")
                self.adbSocket_state_label.setFont(QFont("Roman times", 10, QFont.Bold))
                self.adbSocket_state_label.setPalette(pe)

        """
        cmd: 指令，格式如下：
        update 2018.12.19: 新增size以及kernel的动态支持；
        暂时只支持单size多kernel的模式；
        [
         total_length, times, cmd[2], cmd[3], cmd[4], cmd[5], cmd[6], cmd[7]，
         # 为了支持大size，用两个字节表示，第一个字节为高字节，由于数据是char型，因此采用100进制，size值=100*H + L
         sizeH[H], sizeH[L], sizeW[H], sizeW[L], sizeCin[H], sizeCin[L], sizeCout[H], sizeCout[L],
         # 类型搭配事件的序列号从而匹配c++层对应的序号：这需要小心设计，因为length只有127，因此尽量把kernel选择个数小于50个，当然了，我们也没这么多~
         KernelType0，KernelNum0,KernelType1，KernelNum1,KernelType2，KernelNum2.....   
         ]
        list中每个元素都是char型(<128)的，因为这样子以满足目前的简单需求.
        """

        cmd = []
        for event in CURRENT_LINE:
            #  "CPU_CYCLES" 是默认就包含的，按照协议规定，我无需把之写进指令中
            if event ==  "CPU_CYCLES":
                continue
            cmd.append(PMU_RAW_EVENTS.EventName.index(event))

        # 事件勾选的少于6个，按照通信协议字段的划分，我们得补齐6个；
        # 补齐策略：random，即在未被选中的事件中任意选择。
        if len(cmd) < 6:
            for e in PMU_RAW_EVENTS.EventName:
                if e == "CPU_CYCLES":
                    continue
                elif PMU_RAW_EVENTS.EventName.index(e) in cmd:
                    continue
                else:
                    cmd.append(PMU_RAW_EVENTS.EventName.index(e))
                    if len(cmd) == 6:
                        print("RAW_EVENT_NUM: ", cmd)
                        break

        # 把event排列一下，显示起来是自然顺序，否则就是你乱点的顺序。
        cmd = sorted(cmd)

        # 检查事件字符的合法性
        try:
            for data in cmd:
                temp = chr(data)
        except Exception as e:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "cmd value out of -127~127!!!",
                                 self.tr(e))

        #等价最后的第二号位置插入循环次数，同时检查循环次数的合法性
        try:
            temp = chr(self.spinbox.value())
            cmd.insert(0, int(self.spinbox.value()))
        except Exception as e:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "run times 异常 = %d"%self.spinbox.value(),
                                 self.tr(e))


        #获取size值,并写入指令
        size_str = str(self.LayerSize_combobox_editable.currentText())
        # print size_str.strip().split(":")
        try:
            # 切割数据看是否异常，做初步处理
            sizes = size_str.strip().split(":")
            H    = int(sizes[0])
            W    = int(sizes[1])
            Cin  = int(sizes[2])
            Cout = int(sizes[3])

            # 第一步检查size溢出；
            if H > 8192 or W > 8192 or Cin > 8192 or Cout > 8192:
                QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
                QMessageBox.critical(self, "ERROR!!!",
                                     self.tr("输入的layer size有误！\n {H:W:Cin:Cout}={%d, %d, %d, %d}"%(H, W, Cin, Cout)))
                return

            # 按协议分解数据
            if H > 100:
                H_H = H / 100
                H_L = H % 100
            else:
                H_H = 0
                H_L = H

            if W > 100:
                W_H = W / 100
                W_L = W % 100
            else:
                W_H = 0
                W_L = W

            if Cin > 100:
                Cin_H = Cin / 100
                Cin_L = Cin % 100
            else:
                Cin_H = 0
                Cin_L = Cin

            if Cout > 100:
                Cout_H = Cout / 100
                Cout_L = Cout % 100
            else:
                Cout_H = 0
                Cout_L = Cout

            # size 处理完后, 接着检查数据的合法性,然后将int数据合并到指令中（发送的时候再转成chr）。
            temp = chr(H_H)
            temp = chr(H_L)
            temp = chr(W_H)
            temp = chr(W_L)
            temp = chr(Cin_H)
            temp = chr(Cin_L)
            temp = chr(Cout_H)
            temp = chr(Cout_L)

            cmd.append(H_H)
            cmd.append(H_L)
            cmd.append(W_H)
            cmd.append(W_L)
            cmd.append(Cin_H)
            cmd.append(Cin_L)
            cmd.append(Cout_H)
            cmd.append(Cout_L)

        except Exception as e:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "ERROR!!!" + str(e),
                                 self.tr("输入的layer size有误！"))
            return


        # 开始插入kernel数组
        if len(CURRENT_KERNEL["operators"]) == 0:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "ERROR!!!",
                                 self.tr("至少选择一个operator，老铁！"))
            return

        # 将kernnel set转成list后重排一下，那么结果显示就是按照UI上的自然顺序进行排列显示的。
        OperatorType = CURRENT_KERNEL["typeNo"]

        KernelOperators = list(CURRENT_KERNEL["operators"])
        KernelOperators = sorted(KernelOperators)
        for kernelNum in KernelOperators:
            cmd.append(OperatorType)
            cmd.append(kernelNum)


        # 最开始0位置插入完整的数组长度
        cmd.insert(0, len(cmd) + 1)

        print("total_length, times,"
              +"cmd[2],cmd[3], cmd[4], cmd[5], cmd[6], cmd[7],"
              +" sizeH[H], sizeH[L], sizeW[H], sizeW[L], sizeCin[H], sizeCin[L], sizeCout[H], sizeCout[L],"
              +"KernelType0，KernelNum0,KernelType1，KernelNum1,KernelType2，KernelNum2.....   ")
        print(cmd)



        # 一路通关，开始发射指令！
        if self.communicateor.SendCmd2JavaServer(cmd):
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkYellow)
            self.adbSocket_state_label.setText("Adb Socket State: send command successed.")
            self.adbSocket_state_label.setFont(QFont("Roman times", 14, QFont.Bold))
            self.adbSocket_state_label.setPalette(pe)
        else:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.darkRed)
            self.adbSocket_state_label.setText("Adb Socket State: send command failed.")
            self.adbSocket_state_label.setFont(QFont("Roman times", 10, QFont.Bold))
            self.adbSocket_state_label.setPalette(pe)

    def pushbutton_clear_recall(self, pbc_c):
        # # pbc_c = push button checkable clear
        # if pbc_c.isChecked():
        #     pbc_c.setText("clear")
        #     # （我们清空后Filter仍然可能把延迟到达的数据扔进来，因此在打开的时候记得也要清理一下哈）
        #     # 当前check box只要选中或取消我们都要清空显示数据槽的。
        #     # 显示前清空list也就是清空line
        #     # for event_name in CURRENT_LINE:
        #     #     DISPATCH_DICTS[event_name]["Line_Y"] = []
        #     for kv in DISPATCH_DICTS.items():
        #         kv[1]["Line_Y"] = []
        #     # print pbc_x.text()#synchronizing
        # else:
        #     pbc_c.setText("clearing...")

        # 清空CURRENT LINE就完事了。
        for kv in DISPATCH_DICTS.items():
            kv[1]["Line_Y"] = []

def main():
    # creates the application and takes arguments from the command line
    application = QtGui.QApplication(sys.argv)

    # creates the window and sets its properties
    window = Window()
    window.setWindowTitle('POWER PERF')  # title
    # 只能用ico格式
    # window.setWindowIcon或者application.setWindowIcon都行；
    # 如果任务栏不显示图标：https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    ico_path = os.path.join(os.getcwd(),'ICO\icon25.ico')
    window.setWindowIcon(QtGui.QIcon(ico_path))
    window.resize(1250, 800)  # size

    # loads and sets the Qt stylesheet
    qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
    window.setStyleSheet(qss)

    window.show()  # shows the window

    # runs the application and waits for its return value at the end
    sys.exit(application.exec_())

if __name__ == '__main__':
    if (sys.version_info > (3, 0)):
        # python3
        q_data = Queue()
    else:
        # python2
        q_data = Queue.Queue()

    global DISPATCH_DICTS
    DISPATCH_DICTS = {
        # cpu cycles是默认有的, 碰到BUG了先不这么做，怎么先实现功能先怎么来。
        # "CPU_CYCLES": {"Line_Y":[], "NEW_DATA": False, "Line": None}
    }

    global CURRENT_LINE
    CURRENT_LINE   = set()

    global CURRENT_KERNEL
    CURRENT_KERNEL = {
        "typeNo": -1, "operators": set()
    } #每次只能测一个类型的kernel

    # Step1: 设置adb位置，会自动去ANDROID_HOME下找"platform-tools", "adb.exe"。
    # filter.py, server_control.py, server_communicate.py都在用，大家都说好！
    SDK_dir = "E:\SDK"
    os.environ['ANDROID_HOME'] = SDK_dir


    PowerPerfFilter = Filter_thread(threadID=0, name="Filter_thread unit_test", q_data=q_data)
    PowerPerfFilter.start()


    PowerPerfDispatcher = dispatch_thread(threadID=1, name="dispatch_thread unit_test", q_data=q_data,
                                          dispatched_dict=DISPATCH_DICTS)
    PowerPerfDispatcher.start()

    main()