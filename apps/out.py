#!/usr/bin/env python
# encoding: utf-8
"""
out.py

Created by 刘 智勇 on 2011-06-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

rss_feed = []

RSS_MAIN_TYPE = [(u'technology', u'科技'),
            (u'fun', u'娱乐'),
            (u'news', u'实事'),
            (u'money', u'财经'),
            (u'life', u'生活'),
            (u'human', u'人文'),
            (u'tools', u'工具，技术'),
            ]


RSS_TECH = [(u'feed://app.epuber.com/?app=rss&controller=index&action=feed', u'数字出版在线'),
            (u'feed://www.techweb.com.cn/rss/focus.xml', u'TechWeb 今日焦点'),
            (u'feed://apple4.us/feed', u'apple4us'),
            (u'http://feed.caozenghui.cn/', u'一言谈-曹增辉')]
rss_feed.extend(RSS_TECH)

RSS_FUNS = [(u'feed://www.u148.net/rss/', u'有意思吧'),
            (u'http://feed.feedsky.com/leica', u'Leica中文摄影杂志')]
rss_feed.extend(RSS_FUNS)

RSS_NEWS =  [(u'feed://feed.feedsky.com/my1510', u'一五一十部落头条'),
            (u'feed://www.infzm.com/rss/home/rss2.0.xml', u'南方周末-热点新闻'),
            (u'feed://www.nbweekly.com/rss.xml', u'南都周刊')]
rss_feed.extend(RSS_NEWS)

RSS_MONEY = [(u'', u'今日焦点-21世纪网')]
#rss_feed.extend(RSS_MONEY)

RSS_LIFE =  [(u'', u'春日迟迟的BLOG')]
#rss_feed.extend(RSS_LIFE)

RSS_HUMAN = [(u'', u'Lohasly 乐活杂志'),
            (u'', u'《槽边往事》---比特海日志')]
#rss_feed.extend(RSS_HUMAN)

RSS_TOOLS = [(u'', '月光博客')]
#rss_feed.extend(RSS_TOOLS)
            