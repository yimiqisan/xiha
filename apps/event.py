#!/usr/bin/env python
# encoding: utf-8
"""
event.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from BeautifulSoup import BeautifulSoup
import cStringIO

from component import EventComp, WeiboComp, AlbumComp, TopicComp
from common import BaseHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.web import asynchronous

class Event(object):
    def __init__(self, api=EventComp, weibo=WeiboComp, album=AlbumComp, topic=TopicComp):
        self._api=api
        self._weibo=weibo
        self._album=album

class EventListHandler(BaseHandler):
    def get(self):
        self.render("event/list.html", **{'data':''})
    
    @asynchronous
    def post(self):
        html = self.get_argument("site", None)
        http = AsyncHTTPClient()
        http.fetch(html, callback=self.async_callback(self.do_html))
        
    def do_html(self, response):
        soup = BeautifulSoup(cStringIO.StringIO(response.body))
        data = soup.findAll(attrs={'class':'acv_dl03single'})
        d = data[0].findAllNext(text=True)
        self.render("event/list.html", **{'data':data})

class EventHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/main.html")

class EventTopicHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/main.html")

class EventMemberHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/member.html")

class EventAlbumHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/album.html")

class EventRouteHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/route.html")

class EventWeiboHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/weibo.html")

class EventInsureHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/insure.html")

class EventSupportHandler(BaseHandler):
    def get(self, uadd):
        self.render("event/support.html")
