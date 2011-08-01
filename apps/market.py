#!/usr/bin/env python
# encoding: utf-8
"""
market.py

Created by 刘 智勇 on 2011-06-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from common import BaseHandler

class MarketHandler(BaseHandler):
    def get(self, uadd):
        self.render("market/main.html")

class MarketTaobaoHandler(BaseHandler):
    def get(self, uadd):
        self.render("market/taobao.html")

class MarketUsedHandler(BaseHandler):
    def get(self, uadd):
        self.render("market/used.html")

class MarketLeaseHandler(BaseHandler):
    def get(self, uadd):
        self.render("market/lease.html")

class MarketRegieHandler(BaseHandler):
    def get(self, uadd):
        self.render("market/regie.html")
