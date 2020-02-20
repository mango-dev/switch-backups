import os
from utils.logs import LogConfig
import logging
import traceback
from switch.copy import FileCopy

PATH = os.path.split(os.path.realpath(__file__))[0]

if __name__ == '__main__':
    try:
        LogConfig(PATH)
        logging.info("脚本初始化完成.")
        # TODO:程序执行入口
        FileCopy().telnet()
        logging.info("脚本执行完成.")
        pass
    except Exception as ex:
        msg = traceback.format_exc()
        logging.error(msg)
        pass
    finally:
        logging.info("脚本执行结束.")
        pass