# -*- coding:utf-8 -*-

"""
    redis pool
"""

import datetime

from tornado.ioloop import IOLoop
from tbag.core.context import TornadoContext
from tbag.core.db.redis import RedisDBBase


class TestRedisPool(RedisDBBase):

    async def test_HSET(self):
        key = 'hash:test:huangtao'
        await self.exec_cmd('HSET', key, 'age', 27)

    async def test_HGET(self):
        key = 'hash:test:huangtao'
        result = await self.exec_cmd('HGET', key, 'age')
        print('result:', result)


async def test_redis_pool():
    redis = TestRedisPool()
    await redis.test_HSET()
    await redis.test_HGET()


def main():
    # 设置配置模块
    config_module = 'config'

    # 初始化context
    t_context = TornadoContext(config_module)

    # 注册测试函数
    IOLoop.current().add_timeout(datetime.timedelta(seconds=2), test_redis_pool)

    # 启动io loop
    t_context.start()


if __name__ == '__main__':
    main()
