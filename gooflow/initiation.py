# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/8/17 下午3:44

import os
from config.loads import properties
from common.log.logger import log
from database.SQLHelper import SQLUtil
from common.variable.globalVariable import *
from config.serviceInit import service_init


class Initiation:

    def __init__(self):
        log.info("启动初始化任务..")

    @staticmethod
    def clear_var():

        # 清空过程变量值
        clear_process_var()
        log.info("清理流程过程变量")

    @staticmethod
    def remove_download_file():

        # 清空下载目录里的文件
        download_path = properties.get("downLoadPath")
        for f in os.listdir(download_path):
            file_data = download_path + f
            if os.path.isfile(file_data):
                os.remove(file_data)
        log.info("清理临时下载文件")

    @staticmethod
    def init_zg_table(db, server_var_name, table_zh_name, temp_type):

        # 根据中文名，获取表英文名
        sql_util = SQLUtil(db, "main")
        sql = "select zg_table_name from zg_temp_cfg where zg_temp_name='{0}' and zg_temp_type='{1}'".format(
            table_zh_name, temp_type)
        table_en_name = sql_util.select(sql)
        if table_en_name is None:
            log.warn("表【{0}】不存在".format(table_zh_name))
        # 赋值给业务变量
        set_global_var(server_var_name, table_en_name, "service")

    @staticmethod
    def init_cust_table(db, server_var_name, table_zh_name, update_mode):

        # 根据中文名，获取表英文名
        sql_util = SQLUtil(db, "main")
        sql = "select table_name_en from edata_custom_temp where table_name_ch='{0}' and update_mode='{1}'".format(
            table_zh_name, update_mode)
        table_en_name = sql_util.select(sql)
        if table_en_name is None:
            log.warn("表【{0}】不存在".format(table_zh_name))
        # 赋值给业务变量
        set_global_var(server_var_name, table_en_name, "service")


def initiation_work():

    init = Initiation()

    # 临时文件清理
    init.remove_download_file()

    db = properties.get("environment")
    # 业务变量赋值
    init.init_zg_table(db, "BasicInfoTableName", "auto_网元基础信息表", "1")
    init.init_zg_table(db, "SupplyInfoTableName", "auto_网元辅助资料", "2")
    init.init_zg_table(db, "OtherInfoTableName", "auto_网元其它资料", "3")

    set_global_var("DatabaseP", "v31.postgres")
    set_global_var("DatabaseO", "gmcc.oracle")
    set_global_var("DatabaseM", "v3.maria")

    if get_global_var("Application") == "AlarmPlatform":
        # 告警平台用postgres告警表名
        init.init_zg_table(get_global_var("DatabaseP"), "AlarmTableNameP", "auto_测试告警表", "3")
        # 告警平台用mysql告警表名
        init.init_zg_table(get_global_var("DatabaseM"), "AlarmTableNameM", "auto_测试告警表", "3")
        # 告警平台用oracle告警表名
        init.init_zg_table(get_global_var("DatabaseO"), "AlarmTableNameO", "auto_测试告警表", "3")
        # 告警平台用postgres输出表名
        init.init_zg_table(get_global_var("DatabaseP"), "OutputTableName", "auto_测试输出表", "3")

    init.init_cust_table(db, "Edata1TableName", "pw自动化数据拼盘_二维表模式", "2D_TABLE_MODE")
    init.init_cust_table(db, "Edata2TableName", "pw自动化数据拼盘_列更新模式", "NORMAL_MODE")
    init.init_cust_table(db, "Edata3TableName", "pw自动化数据拼盘_分段模式", "SUBSECTION_MODE")
    init.init_cust_table(db, "Edata4TableName", "pw自动化数据拼盘_数据模式", "DATA_MODE")
    init.init_cust_table(db, "Edata5TableName", "pw自动化数据拼盘_合并join模式", "JOIN_MODE")

    # 其它业务参数初始化
    service_init()

    log.info("加载业务参数配置...")
    for key, value in global_set.get("service").items():
        log.info("{0}: {1}".format(key, value))
    log.info("加载业务参数完成。")

