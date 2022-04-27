#!/usr/bin/python3
# -*- coding: utf-8 -*-

import win32con
import win32gui

from hexHelper import d2xK


class HandleGetter(object):
    """
    本类用于存放一些常见应用软件句柄的获取方法
    """

    def __init__(self):
        pass

    @staticmethod
    def Nox():
        """
        夜神模拟器
        :return: （模拟器句柄， 客户窗口句柄）
        """
        simulatorHandle = win32gui.FindWindow("Qt5QWindowIcon", "夜神模拟器")
        # 模拟器每打开一个窗口，就会多出一个Nox，默认会有一个
        preHandle = 0
        while True:
            res = win32gui.FindWindowEx(simulatorHandle, preHandle, None, "Nox")
            if not res:
                lastNox = preHandle
                break
            else:
                preHandle = res
        # 子窗口依次是toolbar，客户区父和标题栏
        clientFatherHandle = win32gui.FindWindowEx(lastNox, 0, None, "Nox")
        clientHandle = win32gui.FindWindowEx(clientFatherHandle, 0, None, "Nox")
        print(f"模拟器句柄：{d2xK(simulatorHandle, 8)}\n客户区句柄：{d2xK(clientHandle, 8)}")
        return simulatorHandle, clientHandle

    @staticmethod
    def Xiaoyao():
        """
        逍遥模拟器
        :return: （模拟器句柄， 客户窗口句柄）
        """
        simulatorHandle = win32gui.FindWindow(None, "逍遥模拟器")
        MainWindow = win32gui.FindWindowEx(simulatorHandle, 0, None, "MainWindowWindow")
        CenterWindow = win32gui.FindWindowEx(MainWindow, 0, None, "CenterWidgetWindow")
        Render = win32gui.FindWindowEx(CenterWindow, 0, None, "RenderWindowWindow")
        clientHandle = Render
        print(f"模拟器句柄：{d2xK(simulatorHandle, 8)}\n客户区句柄：{d2xK(clientHandle, 8)}")
        return simulatorHandle, clientHandle

    @staticmethod
    def LeiDian():
        """
        雷电模拟器
        :return: （模拟器句柄， 客户窗口句柄）
        """
        simulatorHandle = win32gui.FindWindow("LDPlayerMainFrame", None)
        clientHandle = win32gui.FindWindowEx(simulatorHandle, 0, "RenderWindow", "TheRender")
        print(f"模拟器句柄：{d2xK(simulatorHandle, 8)}\n客户区句柄：{d2xK(clientHandle, 8)}")
        # print(f"模拟器句柄：{simulatorHandle}({hex(simulatorHandle)})\n客户区句柄：{clientHandle}({hex(clientHandle)})")
        return simulatorHandle, clientHandle

    @staticmethod
    def Notepad():
        """
        记事本(测试用)
        :return: （主窗口句柄， 客户窗口句柄）
        """
        notepadHandle = win32gui.FindWindow("Notepad", None)
        clientHandle = win32gui.FindWindowEx(notepadHandle, 0, "edit", None)
        return notepadHandle, clientHandle

    @staticmethod
    def Typora(title):
        """
        Typora(测试用)
        title: 格式:filename.md - Typora
        :return: （主窗口句柄， 客户窗口句柄）
        """
        typoraHandle = win32gui.FindWindow(None, title)
        clientHandle = win32gui.FindWindowEx(typoraHandle, 0, None, "Chrome Legacy Window")
        return typoraHandle, clientHandle

    @staticmethod
    def Genshin():
        genshinHandle = win32gui.FindWindow("UnityWndClass", "原神")
        return genshinHandle

    # 激活并置底
    @staticmethod
    def simulatorInit(handle):
        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
            print("检测到最小化，激活窗口")
        win32gui.SetWindowPos(handle, win32con.HWND_TOP, 0, 0, 0, 0,
                              win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        print("运行过程中窗口允许置底，但请勿最小化")


if __name__ == '__main__':
    # _, clientHandle = HandleGetter.Nox()
    # _, clientHandle = HandleGetter.LeiDian()
    HandleGetter.Xiaoyao()
