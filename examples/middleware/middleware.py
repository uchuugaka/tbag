# -*- coding:utf-8 -*-

from tbag.core.middleware import Middleware
from tbag.utils import log as logger


class TestMiddleware(Middleware):

    async def prepare(self, request):
        logger.info('test middleware in', caller=self)

    async def finish(self, response):
        logger.info('test middleware out', caller=self)
