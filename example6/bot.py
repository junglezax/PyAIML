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
        self.currentSessionId = self.k._globalSessionID
        
    def login(self, username):
        userList = self.db.keys()
        self.currentSessionId = username
        
        if username not in userList:
            userList.append(username)
            self.k._addSession(username)

    def run(self):
        while True:
            t = raw_input("> ")
            if t == 'bye':
                break
            else:
                t = t.decode('gbk')
                print self.k.respond(t, self.currentSessionId).decode('utf-8')
                self.db.sync()
