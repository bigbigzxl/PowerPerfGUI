# server.py
import socket
import time

# create a socket object
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#time.ctime(time.time()) + "\r\n"
    print("return:", currentTime)
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()



# import socket
#
#
# print socket.gethostname()
# try:
#     sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
#     print("create socket succ!")
#
#     sock.bind(('192.168.171.2',8080))
#     print('bind socket succ!')
#
#     sock.listen(5)
#     print('listen succ!')
#
# except:
#     print("init socket error!")
#
# while True:
#     print("listen for client...")
#     conn,addr=sock.accept()
#     print("get client")
#     print(addr)
#
#     conn.settimeout(30)
#     szBuf=conn.recv(1024)
#     print("recv:"+str(szBuf,'utf-8'))
#
#     if "0"==szBuf:
#         conn.send(b"exit")
#     else:
#         conn.send(b"welcome client")
#
#     conn.close()
#     print("end of servive")


# import socket
# import sys
# HOSTNAME = 'localhost'
# PORT = 5037
# TIMEOUT = 15
# OKAY = 'OKAY'
# FAIL = 'FAIL'
# DEBUG = 1
#
#
# class AdbClient:
#     def __init__(self, hostname=HOSTNAME, port=PORT):
#         if DEBUG:
#             print "\t__init__."
#         self.hostname = hostname
#         self.port = port
#         self.reconnect = False
#         self._connect()
#         # self.checkVersion(True)
#
#     def _connect(self):
#         if DEBUG:
#             print "\t_connect()"
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.settimeout(TIMEOUT)
#         try:
#             self.socket.connect((self.hostname, self.port))
#         except socket.error, ex:
#             raise RuntimeError(
#                 "ERROR: Connecting to %s:%d: %s.\nIs adb running on your computer?" % (self.socket, self.port, ex))
#         if DEBUG:
#             print "\t\t_connect success."
#
#     def _send(self, msg, checkok, reconnect):
#         if DEBUG:
#             print "\t_send(%s, checkok=%s, reconnect=%s)" % (msg, checkok, reconnect)
#         self.checkConnected()
#         b = bytearray(msg, 'utf-8')
#         self.socket.send('%04X%s' % (len(b), b))
#         if checkok:
#             self._checkOk()
#         if reconnect:
#             if DEBUG:
#                 print "\t\t__send: reconnecting"
#             self._connect()
#
#     def _receive(self, nob=None):
#         if DEBUG:
#             print "\t_receive()"
#         self.checkConnected()
#         if nob is None:
#             nob = int(self.socket.recv(4), 16)
#         if DEBUG:
#             print "\t\t__receive: receiving", nob, "bytes"
#         recv = bytearray()
#         nr = 0
#         while nr < nob:
#             chunk = self.socket.recv(min((nob - nr), 4096))
#             recv.extend(chunk)
#             nr += len(chunk)
#         if DEBUG:
#             print "\t\t__receive: returning len=", len(recv)
#         return str(recv)
#
#     def _checkOk(self):
#         if DEBUG:
#             print "\t_checkOk()"
#         self.checkConnected()
#         recv = self.socket.recv(4)
#         if DEBUG:
#             print "\t\t_checkOk: recv=", repr(recv)
#         try:
#             if recv != OKAY:
#                 error = self.socket.recv(1024)
#                 raise RuntimeError("ERROR: %s %s" % (repr(recv), error))
#         finally:
#             if DEBUG:
#                 print "\t\t_checkOk() return True"
#             return True
#
#     def setReconnect(self, val):
#         self.reconnect = val
#
#     def close(self):
#         print "close()"
#         if self.socket:
#             self.socket.close()
#
#     def checkConnected(self):
#         if DEBUG:
#             print "checkConnected()"
#         if not self.socket:
#             raise RuntimeError("ERROR: Not connected")
#         if DEBUG:
#             print "\tcheckConnected: returning True"
#         return True
#
#     def checkVersion(self, reconnect):
#         if DEBUG:
#             print "checkVersion(reconnect=%s)" % reconnect
#         self._send('host:version', checkok=True, reconnect=False)
#         version = self.socket.recv(8)
#         if DEBUG:
#             print "\t\tcheckVersion: recv=", repr(version)
#         VERSION = '0004001f'
#         if version != VERSION:
#             raise RuntimeError("ERROR: Incorrect ADB server version %s (expecting %s)" % (version, VERSION))
#
#     def resetDevice(self, name):
#         if DEBUG:
#             print  "resetDevice()"
#         self._send('host:devices-l', checkok=False, reconnect=True)
#         self._send('host:transport:%s' % name, True, False)
#
#     def getDevices(self):
#         if DEBUG:
#             print  "getDevices()"
#         self._send('host:devices-l', checkok=False, reconnect=True)
#
#         ###
#         # fixme:for select device
#         self._send('host:transport:YT9109B4UV', True, False)
#         device = Device()
#         device.index = 0
#         device.name = "YT9109B4UV"
#         device.adbc = self
#         return device
#
#
# class Device:
#     index = 0
#     name = ""
#     adbc = AdbClient()
#
#     def getIndex(self):
#         return self.mIndex
#
#     def shell(self, cmd=None):
#         if DEBUG:
#             print "shell(cmd:%s)" % cmd
#         self.adbc.resetDevice(self.name)
#         if cmd:
#             self.adbc._send('shell:%s' % cmd, checkok=True, reconnect=False)
#             out = ''
#             while True:
#                 _str = None
#                 try:
#                     _str = self.adbc.socket.recv(4096)
#                 except Exception, ex:
#                     print >> sys.stderr, "ERROR:", ex
#                 if not _str:
#                     break
#                 out += _str
#             if self.adbc.reconnect:
#                 print >> sys.stderr, "Reconnecting..."
#                 self.adbc.close()
#                 self.adbc._connect()
#             return out
#         else:
#             self.adbc._send('shell:', checkok=True, reconnect=False)
#             # sin = self.socket.makefile("rw")
#             # sout = self.socket.makefile("r")
#             # return (sin, sin)
#             sout = self.adbc.socket.makefile("r")
#             return sout
#
#
# if __name__ == '__main__':
#     adbClient = AdbClient()
#
#     device = adbClient.getDevices()
#     # device.shell('input text aa')
#
#     # device.shell("sendevent /dev/input/event8 0003 57 00000295");
#     # device.shell("sendevent /dev/input/event8 0003 53 00000013");
#     # device.shell("sendevent /dev/input/event8 0003 58 0000002b");
#     # device.shell("sendevent /dev/input/event8 0000 0000 00000000");
#     # device.shell("sendevent /dev/input/event8 0003 57 ffffffff");
#     # device.shell("sendevent /dev/input/event8 0000 0000 00000000");
#
#     adbClient.close()
