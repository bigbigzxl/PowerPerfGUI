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

class dispatch_thread (threading.Thread):

    def __init__(self, threadID, name, q_data, dispatched_dict, MAX_LINE_LENGTH=4096, SAVEFILE=False):
        threading.Thread.__init__(self)
        self.threadID           = threadID
        self.name               = name
        self.q_data             = q_data
        self.dispatched_dict    = dispatched_dict
        self.EventName          = ["SW_INCR",
                                   "L1I_CACHE_REFILL",
                                   "L1I_TLB_REFILL",
                                   "L1D_CACHE_REFILL",       #
                                   "L1D_CACHE",              #
                                   "L1D_TLB_REFILL",         #
                                   "LD_RETIRED",
                                   "ST_RETIRED",
                                   "INST_RETIRED",           #
                                   "EXC_TAKEN",
                                   "EXC_RETURN",
                                   "CID_WRITE_RETIRED",
                                   "PC_WRITE_RETIRED",
                                   "BR_IMMED_RETIRED",
                                   "BR_RETURN_RETIRED",
                                   "UNALIGNED_LDST_RETIRED",
                                   "BR_MIS_PRED",            #
                                   "CPU_CYCLES",             #
                                   "BR_PRED",
                                   "MEM_ACCESS",
                                   "L1I_CACHE",
                                   "L1D_CACHE_WB",           #
                                   "L2D_CACHE",              #
                                   "L2D_CACHE_REFILL",       #
                                   "L2D_CACHE_WB",           #
                                   "BUS_ACCESS",
                                   "MEMORY_ERROR",
                                   "INST_SPEC",              #
                                   "TTBR_WRITE_RETIRED",
                                   "BUS_CYCLES",
                                   "CHAIN",
                                   "L1D_CACHE_ALLOCATE",     #
                                   # A53 support end.
                                   "L2D_CACHE_ALLOCATE",     #
                                   "BR_RETIRED",
                                   "BR_MIS_PRED_RETIRED",
                                   "STALL_FRONTEND",
                                   "STALL_BACKEND",
                                   "L1D_TLB",
                                   "L1I_TLB",
                                   "L2I_CACHE",
                                   "L2I_CACHE_REFILL",
                                   "L3D_CACHE_ALLOCATE",
                                   "L3D_CACHE_REFILL",
                                   "L3D_CACHE",
                                   "L3D_CACHE_WB",
                                   "L2D_TLB_REFILL",
                                   "L2I_TLB_REFILL",
                                   "L2D_TLB",
                                   "L2I_TLB",
                                   "RAW_EVENT_SIZE"
                                   ]
        self.max_line_length    = MAX_LINE_LENGTH
        self.savefile           = SAVEFILE
    def run(self):
        self.dispatch_data()

    def dispatch_data(self):
        """
        deal perf datas.
        :return: None.
        """
        while True:
            # 假设数据都是“name=value”style.
            line = self.q_data.get(block=True, timeout=None)
            if line:
                self.dispatch_2_dict(line)

                if self.savefile:
                    self.SAVEdatas(line)
            else:
                print "IO ERROR: get no data from data_queue."

    def dispatch_2_dict(self, line):
        event_name, event_value = line.split("=")
        if event_name not in self.EventName:
            return
        else:
            # 有则返回字典，没有则返回None；
            if self.dispatched_dict.get(event_name):
                if len(self.dispatched_dict[event_name]["Line_Y"]) >= self.max_line_length:
                    # 实现队列的功能，去掉最老的数据，然后补新的，为了方式line太长从而显示卡顿挂掉；
                    self.dispatched_dict[event_name]["Line_Y"].pop(0)
            else:# 没有字典还
                self.dispatched_dict[event_name] = {"Line_Y": []}

            self.dispatched_dict[event_name]["Line_Y"].append(float(event_value))

    def SAVEdatas(self, line):
        self.folder = os.path.join(os.getcwd(), "TEST_VALUES")
        Today_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.today_fileName = "".join(["MixDatas", " ", Today_time.split(" ")[0], ".txt"])
        self.Today_filePath = os.path.join(self.folder, self.today_fileName)

        # 文件夹是否存在
        if os.path.exists(self.folder):
            pass
        else:
            os.makedirs(self.folder)
            print ("makedir %s success." % self.folder)

        # 无需判断文件是否存在，因为只要文件夹存在，就算文件不存在，以a+方式open就会新建文件；（注：文件夹不存在的话就会报错的）
        with open(self.Today_filePath, "a+") as f:
            f.write(line + "\n")


if __name__ == "__main__":


    from filter import Filter_thread

    if (sys.version_info > (3, 0)):
        # python3
        q_data = Queue()
    else:
        # python2
        q_data = Queue.Queue()


    events_dicts = {}

    PowerPerfFilter = Filter_thread(threadID=0, name="Filter_thread unit_test", q_data=q_data)
    PowerPerfFilter.start()

    PowerPerfDispatcher = dispatch_thread(threadID=1, name="dispatch_thread unit_test", q_data=q_data, dispatched_dict=events_dicts)
    PowerPerfDispatcher.start()

    while True:
        for kv in events_dicts.items():
            print len(kv[1]["Line_Y"]), kv[0]

        print "==============="
        time.sleep(1)
