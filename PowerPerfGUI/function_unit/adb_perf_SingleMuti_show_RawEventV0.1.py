# coding=utf-8
import Queue
import os
import subprocess
import sys
import threading
import time

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
from mpl_toolkits.axes_grid1 import Grid


class myThread_produce (threading.Thread):
    """
    继承父类threading.Thread


    Attributes
    ----------
    exposure : queue
        Exposure in queue.

    Methods
    -------
    colorspace(c='rgb')
        Represent the photo in the given colorspace.
    gamma(n=1.0)
        Change the photo's gamma exposure.

    """

    def __init__(self, threadID, name, PRINT=False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        #传过来的是地址，因此这里直接用q形参或者self.q结果都是一样的，能实现全局操作。
        self.perf_data_detected = False
        self.PRINT = PRINT
        # self.first_time_IN = True
        self.key_string = KEY_STRING_FOR_DETECT
        if   MODE == "Division":
            self.deal_datas_func = self.division_deal_datas
        elif MODE == "single":
            self.deal_datas_func = self.single_deal_datas
        else:
            print "ERROR: MODE is not support yet."
            exit(0)

    def run(self):
        #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.produce_data()

    def produce_data(self):
        """
        检查到数据是目标数据就简单清洗（去除换行符、去掉空格保持“value1，value2， ....”格式）；
        然后就推送到数据队列；
        注：为了尽可能少的时间处理数据，此时是没有检测合法性（比如数据是否有缺损）的；
        :return:
        """

        # reset adb log buffer.
        os.system("adb logcat -c")

        cmd1 = "adb logcat *:E"
        process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.time = time.time()

        while True:
            # block read:
            #   五秒一次，每次到5s这个关卡就连续极快地读四次；
            outline = process.stdout.readline()

            if outline == '' and process.poll() != None:
                print ("break")
                break

            if outline != '' and self.key_string in outline:
                # 只要出现了label@perf，就把这一行送去处理。
                self.deal_datas_func(outline)

    def division_deal_datas(self, data_string):
        # LOGE() style should be: "**label@perf,CYCLES=3.2,GFLOPS=8.2,"
        data_list = data_string.strip().split(",")
        for data in data_list:

            if KEY_STRING_FOR_DIVISION_MODE_numerator in data:
                LIST_DIVISION_MODE_numerator.append(float(data.replace(" ", "").split("=")[-1]))

            if KEY_STRING_FOR_DIVISION_MODE_denominator in data:
                LIST_DIVISION_MODE_denominator.append(float(data.replace(" ", "").split("=")[-1]))




if __name__ == "__main__":

    KEY_STRING_FOR_DETECT = "label@perf"

    ###############################################################################
    # 配置区域：
    #       配置路径、运行模式等参数；
    ###############################################################################
    # for mode single:
    # LOGE() style should be: "**label@perf,time=3.2,GFLOPS=8.2,"
    MODE                  = "Division"


    # numerator/denominator
    KEY_STRING_FOR_DIVISION_MODE_numerator   = "INST_RETIRED"
    KEY_STRING_FOR_DIVISION_MODE_denominator = "CPU_CYCLES"
    LIST_DIVISION_MODE_numerator   = []
    LIST_DIVISION_MODE_denominator = []
    OUTCOME = []

    # 1、子线程1负责去采集、粗过滤数据到公共的q_data队列中；
    produce = myThread_produce(1, "Thread_produce")
    produce.start()

    # 开启交互模式
    plt.ion()

    fig_s = plt.figure(figsize=(8, 6), dpi=80)
    fig_s.set_facecolor('gray')

    axe_s = fig_s.add_subplot(111)
    axe_s.patch.set_facecolor("k")
    axe_s.patch.set_alpha(0.5)

    # line_outcome, = axe_s.plot([], [], "y--o", linewidth=2.0, label="".join(["jitter: ", "%.2f" % (0), "%"]))
    # plt.tight_layout() #只有在全屏显示时效果才好，否则会有些区域看不到。
    myfont = fm.FontProperties(fname="C:/Windows/Fonts/simkai.ttf", size=14)
    plt.legend(loc="best", prop=myfont, shadow=True)

    plt.xlabel("counter", fontsize=16)
    plt.ylabel("value", fontsize=16)

    plt.title("".join(["PMU RAW EVENT: ", KEY_STRING_FOR_DIVISION_MODE_numerator, '/', KEY_STRING_FOR_DIVISION_MODE_denominator]),
              fontsize=18, fontweight='bold', fontstyle='italic',
              backgroundcolor="red", bbox=dict(facecolor='r', edgecolor='black', alpha=0.9))

    _len = 0
    while True:
        if len(LIST_DIVISION_MODE_numerator) == len(LIST_DIVISION_MODE_denominator) > 0 and len(LIST_DIVISION_MODE_numerator) > _len:
            _len = len(LIST_DIVISION_MODE_numerator)
            OUTCOME = list(map(lambda x: x[0] / x[1], zip(LIST_DIVISION_MODE_numerator, LIST_DIVISION_MODE_denominator)))
            plt.cla()
            plt.plot(OUTCOME, "r--o", linewidth=2.0, label="".join(["=", KEY_STRING_FOR_DIVISION_MODE_numerator,"/", KEY_STRING_FOR_DIVISION_MODE_denominator]))
        else:
            plt.pause(0.5)

    # 关闭交互模式，否则上面跑完后就闪退了。
    plt.ioff()

    # 图形显示
    plt.show()
