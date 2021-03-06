# coding=utf-8

# import numpy as np
# import matplotlib
# matplotlib.use('Qt4Agg')
# import matplotlib.pyplot as plt
# import time
#
# fig, ax = plt.subplots()
# line, = ax.plot(np.random.randn(100))
# line1, = ax.plot(np.random.randn(100))
# plt.show(block=False)
#
# tstart = time.time()
# num_plots = 0
# value = []
# i = 1
# while time.time()-tstart < 5:
#     i += 1
#     value.append(i)
#     # 这种方式不会自动调节显示范围的
#     # line.set_xdata(value)
#     # 如果想只设置y数据的话，除非你的x范围是固定的；
#     # line.set_ydata(value)
#
#     # 77 FPS
#     # fig.canvas.draw() #只要用fig.canvas.update()，就必须有这个在ax.draw的前面
#     # ax.draw_artist(ax.patch)
#     # ax.draw_artist(line)
#     # fig.canvas.update()
#     # fig.canvas.flush_events()
#
#     # plt.ylim(0, np.max(value) * 1.02)
#     # plt.xlim(0, np.max(value) + 5)
#     # 95 FPS
#     fig.canvas.draw()
#     fig.canvas.flush_events()
#
#     num_plots += 1
# print(num_plots/5)


import numpy as np
import matplotlib.pyplot as plt

# Make some fake data.
a = b = np.arange(0, 3, .02)
c = np.exp(a)
d = c[::-1]

# Create plots with pre-defined labels.
fig, ax = plt.subplots()
ax.plot(a, c, 'k--', label='Model length')
ax.plot(a, d, 'k:', label='Data length')
ax.plot(a, c + d, 'k', label='Total message length')

legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')

# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#00FFCC')

plt.show()


DISPATCH_DICTS = {}
DISPATCH_DICTS["zxl"] = {"Line_Y":[]}
if DISPATCH_DICTS.get("zxl"):
    print "1111"
# DISPATCH_DICTS["zxl"]["Line"] = None
print DISPATCH_DICTS








# # s = ["1", "2", "3"]
# # print type(s)
#
# import os
# import subprocess
# import time
#
# time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print  "".join([time_str.split(" ")[0], " day"])
#
#
#
# # for dir_path, subpaths, filenames in os.walk(os.getcwd(), True):
# #     print dir_path
# #     print subpaths
# #     print filenames
#
# names = ['adb_perf_SingleMuti_show_generalEventV0.1.py', 'tester_unit.py']
# if "tester_unit.py" in names:
#     print "True"

# import matplotlib.pyplot as plt
# fig,ax = plt.subplots(1)
# l,=ax.plot(range(5))
# l.set_label('line 1')
# ax.legend()
#
# l.set_label('line 2')
# # ax.legend()
# plt.show()


#####################缺点：x轴不能动，优点整个图层不会闪烁##########################
# import matplotlib.pyplot as plt
# import numpy as np
#
# class demo():
#     def __init__(self):
#        pass
#
#     def demo0(self):
#         # 开启交互模式
#         plt.ion()
#
#         self.fig_s = plt.figure(figsize=(8, 6), dpi=80)
#         # self.fig_s.set_facecolor('gray')
#
#         self.axe_s = self.fig_s.add_subplot(111)
#         # self.axe_s.patch.set_facecolor("k")
#         # self.axe_s.patch.set_alpha(0.5)
#
#         self.line_x = []
#         self.line_y = []
#         self.line, = self.axe_s.plot([], [])
#
#         # plt.legend(loc="upper right", shadow=True)
#         #
#         # plt.xlabel("counter")
#         # plt.ylabel("value")
#         # plt.title("".join(["PMU RAW EVENT: ", "xxxx"]),
#         #           fontsize=18, fontweight='semibold', fontstyle='oblique',
#         #           backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))
#
#         for i in range(100):
#             self.line_y.append(i)
#             self.line_x.append(len(self.line_y))
#
#             # self.save_single_Datas(data)
#             self.line.set_xdata(self.line_x)
#             self.line.set_ydata(self.line_y)
#
#             max = np.max(self.line_y)
#             max1 = np.max(self.line_x)
#             plt.ylim(0, max * 1.1)
#             plt.xlim(0, max1 * 1.1)
#             self.fig_s.canvas.draw()
#             self.fig_s.canvas.flush_events()
#
#         # 关闭交互模式，否则上面跑完后就闪退了。
#         plt.ioff()
#
#         # 图形显示
#         plt.show()
#
#         return
#
#     def demo1(self):
#         plt.ion()
#         self.fig = plt.figure(figsize=(8, 6), dpi=80)
#         self.ax = self.fig.add_subplot(111)
#         self.line1, = self.ax.plot([], [], 'r-', label="zxl") # Returns a tuple of line objects, thus the comma
#         xa = []
#         ya = []
#         for i in range(10):
#             xa.append(i)
#             ya.append(i*1.1)
#             self.line1.set_xdata(xa)
#             self.line1.set_ydata(ya)
#             min  = np.min(ya)
#             max  = np.max(ya)
#             max1  = np.max(xa)
#             mean = np.mean(ya)
#             plt.ylim(0, max*1.1)
#             plt.xlim(0, max1 * 1.1)
#             self.fig.canvas.draw()
#             self.fig.canvas.flush_events()
#
#         plt.ioff()
#         plt.show()

# x = np.linspace(0, 6*np.pi, 100)
# y = np.sin(x)
#
# # You probably won't need this if you're embedding things in a tkinter plot...
# plt.ion()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(x, y, 'r-', label="zxl") # Returns a tuple of line objects, thus the comma
# plt.legend(loc="best",  shadow=True)
# plt.xlabel("counter")
# plt.ylabel("value")
# plt.title("".join(["PMU RAW EVENT: ", "CYCLES"]),
#           fontsize=18, fontweight='semibold', fontstyle='oblique',
#           backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))
#
# plt.grid(True)
# xa = []
# ya = []
#
# # ax.set_autoscale_on(True)
#
# for i in range(10):
#     xa.append(i)
#     ya.append(i*1.1)
#     line1.set_xdata(xa)
#     line1.set_ydata(ya)
#     line1.set_label("len=%d"%len(xa))
#     min  = np.min(ya)
#     max  = np.max(ya)
#     max1  = np.max(xa)
#     mean = np.mean(ya)
#     plt.ylim(0, max*1.1)
#     plt.xlim(0, max1 * 1.1)
#     fig.canvas.draw()
#     fig.canvas.flush_events()
#
# plt.ioff()
# plt.show()
#######################################
# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
#     fig.canvas.flush_events()


#########################doblit方式：优点帧率高####################

# #!/usr/bin/env python
#
# import numpy as np
# import time
# import matplotlib
# matplotlib.use('GTKAgg')
# from matplotlib import pyplot as plt
#
#
# def randomwalk(dims=(256, 256), n=20, sigma=5, alpha=0.95, seed=1):
#     """ A simple random walk with memory """
#
#     r, c = dims
#     gen = np.random.RandomState(seed)
#     pos = gen.rand(2, n) * ((r,), (c,))
#     old_delta = gen.randn(2, n) * sigma
#
#     while True:
#         delta = (1. - alpha) * gen.randn(2, n) * sigma + alpha * old_delta
#         pos += delta
#         for ii in xrange(n):
#             if not (0. <= pos[0, ii] < r):
#                 pos[0, ii] = abs(pos[0, ii] % r)
#             if not (0. <= pos[1, ii] < c):
#                 pos[1, ii] = abs(pos[1, ii] % c)
#         old_delta = delta
#         yield pos
#
#
# def run(niter=1000, doblit=True):
#     """
#     Display the simulation using matplotlib, optionally using blit for speed
#     """
#
#     fig, ax = plt.subplots(1, 1)
#     ax.set_aspect('equal')
#     ax.set_xlim(0, 255)
#     ax.set_ylim(0, 255)
#     ax.hold(True)
#     rw = randomwalk()
#     x, y = rw.next()
#
#     plt.show(False)
#     plt.draw()
#
#     if doblit:
#         # cache the background
#         background = fig.canvas.copy_from_bbox(ax.bbox)
#
#     points = ax.plot(x, y, 'o')[0]
#     tic = time.time()
#
#     for ii in xrange(niter):
#
#         # update the xy data
#         x, y = rw.next()
#         points.set_data(x, y)
#
#         if doblit:
#             # restore background
#             fig.canvas.restore_region(background)
#
#             # redraw just the points
#             ax.draw_artist(points)
#
#             # fill in the axes rectangle
#             fig.canvas.blit(ax.bbox)
#
#         else:
#             # redraw everything
#             fig.canvas.draw()
#
#     plt.close(fig)
#     print "Blit = %s, average FPS: %.2f" % (
#         str(doblit), niter / (time.time() - tic))
#
# if __name__ == '__main__':
#     run(doblit=False)
#     run(doblit=True)

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# x = np.arange(0., np.e, 0.01)
# y1 = np.exp(x)
# y2 = np.log(x)
#
# fig = plt.figure()
#
# ax1 = fig.add_subplot(111)
# ax1.plot(x, y1)
# ax1.set_ylabel('Y values for exp(-x)')
# ax1.set_title("Double Y axis")
#
# ax2 = ax1.twinx()  # this is the important function
# ax2.plot(x, y2, 'r')
# ax2.set_xlim([0, np.e])
# ax2.set_ylabel('Y values for ln(x)')
# ax2.set_xlabel('Same X for both exp(-x) and ln(x)')
#
# plt.show()
