#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  query.py
@Time    :  2023/07/11 14:46:00
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  None
'''
from app.utils import cli
import psutil


def query_version() -> str:
    '''
    查询docker版本
    :return 返回版本信息
    '''
    try:
        version = cli.client.version()
        return version
    except Exception:
        return ''


def query_cpu_usage() -> str:
    '''
    获取CPU使用率
    '''
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    return round(sum(cpu_usage) / len(cpu_usage))


def query_mem_usage() -> str:
    '''
    获取内存使用率
    '''
    return round(psutil.virtual_memory().percent)
