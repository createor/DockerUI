#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  config.py
@Time    :  2023/07/19 10:14:58
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  配置表
'''
from app.db.db import Base, session
from sqlalchemy import Column, Integer, String
from typing import Union


class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(200), nullable=False)


def create_config(conf: Config, db: session = session) -> bool:
    '''
    新增配置
    '''
    result = True
    s = session()
    try:
        s.add(conf)
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result


def get_config(db: session = session, **kwargs) -> Union[Config, list]:
    '''
    查询配置
    '''
    with session() as s:
        if len(kwargs) > 0:
            return s.query(Config).filter_by(**kwargs).first()
        else:
            return s.query(Config).all()


def update_config(key: str, value: str, db: session = session) -> bool:
    '''
    更新配置
    '''
    result = True
    s = session()
    try:
        s.query(Config).filter(Config.key == key).update({Config.value: value})
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result
