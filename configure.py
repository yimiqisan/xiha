#!/usr/bin/env python
# encoding: utf-8
"""
configure.py

Created by 刘 智勇 on 2011-05-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import os
from mongokit import Connection
import redis

#loggging config
from logging import basicConfig, DEBUG
basicConfig(filename = 'app.log',
            format = '%(asctime)s %(module)s %(lineno)s %(message)s',
            level = DEBUG
)

#tornado settings
from apps import uimodules, uimethods
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "htmls"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        login_url="/login",
        autoescape="xhtml_escape",
        ui_modules=uimodules,
        ui_methods=uimethods,
#        xsrf_cookies=True,
        debug=True,
        cache_engine=redis.Redis(host='localhost', port=6379, db=1),
)

#mongodb settings
DB_NAME = 'duobianxing'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_CON = Connection(host=MONGO_HOST, port=MONGO_PORT)

#session initialize settings
SESSION_SET = {
    "SESSION_EXPIRE_TIME": 86400,    # sessions are valid for 86400 seconds (24 hours)
    "REDIS_URL": {'ip': 'localhost', 'port': 6379, 'db': 0, },
}

#component init configure
USER_APP_ID = u'a4182b3885964798a847dff117e70840'
TIMELINE_APP_ID = '7c7ee59494b247e186e77090bca6389a'
USER_TIMELINE_APP_ID = 'abfc270dbfa048398d3af48d74fe0224'
ATTENTION_TIMELINE_APP_ID = '64fba3caeffd45da95021b0b8e04ce9b'
RETWEET_TIMELINE_APP_ID = '623a5ca9e098487a902e08f3b010b341'
REPLY_TIMELINE_APP_ID = 'b1bb7c88927b45889dca28c9a5f3fc50'
LBS_TIMELINE_APP_ID = '4d0cc84f2d40406d991869708d3cef32'
REPORT_TIMELINE_APP_ID = 'dd7cff585d4947d7aa9ddc5a67201eba'
SINA_TIMELINE_APP_ID = 'd538928ae0964b08bffdb4326d6573b0'
LIKE_TIMELINE_APP_ID = '0695fef1821a40ca8a5ef838a204d43e'
HATE_TIMELINE_APP_ID = '13e2ac25db56492dad2eb5acab79079d'
OPERATE_APP_ID = '68e0df978493403f85c8cdabcf3c1f49'

DEFAULT_COMP = [USER_APP_ID]

#thirdpart key list
SINA_CONSUME_KEY = '2596118515'
SINA_CONSUME_SECRET = '9e2bcc23eb019638bca07517db91eaaa'
