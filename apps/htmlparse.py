#!/usr/bin/env python
# encoding: utf-8
"""
htmlparse.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from sgmllib import SGMLParser
import urllib

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k =='href']
        if href:
            self.urls.extend(href)

if __name__ == '__main__':
    usock = urllib.urlopen('http://pypi.python.org/simple/')
    parser = URLLister()
    parser.feed(usock.read())
    usock.close()
    print parser.urls