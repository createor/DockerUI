#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  logRecord.py
@Time    :  2023/07/11 14:31:52
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  操作日志记录表
'''
from app.db.db import Base, session
from app.db.user import User
from app.utils import time
from sqlalchemy import Column, Integer, String, desc


class LogRecord(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String)  # 操作内容
    operate_type = Column(String(2))  # 操作类型:1-登陆日志
    operate_user = Column(Integer)  # 操作者
    operate_time = Column(String(20))  # 操作时间


def create_log(log: LogRecord, db: session = session):
    '''创建日志'''
    with session() as s:
        log.operate_time = time.get_time()
        s.add(log)
        s.commit()


def get_log(skip: int = 0, limit: int = 10, db: session = session, **kwargs) -> list:
    '''查询日志'''
    result = []
    with session() as s:
        if len(kwargs) > 0:
            options = []
            if kwargs["operate_type"] and kwargs["operate_type"].strip() != '':
                options.append(LogRecord.operate_type == kwargs["operate_type"].strip())
            if kwargs["operate_user"] and kwargs["operate_user"].strip() != '':
                options.append(User.username.like('%' + kwargs["operate_user"].strip() + '%'))
            if kwargs["operate_start"] and kwargs["operate_start"].strip() != '':
                options.append(LogRecord.operate_time >= kwargs["operate_start"].strip())
            if kwargs["operate_end"] and kwargs["operate_end"].strip() != '':
                options.append(LogRecord.operate_time <= kwargs["operate_end"].strip())
            result = s.query(LogRecord.content, LogRecord.operate_type, LogRecord.operate_time, User.username).join(User, LogRecord.operate_user == User.id).filter(*options).order_by(desc(LogRecord.operate_time)).offset(skip).limit(limit).all()
        else:
            result = s.query(LogRecord.content, LogRecord.operate_type, LogRecord.operate_time, User.username).join(User, LogRecord.operate_user == User.id).order_by(desc(LogRecord.operate_time)).offset(skip).limit(limit).all()
    return result


def count_log(db: session = session, **kwargs) -> int:
    ''''''
    with session() as s:
        if len(kwargs) > 0:
            options = []
            if kwargs["operate_type"] and kwargs["operate_type"].strip() != '':
                options.append(LogRecord.operate_type == kwargs["operate_type"].strip())
            if kwargs["operate_user"] and kwargs["operate_user"].strip() != '':
                options.append(User.username.like('%' + kwargs["operate_user"].strip() + '%'))
            if kwargs["operate_start"] and kwargs["operate_start"].strip() != '':
                options.append(LogRecord.operate_time >= kwargs["operate_start"].strip())
            if kwargs["operate_end"] and kwargs["operate_end"].strip() != '':
                options.append(LogRecord.operate_time <= kwargs["operate_end"].strip())
            return s.query(LogRecord).join(User, LogRecord.operate_user == User.id).filter(*options).count()
        else:
            return s.query(LogRecord).join(User, LogRecord.operate_user == User.id).count()
