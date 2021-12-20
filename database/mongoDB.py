# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/16 下午10:10

import pymongo
from config.loads import mongo_config, properties
from common.log.logger import log


class MongoDB:

    def __init__(self, host=None, username=None, password=None):
        # 初始化，默认根据environment从配置文件加载
        version = properties.get("environment")
        self.default_mongo_info = mongo_config.get(version)
        if host is None:
            host = self.default_mongo_info.get("host")
        if username is None:
            username = self.default_mongo_info.get("username")
        if password is None:
            password = self.default_mongo_info.get("password")
        database = self.default_mongo_info.get("database")
        self.uri = "mongodb://{0}:{1}@{2}/{3}?authMechanism=SCRAM-SHA-1".format(username, password, host, database)
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[database]
        log.info("Mongo Database 连接成功...")
        self.collection = None

    def get_collection(self, collection):
        # 校验集合是否存在
        if not self.db:
            raise MongoDBExistError(self.client.list_database_names())
        collection_list = self.db.list_collection_names()
        if collection not in collection_list:
            raise MongoCollectionExistError(self.db, collection_list)
        collection_name = collection
        self.collection = self.db[collection]
        log.info("Mongo 装载{}成功".format(collection_name))

    def find_one(self):
        # 查询数据
        """
        查询第一条数据
        :return:
        """
        if self.collection:
            result = self.collection.find_one()
            return result
        else:
            raise MongoInitError

    def show(self, columns=None, flag=1):
        """
        查询所有，支持展示部分列
        :param columns: 字段名，列表
        :param flag: 1或0，表示展示或隐藏，默认为1（展示）
        :return: 数组
        """
        result = []
        conditions = {}
        if columns:
            for i in columns:
                conditions[i] = flag
        if self.collection:
            if conditions:
                for x in self.collection.find({}, conditions):
                    result.append(x)
            else:
                for x in self.collection.find():
                    result.append(x)
            return result
        else:
            raise MongoInitError

    def find(self, **kwargs):
        """
        根据查询条件查询指定数据
        :param kwargs: 参数字典
        :return: 数组
        """
        result = []
        for x in self.collection.find(kwargs):
            result.append(x)
        return result


class MongoConnectionException(BaseException):

    def __init__(self, uri):
        self.uri = uri

    def __str__(self):
        exception_msg = "Mongo connection error, uri: {}".format(self.uri)
        return exception_msg


class MongoDBExistError(BaseException):

    def __init__(self, db_list):
        self.db_list = db_list

    def __str__(self):
        exception_msg = "Mongo db doesn't exist in below:\n{0}".format(self.db_list)
        return exception_msg


class MongoCollectionExistError(BaseException):

    def __init__(self, db, collection_list):
        self.db = db
        self.collection_list = collection_list

    def __str__(self):
        exception_msg = "Mongo db 【{0}】doesn't contains the collection, collection list: \n{1}.".format(
            self.db, self.collection_list)
        return exception_msg


class MongoInitError:

    def __str__(self):
        exception_msg = "Mongo init should set db and collection in order."
        return exception_msg


if __name__ == "__main__":
    properties["environment"] = "v3.maria"
    mongo_client = MongoDB()
    mongo_client.get_collection(collection="Workflow.NodeInst.Log.chunks")
    print(mongo_client.find_one())
