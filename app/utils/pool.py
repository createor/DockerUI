#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  pool.py
@Time    :  2023/07/19 10:56:37
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  获取白名单IP池
'''
from app.db.whiteList import get_list
from app.db.config import get_config


class Pool(object):
    def __init__(self):
        '''
        '''
        self.data = [i.ip for i in get_list(limit=0)]
        result = get_config(key="allow_white_list")
        if result:
            if isinstance(result.value, str):
                self.status = bool(int(result.value))
            else:
                self.status = bool(result.value)
        else:
            self.status = False

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Pool, "_instance"):
            Pool._instance = Pool(*args, **kwargs)
        return Pool._instance

    def getter(self) -> list:
        return self.data

    def setter(self, data):
        self.data.append(data)

    def delter(self, data):
        self.data.remove(data)
