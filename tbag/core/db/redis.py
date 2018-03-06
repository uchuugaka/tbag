# -*- coding:utf-8 -*-

"""
redis async操作接口

Author: huangtao
Date:   2017/05/08
Update: None
"""

"""
    消息发布
    * 采用redis的publish
"""

import json

import asyncio
import aioredis
from tornado.ioloop import IOLoop
from tbag.utils import log as logger


__all__ = ('initRedisPool', 'RedisDBBase')


REDIS_CONN_POOL = None  # redis连接池
REDIS_PUB_CONN = None   # redis事件发布链接
REDIS_SUB_CONN = None   # redis事件订阅链接


async def initRedisPool(**kwargs):
    """ 初始化连接池
    """
    host = kwargs.get('host', 'redis://127.0.0.1:6379')
    global REDIS_CONN_POOL
    REDIS_CONN_POOL = await aioredis.create_redis_pool(host, encoding='utf-8')
    logger.info('create redis pool success.')


class RedisDBBase:
    """ redis db基类
    """

    async def exec_cmd(self, *args, **kwargs):
        """ 执行命令
        """
        result = await REDIS_CONN_POOL.execute(*args, **kwargs)
        logger.debug('cmd:', *args, 'result:', result, caller=self)
        return result


# class RedisDBBase:
#     """ redis连接
#     """
#
#     def __init__(self):
#         self.pool = None    # 连接池
#         self.pub_conn = None    # publish连接
#         self.host = REDIS_CONFIG.get('host')
#         self.channel = REDIS_CONFIG.get('channel')
#
#     async def start(self):
#         await self._init_pool()
#         await self._init_publish()
#         await self._init_subscribe()
#
#     async def _init_pool(self):
#         """ 初始化连接池
#         """
#         self.pool = await aioredis.create_redis_pool(self.host, encoding='utf-8')
#         logger.info('create redis pool success.', caller=self)
#
#     async def _init_publish(self):
#         """ 初始化事件发布
#         """
#         self.pub_conn = await aioredis.create_redis(self.host)
#         logger.info('create redis publish channel success. channel:', self.channel, caller=self)
#
#     async def _init_subscribe(self):
#         """ 初始化订阅连接
#         """
#         sub = await aioredis.create_redis(self.host)
#         channel, = await sub.subscribe(self.channel)
#         await asyncio.ensure_future(self.async_reader(channel))
#         logger.info('subscribe channel success. channel:', self.channel, caller=self)
#
#     async def exec_redis_cmd(self, *args):
#         logger.debug('cmd:', *args, caller=self)
#         result = await self.pool.execute(*args)
#         return result
#
#     async def publish(self, content):
#         data = json.dumps(content)
#         await self.pub_conn.execute('PUBLISH', self.channel, data)
#         # logger.debug('content:', content, caller=self)
#
#     async def async_reader(self, channel):
#         while await channel.wait_message():
#             msg = await channel.get(encoding='utf-8')
#             data = json.loads(msg)
#             IOLoop.current().add_callback(WebsocketHandler.push_message, data)
#             # logger.debug('receive data:', data, caller=self)

