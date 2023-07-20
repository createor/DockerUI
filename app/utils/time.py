#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  time.py
@Time    :  2023/07/13 15:56:31
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  获取时间
'''
from datetime import datetime


def get_time() -> str:
    '''
    获取当前时间
    :return 以YYYY-mm-dd HH:MM:SS格式返回时间字符串
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
