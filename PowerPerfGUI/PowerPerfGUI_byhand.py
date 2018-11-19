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

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=8, height=6, dpi=80):
        # 开启交互模式
        # plt.ion()

        self.fig_s = plt.figure(figsize=(width, height), dpi=dpi)
        self.fig_s.set_facecolor('gray')

        FigureCanvas.__init__(self, self.fig_s)
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
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(30)
        self.axe_s = self.fig_s.add_subplot(111)
        self.axe_s.patch.set_facecolor("k")
        self.axe_s.patch.set_alpha(0.75)

        self.line_x = []
        self.line_y = []
        self.line, = self.axe_s.plot([], [], "r--o", linewidth=2.0, label="".join(["jitter: ", "%.2f" % (0), "%"]))

        # plt.tight_layout() #只有在全屏显示时效果才好，否则会有些区域看不到。

        plt.legend(loc="best", prop=self.myfont, shadow=True)

        plt.xlabel("counter", fontsize=16)
        plt.ylabel("value", fontsize=16)

        plt.title("PMU RAW EVENT", fontsize=18, fontweight='bold', fontstyle='italic',
                  backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))

        self.line_x = [1,2,3]
        self.line_y = [12,34,123]

        self.line, = self.axe_s.plot([], [], "r--o", linewidth=2.0, label="".join(["jitter: ", "%.2f" % (0), "%"]))

        self.update_figure()

    def compute_initial_figure(self):
        pass

    def update_figure(self):
        # self.y.append(random.randint(0, 100))
        # self.x.append(len(self.y))
        # self.axes.cla()
        # self.axes.plot(self.y, 'r--o')
        # self.draw()
        self.plot_single_Datas(self.fig_s, self.axe_s, self.line, self.line_x, self.line_y)

        # 关闭交互模式，否则上面跑完后就闪退了。
        plt.ioff()

        # 图形显示
        plt.show()

    def plot_single_Datas(self, fig, axe, line, x, y):
        # 任意一个figure下的任意一条线。
        # 记得中间还有个axes啊！
        line.set_xdata(x)
        line.set_ydata(y)

        max_x  = np.max(x)
        max_y  = np.max(y)
        min_y  = np.min(y)
        mean_y = np.mean(y)
        plt.ylim(0, max_y*1.02)
        plt.xlim(0, max_x + 5)

        line.set_label("".join(["jitter: ","%.2f"%(100.0*(max_y - min_y) / mean_y), "%", "\nMin=%d"%min_y, "\nMax=%d"%max_y ]))
        axe.legend(loc="best", prop=self.myfont, shadow=True)

        fig.canvas.draw()
        fig.canvas.flush_events()

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
    main()
