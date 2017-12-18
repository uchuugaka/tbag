# -*- coding:utf-8 -*-

"""
错误类型定义
"""


class CustomException(Exception):
    """ 通用异常类型错误
    """
    DEFAULT_MSG = 'A server error occurred.'
    DEFAULT_DATA = None
    DEFAULT_CODE = 500

    def __init__(self, msg=DEFAULT_MSG, code=DEFAULT_CODE, data=DEFAULT_DATA):
        self.msg = msg
        self.data = data
        self.code = code

    def __str__(self):
        str_msg = '[{code}] {msg}'.format(code=self.code, msg=self.msg)
        return str_msg


class ValidationError(CustomException):
    """ 字段校验错误
    """
    DEFAULT_MSG = 'Invalid input.'
    DEFAULT_CODE = 400


class AuthenticationFailed(CustomException):
    """ 权限校验失败
    """
    DEFAULT_MSG = 'Incorrect authentication credentials.'
    DEFAULT_CODE = 401


class NotAuthenticated(CustomException):
    """ 未授权
    """
    DEFAULT_MSG = 'Authentication credentials were not provided.'
    DEFAULT_CODE = 401


class PermissionDenied(CustomException):
    """ 权限不够
    """
    DEFAULT_MSG = 'You do not have permission to perform this action.'
    DEFAULT_CODE = 403


class NotFound(CustomException):
    """ 未找到
    """
    DEFAULT_MSG = 'Not found.'
    DEFAULT_CODE = 404


class ArgumentNoneException(CustomException):
    """ 字段丢失
    """
    DEFAULT_MSG = 'Argument can not be None'
    DEFAULT_CODE = 500


class InvalidOperationException(CustomException):
    """ 非法操作
    """
    DEFAULT_MSG = 'Operation is invalid'
    DEFAULT_CODE = 500


class TimeoutException(CustomException):
    """ 超时
    """
    DEFAULT_MSG = 'Timeout'
    DEFAULT_CODE = 502
