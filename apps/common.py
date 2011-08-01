#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-05-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
from tornado.web import RequestHandler

from xiha.configure import DB_CON
from tools import session


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return DB_CON
        
    @property
    def cache(self):
        return self.settings["cache_engine"]
        
    def filter_args(self):
        args = self.request.arguments
        if args.has_key('_xsrf'):args.pop('_xsrf')
        for k in args.keys():
            if isinstance(args[k], list) and (len(args[k])==1):
                args[k] = args[k][0]
        return args
        
    def get_current_user(self):
        return self.get_secure_cookie("user")
        
    def render(self, template_name, **kwargs):
        if 'warning' not in kwargs.keys():
            kwargs['warning'] = None
        super(BaseHandler, self).render(template_name, **kwargs)
        
    @session
    def skip_page(self):
        goto = self.SESSION['goto']
        if goto:
            del self.SESSION['goto']
        else:
            goto = '/'
        return self.redirect(goto)
    
    @session
    def set_goto(self):
        goto = self.get_argument('goto', None)
        if (not goto) and (goto!=self.request.uri):
            self.SESSION['goto'] = goto

class RootHandler(BaseHandler):
    @session
    def get(self):
        self.render("index.html")
        
class SearchHandler(BaseHandler):
    @session
    def get(self):
        self.render("search.html")
    
class TestHandler(BaseHandler):
    @session
    def get(self, page):
        html = page+".html"
        self.render(html)

class Error404Handler(BaseHandler):
    def get(self):
        self.render("error/404.html")