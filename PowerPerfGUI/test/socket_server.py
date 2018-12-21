# coding=utf-8
import socket
import threading
import time


def tcplink(sock, addr):
    print ('Accept new connection from %s:%s...' % addr)
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print ('Connection from %s:%s closed.' % addr)

HOST = '192.168.1.10'
PORT = 9090
server = socket.socket()  # 初始化
server.bind((HOST, PORT))  # 绑定ip和端口
server.listen(5)  # 监听，设置最大数量是5
print("开始等待接受客户端数据----")

while True:
    # 接受一个新连接:
    sock, addr = server.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()





# while True:
#     conn, addr = server.accept()  # 获取客户端地址
#     print(conn, addr)
#     print("客户端来数据了")
#     while True:
#         data = conn.recv(1024)  # 接收数据
#         print("received:", data)
#         if not data:
#             print("client has lost")
#             break
#
#         conn.send(data)  # 返回数据
#         print("send back:", data)
#
# serve.close()  # 关闭socket
