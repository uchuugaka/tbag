# -*- coding: utf-8 -*-

from utils import datetime_help
from core.exceptions import ValidationError


def _field(data, field=None, required=True):
    data = {} if data is None else data
    field_data = data.get(field) if field else data

    if required and field_data is None:
        raise ValidationError('%s必填' % field)
    if data is None:
        return None
    return field_data


def bool_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    if str(field_data).lower() == 'true':
        return True
    if str(field_data).lower() == 'false':
        return False
    raise ValidationError('%s是bool类型' % field)


def int_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    try:
        return int(field_data) if field_data is not None else None
    except:
        raise ValidationError('%s是整数' % field)


def float_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    try:
        return float(field_data) if field_data is not None else None
    except:
        raise ValidationError('%s是浮点数' % field)


def char_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    return str(field_data) if field_data is not None else None


def datetime_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    try:
        return datetime_help.parse_datetime(field_data) if field_data is not None else None
    except:
        raise ValidationError('%s是ISO_8601格式的时间字符串' % field)


def date_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    try:
        return datetime_help.parse_date(field_data) if field_data is not None else None
    except:
        raise ValidationError('%s是ISO_8601格式的日期字符串' % field)


def list_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    if field_data is None:
        return None
    if not isinstance(field_data, list):
        raise ValidationError('%s是列表' % field)
    return field_data


def dict_field(data, field=None, required=True):
    field_data = _field(data, field, required)
    if field_data is None:
        return None
    if not isinstance(field_data, dict):
        raise ValidationError('%s是字典' % field)
    return field_data


__all__ = [int_field, char_field, float_field, date_field, datetime_field, list_field, dict_field, bool_field]
