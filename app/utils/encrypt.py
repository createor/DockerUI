#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  encrypt.py
@Time    :  2023/07/12 09:24:43
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  md5加密数据
'''
import hashlib


def encrypt_data(data: str, salt: str = "DockerUI") -> str:
    '''
    使用md5加密数据
    :param data, 需要加密的数据
    :param salr, 加盐值
    :return, 返回32位加密后的字符串
    '''
    source_data = data + salt
    return hashlib.md5(source_data.encode()).hexdigest()
