#coding:utf-8

import socket
import datetime
import threading
import sys
import os
import signal
import time
import argparse
import platform

pid = os.getpid()

sessionId = '_global'
HOST = "localhost"
PORT = 9011
ADDR = (HOST, PORT)
BUFFERSIZE = 1024

encoding = 'utf-8'
LOGIN_FLAG = 'LOGIN '

parser = argparse.ArgumentParser(description='Bot Client')
parser.add_argument('--host', 
                    default="localhost",
                   help='host name')
parser.add_argument('--port', type=int,
                   default=9011,
                   help='port')
parser.add_argument('-l',
                   default='_global',
                   help='username')

args = parser.parse_args()

sessionId = args.l
HOST = args.host
PORT = args.port

TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClient.connect(ADDR)

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
            
            if platform.system() == 'Windows':
                senddata = senddata.decode('gbk')
            senddata = senddata.encode('utf-8')
            
            if senddata:
                try:
                    TCPClient.send(senddata)
                except:
                    close()
            time.sleep(0.1) 
 
class BotClientReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                recvdata = TCPClient.recv(BUFFERSIZE)
            except:
                close()
            #curTime = datetime.datetime.now()
            #curTime = curTime.strftime('%Y-%m-%m %H:%M:%S')
            recvdata = recvdata.decode(encoding)
            print recvdata
            if recvdata == '88':
                close()

w = BotClientWriter()
r = BotClientReader()
w.start()
r.start()
