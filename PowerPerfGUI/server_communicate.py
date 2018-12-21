#!/usr/bin/evn python
# -*- coding:utf-8 -*-

from adb_tools import *
import types

class ServerCommunicator(AdbTools):

    def __init__(self, HOST= '127.0.0.1', LOCAL_PORT=9000, REMOTE_PORT=9090):
        super(ServerCommunicator, self).__init__()
        self.local_port  = LOCAL_PORT;
        self.remote_port = REMOTE_PORT;
        self.host        = HOST;

        # self.redirect_port() # 通信准备


    def is_redirected(self):
        _pipe = os.popen('netstat -ano|findstr "%d"' % (self.local_port))
        out = _pipe.read()
        if "TCP" in out and "%s:%d" % (self.host, self.local_port) in out and "LISTENING" in out:
            # print ("redirect PORT tcp:%d to tcp:%d success." % (self.local_port, self.remote_port))
            return True
        else:
            print ('\033[1;31m' + "redirect PORT tcp:%d to tcp:%d failed." % (self.local_port, self.remote_port) + '\033[0m')
            return False


    def redirect_port(self):
        # adb tcp Ip地址默认为127.0.0.1，其次不能与PC端使用同样的端口号，因此需要重定向；
        self.adb("forward tcp:%d tcp:%d"%(self.local_port, self.remote_port))

        self.is_redirected()


    def SendCmd2JavaServer(self, cmd):
        """
            GUI调用此部分接口，把Perf的相关指令信息发送到手机JAVA层中的socket server之中；
       :param
            cmd: 指令，格式如下：
                [total_length, times, cmd[2], cmd[3], cmd[4], cmd[5], cmd[6], cmd[7]]
                list中每个元素都是char型的，因为这样子以满足目前的简单需求，以后的需求以后再重构（现在没时间写那么多啊！大佬）
       :return:
       """
        # 检查指令格式是否正确；
        if type(cmd) is not types.ListType or len(cmd) != cmd[0]:
            print ("cmd error.", cmd)
            return False

        # 检查指令参数中是否有越界的（暂时只支持-127~127）
        for item in cmd:
            try:
                temp = chr(item)
            except Exception as e:
                print(e, "cmd item's value is out of byte range.")
                return False

        # 防止中途突然断开连接
        if not self.is_redirected():
            print(" 9000 local port not redirect to 9090 remote port. redirected again...")
            self.redirect_port()

        # 尝试进行连接，检查JAVA端的server是否建立
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 尝试建立连接:[Errno 10061] 端口号对不上。
        try:
            s.connect((self.host, self.local_port))
        except Exception as e:
            print(e)
            if "10054" in e:
                print("PowerPerf server(JAVA) is not set up !")

            return False

            # adb forward tcp:9000 tcp:9090

        # 发送数据:
        try:
            #      1           2       3       4       5      6        7       8
            # [total_length, times, cmd[2], cmd[3], cmd[4], cmd[5], cmd[6], cmd[7]]
            # ex:  =8         =100  event1, event2, event3, event4, event5, event6
            for i, value in enumerate(cmd):
                if (i == 0):
                    CMD_char = chr(cmd[0])
                else:
                    CMD_char += chr(cmd[i])
        except Exception as e:
            print(e)
            print("cmd item's value should not be more than 127.")
            return False

        # 道路通畅，准备发射；
        try:
            s.send(CMD_char)
        except Exception as e:
            print (e)
            print("in send part failed. maybe redirect or pipe error.")
            s.close()
            return  False

        # 发送成功，无需显示，只显示错误就好了。
        # print("send succeed.")

        # 接收JAVA端成功处理的标志；
        try:
            returned_flag = s.recv(1024).strip().replace("\x00\x04", "")
            # print (len(returned_flag), returned_flag.strip().replace("\x00\x04", "")) # 0x00:NULL; 0x04:EOT(end of transmition)
            if (returned_flag == "ack."):
                print("get ack.")
            else:
                print("there is a stall in server(JAVA): the server after receiving the CMD send a ack back, but i dont get it.")
        except Exception as e:
            print(e)
            print("in receive part faild. maybe JAVA socket in your phone is not set up.")

        s.close()

        return True



if __name__ == '__main__':

    # Step1: 设置adb位置，会自动去ANDROID_HOME下找"platform-tools", "adb.exe"。
    SDK_dir = "E:\SDK"
    os.environ['ANDROID_HOME'] = SDK_dir


    # Step2:
    server_communicator = ServerCommunicator()


    from pmu_raw_events import PMU_RAW_EVENTS

    while True:
        server_communicator.SendCmd2JavaServer([8, 1,
                                                PMU_RAW_EVENTS.L1D_CACHE,
                                                PMU_RAW_EVENTS.L1D_CACHE_REFILL,
                                                PMU_RAW_EVENTS.L1D_CACHE_WB,
                                                PMU_RAW_EVENTS.L1D_CACHE_ALLOCATE,
                                                PMU_RAW_EVENTS.L1D_TLB,
                                                PMU_RAW_EVENTS.L1D_TLB_REFILL ])
        time.sleep(0.3)
    # reset adb log buffer.

    # # adb_path = os.path.join("E:\SDK", "platform-tools", "adb.exe")
    # cmd1 = "adb logcat *:E"
    # process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    #
    # while True:
    #     # block read:
    #     #   五秒一次，每次到5s这个关卡就连续极快地读四次；
    #     outline = process.stdout.readline()
    #
    #     if outline == '' and process.poll() != None:
    #         print ("break")
    #         break
    #
    #     if outline != '' and "label@perf" in outline:
    #         print outline


    # Step3: 开始接受GUI过来的事件并进行处理然后做出相应的控制；

