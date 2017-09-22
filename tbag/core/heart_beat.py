# -*- coding:utf-8 -*-

"""
    服务器心跳
"""

import datetime

from tornado.ioloop import IOLoop

from tbag.utils import log as logger


class HeartBeat(object):
    """ 心跳
    """

    def __init__(self):
        self._count = 0 # 心跳次数
        self._interval = 1 # 心跳间隔(秒)

    def start(self):
        self._count += 1
        if self._count > 9999999:
            self._count = 1
        logger.info('do server heartbeat, count:', self._count, caller=self)
        IOLoop.current().add_timeout(datetime.timedelta(seconds=self._interval), self.start)
