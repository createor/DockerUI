#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  user.py
@Time    :  2023/07/11 15:18:11
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  None
'''
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# 密钥,通过命令openssl rand -hex 32生成
SECRET_KEY = "07dded898998a9175b3c1c5ba638afcd5fb6d69cb077d868ec38f73398b945f2"
# 获取token的接口地址
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def create_access_token(data: dict, expired_delta: Union[timedelta, None] = None, algorithm: str = "HS256", secret_key: str = SECRET_KEY) -> str:
    '''
    创建access_token
    :param data, 需要处理的数据
    :param expired_delta, token过期时间
    :param algorithm, token加密算法
    :param secret_key, 密钥
    :return token字符串
    '''
    source_data = data.copy()
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=3)  # 默认token有效期3小时
    source_data.update({"exp": expire})
    return jwt.encode(source_data, secret_key, algorithm=algorithm)


class User(BaseModel):
    uid: int
    user: str


def verify_access_token(token: str, algorithm: str = "HS256", secret_key: str = SECRET_KEY) -> Union[User, None]:
    '''
    解析access_token
    :param token, access_token字符串
    :param algorithm, token加密算法
    :param secret_key, 密钥
    :return User, 用户信息
    '''
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return User(uid=payload.get("uid"), user=payload.get("user"))
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    '''
    获取token中的用户信息
    :param token, access_token字符串
    '''
    user = verify_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="非法的token")
    return user
