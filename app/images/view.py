#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/10 09:45:14
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  容器视图
'''
from fastapi import APIRouter
from app.images.query import query_images, search_images
from app.images.operate import export_image
from fastapi.responses import StreamingResponse

images = APIRouter()


# 查询镜像列表
@images.get("/list")
async def get_images_list():
    data = query_images()
    return {"msg": "success", "count": len(data), "data": data, "code": 0}


# 从仓库搜索镜像
@images.get("/search")
async def search_images_list(name: str):
    data = search_images(name)
    return {"msg": "success", "data": data, "code": 0}


# 导出镜像
@images.get("/export")
def export_image_file(name: str):
    def iterFile():
        for chunk in export_image(name):
            yield chunk
    return StreamingResponse(iterFile(), media_type="application/x-tar")
