#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  client.py
@Time    :  2023/07/10 09:17:16
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  获取docker的客户端实例
'''
import docker


class Client(object):
    def __init__(self, url: str = None) -> None:
        '''
        使用单例返回初始化的docker客户端
        :param url, docker服务端地址
        '''
        self.url = url
        self.client = docker.from_env()

    @classmethod
    def instance(cls, *args, **kwargs):
        '''
        返回唯一实例
        '''
        if not hasattr(Client, "_instance"):
            Client._instance = Client(*args, **kwargs)
        return Client._instance
