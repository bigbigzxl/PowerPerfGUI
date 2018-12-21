# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from PyQt4.QtCore import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


reload(sys)
sys.setdefaultencoding('utf8')


class keyboard(QtGui.QWidget):
    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self, parent)
        self.initUi()
        self.resize(400,300)
        self.show()

    # def setTask(self, taskTemp):d
    #     self.task = taskTemp

    def initUi(self):

        self.label_1 = QtGui.QLabel("键盘监听小测试\n请按下‘D’，或者‘ESC’", self)
        self.label_1.setStyleSheet(_fromUtf8("font: 12pt \"微软雅黑\";\n"""))

        QtCore.QMetaObject.connectSlotsByName(self)



    #键盘监听函数，继承了父类，这里重写
    def keyPressEvent(self, event):
        key = event.key()

        #按下D
        if key == QtCore.Qt.Key_D:
            print "D is pressed"

        #按ESC键，则退出程序
        if key == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)

    app.Encoding(QtGui.QApplication.UnicodeUTF8)
    utfcodec = QTextCodec.codecForName("UTF-8")
    QTextCodec.setCodecForTr(utfcodec)
    QTextCodec.setCodecForLocale(utfcodec)
    QTextCodec.setCodecForCStrings(utfcodec)

    ui = keyboard()


    sys.exit(app.exec_())





