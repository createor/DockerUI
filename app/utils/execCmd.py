#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  execCmd.py
@Time    :  2023/07/17 10:19:44
@Author  :  createor@github.com
@Version :  1.0
@Desc    :  执行linux命令
'''
import subprocess


class Command(object):
    def __init__(self, cmd: str) -> None:
        self.cmd = cmd

    def _exec(self) -> None:
        '''
        执行命令
        '''
        pass

    @staticmethod
    def get_status(self) -> bool:
        '''
        命令执行是否成功
        :return true-成功,false-失败
        '''
        pass

    @staticmethod
    def get_result(self) -> str:
        '''
        命令执行结果
        :return 执行结果
        '''
        pass
