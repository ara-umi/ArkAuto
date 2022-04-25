#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
image_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
root = image_dir + "/image/"
suffix = ".png"


class ImagePath(object):
    """
    用于修改图片相对路径的基类，所有图片文件路径受此类管理
    """

    def __init__(self):
        self.root = root
        self.path = ""

    def myPath(self, filename):
        return self.root + self.path + filename + suffix


class Window(ImagePath):
    """
    对应并非在游戏内，属于模拟器/桌面的大部分图标
    直接存储在button_img之下
    按理说这个类会存很多东西，目前写的只是游戏脚本，以后在其他地方应该可以套用
    """

    def __init__(self):
        super().__init__()
        self.path = "Window/"

        self.simulatorIcon = self.myPath("dn_icon")
        self.simulatorWindow = self.myPath("dn_window")


class Arknights(ImagePath):
    """
    游戏内的杂七杂八的全都在这里面，以后如果写其他的再细分
    """

    def __init__(self):
        super().__init__()
        self.path = "Arknights/"

        # 终端
        self.terminal = self.myPath("zhongduan")
        # 集成战略
        self.rogue = self.myPath("jichengzhanlue")
        # 1x
        self.speed1x = self.myPath("1x")
        # 接管作战
        self.takeOver = self.myPath("jieguanzuozhan")
        # 全员信赖
        self.trustUp = self.myPath("quanyuanxinlai")
        # 开始行动蓝
        self.startActionBlue = self.myPath("kaishixingdong_blue")
        # 开始行动红
        self.startActionRed = self.myPath("kaishixingdong_red")
        # 进驻总览
        self.overview = self.myPath("jinzhuzonglan")

        self.exterminateOver = self.myPath("jiaomiejieshu")
        self.noBrainConfirm = self.myPath("nobrain_confirm")
        # 基建总览:撤下干员
        self.cancelAgent = self.myPath("chexiaganyuan")
        # 总览小红脸
        self.tiredOverview = self.myPath("xiaohonglian_overview")
        # 总览小绿脸
        self.energeticOverview = self.myPath("xiaolvlian_overview")
        # 列表小绿脸
        self.energeticInList = self.myPath("xiaolvlian_list")
        # 列表小绿脸(已勾选)
        self.energeticCheckedInList = self.myPath("xiaolvlian_checked_list")
        # 列表小红脸
        self.tiredInList = self.myPath("xiaohonglian_list")
        # 列表小红脸(已勾选)
        self.tiredCheckedInList = self.myPath("xiaohonglian_checked_list")
        # 列表小黄脸
        self.littleTiredInList = self.myPath("xiaohuanglian_list")
        # 工作中(受背景影响)
        self.onShift = self.myPath("gongzuozhong")
        # 总览空位
        self.blankOverview = self.myPath("blank_overview")
        # 宿(舍)
        self.dormitory = self.myPath("sushe")

        # NOTIFICATION
        self.notification = self.myPath("notification")
        # 可收获
        self.canGet = self.myPath("keshouhuo")
        # 订单交付
        self.deliverOrders = self.myPath("dingdanjiaofu")
        # 干员信赖
        self.getTrust = self.myPath("ganyuanxinlai")

        # 贸易战:获取中
        self.inTrading = self.myPath("huoquzhong")
        # 贸易战:无人机协助
        self.UAV = self.myPath("wurenjixiezhu")


class Agent(ImagePath):
    """
    各种干员头像，招募的作战的，可能还有基建的等等，注意尾缀就行
    """

    def __init__(self):
        super().__init__()
        self.path = "Agent/"

        # 招募头像
        self.banDianZM = self.myPath("bandian_zhaomu")
        self.yangZM = self.myPath("yang_zhaomu")
        self.keLuoSiZM = self.myPath("keluosi_zhaomu")

        # 作战大头贴
        self.banDianZZ = self.myPath("bandian_zuozhan")
        self.yangZZ = self.myPath("yang_zuozhan")
        self.keLuoSiZZ = self.myPath("keluosi_zuozhan")


class Rogue(ImagePath):
    """
    各种干员头像，招募的作战的，可能还有基建的等等，注意尾缀就行
    """

    def __init__(self):
        super().__init__()
        self.path = "Rogue/"

        self.organize = self.myPath("biandui")
        self.mainPage = self.myPath("rougezhuye")

        self.encounterPrizes = [
            self.myPath("prize_youyizhizheng"),
            self.myPath("prize_mamu"),
            self.myPath("prize_kandezhihua"),

            self.myPath("prize_run"),

            self.myPath("prize_stone"),
            self.myPath("prize_hope"),
            self.myPath("prize_health"),
        ]

        self.wasted = self.myPath("lianxizhongduan")
        self.passBattle = self.myPath("chenggongtongguo")
        self.takeItem = self.myPath("nazou_item")
        self.noTake = self.myPath("zoule")
        self.noTakeConfirm = self.myPath("zoule_red")
        self.alter = self.myPath("jitan")
        self.recruit = self.myPath("zhaomu")
        self.quitRed = self.myPath("hongsetuichu")
        self.invest = self.myPath("touzi")
        self.giveUp = self.myPath("fangqibencitansuo")


class Floor(ImagePath):
    """
    肉鸽内各类floor
    """

    def __init__(self):
        super().__init__()
        self.path = "Floor/"

        self.floorXSXW = self.myPath("xunshouxiaowu")
        self.floorYW = self.myPath("yiwai")
        self.floorYCWB = self.myPath("yuchongweiban")
        self.floorLPXD = self.myPath("lipaoxiaodui")

        self.floorXSXWJJ = self.myPath("xunshouxiaowu_jinji")
        self.floorYWJJ = self.myPath("yiwai_jinji")
        self.floorYCWBJJ = self.myPath("yuchongweiban_jinji")
        self.floorLPXDJJ = self.myPath("lipaoxiaodui_jinji")

        self.floorBQEY = self.myPath("buqieryu")
        self.floorGYXS = self.myPath("guiyixingshang")
        self.floorMJYX = self.myPath("mujianyuxing")


class Test(ImagePath):
    """
    用于测试
    """

    def __init__(self):
        super().__init__()
        self.path = "test/"

        self.testImage = self.myPath("myTest")


ark_image = Arknights()

if __name__ == '__main__':
    test = Test()
    print(test.testImage)
