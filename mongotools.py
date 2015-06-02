# -*- coding: utf-8 -*-
import pymongo
from setting import MONGO_REPLICA_SET
from functools import partial
import ConfigParser


# Mongo Replica Set Client
def get_replica_set_client():
    seeds = [MONGO_REPLICA_SET['PRIMARY']] + MONGO_REPLICA_SET[
        'SECONDARY']
    rs_client = pymongo.MongoReplicaSetClient(','.join([':'.join(addr) for addr in seeds]),
                                              document_class=dict,
                                              replicaSet=MONGO_REPLICA_SET['SET_NAME'],
                                              use_greenlets=True,
                                              secondary_acceptable_latency_ms=100,
                                              read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED)
    return rs_client


mongo_cliet = get_replica_set_client()

class MongoFieldMapping(object):
    """
    Mongo Field 对应类 初始化调用
    """
    def __init__(self, fp='mongo_field_mapping.cfg'):
        self.filepath = fp
        cf = ConfigParser.ConfigParser()
        cf.read(fp)
        self.field_list = cf.sections()
        self.field_dict = {key: dict(cf.items(key)) for key in self.field_list}

    def keys(self):
        return self.field_list

    def items(self):
        return self.field_dict

    def __getattr__(self, key):
        return self.field_dict[key]

    def __repr__(self):
        return str(self.field_dict)

    def __str__(self):
        return str(self.field_dict)


field_mapper = MongoFieldMapping()


class MongoDBObj(object):
    def __init__(self, db, field_mapper, collection):
        self._db = db
        self._field_mapper = field_mapper
        self._collection = collection

    def __getattr__(self, act):
        return partial(self._emit, self._db, self._collection, act)

    def _emit(self, db, collection, act, *args, **kwargs):
        field_dict = getattr(self._field_mapper, collection)
        # TODO
        # 暂时简单支持，后续修改
        for arg in args:
            if not isinstance(arg, dict):
                continue
            for key in arg.keys():
                if key in field_dict.keys():
                    if key == field_dict[key]:
                        continue
                    arg.update({field_dict[key]: arg[key]})
                    arg.pop(key)
            for val in arg.values():
                if isinstance(val, dict):
                    for k in val.keys():
                        if k in field_dict.keys():
                            if k == field_dict[k]:
                                continue
                            val.update({field_dict[k]: val[k]})
                            val.pop(k)
                if isinstance(val, list):
                    for v in val:
                        if isinstance(v, dict):
                            for vk in v.keys():
                                if vk in field_dict.keys():
                                    if vk == field_dict[vk]:
                                        continue
                                    vk.update({field_dict[vk]: v[vk]})
                                    v.pop(vk)
        print args
        return getattr(getattr(db, collection), act)(*args, **kwargs)


class MongoHelper(object):
    """
    Mongo Helper Class
    """
    def __init__(self, mongo_client, db_name, cfg_file='mongo_field_mapping.cfg'):
        self.client = mongo_client
        self._db_name = db_name
        self._db = getattr(self.client, self._db_name)
        self.field_mapper = MongoFieldMapping(cfg_file)

    def __getattr__(self, collection):
        return MongoDBObj(self._db, self.field_mapper, collection)


mongo_honey = MongoHelper(mongo_cliet, 'honey')


if __name__ == '__main__':
    # mfm = MongoFieldMapping()
    # print mfm.fuck
    # x = mongo_honey.topic.insert({'title': 'i dont know', 'description': 'shit, dont know', 'category_id': 'want more'})
    # print x
    # x = mongo_honey.topic.update({'description': 'shit, dont know'}, {'$set': {'category_id': 100}}, upsert=True, multi=True)
    # print x
    mongo_honey.topic.remove({'cid': 100}, multi=True)
    # mongo_cliet.honey.test.update({'ss': 'shit'}, {'$set': {'text': 'modify data'}}, upsert=True)
    # z = mongo_honey.topic.find({'cid': 100})
    # for x in z:
    #     print x
