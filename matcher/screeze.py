#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
无法实现后台截图的原因：
    1.请确保窗口处于非最小化
    2.夜神模拟器请关闭OpenGL
    3.查看dxdiag，尝试禁用所有directx相关功能，禁用方法使用“禁用directx.reg，启用使用修复工具
"""

from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT
from matcher.base import MyCv2
from mywin32.handle import HandleGetter

import numpy as np
import win32con
import win32gui
import win32ui


default_save_path = "../screenshot/screenshot.bmp"


class WindowShooter(object):
    """
    用于截取/储存/读取窗口画面
    修改统一的储存路径请用类方法
    """
    _save_path = default_save_path

    def __init__(self, handle):
        self.handle = handle

    @property
    def save_path(self):
        return self._save_path

    @classmethod
    def set_path(cls, path):
        cls._save_path = path

    def screenshot(self):
        """
        直接截图并保存到save_path中
        :return: save_path
        """
        # 获取句柄窗口的大小信息
        left, top, right, bot = win32gui.GetWindowRect(self.handle)
        width = right - left
        height = bot - top

        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hWndDC = win32gui.GetWindowDC(self.handle)

        # 创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)

        # 创建内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()

        # 创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap()

        # 为bitmap开辟存储空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

        # 将截图保存到saveBitMap中
        saveDC.SelectObject(saveBitMap)

        # 保存bitmap到内存设备描述表
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

        # 保存图像
        saveBitMap.SaveBitmapFile(saveDC, self.save_path)

        # 返回图像位置
        return self._save_path

    def screenshot_np(self):
        """
        截图并返回ndarray
        我是没意料到这个代码跑起来意外顺利且成功的
        警告原因是c_long没有定义乘，不用管，能跑
        :return: np.ndarray
        """
        GetDC = windll.user32.GetDC
        CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
        GetClientRect = windll.user32.GetClientRect
        CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
        SelectObject = windll.gdi32.SelectObject
        BitBlt = windll.gdi32.BitBlt
        SRCCOPY = 0x00CC0020
        GetBitmapBits = windll.gdi32.GetBitmapBits
        DeleteObject = windll.gdi32.DeleteObject
        ReleaseDC = windll.user32.ReleaseDC
        rect = RECT()
        GetClientRect(self.handle, byref(rect))
        width, height = rect.right, rect.bottom

        # 开始截图
        dc = GetDC(self.handle)
        cdc = CreateCompatibleDC(dc)
        bitmap = CreateCompatibleBitmap(dc, width, height)
        SelectObject(cdc, bitmap)
        BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)

        # 截图是BGRA排列，因此总元素个数需要乘以4
        total_bytes = width * height * 4
        buffer = bytearray(total_bytes)
        byte_array = c_ubyte * total_bytes
        GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        DeleteObject(bitmap)
        DeleteObject(cdc)
        ReleaseDC(self.handle, dc)

        # 返回为ndarray
        return np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4))


if __name__ == '__main__':
    simulatorHandle, clientHandle = HandleGetter.Nox()
    shooter = WindowShooter(clientHandle)
    res_path = shooter.screenshot()
    res = shooter.screenshot_np()
    mycv2 = MyCv2()
    mycv2.show_path(res_path)
    MyCv2.show_np(res)
