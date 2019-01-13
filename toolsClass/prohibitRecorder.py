#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 15:16
# @Author  : Liquid
# @Site    : 
# @File    : prohibitRecorder.py
# @Software: PyCharm
import time

from lib.redis_coon.redis_conn import conn


class ProhibitRecorder(object):
    def __init__(self, key_name):
        conn.hset(key_name, 'visit_num', 1)
        conn.hset(key_name, 'last_visit_time', time.time())
        conn.hset(key_name, 'target_url', '')

    @classmethod
    def set_target_url(cls, key_name, url):
        conn.hset(key_name, 'target_url', url)

    @classmethod
    def get_target_url(cls, key_name):
        return conn.hget(key_name, 'target_url').decode()

    @classmethod
    def get_visit_num(cls, key_name):
        return conn.hget(key_name, 'visit_num').decode()

    @classmethod
    def update_last_visit_time(cls, key_name):
        conn.hset(key_name, 'last_visit_time', time.time())

    @classmethod
    def visit_num_increment(cls, key_name):
        conn.hset(key_name, 'visit_num', int(conn.hget(key_name, 'visit_num').decode())+1)

    @classmethod
    def get_all_key(cls, key_name):
        return {k.decode(): v.decode() for k, v in conn.hgetall(key_name).items()}

