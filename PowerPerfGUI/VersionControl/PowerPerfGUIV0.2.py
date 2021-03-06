# coding=utf-8
from __future__ import unicode_literals
from pyqt4_proj.GITHUB.PowerPerfGUI.aqua.qsshelper import QSSHelper

import sys,os
import numpy as np
import  Queue

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



from pyqt4_proj.GITHUB.PowerPerfGUI.filter import Filter_thread
from pyqt4_proj.GITHUB.PowerPerfGUI.dispatch import dispatch_thread
from pyqt4_proj.GITHUB.PowerPerfGUI.server_control import Server_control
from pyqt4_proj.GITHUB.PowerPerfGUI.server_communicate import ServerCommunicator
from pyqt4_proj.GITHUB.PowerPerfGUI.pmu_raw_events import PMU_RAW_EVENTS



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
#     2. kernel自动调优平台；
#        2.1 linux端自动编译；
#        2.2 windows端自动编译；
#        2.3 按照一定策略文本修改kernnel汇编代码；
#        2.4 APK安装运行并获取perf结果及显示；
#        2.4 集成测试；
#        2.4 调研机器学习算法并设计优化策略，最终实现kernel自动调优（有限空间内）；
#

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
            if  DISPATCH_DICTS[event_line]["NEW_DATA"]:
                self.axes.plot(DISPATCH_DICTS[event_line]["Line_Y"], '--o', linewidth=1.0, label= event_line)

        self.background()
        self.draw()

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # checkable groupbox --left
        self.checkbox1  = QtGui.QCheckBox('CPU_CYCLES')
        self.checkbox2  = QtGui.QCheckBox('INST_RETIRED')

        self.checkbox3  = QtGui.QCheckBox('LD_RETIRED')
        self.checkbox4  = QtGui.QCheckBox('ST_RETIRED')

        self.checkbox5  = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox6  = QtGui.QCheckBox('L1D_CACHE_REFILL')
        self.checkbox7  = QtGui.QCheckBox('L1D_TLB_REFILL')
        self.checkbox8  = QtGui.QCheckBox('L1D_CACHE_WB')
        self.checkbox9  = QtGui.QCheckBox('L1D_CACHE_ALLOCATE')

        self.checkbox10  = QtGui.QCheckBox('L2D_CACHE')
        self.checkbox11  = QtGui.QCheckBox('L2D_CACHE_REFILL')
        self.checkbox12 = QtGui.QCheckBox('L2D_CACHE_WB')
        self.checkbox13 = QtGui.QCheckBox('L2D_CACHE_ALLOCATE')

        self.checkbox14 = QtGui.QCheckBox('L1I_CACHE')
        self.checkbox15 = QtGui.QCheckBox('L1I_TLB_REFILL')
        self.checkbox16 = QtGui.QCheckBox('L1I_CACHE_REFILL')

        self.checkbox17 = QtGui.QCheckBox('BUS_CYCLES')
        self.checkbox18 = QtGui.QCheckBox('BUS_ACCESS')
        self.checkbox19 = QtGui.QCheckBox('MEM_ACCESS')
        self.checkbox20 = QtGui.QCheckBox('MEMORY_ERROR')
        self.checkbox21 = QtGui.QCheckBox('UNALIGNED_LDST_RETIRED')

        self.checkbox22 = QtGui.QCheckBox('BR_PRED')
        self.checkbox23 = QtGui.QCheckBox('BR_MIS_PRED')
        self.checkbox24 = QtGui.QCheckBox('BR_IMMED_RETIRED')
        self.checkbox25 = QtGui.QCheckBox('BR_RETURN_RETIRED')

        self.checkbox26 = QtGui.QCheckBox('INST_RETIRED')
        self.checkbox27 = QtGui.QCheckBox('INST_SPEC')

        self.checkbox28 = QtGui.QCheckBox('EXC_TAKEN')
        self.checkbox29 = QtGui.QCheckBox('EXC_RETURN')
        self.checkbox30 = QtGui.QCheckBox('CID_WRITE_RETIRED')
        self.checkbox31 = QtGui.QCheckBox('PC_WRITE_RETIRED')
        self.checkbox32 = QtGui.QCheckBox('TTBR_WRITE_RETIRED')
        self.checkbox33 = QtGui.QCheckBox('CHAIN')

        # self.check_boxs = [self.checkbox1 ,self.checkbox2 ,self.checkbox3 ,self.checkbox4 ,self.checkbox5 ,
        #                    self.checkbox6 ,self.checkbox7 ,self.checkbox8 ,self.checkbox9 ,self.checkbox10,
        #                    self.checkbox11,self.checkbox12,self.checkbox13,self.checkbox14,self.checkbox15,
        #                    self.checkbox16,self.checkbox17,self.checkbox18,self.checkbox19,self.checkbox20,
        #                    self.checkbox21,self.checkbox22,self.checkbox23,self.checkbox24,self.checkbox25,
        #                    self.checkbox26,self.checkbox27,self.checkbox28,self.checkbox29,self.checkbox30,
        #                    self.checkbox31,self.checkbox32,self.checkbox33]

        font      = "Times New Roman"
        font_size = 16
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
        self.checkbox32.toggled.connect(lambda: self.checkboxRecall(self.checkbox33))


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


        self.groupbox_checkable = QtGui.QGroupBox('PMU RAW EVENT')
        self.groupbox_checkable.setFont(QFont("Arial Black", 24))
        self.groupbox_checkable.setLayout(groupbox_checkable_layout)
        self.groupbox_checkable.setCheckable(False)

        # checkable pushbutton
        self.pushbutton_checkable_C = QtGui.QPushButton('clear')#synchronizing
        self.pushbutton_checkable_R = QtGui.QPushButton('Run')  # synchronizing
        # self.pushbutton_checkable_C.setCheckable(True)
        # self.pushbutton_checkable_R.setCheckable(True)
        # self.pushbutton_checkable_C.setChecked(True)
        # self.pushbutton_checkable_R.setChecked(True)
        self.pushbutton_checkable_C.clicked.connect(lambda: self.pushbutton_clear_recall(self.pushbutton_checkable_C))
        self.pushbutton_checkable_R.clicked.connect(lambda: self.pushbutton_Run_recall(self.pushbutton_checkable_R))


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
        vlayout_left.addWidget(self.groupbox_checkable)
        vlayout_left.addWidget(self.pushbutton_checkable_C)
        vlayout_left.addWidget(self.pushbutton_checkable_R)
        vlayout_left.addSpacerItem(vspacer_left)
        vlayout_left.setMargin(10)

        # vertical layout on the right
        vlayout_right = QtGui.QVBoxLayout()
        vlayout_right.addWidget(canvas)
        vlayout_right.addWidget( self.adbSocket_state_label)

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
        [total_length, times, cmd[2], cmd[3], cmd[4], cmd[5], cmd[6], cmd[7]]
        list中每个元素都是char型(<128)的，因为这样子以满足目前的简单需求.
        """
        # 循环次数暂时默认取1
        times = 1
        cmd = []
        for event in CURRENT_LINE:
            #  "CPU_CYCLES" 是默认就包含的，按照协议规定，我无需把之写进指令中
            if event ==  "CPU_CYCLES":
                continue
            cmd.append(PMU_RAW_EVENTS.EventName.index(event))


        if len(cmd) < 6:
            # 事件勾选的少于6个，按照通信协议字段的划分，我们得补齐6个；
            # 补齐策略：random，即在未被选中的事件中任意选择。
            for e in PMU_RAW_EVENTS.EventName:
                if e == "CPU_CYCLES":
                    continue
                elif e in cmd:
                    continue
                else:
                    cmd.append(PMU_RAW_EVENTS.EventName.index(e))
                    if len(cmd) == 6:
                        break

        #等价最后的第二号位置插入循环次数
        cmd.insert(0, times)

        # 最开始0位置插入完整的数组长度
        cmd.insert(0, len(cmd) + 1)

        # 检查数组的合法性
        try:
            for data in cmd:
                temp = chr(data)
        except Exception as e:
            QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
            QMessageBox.critical(self, "cmd value out of -127~127!!!",
                                 self.tr(e))

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
    window.setWindowTitle('PowerPerf_V0.1')  # title
    window.resize(800, 100)  # size

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
    CURRENT_LINE = set()

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