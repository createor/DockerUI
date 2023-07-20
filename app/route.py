#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  route.py
@Time    :  2023/07/10 09:25:04
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  路由文件
'''
from fastapi import APIRouter
from app.images.view import images
from app.containers.view import containers
from app.user.view import users
from app.info.view import info
from app.log.view import logs
from app.config.view import conf

routes = APIRouter()

routes.include_router(images, prefix="/api/image", tags=["镜像相关接口"])
routes.include_router(containers, prefix="/api/container", tags=["容器相关接口"])
routes.include_router(users, prefix="/api/user", tags=["用户相关接口"])
routes.include_router(logs, prefix="/api/log", tags=["日志相关接口"])
routes.include_router(info, prefix="/api/info", tags=["系统信息相关接口"])
routes.include_router(conf, prefix="/api/config", tags=["系统配置相关接口"])
