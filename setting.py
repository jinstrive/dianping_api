# -*- coding: utf-8 -*-

MONGO_REPLICA_SET = {
    'PRIMARY': ('172.100.102.163', '27019'),
    'SECONDARY': [
        ('172.100.102.163', '27018'),
    ],
    'ARBITER': ('172.100.102.163', '27017'),
    'SET_NAME': 'qfpay',
}