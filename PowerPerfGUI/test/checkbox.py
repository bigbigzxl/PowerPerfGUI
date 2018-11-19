import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class checkdemo(QWidget):
    def __init__(self, parent=None):
        super(checkdemo, self).__init__(parent)

        layout = QHBoxLayout()
        self.b1 = QCheckBox("Button1")
        self.b1.setChecked(True)
        self.b1.stateChanged.connect(lambda: self.btnstate(self.b1))
        layout.addWidget(self.b1)

        self.b2 = QCheckBox("Button2")
        self.b2.toggled.connect(lambda: self.btnstate(self.b2))

        layout.addWidget(self.b2)
        self.setLayout(layout)
        self.setWindowTitle("checkbox demo")

    def btnstate(self, b):
        if b.text() == "Button1":
            if b.isChecked() == True:
                print b.text() + " is selected"
            else:
                print b.text() + " is deselected"

        if b.text() == "Button2":
            if b.isChecked() == True:
                print b.text() + " is selected"
            else:
                print b.text() + " is deselected"


def main():
    app = QApplication(sys.argv)
    ex = checkdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # main()
    # a = ["zxl", "oas", "fadacai", "fadacai"]
    # a.remove("fadacai")
    # print a
    set_X = set()
    set_X.add("zxl")
    set_X.add("money")
    set_X.add("zxl")
    for item in set_X:
        print item

    print len(set_X), set_X
    if "zxl" in set_X:
        print "ok"

    set_X.discard("zxl")# remove: if the data is not existed, then keyError coming up.
    print set_X
