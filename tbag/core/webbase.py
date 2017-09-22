# -*- coding:utf-8 -*-

"""
    web基类
"""

import json
import datetime

from tornado.web import RequestHandler

from tbag.utils.error import errors, const


class WebHandler(RequestHandler):
    """ web基类
    """

    @property
    def data(self):
        if self.request.body:
            return json.loads(self.request.body.decode('utf-8'))
        else:
            return {}

    def _to_representation(self, instance):
        if isinstance(instance, datetime.datetime):
            return instance.isoformat() + 'Z'

        if isinstance(instance, datetime.date):
            return instance.isoformat()

        if isinstance(instance, list):
            return [self._to_representation(item) for item in instance]

        if isinstance(instance, dict):
            for key in instance.keys():
                instance[key] = self._to_representation(instance[key])
            return instance

        else:
            return instance

    def get_param(self, key, defaut=None):
        """ 获取uri里边携带的参数
        * 直接调用 self.get_argument 如果不附加默认值，如果参数不存在，将会抛异常
        @param key 参数名
        @param defaut 默认如果参数不存在，就赋值None
        @return value 返回的参数值
        """
        value = self.get_argument(key, defaut)
        return value

    def get_params(self, *keys):
        """ 获取uri里边携带的参数
        @param keys 参数名列表
        @return values 返回的参数值列表
        """
        values = []
        for key in keys:
            value = self.get_param(key)
            values.append(value)
        return values

    def get_body(self, parse_json=True):
        """ 提取http请求的body数据
        @param parse_json 是否将body数据解析成json格式
        @return body http请求的body数据
        """
        body = self.request.body
        if not body:
            return None
        if parse_json:
            try:
                body = json.loads(body.decode('utf8'))
            except:
                raise errors.CustomError(const.ERR_MSG_BODY_ERROR)
        return body

    def do_success(self, data={}, msg='success'):
        """ API成功返回
        """
        results = {
            'code': 0,
            'msg': msg,
            'data': self._to_representation(data)
        }
        self.finish(results)

    def do_failed(self, code=400, msg='error', data={}):
        """ API失败返回
        """
        results = {
            'code': code,
            'msg': msg,
            'data': self._to_representation(data)
        }
        self.set_status(200, 'OK')
        self.finish(results)

    def do_http_error(self, err_code=500, msg='error'):
        """ http失败返回
        """
        self.set_status(err_code, msg)
        self.finish()

    def write_error(self, status_code, **kwargs):
        """ 这儿可以捕获自定义异常类
        """
        exc_info = kwargs.get("exc_info")
        ex = exc_info[1]

        if isinstance(ex, (errors.CustomError, errors.AuthError, errors.ParamError, errors.SystemError)):
            self.do_failed(ex.code, ex.msg, ex.data)
        else:
            self.do_http_error(500, 'SYSTEM ERRROR')
