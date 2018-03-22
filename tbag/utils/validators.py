# -*- coding:utf-8 -*-

"""
validator 字段校验
Author: huangtao
Date:   2018/03/21
Update: None
"""

from tbag.utils import datetime_help
from tbag.core import exceptions


def _field(data, field=None, required=True):
    if field:
        data = data or {}
        if not isinstance(data, dict):
            raise exceptions.SystemError()
        if required and field not in data:
            raise exceptions.ValidationError('{field}必填'.format(field=field))
        return data.get(field)
    else:
        return data


def bool_field(data, field=None, required=True):
    """ bool类型检查
    @param data 如果field不为None，那么field从data里取值，否则判断data是否为bool类型
    @param field 如果不为None，那么需要从data里提取值
    @param required 是否data里必须存在field字段，如果字段不存在且required为False，返回None
    """
    field_data = _field(data, field, required)
    if str(field_data).lower() == 'true':
        return True
    if str(field_data).lower() == 'false':
        return False
    if not required:
        return None
    raise exceptions.ValidationError('{field}是bool类型'.format(field=field))


def int_field(data, field=None, required=True):
    """ int类型检查
    @param data 如果field不为None，那么field从data里取值，否则判断data是否为int类型
    @param field 如果不为None，那么需要从data里提取值
    @param required 是否data里必须存在field字段，如果字段不存在且required为False，返回None
    """
    field_data = _field(data, field, required)
    if not field_data and not required:
        return None
    try:
        return int(field_data)
    except:
        raise exceptions.ValidationError('{field}是int类型'.format(field=field))


def float_field(data, field=None, required=True):
    """ float类型检查
    @param data 如果field不为None，那么field从data里取值，否则判断data是否为float类型
    @param field 如果不为None，那么需要从data里提取值
    @param required 是否data里必须存在field字段，如果字段不存在且required为False，返回None
    """
    field_data = _field(data, field, required)
    if not field_data and not required:
        return None
    try:
        return float(field_data)
    except:
        raise exceptions.ValidationError('{field}是float类型'.format(field=field))


def char_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    return str(field_data) if field_data is not None else None


def datetime_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    try:
        return datetime_help.parse_datetime(field_data) if field_data is not None else None
    except:
        raise exceptions.ValidationError('%s是ISO_8601格式的时间字符串' % field)


def date_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    try:
        return datetime_help.parse_date(field_data) if field_data is not None else None
    except:
        raise exceptions.ValidationError('%s是ISO_8601格式的日期字符串' % field)


def list_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    if field_data is None:
        return None
    if not isinstance(field_data, list):
        raise exceptions.ValidationError('%s是列表' % field)
    return field_data


def dict_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    if field_data is None:
        return None
    if not isinstance(field_data, dict):
        raise exceptions.ValidationError('%s是字典' % field)
    return field_data
