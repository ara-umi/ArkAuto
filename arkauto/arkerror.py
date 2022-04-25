#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 用于保存大部分自定义异常

class ClickError(Exception):
    pass


class AssertError(Exception):
    pass


class NoBrainError(Exception):
    pass


class UnknownError(Exception):
    pass


# 发现没有需要休息的干员时抛出的异常，用于提前停止脚本
class NoNeedRestError(Exception):
    pass
