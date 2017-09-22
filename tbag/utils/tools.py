# -*- coding:utf-8 -*-

"""
工具包

Author: huangtao
Date:   2017/09/21
"""

import time
import datetime


class TimeTool(object):
    """ time时间工具
    """

    @classmethod
    def get_cur_timestamp(cls):
        """ 获取当前时间戳
        """
        ts = int(time.time())
        return ts


class DatetimeTool(object):
    """ datetime日期工具
    """

    @classmethod
    def get_cur_datetime_m(cls):
        """ 获取当前日期时间字符串，包含 年 + 月 + 日 + 时 + 分 + 秒 + 微妙
        """
        today = datetime.datetime.today()
        str_m = today.strftime('%Y%m%d%H%M%S%f')
        return str_m

    @classmethod
    def get_datetime(cls):
        """ 获取日期时间字符串，包含 年 + 月 + 日 + 时 + 分 + 秒
        """
        today = datetime.datetime.today()
        str_dt = today.strftime('%Y%m%d%H%M%S')
        return str_dt

    @classmethod
    def get_date(cls):
        """ 获取日期字符串，包含 年 + 月 + 日
        """
        today = datetime.datetime.today()
        str_d = today.strftime('%Y%m%d')
        return str_d

    @classmethod
    def get_utc_time(cls):
        """ 获取当前utc时间
        """
        utc_t = datetime.datetime.utcnow()
        return utc_t
