#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import logging

from xiha.configure import DB_CON, DB_NAME
from modules import UserDoc, IdDoc
from tools import trans_64


class Added_id(object):
    ''' get autoincrement　id '''
    def __init__(self, idx):
        self.idx = idx
        DB_CON.register([IdDoc])
        self.datastroe = DB_CON[DB_NAME]
        self.collection = self.datastroe[IdDoc.__collection__]
        
    def incr(self):
        self.collection.update({"_id":self.idx},{"$inc":{"id":1}}, upsert=True)
    
    def get(self):
        self.incr()
        return trans_64(self.collection.one({"_id":self.idx})["id"])

class API(object):
    ''' common api function '''
    def __init__(self, id=None, col_name=None, collection=None, doc=None):
        self.id = id
        self.datastroe = DB_CON[DB_NAME]
        self.col_name = col_name
        self.collection = collection
        self.doc = doc
        
    def create(self, **kwargs):
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
        a = Added_id(self.col_name)
        self.doc['added_id'] = a.get()
        try:
            self.doc.save(uuid=True, validate=True)
        except Exception, e:
            logging.info(e)
            return (False, unicode(e))
        return (True, None)
        
    def remove(self, id):
        id = id if id else self.id
        self.collection.remove(id)
        
    def del_all(self):
        self.datastroe.drop_collection(self.col_name)

    def edit(self, id=None, *args, **kwargs):
        items=dict(args)
        items.update(kwargs)
        for k, v in items.items():
            if k=="added":
                return(False, 'added key not allowed!')
            elif (k=="counter")and(type(v)==type(0)):
                self.incr(self, "counter", v)
                items.remove(k)
            elif k=="stacker":
                self.push(self, "stacker", v)
                items.remove(k)
            elif k not in self.doc.structure.keys():
                if not items.has_key("added"):items["added"]={}
                items["added"][k]=v
                items.pop(k)
        id = id if id else self.id
        try:
            self.collection.update({"_id":id}, {"$set":items})
        except Exception, e:
            logging.info(e)
            return(False, unicode(e))
        return (True, None)
        
    def incr(self, key, num=1):
        self.collection.update({}, {"counter":{"$inc": {key: num}}}, upsert=True)
    
    def on(self):
        self.edit(logout=False)
    
    def off(self):
        self.edit(logout=True)
    
    def push(self, id, key, value):
        id = id if id else self.id
        self.collection.update({"_id":id}, {"$set":{"stacker":{"$addToSet": {key: {"$each":value}}}}}, upsert=True)
    
    def pop(self, id, key, value):
        id = id if id else self.id
        self.collection.update({"_id":id}, {"stacker":{"$pull": {key: value}}}, upsert=True)
    
    def config(self, **kwargs):
        self.edit(**kwargs)
        
    def one(self, **kwargs):
        return self.collection.one(kwargs)
        
    def find(self, **kwargs):
        return self.collection.find(kwargs)
        
    def page(self, **kwargs):
        page = kwargs.pop('page', 1)
        pglen = kwargs.pop('pglen', 10)
        limit = kwargs.pop('page', 20)
        order_by = kwargs.pop('order_by', 'added_id')
        order = kwargs.pop('order', 1)
        try:
            objs=self.collection.find(kwargs).sort(order_by, order)
            cnt = len(objs)
        except:
            return (False, 'search error')
        start = (page-1)*limit
        end = start+limit
        objs = objs[start:] if end>cnt else objs[start:end]
        #get page additional infomation
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-4, total_page-pglen+1)), min(max(page+1+pglen/2, pglen+1), total_page+1))
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page		
        return (objs, info)
        
    def exist(self, key, value):
        try:
            return self.collection.one({key:value}) is not None
        except Exception, e:
            logging.info(e)
            raise Exception

class UserAPI(API):
    ''' for user '''
    def __init__(self, id=None):
        DB_CON.register([UserDoc])
        datastroe = DB_CON[DB_NAME]
        col_name = UserDoc.__collection__
        collection = datastroe[col_name]
        doc = collection.UserDoc()
        API.__init__(self, id=id, col_name=col_name, collection=collection, doc=doc)
    
    def is_nick_exist(self, nick):
        return self.exist("nick", nick)
    
    def is_email_exist(self, email):
        return self.exist("email", email)
    
    def is_sina_exist(self, sid):
        return self.exist("sina_id", sid)
    
    def diff(self, oid):
        pass
    
    def get_structure(self):
        return UserDoc.structure
        
    def thirdpart(self, **kwargs):
        pass

