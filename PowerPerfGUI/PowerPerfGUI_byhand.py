
# coding=utf-8
from __future__ import unicode_literals
from aqua.qsshelper import QSSHelper
import sys
import os
import numpy as np
import random
from matplotlib.backends import qt_compat
import matplotlib.pyplot as plt
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
import matplotlib.font_manager as fm
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4.QtCore import *
from PyQt4.QtGui import *
progname = os.path.basename(sys.argv[0])
progversion = "0.1"

import  Queue


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
                  backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))
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
                            backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))
        # self.axes.set_title("ARM(V7/V8) HARDWARE PMU RAW EVENT", fontsize=12)
        self.axes.set_xlabel("counts", fontsize=12)
        self.axes.set_ylabel("Raw Events", fontsize=12)

        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(handles[::-1], labels[::-1])
        # plt.legend(loc="best",  shadow=True) #prop=self.myfont,

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        self.axes.cla()

        self.background()

        for event_line in CURRENT_LINE:
            if  DISPATCH_DICTS[event_line]["NEW_DATA"]:
                self.axes.plot(DISPATCH_DICTS[event_line]["Line_Y"], '--o', linewidth=1.0, label= "haha")

        self.draw()

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # checkable groupbox --left
        self.checkbox1  = QtGui.QCheckBox('CPU_CYCLES')
        self.checkbox2  = QtGui.QCheckBox('INST_RETIRED')

        self.checkbox3  = QtGui.QCheckBox('BR_PRED')
        self.checkbox4  = QtGui.QCheckBox('BR_MIS_PRED')

        self.checkbox5  = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox6  = QtGui.QCheckBox('L1D_CACHE_REFILL')
        self.checkbox7  = QtGui.QCheckBox('L1D_TLB_REFILL')
        self.checkbox8  = QtGui.QCheckBox('L1D_CACHE_WB')
        self.checkbox9  = QtGui.QCheckBox('L1D_CACHE_ALLOCATE')

        self.checkbox10  = QtGui.QCheckBox('L2D_CACHE')
        self.checkbox11  = QtGui.QCheckBox('L2D_CACHE_REFILL')
        self.checkbox12 = QtGui.QCheckBox('L2D_CACHE_WB')
        self.checkbox13 = QtGui.QCheckBox('L2D_CACHE_ALLOCATE')

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


        groupbox_checkable_layout = QtGui.QVBoxLayout()

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


        self.groupbox_checkable = QtGui.QGroupBox('PMU RAW EVENT')
        self.groupbox_checkable.setLayout(groupbox_checkable_layout)
        self.groupbox_checkable.setCheckable(False)


        # canvas--right
        self.canvas_widget =  QtGui.QWidget(self)
        canvas = MyDynamicMplCanvas(self.canvas_widget, width=300, height=300, dpi=100)


        # vertical spacer on the left
        vspacer_left = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)

        # vertical spacer on the right
        vspacer_right = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)

        # vertical layout on the left
        vlayout_left = QtGui.QVBoxLayout()
        vlayout_left.addWidget(self.groupbox_checkable)
        vlayout_left.addSpacerItem(vspacer_left)
        vlayout_left.setMargin(10)

        # vertical layout on the right
        vlayout_right = QtGui.QVBoxLayout()
        vlayout_right.addWidget(canvas)

        # horizontal layout
        hlayout = QtGui.QHBoxLayout()
        hlayout.addLayout(vlayout_left)
        hlayout.addLayout(vlayout_right)

        # central widget
        central = QtGui.QWidget()
        central.setLayout(hlayout)
        self.setCentralWidget(central)

    def checkboxRecall(self, cbx):
        event_name = cbx.text()
        if cbx.isChecked():
            if not DISPATCH_DICTS.get(event_name):# 没打开过的, 则创建这么一个位置；
                DISPATCH_DICTS[event_name] = {"Line_Y": [], "NEW_DATA": False, "Line": None}
            # 已经打开过的，有存在的因此直接添加标志位就好了；
            CURRENT_LINE.add(event_name)
        else:
            # 取消显示的话，我们清空数组，并把之从CURRENT_LINE当前显示line中去掉；
            CURRENT_LINE.remove(event_name)

        #（我们清空后Filter仍然可能把延迟到达的数据扔进来，因此在打开的时候记得也要清理一下哈）
        # 当前check box只要选中或取消我们都要清空显示数据槽的。
        # 显示前清空list也就是清空line
        DISPATCH_DICTS[event_name]["Line_Y"] = []



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

    from filter import  Filter_thread
    PowerPerfFilter = Filter_thread(threadID=0, name="Filter_thread unit_test", q_data=q_data)
    PowerPerfFilter.start()

    from dispatch import  dispatch_thread
    PowerPerfDispatcher = dispatch_thread(threadID=1, name="dispatch_thread unit_test", q_data=q_data,
                                          dispatched_dict=DISPATCH_DICTS)
    PowerPerfDispatcher.start()

    main()
