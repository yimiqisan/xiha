#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by 刘 智勇 on 2011-05-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from apps.common import RootHandler, SearchHandler, TestHandler, Error404Handler
from apps.weibo import WeiboStyleHandler, WeiboDynamicHandler, WeiboFollowHandler, WeiboFansHandler, WeiboProfileHandler, WeiboFriendsHandler, WeiboEditHandler, WeiboEditStatusHandler, WeiboEditSyncHandler
from apps.topic import TopicHandler, TopicNewHandler, TopicEditHandler, TopicDeleteHandler, TopicReplyHandler, TopicRSSHandler
from apps.user import LoginHandler, ReloginHandler, LogoutHandler, RegisterHandler, UserHandler, UserTagHandler, UserWriteHandler, UserAlbumHandler, UserTopicHandler, UserEventHandler, UserGroupHandler, UserToolHandler, UserScoreHandler, UserMailHandler, UserEditHandler, SinaLoginHandler, UserAuthHandler
from apps.group import GroupHandler, GroupTopicHandler, GroupMemberHandler, GroupEditHandler, GroupEventHandler, GroupAlbumHandler, GroupWeiboHandler, GroupLikeHandler
from apps.event import EventListHandler, EventHandler, EventTopicHandler, EventMemberHandler, EventAlbumHandler, EventRouteHandler, EventWeiboHandler, EventInsureHandler, EventSupportHandler
from apps.market import MarketHandler, MarketTaobaoHandler, MarketUsedHandler, MarketLeaseHandler, MarketRegieHandler
from apps.application import AppHandler, AppFansHandler, AppTopicHandler, AppWeiboHandler
from apps.site import SiteMapHandler, SiteNaviHandler, SiteJoinHandler, SiteHeartHandler


handlers =  [(r"/", RootHandler),
            (r"/search/?", SearchHandler),
            (r"/login/?", LoginHandler),
            (r"/relogin/?", ReloginHandler),
            (r"/logout/?", LogoutHandler),
            (r"/register/?", RegisterHandler),
            
            (r"/weibo/(.+)/style/?", WeiboStyleHandler),
            (r"/weibo/(.+)/dynamic/?", WeiboDynamicHandler),
            (r"/weibo/(.+)/follow/?", WeiboFollowHandler),
            (r"/weibo/(.+)/fans/?", WeiboFansHandler),
            (r"/weibo/(.+)/profile/?", WeiboProfileHandler),
            (r"/weibo/(.+)/friends/?", WeiboFriendsHandler),
            (r"/weibo/(.+)/edit/?", WeiboEditHandler),
#            (r"/a/weibo/(.+)/edit/?", WeiboAjaxEditHandler),
            (r"/weibo/(.+)/edit_status/?", WeiboEditStatusHandler),
            (r"/weibo/(.+)/edit_sync/?", WeiboEditSyncHandler),
            
            (r"/topic/(.+)/?", TopicHandler),
            (r"/topic/(.+)/new/?", TopicNewHandler),
            (r"/topic/(.+)/edit/?", TopicEditHandler),
            (r"/topic/(.+)/delete/?", TopicDeleteHandler),
            (r"/topic/(.+)/reply/?", TopicReplyHandler),
            (r"/topic/rss/?", TopicRSSHandler),
            
            (r"/people/(.+)/?", UserHandler),
            (r"/people/(.+)/tags/?", UserTagHandler),
            (r"/people/(.+)/writes/?", UserWriteHandler),
            (r"/people/(.+)/albums/?", UserAlbumHandler),
            (r"/people/(.+)/topics/?", UserTopicHandler),
            (r"/people/(.+)/events/?", UserEventHandler),
            (r"/people/(.+)/groups/?", UserGroupHandler),
            (r"/people/(.+)/tools/?", UserToolHandler),
            (r"/people/(.+)/score/?", UserScoreHandler),
            (r"/people/mail/?", UserMailHandler),
            (r"/people/edit/?", UserEditHandler),
#            (r"/a/people/edit/?", UserAjaxEditHandler),
            (r"/people/sinalogin/?", SinaLoginHandler),
            (r"/people/auth/?", UserAuthHandler),
            
            (r"/group/(.+)/?", GroupHandler),
            (r"/group/(.+)/topics/?", GroupTopicHandler),
            (r"/group/(.+)/members/?", GroupMemberHandler),
            (r"/group/(.+)/edit/?", GroupEditHandler),
            (r"/group/(.+)/events/?", GroupEventHandler),
            (r"/group/(.+)/albums/?", GroupAlbumHandler),
            (r"/group/(.+)/weibo/?", GroupWeiboHandler),
            (r"/group/(.+)/like/?", GroupLikeHandler),
#            (r"/a/group/(.+)/edit/?", GroupAjaxEditHandler),
            
            (r"/event/list/?", EventListHandler),
            (r"/event/(.+)/?", EventHandler),
            (r"/event/(.+)/topics/?", EventTopicHandler),
            (r"/event/(.+)/members/?", EventMemberHandler),
            (r"/event/(.+)/album/?", EventAlbumHandler),
            (r"/event/(.+)/route/?", EventRouteHandler),
            (r"/event/(.+)/weibo/?", EventWeiboHandler),
            (r"/event/(.+)/insure/?", EventInsureHandler),
            (r"/event/(.+)/support/?", EventSupportHandler),
            
            (r"/market/(.+)/?", MarketHandler),
            (r"/market/(.+)/taobao/?", MarketTaobaoHandler),
            (r"/market/(.+)/used/?", MarketUsedHandler),
            (r"/market/(.+)/lease/?", MarketLeaseHandler),
            (r"/market/(.+)/regie/?", MarketRegieHandler),
            
            (r"/app/(.+)/?", AppHandler),
            (r"/app/(.+)/fans/?", AppFansHandler),
            (r"/app/(.+)/topics/?", AppTopicHandler),
            (r"/app/(.+)/weibo/?", AppWeiboHandler),
            
            (r"/sitemap/?", SiteMapHandler),
            (r"/navigation/?", SiteNaviHandler),
            (r"/joinus/?", SiteJoinHandler),
            (r"/myheart/?", SiteHeartHandler),
            
            (r"/test/(.*)/?", TestHandler),
            (r".*", Error404Handler),
        ]
