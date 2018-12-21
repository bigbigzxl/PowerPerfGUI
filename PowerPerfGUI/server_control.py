#!/usr/bin/evn python
# -*- coding:utf-8 -*-

from adb_tools import *

class Server_control(AdbTools):

    def __init__(self):
        super(Server_control, self).__init__()
        # self.root()
        # self.get_perf_author()

    def control_funcs(self):
        """
        subprocess.popen是一个超集，包括了其他的。

        1.os.system
            该函数返回命令执行结果的返回值，system()函数在执行过程中进行了以下三步操作：
            1.fork一个子进程；
            2.在子进程中调用exec函数去执行命令；
            3.在父进程中调用wait（阻塞）去等待子进程结束。
            对于fork失败，system()函数返回-1。
            由于使用该函数经常会莫名其妙地出现错误，但是直接执行命令并没有问题，所以一般建议不要使用。
            ---------------------

        2.os.popen
             popen() 创建一个管道，通过fork一个子进程,然后该子进程执行命令。
             返回值在标准IO流中，该管道用于父子进程间通信。
             父进程要么从管道读信息，要么向管道写信息，至于是读还是写取决于父进程调用popen时传递的参数（w或r）。
             通过popen函数读取命令执行过程中的输出示例如下：
                    #!/usr/bin/python
                    import os
                    p=os.popen('ssh 10.3.16.121 ls')
                    x=p.read()
                    print x
                    p.close()

            os.open()适用于你运行一次然后得到结果这种一次性的处理；
            ---------------------

        2.subprocess
            subprocess模块是在2.4版本中新增的，官方文档中描述为可以用来替换以下函数：
                                    os.system、os.spawn、os.popen、popen2

            参数既可以是string，也可以是list。
            subprocess.Popen([“cat”,”test.txt”])
            subprocess.Popen(“cat test.txt”, shell=True)
            对于参数是字符串，需要指定shell=True

            cmd = "adb shell ls /sdcard/ | findstr aa.png"
            fhandle = open(r"e:\aa.txt", "w")
            pipe = subprocess.Popen(cmd, shell=True, stdout=fhandle).stdout
            fhandle.close()

            2.执行结果使用管道输出
            pipe=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).stdout
            print pipe.read()
            ---------------------

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
                pass

    def get_perf_author(self):
        """
        获取perf的权限，自动执行，无需手动开启；
        :return:
        """
        if not self.file_exists("/proc/sys/kernel/perf_event_paranoid"):
            print("Your Android(linux kernel) system is not a Development version.")
            exit(0)

        perf_event_paranoid = self.shell("cat /proc/sys/kernel/perf_event_paranoid").readlines()[0].strip()
        if perf_event_paranoid == "-1":
            print("You're authorized already(perf_event_paranoid).")
            return True
        else:
            # 记得放在config文件下。
            # 注意在安卓下的shell脚本开头是： #! /system/bin/sh
            cmd = "./config/get_perf_author.sh"

            for i in range(5):
                try:
                    # os.system(cmd)
                    # 只有这种方式下才可以连续地执行shell指令，否则只能一条条执行，这里我被卡了很多时间的。
                    data = os.popen("adb shell < " + cmd)

                    perf_event_paranoid = self.shell("cat /proc/sys/kernel/perf_event_paranoid").readlines()[0].strip()

                    if perf_event_paranoid == "-1":
                        print("Get perf author success.")
                        return True

                except Exception as e:
                         print("Error@get perf authority:", e)

            print("For some Unknow Error we can not get perf authority.")

            return False

    def restart_adb(self):
        print("restarting adb....")
        self.adb("kill-server")
        time.sleep(0.3)
        out_pipe = self.adb("start-server")#os.popen("adb start-server")#
        outcome = out_pipe.readlines()
        if "success" in outcome:
            print("Restart adb successed.")
        else:
            print("Restart adb failed.")
            print(outcome)


if __name__ == '__main__':

    # Step1: 设置adb位置，会自动去ANDROID_HOME下找"platform-tools", "adb.exe"。
    SDK_dir = "E:\SDK"
    os.environ['ANDROID_HOME'] = SDK_dir
    # print(os.environ.get('ANDROID_HOME'))

    # Step2: 获取perf的权限
    Server_control = Server_control()
    Server_control.get_perf_author()
    Server_control.restart_adb()


    # Step3: 开始接受GUI过来的事件并进行处理然后做出相应的控制；
    # com.example.administrator.hello_cmake
    # pakeage = "com.example.administrator.hello_cmake"

    # com.example.administrator.hello_cmake/com.example.administrator.hello_cmake.MainActivity
    # print communicator.get_current_activity()

    # communicator.quit_app(pakeage)

    # activity = "com.example.administrator.hello_cmake/com.example.administrator.hello_cmake.MainActivity"
    # communicator.start_application(activity)
    # print os.getenv("path")
    # for path in os.environ:
    #     print path

    # print communicator.shell("cat /proc/sys/kernel/perf_event_paranoid")
    # while True:
    #     print communicator.get_cache_logcat().readlines()
    pass