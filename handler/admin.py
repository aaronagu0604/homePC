#!/usr/bin/env python
# coding=utf8

from handler import BaseHandler
from lib.route import Route


# ----------------------------------------------------------应用页面----------------------------------------------------
@Route(r'/',name='admin_root')    # 主页
class RootHandler(BaseHandler):
    def get(self):
        self.render("personal/index.html")


@Route(r'/about',name='admin_about')    # 公司官网
class AboutHandler(BaseHandler):
    def get(self):
        self.render("personal/about.html")


@Route(r'/post',name='admin_post')    # 公司官网
class PostHandler(BaseHandler):
    def get(self):
        self.render("personal/post.html")


@Route(r'/admin/upload_pic', name='admin_upload_pic')    # 图片上传
class UploadPicHandler(BaseHandler):
    def get(self):
        data = self.get_argument('data', '')
        self.render('admin/picture_edit.html', active='pic', data=data)

