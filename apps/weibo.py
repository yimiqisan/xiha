#!/usr/bin/env python
# encoding: utf-8
"""
weibo.py

Created by 刘 智勇 on 2011-06-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from common import BaseHandler
from user import User
from tools import session
from component import WeiboComp, OperateComp

class Weibo(WeiboComp):
    def __init__(self, uid=None, operate=None):
        self._operate = operate if operate else OperateComp()
        u = User()
        u.whois('_id', uid)
        super(Weibo, self).__init__(u)

class WeiboStyleHandler(BaseHandler):
    @session
    def get(self, uadd):
        uid = self.SESSION['uid']
        u = User()
        u.whois('added_id', unicode(uadd))
        whoid = u.uid
        wb = Weibo(uid=whoid)
        tp = self.get_argument('tp', None)
        if tp == 'del':
            id = self.get_argument('tpid')
            stamp = self.get_argument('stamp', u'origin')
            wb.remove(stamp, id)
        msg_l = wb.get(u'origin')
        ml = []
        for m in msg_l:
            u.whois('_id', m['uid'])
            m['author'] = u
            ml.append(m)
        self.render("weibo/weibo.html", **{"msg_l": ml, "att": False})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        wb = Weibo(uid=uid)
        text = self.get_argument('utimeline', None)
        wb.origin(text=text)
        self.redirect("/weibo/uid/style/")

class WeiboDynamicHandler(BaseHandler):
    def get(self, uadd):
        self.render("weibo/weibo.html")

class WeiboFollowHandler(BaseHandler):
    def get(self, uadd):
        self.render("weibo/follow.html")

class WeiboFansHandler(BaseHandler):
    def get(self, uadd):
        self.render("weibo/fans.html")

class WeiboProfileHandler(BaseHandler):
    def get(self, uadd):
        self.render("weibo/profile.html")

class WeiboFriendsHandler(BaseHandler):
    def get(self, uadd):
        self.render("weibo/friends.html")

class WeiboEditHandler(BaseHandler):
    def get(self, uadd):
        self.render("weibo/edit.html")

class WeiboEditStatusHandler(BaseHandler):
    @session
    def get(self, uadd):
        uid = self.SESSION['uid']
        u = User()
        u.whois('_id', uid)
        self.render("weibo/edit_status.html", **{'to_sina':True})

class WeiboEditSyncHandler(BaseHandler):
    @session
    def get(self, uadd):
        uid = self.SESSION['uid']
        u = User()
        u.whois('_id', uid)
        self.render("weibo/edit_sync.html", **{'is_auth':u.sina_id})
        


