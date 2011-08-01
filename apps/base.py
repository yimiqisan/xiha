#!/usr/bin/env python
# encoding: utf-8
"""
base.py

Created by 刘 智勇 on 2011-05-30.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from datetime import datetime
import logging

from xiha.configure import DB_CON, DB_NAME
from modules import ComponentDoc, TimelineDoc

class Component(object):
    def __init__(self, app_id=None, need_owner=False, **config):
        self.app_id = app_id
        self.need_owner = need_owner
        DB_CON.register([ComponentDoc])
        self.datastroe = DB_CON[DB_NAME]
        self.col_name = ComponentDoc.__collection__
        self.col = self.datastroe[self.col_name]
        self._init_config(**config)
        self.initialize()
    
    def initialize(self):
        ''' init type component overload it to build new component '''
        pass
        
    @property
    def config(self):
        """A config."""
        if not hasattr(self, "__config"):
            self.__config = {}
        return self.__config
        
    @config.setter
    def config(self, key, value):
        self.__config[key] = value
    
    @config.deleter
    def config(self, key):
        if self.__config.has_key(key):
            del self.__config[key]
    
    def _init_config(self, **config):
        try:
            ret = self.col.one({'app_id': self.app_id, 'uid': self.uid})
        except:
            return (False, 'init config failure')
        if ret is None:
            self.__config = config
        else:
            self.__config = ret.get('config', {})
            self.__config.update(config)
        return (True, 'ok')
    
    def comp_save(self):
        comp = self.col.ComponentDoc()
        try:
            self.col.one({'app_id': self.app_id, 'uid': self.uid})
        except:
            return False
        comp.app_id = self.app_id
        comp.need_owner = self.need_owner
        comp.uid = self.uid
        comp.config = self.config
        return comp.save()
        
class Timeline(Component):
    _CONFIGURE = {}
    
    def __init__(self, app_id, uid, eid, stamp):
        self.app_id = app_id
        self.uid = uid
        self.eid = eid
        self.stamp = stamp
        DB_CON.register([TimelineDoc])
        self.datastroe = DB_CON[DB_NAME]
        self.col_t_name = stamp+'timeline'
        self.col_t = self.datastroe[self.col_t_name]
        Component.__init__(self, app_id=app_id, need_owner=False, **self._CONFIGURE)
    
    def _check_content_type(self, value_dict):
        for v in value_dict.keys():
            if v not in self._CONTENT_TYPE:
                msg = v+' is not in _CONTENT_TYPE!'
                return (False, msg)
        return (True, 'ok')
    
    def merge(self, timelines=[]):
        ''' make multi timeline together '''
        pass
    
    def push(self, *args, **kwargs):
        value = dict(args)
        value.update(kwargs)
        author = value.pop('author')
        ret = self._check_content_type(value)
        if not ret[0]:
            return ret
        tl = self.col_t.TimelineDoc()
        tl.uid = self.uid
        tl.author = author
        tl.eid = self.eid
        if 'mark' in value.keys():
            tl.mark = value.pop('mark')
        tl.stamp = self.stamp
        tl.content = value
        tl.lzy = 'shuai'
        tl.save(uuid=True, validate=True)
    
    def pop(self, num):
        pass
    
    def remove(self, id):
        return self.col_t.remove(id)
    
    def get(self, *args, **kwargs):
        condition = dict(args)
        condition.update(kwargs)
        condition.update({'uid':self.uid})
        return self.col_t.find(condition).sort('created', -1)
    
    def count(self, *arg, **kwargs):
        tl = self.col_t.TimelineDoc()
        return tl.count(*arg, **kwargs)
    
    def incr(self, key, num):
        pass
    
    def decr(self, key, num):
        pass
    
    def drop(self):
        self.col_t.drop()
    
if __name__ == '__main__':
    test_app_id = u'8f452f2f24c243498dfc24f4df431ca1'
    orgTimeLine = Timeline(test_app_id, u'liuzhiyong', u'liuzhiyong', u'test')
    orgTimeLine.push(name='lzy', age='26', height='173cm')
    print orgTimeLine.get()
    
    
    
    
    
    