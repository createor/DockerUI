#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/10 15:18:23
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  容器视图
'''
# from typing import Union
from fastapi import APIRouter, WebSocket, Depends
from app.containers.query import query_containers
from app.containers.operate import operate_container, cat_container_log, conn_container
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.db import logRecord as log
from app.user.view import User, get_current_user

containers = APIRouter()


@containers.get("/list")
async def get_containers_list(current_user: User = Depends(get_current_user)):
    data = query_containers()
    log.create_log(log.LogRecord(content="查询容器列表", operate_type="3", operate_user=current_user.uid))
    return {"msg": "success", "count": len(data), "data": data, "code": 0}


class Operate(BaseModel):
    id: str
    name: str
    operateType: str


@containers.post("/operate")
async def set_container_status(operate: Operate, current_user: User = Depends(get_current_user)):
    isSucc = operate_container(operate.name, operate.operateType)
    operate_name = "启动" if operate.operateType == "1" else "停止"
    if isSucc:
        log.create_log(log.LogRecord(content="{}容器{}成功".format(operate_name, operate.name), operate_type="3", operate_user=current_user.uid))
        return {"msg": "success", "data": "", "code": 0}
    else:
        log.create_log(log.LogRecord(content="{}容器{}失败".format(operate_name, operate.name), operate_type="3", operate_user=current_user.uid))
        return {"msg": "failed", "data": "", "code": -1}


@containers.get("/log/{container_name}")
async def get_container_log(container_name: str, current_user: User = Depends(get_current_user)):
    log.create_log(log.LogRecord(content="查看容器{}日志".format(container_name), operate_type="3", operate_user=current_user.uid))
    return StreamingResponse(cat_container_log(container_name))


@containers.websocket("/ws/{container_name}")
async def websocket_endpoint(*, websocket: WebSocket, container_name: str):
    log.create_log(log.LogRecord(content="连接容器{}".format(container_name), operate_type="3"))
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        message = conn_container(container_name, data)[1]
        await websocket.send_text(message.decode())
