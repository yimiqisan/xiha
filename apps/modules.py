#!/usr/bin/env python
# encoding: utf-8
"""
document.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from datetime import datetime
import logging
import re

from mongokit import Document, IS
from xiha.configure import DB_CON, DB_NAME

class IdDoc(Document):
    __collection__ = 'ids'
    __database__ = DB_NAME

    structure = {
                '_id':unicode,
                'id':int,
    }
    use_schemaless = True
    use_dot_notation=True


class UserDoc(Document):
    __collection__ = 'people'
    __database__ = DB_NAME

    structure = {
            'email':unicode,
            'nick': unicode,
            'passwd':unicode,
            'created':datetime,
            'uid':unicode,
            'sina_id':unicode,
            'added':dict,
            'added_id':unicode,
            'counter':{unicode:int},
            'stacker':{unicode:list},
    }
    required_fields = ['created']
    default_values = {'created':datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True
    

class TopicDoc(Document):
    __collection__ = 'topic'
    __database__ = DB_NAME

    structure = {
            'title':unicode,
            'owner': unicode,
            'content':dict,
            'created':datetime,
            'from':unicode,
            'mtype':IS(u'note', u'vote', u'test', u'zhidao', u'rss'),
            'stype':unicode,
            'added':dict,
            'added_id':unicode,
            'counter':{unicode:int},
            'stacker':{unicode:list},
    }
    required_fields = ['created', 'mtype']
    default_values = {'created':datetime.utcnow, 'mtype':u'note'}
    
    use_schemaless = True
    use_dot_notation=True

    
class AlbumDoc(Document):
    pass

class TimelineDoc(Document):
    structure = {
            'uid':unicode,
            'eid':unicode,
            'mark':int,
            'stamp':unicode,#type of xxxtimeline
            'day': unicode,
            'created':datetime,
            'content':dict,
            'counter':{unicode:int},
            'stacker':{unicode:list},
    }
    required_fields = ['uid', 'eid', 'mark', 'stamp', 'day', 'created']
    default_values = {'mark': 1, 'day': unicode(datetime.utcnow().strftime('%Y-%m-%d')), 'created': datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True
    
class CounterDoc(Document):
    __collection__ = 'counter'
    __database__ = DB_NAME

    structure = {
            'main_id':unicode,
            'sub_id':unicode,
            'counter_result': int,
            'created': datetime,
    }
    required_fields = ['main_id', 'created']
    default_values = {'created': datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True
    def validate(self, *args, **kwargs):
        super(CounterDoc, self).validate(*args, **kwargs)

    
class StackerDoc(Document):
    __collection__ = 'stacker'
    __database__ = DB_NAME

    structure = {
            'main_id':unicode,
            'sub_id':unicode,
            'stacker_result': [],
            'created': datetime,
    }
    required_fields = ['main_id', 'created']
    default_values = {'created': datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True
    
    def validate(self, *args, **kwargs):
        super(StackerDoc, self).validate(*args, **kwargs)
