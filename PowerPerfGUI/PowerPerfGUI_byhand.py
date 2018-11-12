import os
import sys  # provides interaction with the Python interpreter

from PyQt4 import QtGui  # provides the graphic elements
from PyQt4.QtCore import Qt  # provides Qt identifiers

from aqua.qsshelper import QSSHelper


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
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



def main():
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