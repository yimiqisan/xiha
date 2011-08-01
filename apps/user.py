#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by 刘 智勇 on 2011-06-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import re
from weibopy.auth import OAuthHandler
from weibopy.api import API as WeiboAPI
from tornado.web import authenticated

from api import UserAPI
from component import WeiboComp, AlbumComp, OperateComp
from common import BaseHandler
from tools import session, _unicode
from xiha.configure import SINA_CONSUME_KEY, SINA_CONSUME_SECRET


class User(object):
    reg_keys = {'email':u'email', 'passwd':u'密码', 'repwd':u'密码确认'}
    def __init__(self, api=None, weibo=None, album=None, operate=None):
        self._api = api if api else UserAPI()
#        self._weibo = weibo if weibo else WeiboComp()
        self._album = album if album else AlbumComp()
        self._operate = operate if operate else OperateComp()

    def whois(self, key, value):
        ret = self._api.one(**{key:value})
        if ret:
            self.info = ret
            self.uid = self.info['_id']
        else:
            self.uid = self.info = None

    def check_pwd(self, passwd):
        return (self.passwd is not None)and(self.passwd == passwd)
    
    def check_reg(self, **data):
        data.pop('_xsrf', None)
        for i in data:
            v = data.get(i, [])
            v = [re.sub(r"[\x00-\x08\x0e-\x1f]", " ", x) for x in v]
            v = [_unicode(x) for x in v]
            v = [x.strip() for x in v]
            data[i] = v[-1]
        for k in self.reg_keys.keys():
            i = data.get(k, None)
            if i is None:return(False, u'请填写'+self.reg_keys[k])
        email = data.get('email', None)
        nick = data.get('nick', None)
        if self._api.is_email_exist(email):return(False, u'email已存在！')
        if (nick is not None) and (self._api.is_nick_exist(nick)):return(False, u'nick已存在!')
        if data.get('passwd', 'not') != data.get('repwd', 'equal'):return(False, u'密码不匹配！')
        ret_d = {}
        kwords_l = self._api.get_structure().keys()
        for i in data.keys():
            if i in kwords_l:
                ret_d[i] = data.pop(i)
        data.pop('repwd')
        ret_d.update(data)
        return (True, ret_d)

    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class ACC_TOKEN(object):
    ''' sina access token object '''
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

class LoginHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        n = self.get_secure_cookie("user")
        if n and uid:
            self.redirect('/')
        #self.set_goto()
        self.render("login.html", **{'sina_id':self.SESSION['sina_id']})
    
    @session
    def post(self):
        email = self.get_argument('email', None)
        passwd = self.get_argument('passwd', None)
        if not email or not passwd:
            return self.render('login.html', **{'warning': u'用户名或密码错误！', 'sina_id':self.SESSION['sina_id']})
        u = User()
        u.whois('email', email)
        if u.check_pwd(passwd):
            n = u.nick.encode('utf-8') if u.nick else u.email
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            at = u.added.get('access_token', None)
            self.set_access_token(u.sina_id, at)
            self.skip_page()
        else:
            return self.render('login.html', **{'warning': u'用户名或密码错误！', 'sina_id':self.SESSION['sina_id']})
    
    @session
    def set_access_token(self, sid, at):
        uid, sina_id, access_token = self.SESSION['uid'], self.SESSION['sina_id'], self.SESSION['oauth_access_token']
        if sid and not access_token:
            if at:
                k, s = tuple(at.split("&"))
                self.SESSION['oauth_access_token'] = ACC_TOKEN(k, s)
        elif not sid and access_token:
            u = User()
            at = access_token.key+'&'+access_token.secret
            u._api.edit(uid, sina_id=unicode(sina_id), access_token=at)

class ReloginHandler(BaseHandler):
    @session
    def get(self):
        to_url = self.get_argument('url_to', '/')
        uid = self.SESSION['uid']
        u = User()
        u.whois('_id', uid)
        n = u.nick.encode('utf-8') if u.nick else u.email
        self.set_secure_cookie("user", n, 1)
        self.SESSION['uid']=u._id
        at = u.added.get('access_token', None)
        self.set_access_token(u.sina_id, at)
        self.redirect(to_url)
        
    @session
    def set_access_token(self, sid, at):
        uid, sina_id, access_token = self.SESSION['uid'], self.SESSION['sina_id'], self.SESSION['oauth_access_token']
        if sid and not access_token:
            if at:
                k, s = tuple(at.split("&"))
                self.SESSION['oauth_access_token'] = ACC_TOKEN(k, s)
        elif not sid and access_token:
            u = User()
            at = access_token.key+'&'+access_token.secret
            u._api.edit(uid, sina_id=unicode(sina_id), access_token=at)


class LogoutHandler(BaseHandler):
    @authenticated
    @session
    def get(self):
        #self.set_goto()
        self.clear_cookie("user")
        try:
            self.SESSION.delete()
        except:
            pass
        self.skip_page()

class RegisterHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        n = self.get_secure_cookie("user")
        if n and uid:
            self.redirect('/')
        self.render("register.html")
    
    @session
    def post(self):
        u = User()
        cek_ret = u.check_reg(**self.request.arguments)
        if cek_ret[0]:
            info = cek_ret[1]
            email = info['email']
        else:
            return self.render('register.html', **{'warning': cek_ret[1]})
        ret = u._api.create(**info)
        if ret[0]:
            u.whois('email', email)
            n = u.nick.encode('utf-8') if u.nick else u.email
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            at = u.added.get('access_token', None)
            self.set_access_token(u.sina_id, at)
            self.skip_page()
        else:
            self.render('register.html', **{'warning': ret[1]})
    
    @session
    def set_access_token(self, sid, at):
        uid, sina_id, access_token = self.SESSION['uid'], self.SESSION['sina_id'], self.SESSION['oauth_access_token']
        if sid and not access_token:
            if at:
                k, s = tuple(at.split("&"))
                self.SESSION['oauth_access_token'] = ACC_TOKEN(k, s)
        elif not sid and access_token:
            u = User()
            at = access_token.key+'&'+access_token.secret
            u._api.edit(uid, sina_id=unicode(sina_id), access_token=at)

class UserHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/mine.html")

class UserTagHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/tag.html")

class UserWriteHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/write.html")

class UserAlbumHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/album.html")

class UserTopicHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/topic.html")

class UserEventHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/event.html")

class UserGroupHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/group.html")

class UserToolHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/tool.html")

class UserScoreHandler(BaseHandler):
    def get(self, uadd):
        self.render("user/score.html")

class UserMailHandler(BaseHandler):
    def get(self):
        self.render("user/mail.html")

class UserEditHandler(BaseHandler):
    @authenticated
    def get(self):
        #self.set_goto()
        self.render("user/edit.html")

    @session
    def post(self):
        uid = self.SESSION['uid']
        u = User()
        if uid:
            u.whois('_id', uid)
            args = self.filter_args()
            u._api.edit(u._id, **args)
            self.redirect('/relogin/')
        else:
            self.render("user/edit.html", **{'warning': u''})

class SinaLoginHandler(BaseHandler):
    @session
    def get(self):
        access_token = self.SESSION['oauth_access_token']
        auth = OAuthHandler(SINA_CONSUME_KEY, SINA_CONSUME_SECRET)
        auth.setToken(access_token.key, access_token.secret)
        me = WeiboAPI(auth).me()
        u = User()
        has_sina = u._api.is_sina_exist(unicode(me.id))
        if not has_sina:
            data = {}
            data['nick'] = me.name
            data['sina_id'] = unicode(me.id)
            data['photo'] = unicode(me.profile_image_url)
            access_token = self.SESSION['oauth_access_token']
            data['access_token'] = access_token.key+'&'+access_token.secret
            u._api.create(**data)
        u.whois('sina_id', unicode(me.id))
        self.set_secure_cookie("user", u.nick.encode('utf-8'), 1)
        self.SESSION['uid']=u._id
        return self.redirect('/')

class UserAuthHandler(BaseHandler):
    @session
    def get(self):
        verifier = self.get_argument('oauth_verifier', None)
        auth = OAuthHandler(SINA_CONSUME_KEY, SINA_CONSUME_SECRET)
        if not verifier:
            #self.SESSION['goto'] = self.get_argument('to_url', None)
            auth_url = auth.get_authorization_url()+'&oauth_callback='+self.request.protocol+'://'+self.request.host+'/people/auth/'
            self.SESSION['oauth_request_token'] = auth.request_token
            self.redirect(auth_url)
        else:
            request_token = self.SESSION['oauth_request_token']
            del self.SESSION['oauth_request_token']
            auth.set_request_token(request_token.key, request_token.secret)
            access_token = auth.get_access_token(verifier)
            self.SESSION['oauth_access_token'] = access_token
            me = WeiboAPI(auth).me()
            self.after_auth(me)
    
    @session
    def after_auth(self, me):
        uid = self.SESSION['uid']
        u = User()
        if uid:# sync account
            u.whois('_id', uid)
            access_token = self.SESSION['oauth_access_token']
            if access_token:
                at = access_token.key+'&'+access_token.secret
                kwargs = {'sina_id':unicode(me.id), 'access_token':at}
                if not u.nick:kwargs['nick']=me.name
                u._api.edit(uid, **kwargs)
                return self.redirect('/relogin/?url_to=/weibo/uid/edit_sync/')
        else:# sina login
            sina_id = unicode(me.id)
            u.whois('sina_id', sina_id)
            if u._id:
                self.SESSION['uid'] = u._id
                return self.redirect('/relogin/')
            else:
                self.SESSION['sina_id'] = sina_id
                return self.redirect('/login/')
        #return self.redirect(self.request.headers.get('Referer', '/'))
        
        







