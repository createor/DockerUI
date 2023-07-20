#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/20 11:41:24
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  None
'''
from fastapi import APIRouter, UploadFile


upload = APIRouter()


# 上传镜像
@upload.post("/image")
async def upload_image(file: UploadFile):
    try:
        filename = ''
        with open(filename, 'wb') as f:
            f.write(file.file.read())
        return {"msg": "success", "code": 0}
    except Exception:
        return {"msg": "failed", "code": -1}
