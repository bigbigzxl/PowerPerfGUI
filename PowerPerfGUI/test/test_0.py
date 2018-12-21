#
# co = 64
# ci = 64
# H  = 64
# W  = 64
#
# sizes = [
#         [16,192,64,64],
#         [16,64,192,64],
#         [16,64,64,192],
#         [64,16,192,64],
#         [64,16,64,192],
#         [64,64,16,192],
#         [64,64,192,16]
#         ]
#
# m1 = {"read":6, "write":2}
# m2 = {"read":8, "write":4}
#
# def read(size, method):
#     return size[3]*size[2]*(0.25 + (size[1]*size[0]/64.0)*method["read"])
#
# def write(size, method):
#     return size[3]*size[2]*((size[1]*size[0]/64.0)*method["write"])
#
# # def read(x):
# #     return co*ci*(0.25 + (H*W/64.0)*x)
# # def write(x):
# #     return co*ci*((H*W/64.0)*x)
# #
# # def I(x):
# #     return co*ci*((H*W/64.0)*x)
#
# # print read(8), read(6), read(8)/read(6)
# # print write(4), write(2), write(4)/write(2)
#
# # def read(x):
# #     return co*ci*(0.25 + (H*W/64.0)*x)
# # def write(x):
# #     return co*ci*((H*W/64.0)*x)
# reads_m1 = []
# reads_m2 = []
# writes_m1 = []
# writes_m2 = []
#
# # for size in sizes:
# #     reads_m1.append(read(size,m1))
# #     reads_m2.append(read(size,m2))
#
# import matplotlib.pyplot as plt
#
# plt.plot(list(map(lambda x: 100.0*(x[0]/x[1] - 1), zip(reads_m2, reads_m1))))
# # # plt.plot(reads_m2)
# # plt.show()
#
# class a:
#     a = 1
#     name = "a"
#
#     class a1:
#         a1 = 1
#         name = "a1"
#
#     class a2:
#         a2 = 1
#         name = "a2"
# A = a()
#
# # print A.a1.name
#
#
# from PyQt4 import QtGui  # provides the graphic elements
# from PyQt4.QtCore import Qt  # provides Qt identifiers
# from conv_kernel_operators import *
#
# class Window(QtGui.QWidget):
#     def __init__(self, val):
#         QtGui.QWidget.__init__(self)
#         mygroupbox = QtGui.QGroupBox('this is my groupbox')
#         myform = QtGui.QFormLayout()
#         labellist = []
#         combolist = []
#         for i in range(val):
#             labellist.append(QtGui.QLabel('mylabel'))
#             combolist.append(QtGui.QComboBox())
#             myform.addRow(labellist[i],combolist[i])
#         mygroupbox.setLayout(myform)
#         scroll = QtGui.QScrollArea()
#         scroll.setWidget(mygroupbox)
#         scroll.setWidgetResizable(True)
#         scroll.setFixedHeight(400)
#         layout = QtGui.QVBoxLayout(self)
#         layout.addWidget(scroll)
#
# if __name__ == '__main__':
#
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     window = Window(25)
#     window.setGeometry(500, 300, 300, 400)
#     window.show()
#     sys.exit(app.exec_())


a = set()
a.add(10)
a.add(2)
a.add(22)

# a.remove(3)
# a.discard(1)
# if not a:
#     print(111)
l = list(a)
print sorted(l)

b = [2,1,3]
b = sorted(b)
a = 1
b = 2
c = 1
if a==b==c:
    print "xxxxxxxx"
print("aosdoado"
      +"adadsadsads")

import os
print(os.path.join(os.getcwd(), "zxl\demos.h"))