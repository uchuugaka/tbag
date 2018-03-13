# -*- coding:utf-8 -*-

"""
初始化日志、uri路由、数据库连接，启动服务器心跳

Author: huangtao
Date:   2017/8/8
Update: 2017/11/20  1. 删除root_dir配置;
        2017/12/17  1. 修改配置参数传入方式，改为传入配置模块;
                    2. 增加middleware中间件;
        2017/12/17  1. 增加web app初始化;
        2018/01/18  1. 引入asyncio;
        2018/03/06  1. 初始化redis;
        2018/03/14  1. 修改heartbeat模块名;
"""

import sys
import asyncio

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado import options
from tornado.ioloop import IOLoop
from tornado.web import Application

from tbag.utils import tools
from tbag.utils.routes import route
from tbag.utils import log as logger
from tbag.core.middleware import Middleware


class TornadoContext(object):
    """ 初始化日志、uri路由、数据库连接，启动服务器心跳
    """

    def __init__(self, setting_module):
        """ 初始化
        @param setting_module 配置模块
            `DEBUG`         debug模式，默认为False
            `RUN_MODE`      运行模式，online为线上服务器，inner-test为内测测试服，test为测试服，console为本地调试
                            online/inner-test/test模式将会把日志写入日志文件，console模式不写日志文件而打印到控制台
            `LOG`           日志配置
                `level`     级别 DEBUG/INFO
                `path`      日志保存路径
                `name`      日志名
            `HANDLER_PATHES`    uri注册处理器路径
            `HTTP_PORT`     HTTP监听端口号
            `MIDDLEWARES`   中间件配置
            `MYSQL`         mysql配置
            `MONGODB`       mongodb配置
            `REDIS`         redis配置
            `ALLOW_CORS`    是否支持跨域，True为支持，False为不支持，默认False
            `COOKIE_SECRET` cookie加密字符串
        """
        self.loop = None
        self.setting_module = setting_module

        self._get_event_loop()
        self._load_settings()
        self._init_logger()
        self._init_middlewares()
        self._init_db_instance()
        self._init_uri_routes()
        self._init_application()
        self._do_heartbeat()

    def start(self):
        """ 启动
        """
        logger.info('start io loop ...')
        self.loop.run_forever()

    def _get_event_loop(self):
        if not self.loop:
            tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOMainLoop')
            self.loop = asyncio.get_event_loop()
        return self.loop

    def _load_settings(self):
        """ 加载配置
        """
        settings = __import__(self.setting_module, {}, {}, ['models'])

        # 调试模式
        self.debug = getattr(settings, 'DEBUG', False)

        # 运行模式
        self.run_mode = getattr(settings, 'RUN_MODE', 'console')

        # 日志配置
        self.log_config = getattr(settings, 'LOG', {})

        # uri处理路径
        self.handler_pathes = getattr(settings, 'HANDLER_PATHES', [])

        # HTTP监听端口号
        if len(sys.argv) > 1:
            self.http_port = sys.argv[1]
        else:
            self.http_port = getattr(settings, 'HTTP_PORT', 10000)

        # 中间件
        self.middlewares = getattr(settings, 'MIDDLEWARES', [])

        # mysql配置
        self.mysql_config = getattr(settings, 'MYSQL', None)

        # mongodb配置
        self.mongo_config = getattr(settings, 'MONGODB', None)

        # redis配置
        self.redis_config = getattr(settings, 'REDIS', None)

        # 是否支持跨域，True为支持，False为不支持，默认False
        self.cors = getattr(settings, 'ALLOW_CORS', False)
        options.define('cors', self.cors, help='set http response header `Access-Control-Allow-Origin` to `*`')

        # cookie加密字符串
        self.cookie_secret = getattr(settings, 'COOKIE_SECRET', tools.get_uuid4())

    def _init_logger(self):
        """ 初始化日志
        """
        level = self.log_config.get('level', 'debug')
        path = self.log_config.get('path', '/tmp/logs')
        name = self.log_config.get('name', 'tbag.log')
        if self.run_mode == 'console':
            logger.initLogger()
        else:
            log_filename = '%s_%s.log' % (name.split('.')[0], self.http_port)
            logger.initLogger(level, path, log_filename)
        options.parse_command_line()

    def _init_uri_routes(self):
        """ 初始化uri路由
        """
        logger.info('init uri routes start >>>', caller=self)
        handlers = route.make_routes(self.handler_pathes)
        self.handlers = handlers
        logger.info('init uri routes done <<<', caller=self)

    def _init_db_instance(self):
        """ 初始化数据库对象
        """
        logger.info('init db instance start >>>', caller=self)
        if self.mysql_config:
            from tbag.core.db.mysql import initMySQL
            logger.info('mysql config:', self.mysql_config, caller=self)
            initMySQL(**self.mysql_config)
        if self.mongo_config:
            from tbag.core.db.mongo import initMongodb
            logger.info('mongodb config:', self.mongo_config, caller=self)
            initMongodb(**self.mongo_config)
        if self.redis_config:
            from tbag.core.db.redis import initRedisPool
            logger.info('redis config:', self.redis_config, caller=self)
            self.loop.run_until_complete(initRedisPool(**self.redis_config))
        logger.info('init db instance done <<<', caller=self)

    def _init_middlewares(self):
        """ 加载中间件
        """
        logger.info('load middleware start >>>', caller=self)
        middlewares = []
        for m in self.middlewares:
            l = m.split('.')
            class_name = l[-1]
            model = '.'.join(l[:-1])
            mo = __import__(model, {}, {}, ['classes'])
            middleware = getattr(mo, class_name)
            instance = middleware()
            if not isinstance(instance, Middleware):
                logger.warn('middleware must inherit from tbag.core.middleware.Middleware:', m, caller=self)
                continue
            middlewares.append(instance)
            logger.info('middleware:', middleware, caller=self)
        options.define('middlewares', middlewares, help='set web api middlewares')
        logger.info('load middleware done <<<', caller=self)

    def _init_application(self):
        """ 初始化HTTP监听服务
        """
        settings = {
            'debug': self.debug,
            'cookie_secret': self.cookie_secret
        }
        app = Application(self.handlers, **settings)
        app.listen(self.http_port)
        logger.info('listen http port at:', self.http_port, caller=self)

    def _do_heartbeat(self):
        """ 服务器心跳
        """
        from tbag.core.heartbeat import heartbeat
        IOLoop.current().call_later(1, heartbeat.start)
