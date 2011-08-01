#!/usr/bin/env python
# encoding: utf-8
"""
application.py

Created by 刘 智勇 on 2011-06-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from common import BaseHandler

class AppHandler(BaseHandler):
    def get(self):
        self.render(".html")

class AppFansHandler(BaseHandler):
    def get(self):
        self.render(".html")

class AppTopicHandler(BaseHandler):
    def get(self):
        self.render(".html")

class AppWeiboHandler(BaseHandler):
    def get(self):
        self.render(".html")
