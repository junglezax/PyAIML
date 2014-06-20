#coding:utf-8

import socket
import datetime
import threading
import sys
import os
import signal
import time

pid = os.getpid()

HOST = "localhost"  #服务其地址
PORT = 9011       #服务器端口
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
TCPClient = None
TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClient.connect(ADDR) #连接服务器

sessionId = 'zs' #sys.argv[1]
LOGIN_FLAG = 'LOGIN '

def close():
    print "client close"
    TCPClient.close()
    #sys.exit(0) # not work
    os.kill(pid, signal.SIGTERM)

class BotClientWriter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        TCPClient.send(LOGIN_FLAG + sessionId)
        time.sleep(0.1)
        
        while True:
            try:
                senddata = raw_input("input:")
            except: # KeyboardInterrupt, EOFError
                close()

            if senddata:
                try:
                    TCPClient.send('%s' % (senddata))  #发送数据
                except:
                    close()
            time.sleep(0.1) 
 
class BotClientReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                recvdata = TCPClient.recv(BUFFERSIZE)    #接受数据
            except:
                close()
            curTime = datetime.datetime.now()  #获得当前时间 格式是：datetime.datetime(2012, 3, 13, 1, 29, 51, 872000)
            curTime = curTime.strftime('%Y-%m-%m %H:%M:%S')     #转换格式
            recvdata = recvdata.decode('utf-8')
            print "%s  %s" % (HOST, curTime), recvdata
            if recvdata == '88':
                close()

w = BotClientWriter()
r = BotClientReader()
w.start()
r.start()
