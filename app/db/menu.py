#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  menu.py
@Time    :  2023/07/13 10:50:03
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  菜单表
'''
from app.db.db import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey, asc


class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(String(20), unique=True)  # 菜单ID
    menu_name = Column(String(50), nullable=False)  # 菜单名称
    sort = Column(Integer)  # 顺序


class MenuWithUser(Base):
    __tablename__ = "menu_with_user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(String(20), ForeignKey('menu.menu_id'), nullable=False)  # 菜单ID
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 用户ID


def delete_menu_with_user(uid: str, db: session = session) -> bool:
    '''
    删除用户与菜单的绑定关系
    '''
    result = True
    s = session()
    try:
        s.query(MenuWithUser).filter(MenuWithUser.user_id == uid).delete()
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result


def create_menu_with_user(data: MenuWithUser, db: session = session) -> bool:
    '''
    创建用户绑定菜单
    '''
    result = True
    s = session()
    try:
        s.add(data)
        s.commit()
    except Exception:
        result = False
    finally:
        s.close()
        return result


def get_menu_with_user(uid: str, db: session = session) -> list:
    '''
    联表查询用户绑定的菜单
    :param uid, 用户ID
    '''
    result = []
    with session() as s:
        if uid == 1:  # 如果是admin用户则返回所有菜单
            result = s.query(Menu.menu_id, Menu.menu_name).order_by(asc(Menu.sort)).all()
        else:
            result = s.query(Menu.menu_id, Menu.menu_name).join(MenuWithUser, Menu.menu_id == MenuWithUser.menu_id).filter(MenuWithUser.user_id == uid).order_by(asc(Menu.sort)).all()
    return result


def menu_privilege(uid: str, menu_id: str, db: session = session) -> bool:
    '''
    查询用户是否拥有此菜单下的接口权限
    :param uid, 用户id,
    :param menu_id, 菜单id
    '''
    if uid == 1:
        return True
    else:
        with session() as s:
            result = s.query(MenuWithUser).filter(MenuWithUser.menu_id == menu_id, MenuWithUser.user_id == uid).all()
            return result > 0
