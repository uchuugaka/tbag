# -*- coding:utf-8 -*-

from tbag.utils.error import const


class AuthError(Exception):
    """ 权限校验失败
    """

    def __init__(self, err=const.ERR_MSG_PERMISSION_ERROR, data=None):
        self.msg = err['msg']
        self.code = err['code']
        self.data = data

    def __str__(self):
        str_msg = '[{code}] {msg}'.format(**{'code': self.code, 'msg': self.msg})
        return str_msg


class CustomError(Exception):
    """ 通用类型错误
    """

    def __init__(self, err=const.ERR_MSG_INVALID, data=None):
        self.msg = err['msg']
        self.code = err['code']
        self.data = data

    def __str__(self):
        str_msg = '[{code}] {msg}'.format(**{'code': self.code, 'msg': self.msg})
        return str_msg


class ParamError(Exception):
    """ http参数错误
    """

    def __init__(self, err=const.ERR_MSG_INVALID, data=None):
        self.msg = err['msg']
        self.code = err['code']
        self.data = data

    def __str__(self):
        str_msg = '[{code}] {msg}'.format(**{'code': self.code, 'msg': self.msg})
        return str_msg


class SystemError(Exception):
    """ 系统内部错误
    """

    def __init__(self, err=const.ERR_MSG_SYSTEM_ERROR, data=None):
        self.msg = err['msg']
        self.code = err['code']
        self.data = data

    def __str__(self):
        str_msg = '[{code}] {msg}'.format(**{'code': self.code, 'msg': self.msg})
        return str_msg
