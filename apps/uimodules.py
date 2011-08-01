#!/usr/bin/env python
# encoding: utf-8
"""
uimodules.py

Created by 刘 智勇 on 2011-05-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import tornado.web

class Entry(tornado.web.UIModule):
    def embedded_css(self):
        return ".entry { margin-bottom: 1em; }"

    def render(self, entry, show_comments=False):
        return self.render_string(
            "module-entry.html", show_comments=show_comments)

