# # coding=utf-8
# import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter
# import numpy as np
#
# # 生成数据
# month = np.linspace(1, 12, 12)
# dau = np.random.randint(20000, 30000, 12)
# ctr = np.random.randint(8, 200, 12)
#
# # 画图
# fig, ax1 = plt.subplots(figsize = (10, 5), facecolor='white')
#
# # 左轴
# ax1.plot([0,1,2], [2,3,4], color='g', alpha=0.5)
# ax1.set_xlabel('x')
# ax1.set_ylabel('y_l')
#
# # 右轴
# ax2 = ax1.twinx()
# ax2.plot([0,1,2,3], [0,1,2,4], '-or')
# ax2.set_ylabel('y_r')
# # ax2.set_ylim(0, 0.2)
#
#
# # 将点击率坐标轴以百分比格式显示
# def to_percent(temp, position):
#    return '%2.1f'%(100*temp) + '%'
# # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
# # 标题
# plt.title('afdadfasfdasdfsaf')
# ax2.clear()
# plt.show()
#
#

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
    # set_X = set()
    # set_X.add("zxl")
    # set_X.add("money")
    # set_X.add("zxl")
    # for item in set_X:
    #     print item
    #
    # print len(set_X), set_X
    # if "zxl" in set_X:
    #     print "ok"
    #
    # set_X.discard("zxl")# remove: if the data is not existed, then keyError coming up.
    # print set_X

    a = set()
    a.add(1)
    a.add(2)
    print a
    a.remove(1)
    print a