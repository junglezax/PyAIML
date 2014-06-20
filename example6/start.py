#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")
from bot import Bot

bot = Bot()

bot.k.learn("cn-startup.xml")

bot.k.respond("load aiml cn")

bot.login('zs')

bot.run()
