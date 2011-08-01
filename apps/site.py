#!/usr/bin/env python
# encoding: utf-8
"""
sitemap.py

Created by 刘 智勇 on 2011-06-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from common import BaseHandler

class SiteMapHandler(BaseHandler):
    def get(self):
        self.render("sitemap.html")
        
class SiteNaviHandler(BaseHandler):
    def get(self):
        self.render("navigation.html")

class SiteJoinHandler(BaseHandler):
    def get(self):
        self.render("joinus.html")

class SiteHeartHandler(BaseHandler):
    def get(self):
        self.render("myheart.html")
