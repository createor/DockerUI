#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  run.py
@Time    :  2023/07/10 09:12:17
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  运行脚本
'''
import uvicorn
from app import app


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=1521)
