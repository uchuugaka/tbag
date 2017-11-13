# -*- coding:utf-8 -*-

"""
    web基类
"""

import json
import datetime

from tornado.options import options
from tornado.web import RequestHandler

from tbag.utils.error import errors, const


class WebHandler(RequestHandler):
    """ web基类
    """

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

    @property
    def data(self):
        return self.get_body()

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
        result = {
            'code': 0,
            'msg': msg,
            'data': self._to_representation(data)
        }
        self.do_finish(result)

    def do_failed(self, code=400, msg='error', data={}):
        """ API失败返回
        """
        result = {
            'code': code,
            'msg': msg,
            'data': self._to_representation(data)
        }
        self.set_status(200, 'OK')
        self.do_finish(result)

    def do_http_error(self, err_code=500, msg='error', data=None):
        """ http失败返回
        """
        self.set_status(err_code, msg)
        self.do_finish(data)

    def do_finish(self, result):
        """ 写入result
        """
        # 跨域
        cors = options.cors
        if cors:
            self.set_header("Access-Control-Allow-Origin", "*")
        self.finish(result)

    def write_error(self, status_code, **kwargs):
        """ 这儿可以捕获自定义异常类
        * 此重写了父类函数
        """
        exc_info = kwargs.get("exc_info")
        ex = exc_info[1]

        if isinstance(ex, (errors.CustomError, errors.AuthError, errors.ParamError, errors.SystemError)):
            self.do_failed(ex.code, ex.msg, ex.data)
        else:
            self.do_http_error(500, 'SYSTEM ERRROR')

    async def head(self, *args, **kwargs):
        await self.process('_head_', *args, **kwargs)

    async def get(self, *args, **kwargs):
        await self.process('_get_', *args, **kwargs)

    async def post(self, *args, **kwargs):
        await self.process('_post_', *args, **kwargs)

    async def put(self, *args, **kwargs):
        await self.process('_put_', *args, **kwargs)

    async def delete(self, *args, **kwargs):
        await self.process('_delete_', *args, **kwargs)

    async def patch(self, *args, **kwargs):
        await self.process('_patch_', *args, **kwargs)

    async def options(self, *args, **kwargs):
        await self.process('_options_', *args, **kwargs)

    async def process(self, func_name, *args, **kwargs):
        """ 处理请求
        @param func_name 方法名 [_head_, _get_, _post_, _put_, _delete_, _patch_, _options_]
        @note 此处执行处理请求前的准备工作和处理请求完成的收尾工作
        """
        func = getattr(self, func_name, None)
        if not func:
            self.do_http_error(404, 'NOT FOUND')
            return
        await self.do_prepare()
        await func(*args, **kwargs)
        await self.do_complete()

    async def do_prepare(self):
        """ 准备工作
        * 在执行http方法之前，可以做类似统计、权限校验等操作
        """
        pass

    async def do_complete(self):
        """ 完成工作
        * 在执行http方法之后，可以做类似统计、日志记录等操作
        """
        pass
