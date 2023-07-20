#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  whiteList.py
@Time    :  2023/07/19 10:21:25
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  白名单设置
'''
from app.db.db import Base, session
from sqlalchemy import Column, Integer, String


class WhiteList(Base):
    __tablename__ = "white_list"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String(20), unique=True, nullable=False)


def create_list(w: WhiteList, db: session = session) -> bool:
    '''
    新增白名单
    '''
    result = True
    s = session()
    try:
        s.add(w)
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result


def get_list(skip: int = 0, limit: int = 1, db: session = session, **kwargs) -> list:
    '''
    查询白名单
    '''
    result = []
    with session() as s:
        if len(kwargs) > 0:
            if limit == 0:
                result = s.query(WhiteList).filter_by(**kwargs).all()
            else:
                result = s.query(WhiteList).filter_by(**kwargs).offset(skip).limit(limit).all()
        else:
            if limit == 0:
                result = s.query(WhiteList).all()
            else:
                result = s.query(WhiteList).offset(skip).limit(limit).all()
    return result


def count_list(db: session = session) -> int:
    '''
    统计白名单数量
    '''
    with session() as s:
        return s.query(WhiteList).count()


def del_list(db: session = session, **kwargs) -> bool:
    '''
    删除白名单
    '''
    result = True
    s = session()
    try:
        s.query(WhiteList).filter_by(**kwargs).delete()
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result
