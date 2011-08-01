#!/usr/bin/env python
# encoding: utf-8
"""
group.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from component import GroupComp, WeiboComp, AlbumComp, TopicComp, EventComp, OperateComp
from common import BaseHandler

class Group(object):
    def __init__(self, api=GroupComp, weibo=WeiboComp, album=AlbumComp, topic=TopicComp, event=EventComp, operate=OperateComp):
        self._api=api
        self._weibo=weibo
        self._album=album
        self._topic=topic
        self._event=event
        self._operate=operate


class GroupHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/main.html")

class GroupTopicHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/topic.html")

class GroupMemberHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/member.html")

class GroupEditHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/edit.html")

class GroupEventHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/event.html")

class GroupAlbumHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/album.html")

class GroupWeiboHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/weibo.html")

class GroupLikeHandler(BaseHandler):
    def get(self, uadd):
        self.render("group/like.html")
