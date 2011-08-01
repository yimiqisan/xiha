#!/usr/bin/env python
# encoding: utf-8
"""
uimethods.py

Created by 刘 智勇 on 2011-05-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from weibopy.models import ResultSet
from mongokit.cursor import Cursor
from datetime import datetime

def sina_msg_filter(template, data):
    ret_l = []
    if type(data) == type(ResultSet()):
        ret_l = data
    elif type(data) == type([]):
        ret_l = data
    elif hasattr(data,'next'):
        ret_l = data
    else:
        ret_l.append(data)
    return ret_l
    
def sina_disp(template, item, loop=True):
    content = r''
    types = [type(i) for i in [True, 0, "0", u"", [0], {0:1}, (0,), datetime(2012,12,20)]]
    for k in dir(item):
        if k.count(r'__') == 2:
            continue
        if k == '_api':
            continue
        var = getattr(item, k)
        v = str(type(var))
        if loop:
            content += r"%s:&#9;" % k
        else:
            content += r"&#9;&#9;&#9;%s:" % k
        if type(var) in types:
            content += r"%s<br/>" % var
        elif not hasattr(var, '__call__'):
            if loop:
                c = sina_disp(template, var, False)
                content += r"<br/>%s<br/>" % c
            else:
                content += r"<br/>"
        else:
            content += r"method class<br/>"
    return content
