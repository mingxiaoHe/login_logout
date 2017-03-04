#!/usr/bin/env python
# coding=utf-8

import os
import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

from tornado.options import define, options
define('port', default=80, help='run on the given port', type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', username=self.current_user)

class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('login.html', **{'status':''})

    @tornado.web.asynchronous
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == 'admin' and password == 'admin':
            self.set_secure_cookie('username', self.get_argument('username'), expires_days=None, expires=time.time()+60)
            self.redirect('/')
        else:
            self.render('login.html', **{'status': '用户名或密码错误'})

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('username')
        self.redirect('/login')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    settings = {
        'template_path':  os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path':  os.path.join(os.path.dirname(__file__), 'static'),
        'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
        'xsrf_cookies': True,
        'login_url': '/login',
    }
    app = tornado.web.Application(
        handlers = [
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
