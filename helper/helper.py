import time


# 显示时间装饰器
def show_time_self(func):
    def main(self, *args, **kwargs):
        print(f"\n{time.strftime('%m-%d %H:%M:%S', time.localtime())}")
        func(self, *args, **kwargs)

    return main


def show_time_static(func):
    def main(*args, **kwargs):
        print(f"\n{time.strftime('%m-%d %H:%M:%S', time.localtime())}")
        func(*args, **kwargs)

    return main


# 计时装饰器
def count_time_self(func):
    def main(self, *args, **kwargs):
        start_time = time.time()
        func(self, *args, **kwargs)
        over_time = time.time()
        total_time = over_time - start_time
        print(f"耗时{total_time:.2f}秒")

    return main


def count_time_static(func):
    def main(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        over_time = time.time()
        total_time = over_time - start_time
        print(f"耗时{total_time:.2f}秒")

    return main


# 获取当前时间(无特殊符号用于做文件头)
def now_time():
    return time.strftime('%m%d%H%M%S', time.localtime())


# 打印当前时间(已格式化)
def print_now_time():
    print(time.strftime('%m-%d %H:%M:%S', time.localtime()))


if __name__ == '__main__':
    print_now_time()
