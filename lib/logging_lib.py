# coding:UTF-8


"""
记录日志模块
@author: yubang
2016.04.09
"""


import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(name)-12s %(asctime)s level-%(levelname)-8s %(message)s')
fileTimeHandler = TimedRotatingFileHandler("log/app.log", "D", 1, 0)
fileTimeHandler.suffix = "%Y%m%d.log"
fileTimeHandler.setFormatter(formatter)

log = logging.getLogger('app_log')
log.setLevel(logging.INFO)
log.addHandler(fileTimeHandler)



