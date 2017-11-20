# -*- coding:utf-8 -*-

"""
初始化日志、uri路由、数据库连接，启动服务器心跳

Author:     huangtao
Date:       2017/8/8
ChangeLog:  2017/11/20  删除root_dir配置
"""

from tornado.ioloop import IOLoop
from tornado import options

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
            `cors`      是否支持跨域，True为支持，False为不支持，默认False
        """
        configs = kwargs

        # 运行模式
        self.run_mode = configs.get('run_mode', 'console')

        # 日志配置
        self.log_level = configs.get('log_level', 'DEBUG')
        self.log_path = configs.get('log_path', '/tmp/logs')
        self.log_name = configs.get('log_name', 'tbag.log')
        self.log_filename = None

        # uri处理路径
        self.handler_pathes = configs.get('handler_pathes')

        # HTTP监听端口号
        self.http_port = configs.get('http_port')

        # mysql配置
        self.mysql_config = configs.get('mysql_config')

        # mongodb配置
        self.mongo_config = configs.get('mongo_config')

        # 是否支持跨域，True为支持，False为不支持，默认False
        self.cors = configs.get('cors', False)
        options.define('cors', self.cors, help='set http response header `Access-Control-Allow-Origin` to `*`')

        self._init_logger()
        self._print_configures()
        self._init_db_instance()
        self._init_uri_routes()
        self._do_heartbeat()

    def _init_logger(self):
        """ 初始化日志
        """
        if self.run_mode == 'console':
            logger.initLogger()
        else:
            log_filename = '%s_%s.log' % (self.log_name.split('.')[0], self.http_port)
            self.log_filename = log_filename
            logger.initLogger(self.log_level, self.log_path, log_filename)
        options.parse_command_line()

    def _print_configures(self):
        """ 打印配置
        """
        logger.info('RUN MODE:', self.run_mode, caller=self)
        logger.info('log_level:', self.log_level, 'log_path:', self.log_path, 'log_filename:', self.log_filename,
                    caller=self)
        logger.info('handler_pathes:', self.handler_pathes, caller=self)
        logger.info('listen http_port:', self.http_port, caller=self)
        if self.mysql_config:
            logger.info('mysql_config:', self.mysql_config, caller=self)
        if self.mongo_config:
            logger.info('mongo_config:', self.mongo_config, caller=self)

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
        logger.info('init db instance done <<<', caller=self)

    def _do_heartbeat(self):
        """ 服务器心跳
        """
        from tbag.core.heart_beat import heart_beat
        IOLoop.current().call_later(2, heart_beat.start)
