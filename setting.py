import logging

from mywin32.handle import HandleGetter
from position import ArkPosition as ark_position


# 模拟器类型
def getHandle():
    # return HandleGetter.Nox()
    # return HandleGetter.LeiDian()
    return HandleGetter.Xiaoyao()


# 分辨率
w = 1600
h = 900

# 日志情况
logging_dict = {
    "level": logging.DEBUG,
    "filename": None,
    "format": "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    "datefmt": "%a-%d-%b %H:%M:%S",
    "filemode": "w"
}
# 控制台显示
console_handler_level = logging.CRITICAL

# 自适应分辨率
selfAdaptation = 1

# 默认截图存储名称/格式
default_save_name = "screenshot.bmp"

# 默认加速位置(左侧第一间，类型1为贸易，2为制造)
accelerateFloor = ark_position.leftFloor11
accelerateType = 1

# 匹配参数
thresh = 0.95
# 读取模式
read_mode = 1
# 寻找按钮超时
find_button_timeout = 5
# 寻找间隙，建议不要调太低
find_button_interval = 0.5
