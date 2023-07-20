#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  user.py
@Time    :  2023/07/11 14:07:04
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  用户表
'''
from typing import Union
from app.db.db import Base, session
from sqlalchemy import Boolean, Column, Integer, String, desc, asc


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)  # 用户名
    password = Column(String(32), nullable=False)  # md5加密后的密码
    create_user = Column(Integer)  # 创建者的id
    create_time = Column(String(20))  # 创建时间
    status = Column(Boolean, default=True)  # 状态


def create_user(user: User, db: session = session) -> bool:
    '''
    创建用户
    :param db, 会话
    :param user, 用户对象
    :return bool, 是否成功
    '''
    result = True
    s = session()
    try:
        s.add(user)
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result


def get_user(db: session = session, order: str = 'id', orderType: int = 1, skip: int = 0, limit: int = 1, **kwargs) -> list:
    '''
    查询用户
    :param db, 会话
    :param order, 按什么排序
    :param orderType, 排序方式, 1-desc, 2-asc
    :param skip, 需要跳过的数量
    :param limit, 需要查询数量
    :param kwargs, 查询条件
    '''
    result = []
    with session() as s:
        if orderType == 1:
            order = desc(order)
        else:
            order = asc(order)
        if len(kwargs) == 0:
            result = s.query(User).order_by(order).offset(skip).limit(limit).all()
        else:
            result = s.query(User).filter_by(**kwargs).order_by(order).offset(skip).limit(limit).all()
    return result


def count_user(db: session = session, **kwargs) -> int:
    '''
    查询符合条件的用户的数量
    '''
    with session() as s:
        return s.query(User).filter_by(**kwargs).count()


def update_user(uid: str, newPassword: Union[str, None] = None, newStatus: Union[bool, None] = None, db: session = session) -> bool:
    '''
    更新用户密码
    :param uid, 用户id
    :param newPassword, 新的密码
    :param newStatus, 新的状态
    '''
    result = True
    s = session()
    try:
        if newPassword:
            s.query(User).filter(User.id == uid).update({User.password: newPassword})
        if newStatus is not None:
            s.query(User).filter(User.id == uid).update({User.status: newStatus})
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result
