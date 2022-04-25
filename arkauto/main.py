#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import time
import traceback

import cv2
import win32con
import win32gui

import setting
from arkerror import UnknownError, NoBrainError, AssertError
from button import ark_image
from helper.helper import count_time_self, print_now_time
from matcher.screeze import WindowShooter
from matcher.template import template
from mywin32 import messeger
from mywin32 import mywin32con as con
from mywin32.handle import HandleGetter
from position import ark_position


class ArkBase(object):
    def __init__(self):
        self._simulatorHandle, self._clientHandle = setting.getHandle()
        self.shooter = WindowShooter(self._clientHandle)
        self._getFxFy()

    # 自适应比例
    def _getFxFy(self):
        image_path = self.shooter.screenshot()
        image = template.read(image_path)
        shape = image.shape
        self.fx = shape[1] / setting.w
        self.fy = shape[0] / setting.h

    def initWindow(self):
        HandleGetter.simulatorInit(self.simulatorHandle)

    @property
    def simulatorHandle(self):
        return self._simulatorHandle

    @property
    def clientHandle(self):
        return self._clientHandle

    # 重写增加自适应功能
    def screenshot(self):
        if setting.selfAdaptation:
            image_path = self.shooter.screenshot()
            original = template.read(image_path)
            resize = cv2.resize(original, (setting.w, setting.h), interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(image_path, resize)
            return image_path
        else:
            return self.shooter.screenshot()

    # 模板匹配按键
    def findButton(self, template_path, *, thresh=setting.thresh, read_mode=setting.read_mode, wait_time=0.0,
                   timeout=setting.find_button_timeout, draw=False):
        """
        自带截图功能的模板匹配，部分参数请参考template.get_location
        :param template_path: 模板路径
        :param thresh: 匹配阈值
        :param read_mode: BGR 1/GRAY 0
        :param wait_time: 匹配前等待时间，默认为0
        :param timeout: 匹配超时
        :param draw: 是否绘制匹配结果
        :return: tuple/None
        """
        template_name = template_path.split("/")[-1]
        time.sleep(wait_time)
        print(f"\t开始匹配：{template_name}")
        startTime = time.time()
        while True:
            image_path = self.screenshot()
            centers = template.get_location(template_path, image_path, thresh, read_mode, 1, draw)
            if centers:
                print(f"\t获取到匹配：{centers[0]}")
                return centers[0]
            else:
                if time.time() - startTime < timeout:
                    time.sleep(setting.find_button_interval)
                else:
                    print("\t超时未匹配")
                    return

    # 模板匹配按键(Knn)
    def findButtonKnn(self, template_path, k, *, thresh=setting.thresh, read_mode=setting.read_mode, wait_time=0.0,
                      timeout=setting.find_button_timeout, draw=False):
        """
         自带截图功能的模板匹配，可以匹配多个对象，部分参数请参考template.get_location
         :param template_path: 模板路径
         :param k: Knn
         :param thresh: 匹配阈值
         :param read_mode: BGR 1/GRAY 0
         :param wait_time: 匹配前等待时间，默认为0
         :param timeout: 匹配超时
         :param draw: 是否绘制匹配结果
         :return: list(tuple)/[]
         """
        template_name = template_path.split("/")[-1]
        time.sleep(wait_time)
        print(f"\t开始匹配：{template_name}")
        startTime = time.time()
        while True:
            image_path = self.screenshot()
            centers = template.get_location(template_path, image_path, thresh, read_mode, k, draw)
            if centers:
                print(f"\t获取到匹配：{centers}")
                return centers
            else:
                if time.time() - startTime < timeout:
                    time.sleep(setting.find_button_interval)
                else:
                    print("\t超时未匹配")
                    return []

    def makeAdaptationPosition(self, position):
        return int(position[0] * self.fx), int(position[1] * self.fy)

    # 自定义简单点击函数，自带自适应(识别最近一次)
    def simpleClick(self, position):
        """
        :param position: 点击位置
        setting.selfAdaptation :
            是否通过初始化时得到的缩放比自适应窗口大小
            因为缩放比是类初始化时得到的，所以脚本运行后调整窗口大小会出错
                当然是可以每次操作前都重新获取缩放比的，怕影响速度(写个进程检测感觉挺多此一举的)
            其他的操作是不带缩放功能的，可以用makeAdaptation...慢慢重写
            拖动函数就重写了，其实很简单就是把起点终点都缩放处理就可以了
        :return:
        """
        if not position:
            raise AssertError
        if setting.selfAdaptation:
            position = self.makeAdaptationPosition(position)
            messeger.clickInput(self.clientHandle, position, con.LEFT_BUTTON)


class LoopBattle(ArkBase):
    """
    重复战斗功能区
    剿灭功能写在别处了(新建文件夹)
    """

    def __init__(self):
        super(LoopBattle, self).__init__()

    def preBattle(self):
        # 检测蓝色开始按钮并点击
        startActionBlueCP = self.findButton(ark_image.startActionBlue)
        self.simpleClick(startActionBlueCP)

        # 检测红色开始按钮并点击
        startActionRedCP = self.findButton(ark_image.startActionRed, wait_time=2)
        if not startActionRedCP:

            # 未检测到红色开始按钮，进入理智判定
            noBrainConfirmCP = self.findButton(ark_image.noBrainConfirm)
            if noBrainConfirmCP:
                print("理智不足")
                raise NoBrainError
            else:
                print("未检测到红色开始按钮与理智补充按钮，脚本退出")
                raise UnknownError
        else:
            self.simpleClick(startActionRedCP)

        # 检测接管作战
        takeOverCP = self.findButton(ark_image.takeOver, wait_time=10, timeout=20)
        if takeOverCP:
            print("已进入战斗")
        else:
            print("超时未检测到标志：接管作战，进入战斗失败")
            raise UnknownError

    # 等待60秒，检测180秒，应该适用于所有普通战斗了
    def afterBattle(self):
        # 检测全员信赖标志
        trustUpCP = self.findButton(ark_image.trustUp, wait_time=60, timeout=180)

        # 等待结算，不然点了没反应
        time.sleep(5)
        self.simpleClick(trustUpCP)
        print("已结束战斗")

        # 重新检测蓝色开始，判定是否回到主界面
        startActionBlueCP = self.findButton(ark_image.startActionBlue, wait_time=3, timeout=10)
        if startActionBlueCP:
            print("已回到主界面")
        else:
            print("超时未检测到标志：开始行动(蓝)，进入战斗失败")
            raise UnknownError

    # 补充理智
    def replenish(self):
        """
        理智补充逻辑：有啥点啥，顺序全看弹出来是什么，只负责确定
        :return:
        """
        time.sleep(2)
        self.simpleClick(ark_position.replenish)
        time.sleep(5)

    @count_time_self
    def run(self):
        print("""
----------------------------------------------------------------
            非常稳定的明日方舟后台刷图脚本
说明：
    1.该脚本可以后台运行，但不支持最小化
    2.运行前请将界面停留在有(蓝)开始行动按钮处，并勾选代理指挥
    3.刷够次数或理智耗尽(达到补充上限)脚本会自动退出
    4.补充理智逻辑为：有啥点啥(懒死了不想写很复杂的逻辑)
    5.极有可能发生各种意外情况，因为bug也是程序的一部分
----------------------------------------------------------------

""")

        # 输入信息，如果都Enter，要敲Enter三次
        loops = input("请输入刷图次数(Enter为刷到死)：")
        if not loops:
            loops = 999
        else:
            loops = int(loops)

        replenishTimes = input("请输入理智补充次数(Enter为不补充)：")
        if not replenishTimes:
            replenishTimes = 0
        else:
            replenishTimes = int(replenishTimes)

        # 最小化cmd
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

        # 激活模拟器窗口或置底
        self.initWindow()

        nowReplenish = 0
        i = 1

        try:
            while i <= loops:
                print("\n----------------------------------------------------------------")
                print_now_time()
                print(f"当前第{i}次战斗\n")
                try:
                    self.preBattle()

                # 理智不足
                except NoBrainError:
                    if nowReplenish < replenishTimes:
                        self.replenish()
                        nowReplenish += 1
                        print(f"第{nowReplenish}次补充理智")
                        continue
                    else:
                        print(f"\n已达到理智补充次数上限, 共刷了{i}次")
                        return

                self.afterBattle()
                i += 1

            # 如果你想要结束后不要自动弹窗，请注释掉下面这一行
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_RESTORE)
            print(f"\n刷图{loops}次已全部完成！")

        except:
            # 打印traceback
            info = traceback.format_exc()
            print(info)

            # 如果你想要出错后不要自动弹窗，请注释掉下面这一行
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_RESTORE)


if __name__ == '__main__':
    main = LoopBattle()
    main.run()
