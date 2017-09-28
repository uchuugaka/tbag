# -*- coding:utf-8 -*-

"""
    初始化日志、uri路由、数据库连接，启动服务器心跳
"""

import os

from tornado.ioloop import IOLoop
from tornado.options import options

from tbag.utils.routes import route
from tbag.utils import log as logger


class TornadoContext(object):
    """ 初始化日志、uri路由、数据库连接，启动服务器心跳
    """

    def __init__(self, **kwargs):
        """ 初始化
        @param kwargs 配置选项入参
            `run_mode`  运行模式，online为线上服务器，inner-test为内测测试服，test为测试服，console为本地调试
                        online/inner-test/test模式将会把日志写入日志文件，console模式不写日志文件而打印到控制台
            `log_level` 日志级别 DEBUG/INFO
            `log_path`  日志保存路径
            `log_name`  日志名
            `handler_pathes`    uri注册处理器路径
            `http_port` HTTP监听端口号
            `mysql_config`  mysql配置
            `mongo_config`  mongodb配置
        """
        configs = kwargs
        src_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        root_dir = os.path.dirname(src_dir)
        self.src_dir = src_dir
        self.root_dir = root_dir

        # 运行模式
        self.run_mode = configs.get('run_mode', 'console')

        # 日志配置
        self.log_level = configs.get('log_level', 'DEBUG')
        self.log_path = configs.get('log_level', '/tmp/logs')
        self.log_name = configs.get('log_level', 'tbag.log')

        # uri处理路径
        self.handler_pathes = configs.get('handler_pathes')

        # HTTP监听端口号
        self.http_port = configs.get('http_port')

        # mysql配置
        self.mysql_config = configs.get('mysql_config')

        # mongodb配置
        self.mongo_config = configs.get('mongo_config')

        self._init_logger()
        self._init_db_instance()
        self._init_uri_routes()
        self._do_hearbeat()

    def _init_logger(self):
        """ 初始化日志
        """
        if self.run_mode == 'console':
            logger.initLogger()
        else:
            logfile = '%s_%s.log' % (self.log_name.split('.')[0], self.http_port)
            logger.initLogger(self.log_level, self.log_path, logfile)
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
            pass
        if self.mongo_config:
            from tbag.core.db.mongo import initMongodb
            logger.info('mongodb config:', self.mongo_config, caller=self)
            initMongodb(**self.mongo_config)
        logger.info('init db instance done <<<', caller=self)

    def _do_hearbeat(self):
        """ 服务器心跳
        """
        from tbag.core.heart_beat import heart_beat
        IOLoop.current().call_later(2, heart_beat.start)
