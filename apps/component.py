#!/usr/bin/env python
# encoding: utf-8
"""
component.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import API
from xiha.configure import DB_CON, DB_NAME
from modules import TopicDoc, AlbumDoc, TimelineDoc

class TopicComp(API):
    ''' for topic '''
    def __init__(self, id=None):
        DB_CON.register([TopicDoc])
        datastroe = DB_CON[DB_NAME]
        col_name = TopicDoc.__collection__
        collection = datastroe[col_name]
        doc = collection.TopicDoc()
        API.__init__(self, id=id, col_name=col_name, collection=collection, doc=doc)
        

class AlbumComp(API):
    pass

class TimelineComp(API):
    ''' for weibo '''
    def __init__(self, uid, eid, stamp):
        self.uid = uid
        self.eid = eid
        self.stamp = stamp
        DB_CON.register([TimelineDoc])
        self.datastroe = DB_CON[DB_NAME]
        col_name = stamp+'timeline'
        collection = self.datastroe[col_name]
        doc = collection.TimelineDoc()
        API.__init__(self, id=None, col_name=col_name, collection=collection, doc=doc)
    
    def create(self, **kwargs):
        kwargs.update({'eid':self.eid,'stamp':self.stamp})
        for k, v in kwargs.items():
            if k=="added":
                return(False, 'added key not allowed!')
            elif (k=="counter")and(type(v)==type(0)):
                self.incr(k, v)
            elif k=="stacker":
                self.push(k, v)
            elif k in self.doc.structure.keys():
                self.doc[k]=v
            else:
                self.doc['added'][k] = v
        try:
            self.doc.save(uuid=True, validate=True)
        except Exception, e:
            logging.info(e)
            return (False, unicode(e))
        return (True, None)
    
    def merge(self, timelines=[]):
        ''' make multi timeline together '''
        pass

class WeiboComp(object):
    ''' for weibo '''
    STAMP_LIST = [u'origin',u'reply',u'report',u'attention',u'retweet']
    def __init__(self, own=None):
        self.own = own
        self.id = self.own._id# if own and hasattr(own, '_id') else None
    
    def _instance(self, stamp, eid=None):
        if (stamp==u'origin'):eid = self.id
        return TimelineComp(self.id, eid, unicode(stamp)) if (stamp in self.STAMP_LIST) else None
    
    def get(self, stamp, **kwargs):
        if self.id:kwargs['uid']=self.id 
        tl = self._instance(stamp, eid=None)
        return tl.find(**kwargs) if tl else None
    
    def page(self, stamp, **kwargs):
        tl = self._instance(stamp, eid=None)
        return tl.page(**kwargs) if tl else None
    
    def remove(self, stamp, id):
        tl = self._instance(stamp)
        tl.remove(id)
    
    def origin(self, text):
        tl = self._instance(u'origin', eid=None)
        content = {'text':text}
        if tl:tl.create(uid=self.id, content=content)
    
    def reply(self, eid, text):
        tl = self._instance(u'reply', eid=eid)
        if tl:tl.create(author=self.own, text=text)
    
    def report(self, eid, text):
        tl = self._instance(u'report', eid=eid)
        if tl:tl.create(author=self.own, text=text)
    
    def attention(self, eid):
        tl = self._instance(u'attention', eid=eid)
        if tl:tl.create(author=self.own)
    
    def check(self, eid):
        tl = self._instance(u'check', eid=eid)
        if tl:tl.create(author=self.own)
    
    def retweet(self, eid, text):
        tl = self._instance(u'retweet', eid=eid)
        if tl:tl.create(author=self.own, text=text)

class EventComp(API):
    pass
    
class GroupComp(API):
    pass
    
class MarketComp(API):
    pass

class AppComp(API):
    pass

class OperateComp(object):
    def __init__(self, own=None):
        self.own = own
        self.id = self.own['_id'] if (not own) and hasattr(own, '_id') else None
    
    def like(self, eid, text):
        tl = TimelineComp(self.id, eid, 'like')
        tl.push(author=self.own, text=text)
        
    def hate(self, eid, text):
        tl = TimelineComp(self.id, eid, 'hate')
        tl.push(author=self.own, text=text)
        
    def store(self, eid):
        tl = TimelineComp(self.id, eid, 'store')
        tl.push(author=self.own)

