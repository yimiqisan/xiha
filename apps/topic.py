#!/usr/bin/env python
# encoding: utf-8
"""
topic.py

Created by 刘 智勇 on 2011-06-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado.web import asynchronous
from tornado.escape import json_encode
from tornado.httpclient import AsyncHTTPClient

import feedparser
import json
from datetime import datetime
import time
import cStringIO
from hashlib import md5
import pickle
import re
import logging

from common import BaseHandler
from component import TopicComp, OperateComp, TimelineComp
from tools import session, _unicode
from out import rss_feed


class Topic(object):
    def __init__(self, api=None, operate=None):
        self._api = api if api else TopicComp()
        self._operate = operate if operate else OperateComp()


class TopicHandler(BaseHandler):
    def get(self, uadd):
        self.render("topic/main.html")

class TopicNewHandler(BaseHandler):
    def get(self, uadd):
        self.render("topic/main.html")

class TopicEditHandler(BaseHandler):
    def get(self, uadd):
        self.render("topic/main.html")

class TopicDeleteHandler(BaseHandler):
    def get(self, uadd):
        self.render("topic/main.html")

class TopicReplyHandler(BaseHandler):
    def get(self, uadd):
        self.render("topic/main.html")

class TopicRSSHandler(BaseHandler):
    def get(self, uadd):
        data = []
        self.render("topic/rss.html", **{'output':{}})
    
    @asynchronous
    def post(self):
        feed = self.get_argument("feed", None)
        self.feed = feed.replace('feed://','http://') if feed else None
        cacheKey = self.getCacheKey()
        output = None#self.cache.get(cacheKey)
        if output is None:
            http = AsyncHTTPClient()
            http.fetch(self.feed, callback=self.async_callback(self.printJSONP))
        else:
            data = pickle.loads(output)
            self.render("topic/rss.html", **{'output':data})
            self.finish()
    
    def printJSONP(self, response):
        success = False
        try :
            output = self.parseFeed(cStringIO.StringIO(response.body))
            success = True
        except Exception, error:
            print error
            output = {}
            output["error"] = {};
            output["error"]["code"] = error[0];
            output["error"]["message"] = error[1]
        if success:
            cacheKey = self.getCacheKey()
            data = pickle.dumps(output)
            self.cache.set(cacheKey, data)
            #self.save_feed(output)
            self.render("topic/rss.html", **{'output': output})
        else:
            self.render("topic/rss.html", **{'warning': output["error"]["message"], 'output':{}})
        self.finish()
    
    def parseFeed(self, feedContent):
        if feedContent == None:
            raise Exception('1', "Not valid Feed" ) 
        fetchedData = feedparser.parse(feedContent)
        if fetchedData.bozo == 1:
            raise Exception('2', "Malformatted feed" ) 
        items = []
        cover = fetchedData['feed']
        print cover
        for entry in fetchedData['entries']:
            item = {}
            item["title"] = entry.title
            item["link"]  = entry.link
            item["description"] = None #will be popuplated below
            item["date"] = None #will be populated below
            try: #for rss feeds
                item["description"] = entry.description
            except: #for atom feeds
                item["description"] = entry.summary
            try: #for rss
                item["date"] = int(time.mktime(entry.date_parsed))
            except: #for atom
                item["date"] = int(time.mktime(entry.updated_parsed))
            items.append(item)

        return {'info': items, 'cover':cover}
    
    def get_img(self, src):
        src = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", src)
        src = _unicode(src)
        src = src.strip()
        c=re.compile(r"<img(.*?)>+?")
        try:
            m = c.search(src)
            img = m.group()
        except Exception, e:
            print e
        l = img.split()
        for i in l:
            if i.startswith(r"src="):
                return i[4:]
        return None
    
    def getCacheKey(self):
        urlWithTime = self.feed + datetime.strftime(datetime.now(), "%Y-%m-%d-%H")
        return md5(urlWithTime).hexdigest()
    
    def getFeed(self, data):
        if isinstance(data, str) or isinstance(data, unicode):
            data = [(data, '')]
        for feed in data:
            cacheKey = self.getCacheKey()
            output = self.cache.get(cacheKey)
            if output is None:
                http = AsyncHTTPClient()
                http.fetch(feed[0], callback=self.async_callback(self.printJSONP))
            else:
                data = pickle.loads(output)
                self.render("topic/rss.html", **{'output':data})
                self.finish()
    
    def save_feed(self, output):
        cover = output['cover']
        self.save_cover(**cover)
        #self.save_info(output['info'], output['cover']['link'])
    
    @session
    def save_cover(self, **c):
        uid = self.SESSION['uid']
        t = Topic()
        d = {}
        d['title'] = c.pop('title')
        d['owner'] = uid
        d['content'] = {'subtitle':c.pop('subtitle')}
        d['from'] = unicode(c.pop('links'))
        d['mtype'] = u'rss'
        d['stype'] = c.pop('link')
        #d['updated_parsed'] = datetime.strftime(c.pop('updated_parsed'), '%Y-%m-%d %X')
        c.pop('updated_parsed')
        d.update(c)
        t._api.create(**d)
    
    @session
    def save_info(self, info_l, link):
        uid = self.SESSION['uid']
        tl = TimelineComp(uid, link, u'rss')
        for i in info_l:
            tl.create(author=self.own, title=i['title'], description=i['description'], link=i['link'])





'''
{'updated': u'Wed, 29 Jun 2011 15:46:32 +0800', 
'subtitle': u'\u5173\u6ce8\u4e92\u8054\u7f51\u548c\u641c\u7d22\u5f15\u64ce\u7684\u79d1\u6280\u535a\u5ba2', 
'language': u'zh-CN', 
'links': [
    {'href': u'http://feed.williamlong.info/', 'type': u'application/rss+xml', 'rel': u'self'}, 
    {'href': u'http://www.williamlong.info/', 'type': u'text/html', 'rel': u'alternate'}
    ], 
'title': u'\u6708\u5149\u535a\u5ba2', 
'image': {
    'title_detail': {'base': u'', 'type': u'text/plain', 'value': u'\u6708\u5149\u535a\u5ba2', 'language': None}, 
    'href': u'http://feed.williamlong.info/subscribers_count.png?wbgc=D2D2D2&nbgc=eaeaea&bc=AAAAAA&wc=424242&nc=424242&bgc=2f699a', 
    'link': u'http://www.williamlong.info/', 
    'links': [{'href': u'http://www.williamlong.info/', 'type': u'text/html', 'rel': u'alternate'}], 
    'title': u'\u6708\u5149\u535a\u5ba2'
    }, 
'rights': u'This site is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 2.5 License.', 
'subtitle_detail': {
    'base': u'', 
    'type': u'text/html', 
    'value': u'\u5173\u6ce8\u4e92\u8054\u7f51\u548c\u641c\u7d22\u5f15\u64ce\u7684\u79d1\u6280\u535a\u5ba2', 
    'language': None
    }, 
'title_detail': {'base': u'', 'type': u'text/plain', 'value': u'\u6708\u5149\u535a\u5ba2', 'language': None}, 
'link': u'http://www.williamlong.info/', 
'rights_detail': {
    'base': u'', 
    'type': u'text/plain', 
    'value': u'This site is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 2.5 License.', 
    'language': None
    }, 
'updated_parsed': time.struct_time(tm_year=2011, tm_mon=6, tm_mday=29, tm_hour=7, tm_min=46, tm_sec=32, tm_wday=2, tm_yday=180, tm_isdst=0)}
'''



{'Content-Length': '2259', 
'Via': '1.0 squid.i-soft.com.cn:3128 (squid/2.6.STABLE21)', 'X-Cache': 'MISS from squid.feedsky.com,HIT from squid.i-soft.com.cn', 'X-Powered-By': 'PHP/5.2.0', 'X-Cache-Lookup': 'MISS from squid.feedsky.com:80,HIT from squid.i-soft.com.cn:3128', 'Expires': 'Thu, 07 Jul 2011 06:24:01 GMT', 'Vary': 'Accept-Encoding', 'Server': 'Apache/2.2.3 (Unix) PHP/5.2.0', 'Last-Modified': 'Thu, 07 Jul 2011 02:46:30 GMT', 'Connection': 'close', 'Etag': '"1911aeaa5210eb12fe135442b72d8a89"', 'Cache-Control': 'max-age=600', 'Date': 'Thu, 07 Jul 2011 06:14:01 GMT', 'Content-Type': 'application/xml; charset=utf-8', 'Content-Encoding': 'gzip'}
{'Wp-Super-Cache': 'Served legacy cache file', 
'Via': '1.0 squid.i-soft.com.cn:3128 (squid/2.6.STABLE21)', 'X-Cache': 'MISS from squid.i-soft.com.cn', 'X-Cache-Lookup': 'HIT from squid.i-soft.com.cn:3128', 'Vary': 'Accept-Encoding,Cookie', 'Server': 'nginx', 'Connection': 'close', 'Etag': '"87da4041a7ee70963d9bf376cc06ddd6"', 'Date': 'Thu, 07 Jul 2011 06:55:31 GMT', 'Content-Type': 'text/xml; charset=UTF-8', 'X-Pingback': 'http://apple4.us/wordpress/xmlrpc.php'}



















