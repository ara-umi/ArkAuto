from mywin32.handle import HandleGetter


# 模拟器类型
def getHandle():
    return HandleGetter.Nox()
    # return HandleGetter.LeiDian()


# 分辨率
w = 1600
h = 900

# 自适应分辨率
selfAdaptation = 1

# 默认截图存储名称/格式
default_save_name = "screenshot.bmp"

# 匹配参数
thresh = 0.95
# 读取模式
read_mode = 1
# 寻找按钮超时
find_button_timeout = 5
# 寻找间隙，建议不要调太低
find_button_interval = 0.5
