#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/19 10:48:55
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  None
'''
from fastapi import APIRouter
from pydantic import BaseModel
from app.db.whiteList import WhiteList, create_list, count_list, get_list, del_list
from app.db.config import get_config

conf = APIRouter()


# 查询白名单
@conf.get("/whitelist")
async def query_white_list(page: int, limit: int):
    count = count_list()
    data = get_list(skip=page - 1, limit=limit)
    return {"msg": "success", "count": count, "data": [{"id": i.id, "ip": i.ip} for i in data], "code": 0}


class WhiteMember(BaseModel):
    ip: str


@conf.post("/addip")
async def add_white_list(w: WhiteMember):
    isExist = get_list(ip=w.ip)
    if len(isExist) > 0:
        return {"msg": "ip已存在", "code": 0}
    isSucc = create_list(WhiteList(ip=w.ip))
    if isSucc:
        return {"msg": "success", "code": 0}
    else:
        return {"msg": "failed", "code": -1}


@conf.post("/delip")
async def del_white_list(w: WhiteMember):
    isSucc = del_list(ip=w.ip)
    if isSucc:
        return {"msg": "success", "code": 0}
    else:
        return {"msg": "failed", "code": -1}


@conf.get("/all")
async def query_config():
    return {"msg": "success", "data": get_config(), "code": 0}


class BaseConfig(BaseModel):
    pass


@conf.post("/update")
async def set_config():
    pass
