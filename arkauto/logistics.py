#!/usr/bin/python3
# -*- coding: utf-8 -*-
import ctypes
import time
import traceback

import cv2
import win32con

import setting
from arkerror import UnknownError, NoNeedRestError
from button import ark_image
from helper import helper
from main import ArkBase
from matcher.template import template
from mywin32 import messeger
from position import ark_position


# 自动更换基建
class Logistics(ArkBase):
    """
    各类后勤功能，包括但不限于：
    自动基建换人
    自动无人机充能
    自动访问好友基建
    自动消费信誉低
    自动收取公招
    自动领任务
    """

    def __init__(self):
        super(Logistics, self).__init__()

    # 通过模板匹配小红脸(总览中)定位
    def _findTiredOverview(self):
        image_path = self.screenshot()
        tiredOverviewCPs = template.get_location(ark_image.tiredOverview, image_path,
                                                 thresh=0.98, flags=1, k=20)
        print(f"\t本页涣散干员数量: {len(tiredOverviewCPs)}")
        return list(map(lambda x: (x[0] + 55, x[1] - 64), tiredOverviewCPs))

    # 通过模板匹配小红脸(列表中，已选中)定位
    def _findTiredCheckedInList(self):
        image_path = self.screenshot()
        return template.get_location(ark_image.tiredCheckedInList, image_path,
                                     thresh=0.98, flags=1, k=5)

    # 通过模板匹配小绿脸(列表中)定位
    def _findEnergeticInList(self, number):
        image_path = self.screenshot()
        # 找12个，保证全都找到，最终排序保证从左到右从上到下不漏(模板匹配时minMaxVal是玄学参数，所以需要k很大，最后通过排序过滤)
        energeticInListCPs = template.get_location(ark_image.energeticInList,
                                                   image_path, thresh=0.98, flags=1, k=12)

        energeticInListCPs.sort(key=lambda x: (x[0], x[1]))
        energeticInListCPs = energeticInListCPs[:number]
        return energeticInListCPs

    # 通过模板匹配小绿脸(列表中，已选中)定位
    def _findEnergeticCheckedInList(self, number):
        image_path = self.screenshot()
        # 根据总览中检测到的充沛干员数量进行定位
        energeticCheckedInListCPs = template.get_location(ark_image.energeticCheckedInList,
                                                          image_path, thresh=0.98, flags=1, k=number)

        return energeticCheckedInListCPs

    # 通过模板匹配需要休息的干员(列表中)定位
    def _findNeedRestInList(self, number):
        """
        需要休息的分两种：红脸和黄脸
        在心情升序的情况下，是不需要翻页的
        所以只用判断第一页的内容，找得够最好
        找不够说明你的干员都比较精神
        明日方舟排序很智能的，其他宿舍休息中的干员是会沉底的，除非你用其他排序
        """
        image_path = self.screenshot()
        tiredInListCPs = template.get_location(ark_image.tiredInList, image_path,
                                               thresh=0.98, flags=1, k=12)
        tiredInListCPs.sort(key=lambda x: (x[0], x[1]))
        tiredInListCPs = tiredInListCPs[:number]

        # 如果涣散干员够了就直接返回
        if len(tiredInListCPs) == number:
            return tiredInListCPs

        # 不够就再加上黄脸干员
        else:
            number -= len(tiredInListCPs)
            littleTiredInListCPs = template.get_location(ark_image.littleTiredInList, image_path, thresh=0.98,
                                                         flags=1, k=12)
            littleTiredInListCPs.sort(key=lambda x: (x[0], x[1]))

            # 检测黄脸干员是否在工作中
            littleTiredInListFilterCPs = []
            for littleTiredInListCP in littleTiredInListCPs:
                CP = littleTiredInListCP

                # 截取整个干员
                image_path = self.screenshot()
                screenshot = template.read(image_path, flags=1)
                screenshot = screenshot[CP[1] - 300:CP[1] + 49, CP[0] - 28: CP[0] + 135, :]
                cv2.imwrite(image_path, screenshot)

                # 不在工作中则保留
                onShiftCP = template.get_location(ark_image.onShift, image_path, thresh=0.9,
                                                  flags=1, k=1)

                if not onShiftCP:
                    littleTiredInListFilterCPs.append(CP)

                if len(littleTiredInListFilterCPs) == number:
                    break
            return tiredInListCPs + littleTiredInListFilterCPs

    # 总览中定位宿舍
    def _findDormitory(self):
        image_path = self.screenshot()
        dormitoryCPs = template.get_location(ark_image.dormitory, image_path, thresh=0.95,
                                             flags=1, k=2)
        return dormitoryCPs

    # 根据特定宿舍位置，寻找充沛干员数量，并进入宿舍
    def _findEnergeticNumber(self, dormitory_cp):
        """
        充沛干员的数量 = 小绿脸数量 + blank数量
        """
        # 获取宿舍高度(用于裁剪)
        dormitory = template.read(ark_image.dormitory, flags=1)
        height, _, _ = dormitory.shape
        dormitoryCP = dormitory_cp

        # 获取第一个干员位置以方便进入图鉴列表
        firstAgentCP = dormitoryCP[0] + 290, dormitoryCP[1]

        # 截取宿舍栏
        start = dormitoryCP[1] - height // 2
        end = dormitoryCP[1] + height // 2
        image_path = self.screenshot()
        screenshot = template.read(image_path, flags=1)
        screenshot = screenshot[start:end, :, :]
        cv2.imwrite(image_path, screenshot)

        # 匹配小绿脸
        energeticOverviewCPs = template.get_location(ark_image.energeticOverview,
                                                     image_path, thresh=0.98, flags=1, k=5)
        energeticNumber = len(energeticOverviewCPs)

        # 匹配空位
        """
        未解之谜是如果空十字叉模板选大点(包含边框)，0.98就不行，得0.95
        小到只保留十字叉后0.95就可以了
        估计是受缩放影响
        """
        blankOverviewCPs = template.get_location(ark_image.blankOverview,
                                                 image_path, thresh=0.98, flags=1, k=5)
        blankNumber = len(blankOverviewCPs)

        # 根据结果判断是否进入宿舍
        print("\t检测到宿舍:", dormitoryCP, "已恢复干员:", energeticNumber, "空位:", blankNumber)
        total = energeticNumber + blankNumber
        if not total:
            print("\t该宿舍已满")
        else:
            # 点击第一个干员进入宿舍
            self.simpleClick(firstAgentCP)
        return energeticNumber, blankNumber

    # 从主界面进入基建
    def _enterBaseStation(self):
        terminalCP = self.findButton(ark_image.terminal)
        if terminalCP:
            self.simpleClick(ark_position.baseStation)
            overviewCP = self.findButton(ark_image.overview, wait_time=5, timeout=10)
            if overviewCP:
                print("\n已进入基建")
                # 进入后还不能马上操作
                time.sleep(3)
                return
        else:
            raise UnknownError("当前非主界面！")

    # 从基建进入总览
    def _enterOverview(self):
        self.simpleClick(ark_position.overview)
        flag = self.findButton(ark_image.cancelAgent)
        if flag:
            print("\n已进入总览")
            # 进入后还不能马上操作
            time.sleep(3)
        else:
            print("\n超时未进入总览")
            raise UnknownError

    # 收物资与信赖
    def dealNotification(self):
        # 进入后会先弹出信赖，需要等待/通知消息出现位置会不同，检测降低阈值
        print("\n开始处理通知")
        notificationCP = self.findButton(ark_image.notification, thresh=0.95, timeout=5)
        if not notificationCP:
            print("\t暂无任何通知")

        # 若有通知，先点击通知
        self.simpleClick(notificationCP)
        time.sleep(1)  # 等待响应

        backlogs = [
            (ark_image.canGet, "可收获"),
            (ark_image.deliverOrders, "订单交付"),
            (ark_image.getTrust, "干员信赖")
        ]

        for backlog in backlogs:
            backlogCP = self.findButton(backlog[0], timeout=3)
            if backlogCP:
                self.simpleClick(backlogCP)
                print(f"\t已处理待办事项：{backlog[1]}")
                # 收取后会有动画，等待
                time.sleep(2)
            else:
                print(f"\t未发现待办事项：{backlog[1]}")
        self.simpleClick(notificationCP)
        print("\n已处理所有通知")
        time.sleep(2)  # 等待响应

    # 总览下拉
    def pagedownOverview(self, distance):
        w, h = setting.w, setting.h
        center = w // 2, h // 2
        start = self.makeAdaptationPosition((center[0], center[1] + distance // 2))
        end = self.makeAdaptationPosition((center[0], center[1] - distance // 2))
        messeger.drag(self.clientHandle, start, end, interval=0.002, wait_time=0.2)

    # 总览上拉
    def pageupOverview(self, distance):
        center = setting.w // 2, setting.h // 2
        start = self.makeAdaptationPosition((center[0], center[1] - distance // 2))
        end = self.makeAdaptationPosition((center[0], center[1] + distance // 2))
        messeger.drag(self.clientHandle, start, end, interval=0.002, wait_time=0.2)

    # 图鉴列表右拉
    def pageRightList(self, distance):
        w, h = setting.w, setting.h
        center = w // 2, h // 2
        start = self.makeAdaptationPosition((center[0] + distance // 2, center[1]))
        end = self.makeAdaptationPosition((center[0] - distance // 2, center[1]))
        messeger.drag(self.clientHandle, start, end, interval=0.002, wait_time=0.2)

    # 更换一页涣散干员
    def substitutionOnePage(self):
        # 识别一页崩溃干员，若无则返回
        tiredAgentCPs = self._findTiredOverview()
        if not tiredAgentCPs:
            return

        # 记录上一次点击位置(随便设个初始值)，取一个大致范围过滤，保证每次点击位置不在同一行
        lastClickCP = (0, 0)
        for tiredAgentCP in tiredAgentCPs:
            if not (lastClickCP[1] - 2 <= tiredAgentCP[1] <= lastClickCP[1] + 2):
                self.simpleClick(tiredAgentCP)

                # 等待进入图鉴列表
                time.sleep(3)

                # 寻找上阵的涣散干员
                """
                主要考虑阈值问题，会不会错匹配到其他小红脸
                """
                tiredCheckedInListCPs = self._findTiredCheckedInList()
                tiredNumber = len(tiredCheckedInListCPs)

                # 涣散干员取消选择
                for tiredCheckedInListCP in tiredCheckedInListCPs:
                    self.simpleClick(tiredCheckedInListCP)
                    time.sleep(0.5)

                # 换上充沛干员(没写超时)
                """
                默认排序下基本上用不到翻页，除非你整个图鉴找不够5个满心情
                """
                # 找12个排序，取所需数量列表切片
                energeticInListCPs = self._findEnergeticInList(tiredNumber)
                energeticNumber = len(energeticInListCPs)
                while True:
                    for energeticInListCP in energeticInListCPs:
                        self.simpleClick(energeticInListCP)
                        time.sleep(0.5)
                    if energeticNumber == tiredNumber:
                        break
                    # 如果找到的多于所需，返回就会相等，就不需要翻页，反之就翻页
                    else:
                        tiredNumber -= energeticNumber
                        self.pageRightList(900)
                        time.sleep(1)
                        energeticInListCPs = self._findEnergeticInList(tiredNumber)
                        energeticNumber = len(energeticInListCPs)

                # 确认并退出
                lastClickCP = tiredAgentCP
                self.simpleClick(ark_position.substitutionConfirm)
                self.findButton(ark_image.cancelAgent, wait_time=2)

    # 休息一页干员
    def restOnePage(self):
        # 寻找宿舍
        dormitoryCPs = self._findDormitory()
        for dormitoryCP in dormitoryCPs:
            # 寻找充沛干员数量，进入宿舍
            energeticNumber, blankNumber = self._findEnergeticNumber(dormitoryCP)
            total = energeticNumber + blankNumber
            if not total:
                continue

            # 等待进入宿舍
            time.sleep(3)

            # 寻找充沛干员
            energeticCheckedInListCPs = self._findEnergeticCheckedInList(energeticNumber)

            # 寻找需要休息的干员
            needRestCPs = self._findNeedRestInList(total)

            # 换下充沛干员
            for energeticCheckedInListCP in energeticCheckedInListCPs:
                self.simpleClick(energeticCheckedInListCP)
                time.sleep(0.5)

            time.sleep(0.5)

            # 换上需要休息的干员
            for needRestCP in needRestCPs:
                self.simpleClick(needRestCP)
                time.sleep(0.5)

            # 确认并退出
            self.simpleClick(ark_position.substitutionConfirm)
            self.findButton(ark_image.cancelAgent, wait_time=2)

            # 若没有需要休息干员，抛出异常停止脚本
            if len(needRestCPs) == 0:
                print("\t您的干员都很精神！")
                raise NoNeedRestError

        return

    # 休息所有干员(从底部开始)
    def restAllPageFromBottom(self):
        print("\n开始更换全部宿舍干员")
        for i in range(7):
            self.restOnePage()
            time.sleep(1)
            self.pageupOverview(600)
            time.sleep(1)
        print("\n已完成宿舍换人")

    # 休息所有干员(从顶部开始)
    def restAllPageFromTop(self):
        for i in range(7):
            self.restOnePage()
            time.sleep(1)
            self.pagedownOverview(600)
            time.sleep(1)
        print("已完成宿舍换人")

    # 更换所有涣散干员
    def substitutionAllPage(self):
        print("\n开始更换全部涣散干员")
        for i in range(7):
            self.substitutionOnePage()
            time.sleep(1)
            self.pagedownOverview(600)
            time.sleep(1)
        print("\n已撤下全部涣散干员")

    # 贸易战加速
    def accelerateTrade(self):
        """
        在点击通知后，整个视图会被拉远，能显示所有的楼层，是方便定位的
        问题在于如果没有蓝色通知，就无法拉远视图，匹配就会想当困难
        所以我建议这项行为和收通知一起进行
        """
        # 点击加速楼层
        floorCP = setting.accelerateFloor
        self.simpleClick(floorCP)
        inTradingCP = self.findButton(ark_image.inTrading, wait_time=0.5, timeout=3)

        # 如果出现需要收取物资的情况，需要点两次
        if not inTradingCP:
            self.simpleClick(floorCP)
            inTradingCP = self.findButton(ark_image.inTrading, wait_time=0.5, timeout=3)

        print("\n已进入贸易战")
        if not inTradingCP:
            print("进入贸易战失败")
            raise UnknownError

        # 点击获取中
        self.simpleClick(inTradingCP)
        time.sleep(2)

        while True:
            UAV_CP = self.findButton(ark_image.UAV, thresh=0.98, timeout=3)
            self.simpleClick(UAV_CP)
            time.sleep(1)
            flag = self.findButton(ark_image.NoUAV, timeout=1)

            # 如果检测不到无人机为0-0，就加速
            if not flag:
                self.simpleClick(ark_position.mostInTradeAccelerate)
                time.sleep(1)
                self.simpleClick(ark_position.confirmBlueInTradeAccelerate)
                time.sleep(2)
            else:
                self.simpleClick(ark_position.confirmBlueInTradeAccelerate)
                time.sleep(2)
                break

        print("无人机加速完成，退出中")
        self.simpleClick(ark_position.back)
        time.sleep(2)
        self.simpleClick(ark_position.back)
        time.sleep(2)
        return

    # 制造站加速
    def accelerateManufacture(self):
        pass

    def test(self):
        self.accelerateTrade()

    @helper.count_time_self
    def run(self):
        print("""
----------------------------------------------------------------
            非常稳定的明日方舟基建换人脚本
说明：
    1.该脚本可以后台运行，但不支持最小化
    2.运行前请停留在游戏主页即可
    3.运行中请不要乱see！忙你的就好了！运行后不支持更改窗口大小
    4.请关闭退出基建确认，开启收获提示等提醒
    5.极有可能发生各种意外情况，因为bug也是程序的一部分
----------------------------------------------------------------

    """)
        input("""
一条龙服务：
    从主页进入基建 -->> 通知收取 -->> 基建换人 
    尚未完成加速和线索收集功能

回车确认:""")
        print()
        helper.print_now_time()

        # 最小化cmd
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

        # 激活模拟器窗口或置底
        self.initWindow()

        try:
            # 进入基建
            self._enterBaseStation()
            # 收取通知消息
            self.dealNotification()
            # 进入总览
            self._enterOverview()
            # 从上到下换下涣散干员
            self.substitutionAllPage()
            # 从下到上填满宿舍
            time.sleep(2)
            self.restAllPageFromBottom()
            # 退回到主界面
            self.simpleClick(ark_position.back)
            time.sleep(2)
            self.simpleClick(ark_position.back)

        except NoNeedRestError:
            # 退回到主界面
            self.simpleClick(ark_position.back)
            time.sleep(2)
            self.simpleClick(ark_position.back)
        except:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_RESTORE)

            # 打印traceback
            info = traceback.format_exc()
            print(info)
            return

        # 完成后自动弹出
        print("已全部完成!")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_RESTORE)


if __name__ == '__main__':
    main = Logistics()
    # main.run()
    main.test()
