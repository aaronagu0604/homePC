#!/usr/bin/env python
# coding=utf8

import os

# 是否 debug
DEBUG = True

# 数据库 setting
DB_PORT = 3306
DB_HOST = '123.56.94.179'
DB_USER = 'root'
DB_PASSWD = '6V^efYdy'
DB_NAME = 'czj'
MAX_CONNECTIONS = 300  # mysql 连接池最大数量
STALE_TIMEOUT = 432000  # mysql 连接池回收时间 (5天)

# memcached setting
MEMCACHE_HOST = '127.0.0.1:11211'

# RebbitMQ setting
MQSERVER = '127.0.0.1'
MQPORT = '5672'
MQUSER = 'guest'
MQPASSWORD = '1q2w3e4R'
MQEXCHANGENAME = 'czj_exchange'
MQQUEUENAME = 'czj_queue'
MQROUTINGKEY = 'czj_routing_key'

# jinja2 setting
template_path = os.path.join(os.path.dirname(__file__), 'template')
static_path = os.path.join(os.path.dirname(__file__), 'style')
upload_path = os.path.join(os.path.dirname(__file__), 'upload')
cookie_secret = "Fux+poCnRSGIb/EsikPs5gI0BTwBBkN5k8U4kPxaV1o="
login_url = '/signin'
xsrf_cookies = True
autoescape = False    # autoescape XML/HTML自动转义，缺省为false. 就是在渲染模板时自动把变量中的<>&等字符转换为&lt;&gt;&amp;。

if DEBUG:
    imgDoman = 'http://img.520czj.com/image/'
    domanName = 'http://api.dev.test.520czj.com'
    wxdomanName = 'http://wx.dev.520czj.com'
    baseUrl = domanName + '/mobile/'
else:
    imgDoman = 'http://img.520czj.com/image/'
    domanName = 'http://api.dev.test.520czj.com'
    wxdomanName = 'http://wx.dev.520czj.com'
    baseUrl = domanName + '/mobile/'

typeface = '/home/www/workspace/eofan/src/simsun.ttc'

user_token_prefix = "mt:"  # 用户登录token的前缀
#
ADMIN_PAGESIZE = 20  # 管理后台页面数据条数
USER_PAGESIZE = 10  # 商家后台页面数据条数
MOBILE_PAGESIZE = 20  # 移动端数据条数




