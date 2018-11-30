# from matplotlib import pyplot as plt
#
# class LineBuilder:
#     def __init__(self, line):
#         self.line = line
#         self.xs = list(line.get_xdata())
#         self.ys = list(line.get_ydata())
#         self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
#
#     def __call__(self, event):
#         print('click', event)
#         if event.inaxes!=self.line.axes: return
#         self.xs.append(event.xdata)
#         self.ys.append(event.ydata)
#         self.line.set_data(self.xs, self.ys)
#         self.line.figure.canvas.draw()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click to build line segments')
# line, = ax.plot([0], [0])  # empty line
# linebuilder = LineBuilder(line)
#
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on points')

line, = ax.plot(np.random.rand(100), '-o', picker=5)  # 5 points tolerance

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    points = tuple(zip(xdata[ind], ydata[ind]))
    print('onpick points:', points)

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()








# """
# compute the mean and stddev of 100 data sets and plot mean vs stddev.
# When you click on one of the mu, sigma points, plot the raw data from
# the dataset that generated the mean and stddev
# """
# import numpy as np
# import matplotlib.pyplot as plt
#
# X = np.random.rand(100, 1000)
# xs = np.mean(X, axis=1)
# ys = np.std(X, axis=1)
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click on point to plot time series')
# line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance
#

# def onpick(event):
#
#     if event.artist!=line: return True
#
#     N = len(event.ind)
#     if not N: return True
#
#
#     figi = plt.figure()
#     for subplotnum, dataind in enumerate(event.ind):
#         ax = figi.add_subplot(N,1,subplotnum+1)
#         ax.plot(X[dataind])
#         ax.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f'%(xs[dataind], ys[dataind]),
#                 transform=ax.transAxes, va='top')
#         ax.set_ylim(-0.5, 1.5)
#     figi.show()
#     return True
#
# fig.canvas.mpl_connect('pick_event', onpick)
#
# plt.show()