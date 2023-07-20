#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  app.py
@Time    :  2023/07/10 09:13:06
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  app
'''
from app.utils import client, cache_pool
from fastapi import FastAPI, Request, Response
from app.route import routes
from app.db import db
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> any:
    '''
    创建app实例
    :return app,fastapi实例
    '''
    # 先创建数据库、表
    db.Base.metadata.create_all(db.engine)
    # 再实例化接口
    app = FastAPI()

    # 添加自定义的中间件
    @app.middleware("http")
    async def check_white_list(request: Request, call_next):
        '''白名单设置'''
        if cache_pool.status:
            # 获取请求IP
            ip = request.client.host
            x_real_ip = request.headers.get("X-Real-IP", "")
            x_forwarded_for = request.headers.get("X-Forwarded-For", "")
            if ip not in cache_pool.getter() and x_real_ip not in cache_pool.getter() and x_forwarded_for not in cache_pool.getter():
                return Response(status_code=403)
        response = await call_next(request)
        return response
    # 添加跨域设置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    # 先初始化docker客户端
    _ = client.Client()
    # 初始化路由
    app.include_router(routes)
    return app
