# 基于雷电模拟器1600:900
class ArkPosition(object):
    # 灰色返回键，应该是全世界都统一
    back = (116, 45)
    # skip，应该所有的都是这个位置
    skip = (1525, 50)
    # 开始行动，蓝色，通用键
    startActionBlue = (1428, 820)
    # 开始行动，红色，通用键
    startActionRed = (1370, 645)
    # 购买理智确认键
    replenish = (1362, 723)
    # 基建
    baseStation = (1231, 755)
    # 进驻总览
    overview = (150, 150)

    # 基建换人界面确认
    substitutionConfirm = (1477, 850)
    # 左建筑群:1-1
    leftFloor11 = (260, 400)
    # 贸易战加速：最多
    mostInTradeAccelerate = (1200, 423)
    # 贸易战加速：确定
    confirmBlueInTradeAccelerate = (1185, 725)

    # 肉鸽主界面开始探索
    startExplore = (1450, 750)
    # 指挥分队(默认分队应该是人人都有，而且是第一个，定位靠下方便连点)
    teamZHFD = (215, 745)
    # 稳扎稳打(定位靠下方便连点)
    recruitComboWZWD = (622, 750)
    # 招募键*3
    recruitList = [(439, 687), (802, 687), (1161, 687)]
    # 确认招募，蓝色(和新编队时确认时使用的蓝色按键是同一位置)
    recruitConfirm = (1456, 850)
    # 招募：第一个干员的位置
    recruitFirstAgent = (686, 190)
    # 进入古堡
    enterCastle = (1500, 440)
    # 肉鸽编队
    organize = (1380, 847)
    # 用于编队连点(加号/第一位干员二合一)
    addAgent = (650, 140)
    # 进入ENTER
    enterFloor = (1435, 615)
    # 开始行动
    startActionRed_rogue = (1365, 845)
    # 肉鸽内安全点，怎么点都不太可能点到控件的地方(左下角)
    safePoint = (55, 740)
    # 离开商店，需要连点
    quitStore = (1530, 684)
    # 放弃本次探索
    giveUpRogue = (1458, 402)
    # 确认放弃探索
    giveUpRogueConfirmRed = (1056, 622)
    # 结算时持续点击的位置，有一个灰色的√
    giveUpConstantConfirm = (800, 800)
    # 第一件商品位置
    storeItem1 = (642, 243)
    # 第二件商品位置(一定是支援器械)
    storeItem2 = (890, 269)
    # 确认购买
    purchaseConfirm = (1236, 620)


ark_position = ArkPosition()
