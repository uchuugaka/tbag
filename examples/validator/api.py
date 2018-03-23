# -*- coding:utf-8 -*-

from tbag.utils import validators
from tbag.utils.routes import route
from tbag.core.web import WebHandler
from tbag.utils import log as logger


@route('/api/test', 'api.test')
class TestHandler(WebHandler):

    async def _get_(self, *args, **kwargs):
        page = validators.int_field(self.query_params, 'page')
        logger.info('test handler GET:', self.request.path, 'page:', page, caller=self)
        result = {'ok': 1}
        self.do_success(result)

    async def _post_(self, *args, **kwargs):
        info = validators.dict_field(self.data, 'info')
        logger.info('test handler POST:', self.request.path, 'info:',  info, caller=self)
        result = {'ok': 1}
        self.do_success(result)
