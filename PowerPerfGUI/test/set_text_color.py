# coding:utf-8
'''
Created on 2015年2月9日
@author: guowu
'''
import sys
from PyQt4.QtGui import QPalette, QPixmap, QFont, QMainWindow, QLabel, QApplication
from PyQt4.QtCore import Qt


# import classblock

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setFixedSize(600, 600)
        self.label = QLabel(self)
        self.label.setFixedWidth(400)
        self.label.setFixedHeight(400)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(u"这个标签的长裤可以变化吗aaaaaaaa东西南北？")

        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        # self.label.setAutoFillBackground(True)
        # pe.setColor(QPalette.Window, Qt.blue)
        # pe.setColor(QPalette.Background,Qt.blue)
        self.label.setPalette(pe)

        self.label.setFont(QFont("Roman times", 10, QFont.Bold))

        self.label.move(100, 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
