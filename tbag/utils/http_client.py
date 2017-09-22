# -*- coding:utf-8 -*-

"""
tornado实现的HTTP异步非阻塞客户端

Author: huangtao
Date:   2017/07/31
UPDATE:
    2017/09/19  增加对POST请求body的编码格式区分
"""

import json

from tornado.httputil import url_concat, urlencode
from tornado.httpclient import AsyncHTTPClient

from tbag.utils import log as logger
from tbag.utils.error import errors, const


class AsyncHttpRequests(object):
    """ HTTP异步请求封装
    """

    @classmethod
    async def get(cls, url, params=None, headers=None, decode_type='utf-8', parse_json=True):
        """ HTTP GET 请求
        @param url 请求url
        @param params 请求的uri qurey参数
        @param decode_type 返回body解码格式，默认使用utf-8解码
        @param parse_json 是否解析返回body为json格式，默认为True
        @return data 返回的http body
        """
        if params:
            url = url_concat(url, params)
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url, headers=headers)
        if response.code != 200:
            logger.error('url:', url, 'response code:', response.code, 'response body:', response.body, caller=cls)
            raise errors.CustomError(const.ERR_MSG_INVALID)
        if response.body:
            data = response.body.decode(decode_type)
            if parse_json:
                return json.loads(data)
            else:
                return data
        else:
            return None

    @classmethod
    async def post(cls, url, body=None, headers=None, encode_type='utf-8', decode_type='utf-8', parse_json=True):
        """ HTTP POST 请求
        @param url 请求url
        @param body 请求的body参数
        @param encode_type 请求body编码格式，默认使用utf-8编码
        @param decode_type 返回body解码格式，默认使用utf-8解码
        @param parse_json 是否解析返回body为json格式，默认为True
        @return data 返回的http body
        """
        if body:
            if encode_type == 'utf-8':
                body = json.dumps(body)
            else:
                body = urlencode(body, encoding=encode_type)
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url, method='POST', body=body, headers=headers)
        if response.code != 200:
            logger.error('url:', url, 'post data:', body, 'response code:', response.code, 'response body:',
                         response.body, caller=cls)
            raise errors.CustomError(const.ERR_MSG_INVALID)
        if response.body:
            data = response.body.decode(decode_type)
            if parse_json:
                return json.loads(data)
            else:
                return data
        else:
            return None
