#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/14 10:24:24
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  日志视图
'''
from fastapi import APIRouter
from app.db import logRecord as log


logs = APIRouter()


# 操作日志查询接口
@logs.get("/record")
async def get_log_record(page: int = 0, limit: int = 10, operateType: str = None, operateUser: str = None, operateStart: str = None, operateEnd: str = None):
    data = [{"user": i.username, "time": i.operate_time, "type": i.operate_type, "content": i.content} for i in log.get_log(skip=page - 1, limit=limit, operate_type=operateType, operate_user=operateUser, operate_start=operateStart, operate_end=operateEnd)]
    return {"msg": "success", "count": log.count_log(operate_type=operateType, operate_user=operateUser, operate_start=operateStart, operate_end=operateEnd), "data": data, "code": 0}
