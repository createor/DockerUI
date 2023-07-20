#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  operate.py
@Time    :  2023/07/18 16:13:23
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  操作镜像
'''
from app.utils import cli


def export_image(id_or_name: str) -> bytes:
    '''
    导出镜像
    '''
    try:
        image = cli.client.images.get(name=id_or_name)
        return image.save()
    except Exception:
        return ''
