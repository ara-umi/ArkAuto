from mywin32.handle import HandleGetter

# 模拟器类型
getHandle = HandleGetter.Nox()
# getHandle = HandleGetter.LeiDian()


# 匹配参数
thresh = 0.95
# 读取模式
read_mode = 1
# 寻找按钮超时
find_button_timeout = 5
# 寻找间隙，建议不要调太低
find_button_interval = 0.5
