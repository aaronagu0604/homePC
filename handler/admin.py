#!/usr/bin/env python
# coding=utf8

from handler import BaseHandler
from lib.route import Route


@Route(r'/admin', name='admin')    # 图片上传
class UploadPicHandler(BaseHandler):
    def get(self):
        self.write('/admin/upload_pic')
        # self.redirect('/admin/upload_pic')


@Route(r'/admin/upload_pic', name='admin_upload_pic')    # 图片上传
class UploadPicHandler(BaseHandler):
    def get(self):
        data = self.get_argument('data', '')
        self.render('admin/picture_edit.html', active='pic', data=data)
