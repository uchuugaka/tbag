# -*- coding:utf-8 -*-

from tbag.utils.routes import route
from tbag.core.web import WebHandler
from tbag.utils import log as logger


@route('/api/test', 'api.test')
class TestHandler(WebHandler):

    async def _get_(self, *args, **kwargs):
        logger.info('test handler GET:', self.request.path, caller=self)
        result = {'ok': 1}
        self.do_success(result)
