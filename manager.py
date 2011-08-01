#!/usr/bin/env python
# encoding: utf-8
"""
manage.py

Created by 刘 智勇 on 2011-05-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

import configure
from urls import handlers


define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **configure.settings)

def main():
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)
    IOLoop.instance().start()
    
if __name__ == '__main__':
    main()

