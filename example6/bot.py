#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiml
import json
import shelve
import os

class Bot:
    def __init__(self, sessionStore=None):
        self.db = shelve.open("session.db", "c", writeback=True)
        self.k = aiml.Kernel(sessionStore=self.db)
        self.k.learn("cn-startup.xml")
        print self.k._brain._root.keys()
        self.k.respond("load aiml cn")
        print self.k._brain._root.keys()
        
    def login(self, username):
        userList = self.db.keys()
        self.currentSessionId = username
        
        if username not in userList:
            userList.append(username)
            self.k._addSession(username)
            
    def say(self, s, sessionId):
        r = self.k.respond(s, sessionId).decode('utf-8')
        self.db.sync()
        return r

    def run(self):
        while True:
            t = raw_input("> ")
            if t == 'bye':
                break
            else:
                t = t.decode('gbk')
                self.db.sync()
