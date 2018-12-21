from PyQt4 import QtGui  # provides the graphic elements
from PyQt4.QtCore import Qt  # provides Qt identifiers
from conv_kernel_operators import *

class Window(QtGui.QWidget):
    def __init__(self, val):
        QtGui.QWidget.__init__(self)
        self.mygroupbox = QtGui.QGroupBox('this is my groupbox')
        self.myform = QtGui.QFormLayout()
        self.labellist = []
        combolist = []
        self.temp = 0

        for i,name in enumerate(ConvOperators.Conv1x1s1Operators.operators_name):
            # labellist.append(QtGui.QLabel('mylabel'))
            # combolist.append(QtGui.QComboBox())
            # myform.addRow(labellist[i],combolist[i])
            # must use slef.temp , not just temp;
            self.temp = QtGui.QCheckBox(name)
            combolist.append(self.temp)
            self.myform.addRow(self.temp)

        # size = len(combolist)
        # for i in range(size):
        #     combolist[i].toggled.connect(lambda: self.checkboxRecall(combolist[i]))
        # you must do it lick this not before;
        combolist[0].toggled.connect(lambda: self.checkboxRecall(combolist[0]))
        combolist[1].toggled.connect(lambda: self.checkboxRecall(combolist[1]))
        combolist[2].toggled.connect(lambda: self.checkboxRecall(combolist[2]))
        combolist[3].toggled.connect(lambda: self.checkboxRecall(combolist[3]))
        combolist[4].toggled.connect(lambda: self.checkboxRecall(combolist[4]))

        self.mygroupbox.setLayout(self.myform)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.scroll)

    def checkboxRecall(self, cbx):
        print (str(cbx.text()))

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(25)
    window.setGeometry(500, 300, 300, 400)
    window.show()
    sys.exit(app.exec_())