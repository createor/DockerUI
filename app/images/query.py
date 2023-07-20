#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  query.py
@Time    :  2023/07/10 09:14:28
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  查询当前所有的镜像
'''
from ..utils import cli


def query_images(name: str = None) -> list:
    '''
    根据镜像名查询docker本地镜像列表
    :param name, 镜像名, 为空表示查询所有
    :return 返回查询的镜像列表
    '''
    try:
        if name:
            imageList = cli.client.images.list(name=name)
        else:
            imageList = cli.client.images.list(all=True)
        return [{"id": image.short_id[7:], "name": image.tags[0].split(":")[0], "tag": image.tags[0].split(":")[1]} for image in imageList]
    except Exception:
        return []


def search_images(name: str, limit: int = 10) -> list:
    '''
    根据名称从仓库查询镜像
    :param name, 镜像名
    :param limit, 默认限制10条
    :return 返回搜索的镜像列表
    '''
    try:
        imageList = cli.client.images.search(term=name, limit=limit)
        return [{"name": image.name, "star": image.star_count, "is_official": image.is_official, "desc": image.description} for image in imageList]
    except Exception:
        return []
