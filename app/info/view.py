#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/17 11:39:34
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  None
'''
from fastapi import APIRouter
from app.info.query import query_cpu_usage, query_mem_usage, query_version

info = APIRouter()


@info.get("/version")
def get_docker_version():
    return {"msg": "success", "version": query_version(), "code": 0}


@info.get("/system")
def get_system_usage():
    return {"msg": "success", "data": {"cpu_usage": query_cpu_usage(), "mem_usage": query_mem_usage()}, "code": 0}


# 程序保活接口
@info.get("/alive")
def keepalive():
    return {"msg": "success", "code": 0}
