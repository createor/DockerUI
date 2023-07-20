#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  query.py
@Time    :  2023/07/10 15:13:30
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  查询容器列表
'''
from app.utils import cli


def query_containers(**kwargs) -> list:
    '''
    查询容器列表
    '''
    try:
        if len(kwargs) > 0:
            containerList = cli.client.containers.list(**kwargs)
        else:
            containerList = cli.client.containers.list(all=True)
        return [{"id": container.short_id, "name": container.name, "status": container.status} for container in containerList]
    except Exception:
        return []
