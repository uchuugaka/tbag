# -*- coding:utf-8 -*-

"""
mongodb async操作接口

Author: huangtao
Date:   2017/05/08
"""

import copy

import motor
from bson.objectid import ObjectId
from urllib.parse import quote_plus

from tbag.utils import tools
from tbag.utils import log as logger


MONGO_CONN = None
DELETE_FLAG = 'delete'  # True 已经删除，False 或者没有该字段表示没有删除


def initMongodb(host='127.0.0.1', port=27017, dbuser='', dbpass='', dbname='admin'):
    """ 初始化mongodb连接
    """
    if dbuser and dbpass:
        uri = "mongodb://%s:%s@%s:%s/%s" % (quote_plus(dbuser), quote_plus(dbpass), host, port, dbname)
    else:
        uri = "mongodb://%s:%s" % (host, port)
    mongo_client = motor.motor_tornado.MotorClient(uri)
    global MONGO_CONN
    MONGO_CONN = mongo_client
    logger.info('create mongodb connection pool.')


class DBBase(object):
    """ mongodb 数据库操作接口
    """

    def __init__(self):
        """ 初始化
        * self._db 初始化连接的数据库，子类指定
        * self._table 初始化连接的colletion，子类指定
        """
        self.conn = MONGO_CONN
        self.dao = self.conn[self._db][self._table]

    async def get_list(self, spec={}, fields=None, sort=[], skip=0, limit=9999):
        """ 批量获取数据
        @param spec 查询条件
        @param fields 返回数据的字段
        @param sort 排序规则
        @param skip 查询游标
        @param limit 返回数据条数
        * NOTE: 必须传入limit，否则默认返回数据条数可能因为pymongo的默认值而改变
        """
        if '_id' in spec:
            spec['_id'] = ObjectId(spec['_id'])
        spec[DELETE_FLAG] = {'$ne': True}
        datas = []
        cursor = self.dao.find(spec, fields, sort=sort, skip=skip, limit=limit)
        async for item in cursor:
            item['_id'] = str(item['_id'])
            datas.append(item)
        return datas

    async def find_one(self, spec, fields=None, sort=[]):
        """ 查找单条数据
        @param spec 查询条件
        @param fields 返回数据的字段
        @param sort 排序规则
        """
        data = await self.get_list(spec, fields, sort, limit=1)
        if data:
            return data[0]
        else:
            return None

    async def count(self, spec={}):
        """ 计算数据条数
        @param spec 查询条件
        @param n 返回查询的条数
        """
        spec[DELETE_FLAG] = {'$ne': True}
        n = await self.dao.count(spec)
        return n

    async def insert(self, docs_data):
        """ 插入数据
        @param docs_data 插入数据 dict或list
        @param ret_ids 插入数据的id列表
        """
        docs = copy.deepcopy(docs_data)
        ret_ids = []
        is_one = False
        create_time = tools.get_utc_time()
        if not isinstance(docs, list):
            docs = [docs]
            is_one = True
        for doc in docs:
            doc['_id'] = ObjectId()
            doc['create_time'] = create_time
            doc['modify_time'] = create_time
            ret_ids.append(str(doc['_id']))
        self.dao.insert_many(docs)
        if is_one:
            return ret_ids[0]
        else:
            return ret_ids

    async def update(self, spec, update_fields, upsert=False, multi=False):
        """ 更新
        @param spec 更新条件
        @param update_fields 更新字段
        @param upsert 如果不满足条件，是否插入新数据
        @param multi 是否批量更新
        @return modified_count 更新数据条数
        """
        spec[DELETE_FLAG] = {'$ne': True}
        if '_id' in spec:
            spec['_id'] = ObjectId(spec['_id'])
        set_fields = update_fields.get('$set', {})
        set_fields['modify_time'] = tools.get_utc_time()
        update_fields['$set'] = set_fields
        if not multi:
            result = await self.dao.update_one(spec, update_fields, upsert=upsert)
            return result.modified_count
        else:
            result = await self.dao.update_many(spec, update_fields, upsert=upsert)
            return result.modified_count

    async def delete(self, spec):
        """ 软删除
        @param spec 删除条件
        @return delete_count 删除数据的条数
        """
        spec[DELETE_FLAG] = {'$ne': True}
        if '_id' in spec:
            spec['_id'] = ObjectId(spec['_id'])
        update_fields = {'$set': {DELETE_FLAG: True}}
        delete_count = await self.update(spec, update_fields, multi=True)
        return delete_count

    async def remove(self, spec, multi=False):
        """ 彻底删除数据
        @param spec 删除条件
        @param multi 是否全部删除
        @return deleted_count 删除数据的条数
        """
        if not multi:
            result = await self.dao.delete_one(spec)
            return result.deleted_count
        else:
            result = await self.dao.delete_many(spec)
            return result.deleted_count

    async def distinct(self, key, spec={}):
        """ distinct查询
        @param key 查询的key
        @param spec 查询条件
        @return result 过滤结果list
        """
        spec[DELETE_FLAG] = {'$ne': True}
        if '_id' in spec:
            spec['_id'] = ObjectId(spec['_id'])
        result = await self.dao.distinct(key, spec)
        return result


__all__ = [initMongodb, DBBase]
