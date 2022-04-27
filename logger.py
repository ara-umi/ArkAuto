#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os

from helper.helper import now_time
from setting import logging_dict, console_handler_level

root = os.path.abspath(os.path.dirname(__file__))


def get_logger(chlr_level=console_handler_level):
    """
    :param chlr_level:
        主要控制console， file中的level靠setting中修改，默认是最高的debug(其实就等于notset，全写入)
        critical 50
        error 40
        warning 30
        info 20
        debug 10
        notset 0
    :return: logger
    """
    log_dir = root + "\\log\\"
    log_path = log_dir + now_time() + ".log"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging_dict["filename"] = log_path
    logger = logging.getLogger()
    logger.setLevel(logging_dict["level"])
    BASIC_FORMAT = logging_dict["format"]
    DATE_FORMAT = logging_dict["datefmt"]
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

    # 输出到console
    chlr = logging.StreamHandler()
    chlr.setFormatter(formatter)
    chlr.setLevel(chlr_level)

    # 输出到文件(level沿用logger的level)
    fhlr = logging.FileHandler(logging_dict["filename"])
    fhlr.setFormatter(formatter)

    logger.addHandler(chlr)
    logger.addHandler(fhlr)

    return logger


if __name__ == '__main__':
    logger = get_logger()
    logger.debug("this is debug")
    logger.info("this is info")
