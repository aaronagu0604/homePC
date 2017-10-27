#!/usr/bin/env python
# coding=utf8

from handler import BaseHandler
from lib.route import Route
import time
import tornado
import tornado.httpclient
import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.gen import coroutine
from tornado.web import asynchronous
import logging



# ----------------------------------------------------------应用页面----------------------------------------------------
@Route(r'/',name='admin_root')    # 公司官网
class RootHandler(BaseHandler):
    def get(self):
        self.render("index.html")


@Route(r'/m_index', name='m_index')  # APP宣传页面移动端
class IndexMHandler(BaseHandler):
    def get(self):
        self.render("index_m.html")


@Route(r'/admin/upload_pic', name='admin_upload_pic')    # 图片上传
class UploadPicHandler(BaseHandler):
    def get(self):
        data = self.get_argument('data', '')
        self.render('admin/picture_edit.html', active='pic', data=data)


# ----------------------------------------------------------并发测试（已完成）------------------------------------------
@Route(r'/admin/test0', name='admin_test0')    # 普通方式
class IndexHandler(BaseHandler):
    def get(self):
        self.write("""
<div style="text-align: center">
    <div style="font-size: 72px">%s</div>
</div>""" % time.time())


@Route(r'/admin/test1', name='admin_high_concurrency_test1')    # 异步装饰器 实现异步
class IndexHandler(BaseHandler):
    @tornado.web.asynchronous    # 用此装饰器来实现异步的话必须在结束时调用self.finish()来结束，否则是一个长连接不会自动结束；
    def get(self):
        self.write("""
<div style="text-align: center">
    <div style="font-size: 72px">%s</div>
</div>""" % (time.time()))
        self.finish()


@Route(r'/admin/test2', name='admin_high_concurrency_test2')    # 基于协成的方式异步
class NoBlockingHnadler(tornado.web.RequestHandler):
    """
    Tornado 提供了多种的异步编写形式：回调、Future、协程等，其中以协程模式最是简单和用的最多
    coroutine 装饰器是指定改请求为协程模式，说明白点就是能使用 yield 配合 Tornado 编写异步程序。
    Tronado 为协程实现了一套自己的协议，不能使用 Python 普通的生成器。
    使用 coroutine 方式有个很明显是缺点就是严重依赖第三方库的实现，如果库本身不支持 Tornado 的异步操作再怎么使用协程也是白搭依然会是阻塞的
    """
    @gen.coroutine
    def gen_sleep(self):
        gen.sleep(3)
        # time.sleep(30)  # 使用time sleep的话会阻塞，必须使用gen提供的函数
        raise gen.Return([1, 2])

    @gen.coroutine
    def get(self):
        start_time = time.time()
        end_time = yield self.gen_sleep()
        self.write(u'起始时间：%s, 结束时间：%s' % (start_time, end_time))


@Route(r'/admin/test3', name='admin_high_concurrency_test3')    # 基于线程的方式异步
class LoopTestHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)    # 搞出10个线程
    @coroutine
    def get(self):
        a = yield self._sleep(time.time())

    @run_on_executor    # 这个耗时的函数放到线程中取执行
    def _sleep(self, start_time):
        time.sleep(3)
        end_time = time.time()
        self.write("""
<div style="text-align: center">
    <div style="font-size: 24px">start  time: %s</div>
    <div style="font-size: 24px">end    time: %s</div>
    <div style="font-size: 24px">handle time: %s</div>
</div>""" % (start_time, end_time, end_time-start_time))


# ----------------------------------------------------------测试中----------------------------------------------------
@Route(r'/admin/test20', name='admin_high_concurrency_test20')    # 协成
class NoBlocking0Hnadler(BaseHandler):
    @gen.coroutine
    def getUser(self):
        client = tornado.httpclient.AsyncHTTPClient()
        resp = client.fetch("http://127.0.0.1:8890/admin/time_consuming_operation", callback=self.on_response)
        raise gen.Return(resp)

    @gen.coroutine
    def get(self):
        start_time = time.time()
        end_time = yield self.getUser()
        self.write(u'起始时间：%s, 结束时间：%s' % (start_time, end_time))


from tornado.concurrent import Future
# Tornado 提供了多种的异步编写形式：回调、Future、协程等，其中以协程模式最是简单和用的最多
@Route(r'/admin/test21', name='admin_high_concurrency_test21')    # 阻塞
class NoBlockingHnadler(tornado.web.RequestHandler):
    @gen.coroutine
    def asyn_sum(self, a, b):
        print("begin calculate:sum %d+%d"%(a,b))
        future = Future()

        def callback(a, b):
            print("start callback")
            # do something
            time.sleep(3)
            future.set_result(a+b)

        print("add_callback")
        tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)

        print("yield")
        result = yield future

        print("after yielded")
        print("the %d+%d=%d"%(a, b, result))

    def get(self):
        self.asyn_sum(2, 3)


@Route(r'/admin/test22', name='admin_high_concurrency_test22')    # 高并发测试二 （失败）
class IndexHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch("http://127.0.0.1:8890/admin/time_consuming_operation", callback=self.on_response)

    def on_response(self, response):
        self.write("""
<div style="text-align: center">
    <div style="font-size: 24px">get connect time: %s</div>
    <div style="font-size: 24px">end connect time: %s</div>
    <div style="font-size: 24px">handle time: %s</div>
</div>""" % (1, 2, 3))
        self.finish()


import urllib
@Route(r'/admin/test4', name='admin_high_concurrency_test4')    # 高并发测试四
class Test4Handler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        query = self.get_argument('q', '')
        logging.info('-----start-time: %s' % time.time())
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,
                "http://127.0.0.1:8890/admin/sleep?" + \
                urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}))
        self.write("""
<div style="text-align: center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 24px">tweets per second</div>
</div>""" % (query, 3))
        logging.info('-----end-time: %s' % time.time())
        self.finish()