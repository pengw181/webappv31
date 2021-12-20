# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/8/17 下午3:44

import os
from common.variable.global_variable import clear_process_var
from config.loads import properties
from common.log.logger import log


def init():

    log.info("启动测试初始化任务..")
    # 清空过程变量值
    clear_process_var()

    # 清空下载目录里的文件
    download_path = properties.get("downLoadPath")
    for f in os.listdir(download_path):
        file_data = download_path + f
        # log.info(file_data)
        if os.path.isfile(file_data):
            os.remove(file_data)
    log.info("初始化完成.")



