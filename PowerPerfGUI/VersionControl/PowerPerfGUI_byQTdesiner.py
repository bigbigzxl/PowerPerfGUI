import os
import sys  # provides interaction with the Python interpreter

from PyQt4 import QtGui  # provides the graphic elements

from pyqt4_proj.GITHUB.PowerPerfGUI.aqua.qsshelper import QSSHelper



from pyqt4_proj.GITHUB.PowerPerfGUI.VersionControl.PowerPerfMainWindow import Ui_MainWindow

class Window(Ui_MainWindow, QtGui.QMainWindow ):#
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ICO/ICON.ICO'))





def main():
    # creates the application and takes arguments from the command line
    application = QtGui.QApplication(sys.argv)

    # creates the window and sets its properties
    window = Window()
    window.setWindowTitle('PowerPerf GUI(authored by zxl)')  # title
    window.resize(800, 700)  # size

    # loads and sets the Qt stylesheet
    qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
    window.setStyleSheet(qss)


    window.show()  # shows the window

    # runs the application and waits for its return value at the end
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()


