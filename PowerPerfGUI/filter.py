# coding=utf-8
import Queue
import os
import subprocess
import sys
import threading
import time
import numpy as np
import Queue

class Filter_thread(threading.Thread):
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

    def __init__(self, threadID, name, q_data, MAX_QUEUE_SIZE=10240):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        #传过来的是地址，因此这里直接用q形参或者self.q结果都是一样的，能实现全局操作。
        self.q = q_data
        self.max_queue_size = MAX_QUEUE_SIZE
        self.key_string = "label@perf"

    def run(self):
        #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.filter_datas()

    def filter_datas(self):
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
                if self.q.qsize() > self.max_queue_size:
                    print ("WARNNING!!! you deal data too slow, drop datas...")
                    continue

                # 只要出现了label@perf，就把这一行送去处理。
                self.filter_datas_func(outline)
            else:
                # For PowerSave
                time.sleep(0.03)

    def filter_datas_func(self, data_string):
        # LOGE() style should be: "**label@perf,CYCLES=3.2,GFLOPS=8.2,"
        data_list = data_string.strip().split(",")

        for data in data_list:
            if "=" in data and len(data) > 1:
                # 这里不能block的, 会影响性能。
                self.q.put(data.replace(" ", ""), block=False, timeout=None)
                print data
                return


if __name__ == "__main__":
    if (sys.version_info > (3, 0)):
        # python3
        q_data = Queue()
    else:
        # python2
        q_data = Queue.Queue()

    PowerPerfFilter = Filter_thread(threadID=0, name="unit_test", q_data=q_data)
    PowerPerfFilter.start()
