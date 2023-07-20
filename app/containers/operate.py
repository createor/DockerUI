#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  operate.py
@Time    :  2023/07/10 15:28:36
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  操作容器
'''
from app.utils import cli
from typing import Union


def operate_container(id_or_name: str, operateType: str) -> bool:
    '''
    启动停止状态的容器
    :param id_or_name, 容器ID或者名称
    :param operateType, 操作类型, 1-启动, 2-停止
    :return 操作是否成功
    '''
    try:
        container = cli.client.containers.get(id_or_name)
        if operateType == '1':
            container.start()
        if operateType == '2':
            container.stop()
        if operateType == '3':
            container.remove()
        return True
    except Exception:
        return False


def cat_container_log(id_or_name) -> str:
    '''
    查看容器日志
    :param id_or_name, 容器ID或者名称
    :return 日志字符串
    '''
    try:
        container = cli.client.containers.get(id_or_name)
        return container.logs(stream=True, follow=True)  # 返回可迭代字符串
    except Exception:
        return ''


def conn_container(id_or_name: str, cmd: str) -> Union[tuple, str]:
    '''
    连接容器执行命令
    :param id_or_name, 容器ID或者名称
    :param cmd, 执行的命令
    :return 返回操作结果或者空字符串
    '''
    try:
        container = cli.client.containers.get(id_or_name)
        return container.exec_run(cmd)
    except Exception:
        return ''


def rename_container(id_or_name: str, newName: str) -> bool:
    '''
    重命名容器
    :param id_or_name, 容器ID或者名称
    :param newName, 新的容器名
    '''
    result = True
    try:
        container = cli.client.containers.get(id_or_name)
        container.rename(newName)
    except Exception:
        result = False
    finally:
        return result
