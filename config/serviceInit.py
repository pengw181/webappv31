# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/11/29 下午2:41

from common.variable.globalVariable import *
from datetime import datetime


def service_init():

    # 根据当前时间设置时间
    now = datetime.now()
    set_global_var("Y", now.strftime('%Y'))
    set_global_var("YM", now.strftime('%Y%m'))
    set_global_var("YMD", now.strftime('%Y%m%d'))

    # 设置当前默认数据库
    set_global_var("Database", "v31.postgres")

    # 第三方系统测试系统ip
    set_global_var("ThirdSystem", "http://192.168.88.116:9312")

    # 第三方接口模拟ip
    set_global_var("MockIp", "192.168.88.204")

    # 当前数据库类型
    set_global_var("DatabaseType", "postgres")

    # 邮箱密码
    set_global_var("EmailPwd", "P!w0401030990")
    set_global_var("EmailPwd2", "Pw0401030990")  # outlook邮箱

    # 告警平台用告警规则表名，根据数据库类型自动选择
    if get_global_var("DatabaseType") == "oracle":
        set_global_var("AlarmTableName", get_global_var("AlarmTableNameO"), "service")
    elif get_global_var("DatabaseType") == "mysql":
        set_global_var("AlarmTableName", get_global_var("AlarmTableNameM"), "service")
    else:
        set_global_var("AlarmTableName", get_global_var("AlarmTableNameP"), "service")

    # 告警平台用告警规则表名，根据数据库类型自动选择
    set_global_var("AlarmRuleTableName", get_global_var("AlarmTableName"), "service")