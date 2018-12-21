#coding=utf-8
import socket


HOST = '127.0.0.1'
PORT = 9000
#  [Errno 10061] 端口号对不上。
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 尝试建立连接:
try:
    s.connect((HOST, PORT))
except Exception as e:
    print(e)
    if "10054" in e:
        print("PowerPerf server(JAVA) is not set up !")

    # adb forward tcp:9000 tcp:9090

# 发送数据:
try:
    times  = 1                        # 1~125
    events_cmd = [times,1,2,3,4,5,6]      # must not be more than 6 items
    CMD = chr(len(events_cmd) + 1)   # 加上自身之后总的指令长度
    for i, value in enumerate(events_cmd):
        CMD += chr(events_cmd[i])
except Exception as e:
    print(e)
    print("cmd item's value should not be more than 127.")

s.send(CMD)
print("send succeed.")
# s.shutdown(flag="SHUT_WR")#防止服务端的read会阻塞在这
returned_flag = s.recv(1024).strip().replace("\x00\x04", "")
# print (len(returned_flag), returned_flag.strip().replace("\x00\x04", "")) # 0x00:NULL; 0x04:EOT(end of transmition)
if (returned_flag == "ack."):
    print("get ack.")
else:
    print("there is a stall in server(JAVA): the server after receiving the CMD send a ack back, but i dont get it.")

s.close()


# print(chr(40)+chr(49))


