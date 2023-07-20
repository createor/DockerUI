#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  codeImage.py
@Time    :  2023/07/14 15:51:29
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  None
'''
from captcha.image import ImageCaptcha
import base64
import io


def get_code_image(code: str, width: int = 130, height: int = 80) -> str:
    '''
    获取验证码图片base64流
    :param code, 验证码
    :param width, 图片宽度
    :param height, 图片高度
    :return base64图片流
    '''
    generator = ImageCaptcha(width=width, height=height)
    img = generator.generate_image(code)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='jpeg')
    return "data:image/jpeg;base64," + base64.b64encode(imgByteArr.getvalue()).decode()
