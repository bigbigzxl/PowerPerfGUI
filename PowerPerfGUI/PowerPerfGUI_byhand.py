# coding=utf-8
from __future__ import unicode_literals
import sys
import os
import random
from matplotlib.backends import qt_compat
import matplotlib.pyplot as plt
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

sys.path.append('../')
from aqua.qsshelper import QSSHelper

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

import os
import sys  # provides interaction with the Python interpreter

from PyQt4 import QtGui  # provides the graphic elements
from PyQt4.QtCore import Qt  # provides Qt identifiers

from aqua.qsshelper import QSSHelper
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import time


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        plt.title("zxl")
        fig.set_facecolor('gray')
        # fig.set_alpha(0.99)
        # plt.rcParams['axes.facecolor'] = 'gray'

        self.axes = fig.add_subplot(111)

        # self.axes.patch.set_facecolor("k")
        # self.axes.patch.set_alpha(0.75)


        # self.axes.set_axis_bgcolor('red')
        # self.axes.set_axis_bgcolor((0.3, 0, 0))

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
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
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(100)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        self.axes.set_title("good")

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.clear()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.axes.set_title("good")
        self.draw()

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.current_events = set()




        QtGui.QMainWindow.__init__(self, parent)

        # checkable groupbox
        self.checkbox1 = QtGui.QCheckBox('CPU_CYCLES')
        self.checkbox2 = QtGui.QCheckBox('L1D_CACHE_REFILL')
        self.checkbox3 = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox4 = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox5 = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox6 = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox7 = QtGui.QCheckBox('L1D_CACHE')
        self.checkbox8 = QtGui.QCheckBox('L1D_CACHE')


        groupbox_checkable_layout = QtGui.QVBoxLayout()
        groupbox_checkable_layout.addWidget(self.checkbox1)
        groupbox_checkable_layout.addWidget(self.checkbox2)
        groupbox_checkable_layout.addWidget(self.checkbox3)
        groupbox_checkable_layout.addWidget(self.checkbox4)
        groupbox_checkable_layout.addWidget(self.checkbox5)
        groupbox_checkable_layout.addWidget(self.checkbox6)
        groupbox_checkable_layout.addWidget(self.checkbox7)
        groupbox_checkable_layout.addWidget(self.checkbox8)

        self.groupbox_checkable = QtGui.QGroupBox('PMU RAW EVENT')
        self.groupbox_checkable.setLayout(groupbox_checkable_layout)
        self.groupbox_checkable.setCheckable(False)


        # toolbox
        textedit = QtGui.QTextEdit('TextEdit')
        plaintextedit = QtGui.QPlainTextEdit('PlainTextEdit')
        self.toolbox = QtGui.QToolBox()
        self.toolbox.addItem(textedit, 'Page 1')
        self.toolbox.addItem(plaintextedit, 'Page 2')


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
        vlayout_right.addWidget(self.toolbox)
        vlayout_right.addSpacerItem(vspacer_right)
        vlayout_right.setMargin(10)

        # horizontal layout
        hlayout = QtGui.QHBoxLayout()
        hlayout.addLayout(vlayout_left)
        hlayout.addLayout(vlayout_right)

        # central widget
        central = QtGui.QWidget()
        central.setLayout(hlayout)
        self.setCentralWidget(central)


        ############################################


    def dynamic_drawlines(self):
        # aim: one func one thing.
        for event_name in self.current_events:
            if DISPATCH_DICTS.get(event_name) and len(DISPATCH_DICTS[event_name]["Line_Y"]) > 0:
                pass


    def plot_single_Datas(self, fig, axe, line, x, y):
        line.set_xdata(x)
        line.set_ydata(y)

        max_x = np.max(x)
        max_y = np.max(y)
        min_y = np.min(y)
        mean_y = np.mean(y)
        plt.ylim(0, max_y * 1.02)
        plt.xlim(0, max_x + 5)

        fig.canvas.draw()
        fig.canvas.flush_events()

def main():
    global DISPATCH_DICTS
    DISPATCH_DICTS = {}

    # creates the application and takes arguments from the command line
    application = QtGui.QApplication(sys.argv)

    # creates the window and sets its properties
    window = Window()
    window.setWindowTitle('Aqua (Qt stylesheet)')  # title
    window.resize(800, 100)  # size

    # loads and sets the Qt stylesheet
    qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
    window.setStyleSheet(qss)

    window.show()  # shows the window

    # runs the application and waits for its return value at the end
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
