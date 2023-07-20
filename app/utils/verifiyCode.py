#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  verifiyCode.py
@Time    :  2023/07/14 09:05:23
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  验证码模块
'''
import uuid
import random
import string
from datetime import datetime, timedelta
from app.utils.time import get_time
import threading
import time


class Code(object):
    def __init__(self) -> None:
        '''
        验证码模块
        '''
        self.data = {}  # {user: {uuid: {code,create_time,expire_time}}}
        self._thread = None

    @classmethod
    def instance(cls, *args, **kwargs):
        '''
        返回唯一实例
        '''
        if not hasattr(Code, "_instance"):
            Code._instance = Code(*args, **kwargs)
        return Code._instance

    def _uuid(self) -> str:
        '''
        获取uuid
        '''
        return str(uuid.uuid1())

    def _random(self) -> str:
        '''
        或者随机验证码的值
        '''
        s = string.digits+string.ascii_letters
        t = ""
        for i in range(6):
            rs = random.choice(s)  # 随机数
            t += rs
        return t

    def _compare(self, t1: str, t2: str, minus: int = 1) -> bool:
        '''
        比较两个时间查是否超过指定时间
        :param t1, 开始时间
        :param t2, 结束时间
        :param minus, 时间差
        :return t1是否大于t2
        '''
        t = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
        t = t + timedelta(minutes=minus)
        return t > datetime.strptime(t2, '%Y-%m-%d %H:%M:%S')

    def _get_time(self, t: str, expire: int = 5) -> str:
        '''
        获取指定时间后的时间
        :param t, 原始时间
        :param expire, 指定时间
        :return 时间字符串
        '''
        t1 = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        t1 = t1 + timedelta(minutes=expire)
        return t1.strftime('%Y-%m-%d %H:%M:%S')

    def _clear(self, wait: int = 3):
        '''
        清理过期数据
        :param wait, 任务时间
        '''
        time.sleep(60 * wait)
        localTime = get_time()
        for k, v in self.data.copy().items():
            if self._compare(localTime, v["expire_time"]):
                del self.data[k]

    def getter(self, key, value) -> int:
        '''
        获取验证码
        '''
        if key in self.data:
            localTime = get_time()
            data = self.data[key]
            del self.data[key]  # 删除数据
            if self._compare(data["expire_time"], localTime):
                if data["code"].lower() == value.lower():
                    return 0  # 校验正确
                else:
                    return 1003  # 校验错误
            else:
                return 1002  # 验证码过期
        return 1001  # uuid不存在

    def setter(self) -> tuple:
        '''
        设置验证码
        :param user, 用户名
        :param length, 每个用户每天获取验证码次数
        '''
        t1 = self._uuid()
        t2 = self._random()
        localTime = get_time()
        self.data[t1] = {
            "code": t2,
            "create_time": localTime,  # 创建时间
            "expire_time": self._get_time(localTime)  # 过期时间
        }
        return [t1, t2]

    def remove(self, key):
        '''
        删除值
        '''
        if key in self.data:
            del self.data[key]

    def task(self):
        '''
        定时任务线程
        '''
        if self._thread:
            return
        self._thread = threading.Thread(target=self._clear, args=())
        self._thread.start()
