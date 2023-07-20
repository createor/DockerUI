#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  view.py
@Time    :  2023/07/11 15:22:48
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  用户视图
'''
from fastapi import APIRouter, Form, status, HTTPException, Depends, Cookie, Response
from app.db import user, menu
from app.db import logRecord as log
from app.utils import encrypt, time, codeImage, code
from app.user.user import create_access_token, get_current_user, User
from pydantic import BaseModel
from typing import Union

users = APIRouter()


# 用户登录接口
@users.post("/login")
async def login(username: str = Form(), password: str = Form(), captcha: str = Form(), code_id: Union[str, None] = Cookie(default=None)):
    if not code_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="获取验证码错误")
    verify_status = code.getter(code_id, captcha)
    if verify_status == 1003:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码错误")
    if verify_status == 1002:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码过期")
    if verify_status == 1001:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="校验验证码错误")
    result = user.get_user(username=username, password=encrypt.encrypt_data(password))
    if len(result) == 1:
        if result[0].status:
            log.create_log(log.LogRecord(content="用户{}登录成功".format(username), operate_type="1", operate_user=result[0].id))  # 日志记录
            return {"msg": "success", "access_token": create_access_token({"uid": result[0].id, "user": username}), "token_type": "bearer", "code": 0}
        else:
            log.create_log(log.LogRecord(content="用户{}登录失败,未激活的用户".format(username), operate_type="1", operate_user=result[0].id))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="被禁用的用户")  # 未激活的用户
    else:
        log.create_log(log.LogRecord(content="用户{}登录失败,用户名/密码错误".format(username), operate_type="1"))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")  # 错误的用户名或密码


# 用户登出接口
@users.get("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    log.create_log(log.LogRecord(content="用户登出成功", operate_type="1", operate_user=current_user.uid))
    return {"msg": "success", "code": 0}


# 创建用户接口
@users.post("/add")
async def add_user(current_user: User = Depends(get_current_user), username: str = Form(), password: str = Form()):
    isAllow = menu.menu_privilege(current_user.uid, 'system-setting')
    if not isAllow:
        log.create_log(log.LogRecord(content="创建用户{}失败,无权限操作".format(username), operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限操作")
    isExist = user.get_user(username=username)
    if len(isExist) > 0:
        log.create_log(log.LogRecord(content="创建用户{}失败,用户已存在".format(username), operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    isSucc = user.create_user(user.User(username=username, password=encrypt.encrypt_data(password), create_user=current_user.uid, create_time=time.get_time()))
    if isSucc:
        log.create_log(log.LogRecord(content="创建用户{}成功".format(username), operate_type="4", operate_user=current_user.uid))
        return {"msg": "success", "code": 0}
    else:
        log.create_log(log.LogRecord(content="创建用户{}失败,未知原因".format(username), operate_type="4", operate_user=current_user.uid))
        return {"msg": "创建失败", "code": -1}


# 获取用户列表接口
@users.get("/list")
async def get_users_list(current_user: User = Depends(get_current_user), page: int = 1, limit: int = 10):
    isAllow = menu.menu_privilege(current_user.uid, 'system-setting')
    if not isAllow:
        log.create_log(log.LogRecord(content="查询用户列表失败,无权限操作", operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限操作")
    count = user.count_user(create_user=current_user.uid)
    if count == 0:
        userList = []
    else:
        userList = user.get_user(skip=page - 1, limit=limit, create_user=current_user.uid)
        userList = [{"id": user.id, "name": user.username, "status": bool(user.status)} for user in userList]
    log.create_log(log.LogRecord(content="查询用户列表成功", operate_type="4", operate_user=current_user.uid))
    return {"msg": "success", "count": count, "data": userList, "code": 0}


# 修改用户密码接口
@users.post("/password")
async def set_user_password(current_user: User = Depends(get_current_user), oldPassword: str = Form(), newPassword: str = Form(), confirmPassword: str = Form()):
    if oldPassword == newPassword:  # 新旧密码不同
        log.create_log(log.LogRecord(content="更新密码失败,新旧密码一致", operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新旧密码不能一样")
    if len(newPassword) < 6:
        log.create_log(log.LogRecord(content="更新密码失败,新密码长度小于6位", operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新密码长度不能小于6位")
    if newPassword != confirmPassword:  # 新密码、确认密码相同
        log.create_log(log.LogRecord(content="更新密码失败,新密码与确认密码不一致", operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新密码与确认密码需一致")
    # 查询旧密码
    iscorrectPasswd = user.get_user(username=current_user.user, password=encrypt.encrypt_data(oldPassword))
    if len(iscorrectPasswd) > 0:
        isUpdate = user.update_user(current_user.uid, encrypt.encrypt_data(newPassword))
        if isUpdate:
            log.create_log(log.LogRecord(content="更新密码成功", operate_type="4", operate_user=current_user.uid))
            return {"msg": "success", "code": 0}
        else:
            log.create_log(log.LogRecord(content="更新密码失败,未知原因", operate_type="4", operate_user=current_user.uid))
            return {"msg": "修改失败", "code": -1}
    else:
        log.create_log(log.LogRecord(content="更新密码失败,旧密码错误", operate_type="4", operate_user=current_user.uid))
        return {"msg": "旧密码不正确", "code": -1}


class Status(BaseModel):
    id: str  # 用户id
    name: str  # 用户名
    status: bool


# 修改用户状态接口
@users.post("/status")
async def change_user_status(status: Status, current_user: User = Depends(get_current_user)):
    isAllow = menu.menu_privilege(current_user.uid, 'system-setting')
    if not isAllow:
        log.create_log(log.LogRecord(content="更新用户{}状态失败,无权限操作".format(status.name), operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=403, detail="无权限操作")
    # 查询此用户是否属于被管理用户
    isCreate = user.get_user(id=status.id, username=status.name, create_user=current_user.uid)
    if isCreate == 0:
        log.create_log(log.LogRecord(content="更新用户{}状态失败,无权限操作".format(status.name), operate_type="4", operate_user=current_user.uid))
        raise HTTPException(status_code=403, detail="无权限操作")
    isUpdate = user.update_user(status.id, newStatus=status.status)
    if isUpdate:
        log.create_log(log.LogRecord(content="更新用户{}状态成功".format(status.name), operate_type="4", operate_user=current_user.uid))
        return {"msg": "success", "code": 0}
    else:
        log.create_log(log.LogRecord(content="更新用户{}状态失败".format(status.name), operate_type="4", operate_user=current_user.uid))
        return {"msg": "failed", "code": -1}


# 查询用户拥有的菜单权限
@users.get("/menu")
async def get_user_menu(current_user: User = Depends(get_current_user), uid: str = None):
    if uid:
        menuList = menu.get_menu_with_user(uid)
    else:
        menuList = menu.get_menu_with_user(current_user.uid)
    data = [{"title": menu.menu_name, "id": menu.menu_id, "field": menu.menu_id} for menu in menuList]
    return {"msg": "success", "data": data, "code": 0}


class Bind(BaseModel):
    uid: str
    name: str
    menu: list


# 绑定用户与菜单关系
@users.post("/bind")
async def bind_user_menu(b: Bind, current_user: User = Depends(get_current_user)):
    # 先删除所有绑定关系
    menu.delete_menu_with_user(b.uid)
    for m in b.menu:
        isSucc = menu.create_menu_with_user(menu.MenuWithUser(menu_id=m, user_id=b.uid))
        if not isSucc:
            log.create_log(log.LogRecord(content="绑定用户{}的菜单关联失败".format(b.name), operate_type="3", operate_user=current_user.uid))
            return {"msg": "failed", "code": -1}
    log.create_log(log.LogRecord(content="绑定用户{}的菜单关联成功".format(b.name), operate_type="3", operate_user=current_user.uid))
    return {"msg": "success", "code": 0}


# 获取验证码
@users.get("/captcha")
async def get_captcha(response: Response, code_id: Union[str, None] = Cookie(default=None)):
    if code_id:
        code.remove(code_id)
    [codeID, char] = code.setter()
    response.set_cookie(key="code_id", value=codeID)
    base64Img = codeImage.get_code_image(char)
    return {"msg": "success", "data": base64Img, "code": 0}


# 校验token接口
@users.get("/auth")
async def auth(current_user: User = Depends(get_current_user)):
    return {"msg": "success", "code": 0}
