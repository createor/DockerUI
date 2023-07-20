#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  db.py
@Time    :  2023/07/11 14:06:29
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  数据库
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 数据库文件地址
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# 初始化引擎, debug设置echo位true打印sql语句
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# 初始化会话
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 定义基类
Base = declarative_base()
