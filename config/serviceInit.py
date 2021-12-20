# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/11/29 下午2:41

from common.variable.global_variable import *
from config.loads import properties


def service_init():
    # 设置当前默认数据库
    set_global_var("Database", "v31.postgres")

    # 设置当前environment，mongodb用到，必须项
    properties["environment"] = "v31.postgres"

    # 设置当前测试应用名称，必须项，与测试用例目录名一致。aisee、visualmodeler、crawler等
    properties["application"] = "visualmodeler"

    # 第三方系统测试系统ip
    set_global_var("ThirdSystem", "http://192.168.88.116:9312")

    # 当前数据库类型
    set_global_var("DatabaseType", "postgres")

    # 网元基础信息表名
    set_global_var("BasicInfoTableName", "ZG_FUT61SGROK")

    # 网元辅助资料表名
    set_global_var("SupplyInfoTableName", "ZG_P_X5ZFE3RQ7C")

    # 网元其它资料表名
    set_global_var("OtherInfoTableName", "ZG_O_AZC9ULO480")

    # 数据拼盘二维表模式表名
    set_global_var("Edata1TableName", "CUST_TABLE_6UYB0HD53L")

    # 数据拼盘列更新模式表名
    set_global_var("Edata2TableName", "CUST_NORMAL_76R34SEQI8")

    # 数据拼盘分段模式表名
    set_global_var("Edata3TableName", "CUST_SECTION_C67HXPSZRG")

    # 数据拼盘数据模式表名
    set_global_var("Edata4TableName", "CUST_DATA_1RSTXIA5NW")

    # 数据拼盘合并模式表名
    set_global_var("Edata5TableName", "CUST_JOIN_E0OGY9BX3F")

