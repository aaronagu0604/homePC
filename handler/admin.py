#!/usr/bin/env python
# coding=utf8

from handler import BaseHandler
from lib.route import Route


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

