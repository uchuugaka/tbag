# -*- coding:utf-8 -*-

from tbag.utils.routes import route
from tbag.core.web import WebHandler
from tbag.utils import log as logger


@route('/api/test', 'api.test')
class TestHandler(WebHandler):

    async def get(self, *args, **kwargs):
        logger.info('test handler GET:', self.request.path, caller=self)
        result = {'ok': 1}
        self.do_success(result)

    async def post(self, *args, **kwargs):
        body = self.get_body()
        logger.info('test handler POST:', self.request.path, 'body:',  body, caller=self)
        result = {'ok': 1}
        self.do_success(result)

    async def put(self, *args, **kwargs):
        body = self.get_body()
        logger.info('test handler PUT:', self.request.path, 'body:',  body, caller=self)
        result = {'ok': 1}
        self.do_success(result)

    async def patch(self, *args, **kwargs):
        body = self.get_body()
        logger.info('test handler PATCH:', self.request.path, 'body:',  body, caller=self)
        result = {'ok': 1}
        self.do_success(result)
