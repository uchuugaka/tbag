# -*- coding:utf-8 -*-

"""
日志打印

Author:     huangtao
Date:       2017/08/22
"""

import os
import sys
import logging

from tornado import log
from tornado.options import options


def initLogger(log_level='debug', log_path=None, logfile_name=None):
    """ 初始化日志输出
    @param log_level 日志级别 debug info
    @param log_path 日志输出路径
    @param logfile_name 日志文件名
    """
    if log_level == 'info':
        options.logging = 'info'
    else:
        options.logging = 'debug'
    logger = logging.getLogger()
    if logfile_name:
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        logfile = os.path.join(log_path, logfile_name)
        print('init logger ...:', logfile)
        handler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
    else:
        handler = logging.StreamHandler()
    fmt_str = '[%(levelname)1.1s %(asctime)s] %(message)s'
    fmt = log.LogFormatter(fmt=fmt_str, datefmt=None)
    handler.setFormatter(fmt)
    logger.addHandler(handler)


def info(*args, **kwargs):
    func_name, kwargs = _log_func_name(*args, **kwargs)
    logging.info(_log(func_name, *args, **kwargs))


def warn(*args, **kwargs):
    func_name, kwargs = _log_func_name(*args, **kwargs)
    logging.warning(_log(func_name, *args, **kwargs))


def debug(*args, **kwargs):
    func_name, kwargs = _log_func_name(*args, **kwargs)
    logging.debug(_log(func_name, *args, **kwargs))


def error(*args, **kwargs):
    logging.error('*' * 40)
    func_name, kwargs = _log_func_name(*args, **kwargs)
    logging.error(_log(func_name, *args, **kwargs))
    logging.error('*' * 40)


exception = error


def _log(func_name, *args, **kwargs):
    _log_msg = func_name
    for l in args:
        if type(l) == tuple :
            ps = str(l)
        else:
            try:
                ps = '%r' % l
            except:
                ps = str(l)
        if type(l) == str:
            _log_msg += ps[1:-1] + ' '
        else:
            _log_msg += ps + ' '
    if len(kwargs) > 0:
        _log_msg += str(kwargs)
    return _log_msg


def _log_func_name(*args, **wkargs):
    """ 获取方法名
    * logger.xxx(... caller=self) for instance method
    * logger.xxx(... caller=cls) for @classmethod
    """
    caller_cls_name = ""
    try:
        _caller = wkargs.get('caller', None)
        if _caller:
            if not hasattr(_caller, '__name__'):
                _caller = _caller.__class__
            caller_cls_name = _caller.__name__
            del wkargs['caller']
    except:
        pass

    func_name_str = '[' + caller_cls_name + '.' + sys._getframe().f_back.f_back.f_code.co_name + '] '
    return func_name_str, wkargs
