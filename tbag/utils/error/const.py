# -*- coding:utf-8 -*-

"""
错误码对应的错误原因
Author: huangtao
Date:   2017/09/21
"""


# 成功消息
MSG_OK = {'code': 0, 'msg': '请求成功'}


# 部分HTTP错误码对照自定义格式错误
ERR_MSG_INVALID = {'code': 400, 'msg': '请求失败'}
ERR_MSG_PERMISSION_ERROR = {'code': 401, 'msg': '权限不够'}
ERR_MSG_BODY_ERROR = {'code': 411, 'msg': '请求body数据格式错误'}
ERR_MSG_SYSTEM_ERROR = {'code': 500, 'msg': '系统内部错误'}
ERR_MSG_MIC_SRV_ERROR = {'code': 510, 'msg': '请求微服务失败'}
