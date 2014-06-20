# Filename: BotServer.py
# @author: nullspace
# Created on 2014-06-20
import threading
import socket
import os
import signal
import sys

from bot import Bot

pid = os.getpid()

LOGIN_FLAG = 'LOGIN '

encoding = 'gbk' #'utf-8'
BUFSIZE = 1024

def onsignal_term(a,b):
    print 'SIGTERM recved'
    os.kill(pid, signal.SIGTERM)
signal.signal(signal.SIGTERM, onsignal_term)

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client, listener, cid):
        threading.Thread.__init__(self)
        self.client = client
        self.listener = listener
        self.cid = cid
        self.sessionId = "";
        
    def login(self, sessionId):
        print sessionId, ' logging in'
        self.sessionId = str(sessionId);

    def run(self):
        while True:
            try:
                data = self.client.recv(BUFSIZE)
            except:
                break
            if(data):
                string = bytes.decode(data, encoding)
                print string
                
                if string == '88':
                    self.client.send('88')
                    break
                elif string == 'shutdown':
                    self.listener.shutdown()
                    break
                elif string[:len(LOGIN_FLAG)] == LOGIN_FLAG:
                    self.login(string[len(LOGIN_FLAG):])
                    continue

                string = self.listener.bot.say(string, self.sessionId)
                try:
                    s1 = string.encode('utf-8')
                    self.client.send(s1)
                except Exception, msg:
                    print msg
            else:
                break

        self.listener.close(self.cid)
        print("close:", self.client.getpeername())

    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string)>2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string

class Listener(threading.Thread):
    def __init__(self, port, bot):
        threading.Thread.__init__(self)
        
        self.bot = bot
        
        self.clients = {}
        self.threads = {}
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)

    def run(self):
        print("listener started")
        try:
            while True:
                client, cltadd = self.sock.accept()
                
                cid = len(self.clients)+1
                self.clients[cid] = client
                
                r = Reader(client, self, cid)
                self.threads[cid] = r
                r.setDaemon(True)
                r.start()
                print "accept a connect from ", cltadd

            alive = False
            for r in self.threads.values():
                alive = alive or r.isAlive()
            if not alive:
                sys.exit(0)
        except KeyboardInterrupt, e:
            print 'KeyboardInterrupt'

    def shutdown(self):
        for clt in self.clients.values():
            try:
                clt.send('88')
            except:
                pass
        os.kill(pid, signal.SIGTERM)
        #sys.exit(0) # not work
        
    def close(self, cid):
        self.clients.pop(cid)
        self.threads.pop(cid)

bot = Bot()
lst  = Listener(9011, bot)   # create a listen thread
lst.start() # then start
