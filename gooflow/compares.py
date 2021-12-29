# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 上午11:14

from common.variable.global_variable import *
from datetime import datetime
from time import sleep
from gooflow.checks import check_db_data, check_msg
from common.download.download import exist_download_file
from database.SQLHelper import SQLUtil
from config.schemaMap import get_schema
from gooflow.codes import store_error_code
from common.log.logger import log


def compare_data(checks):
    """"
    :param: checks：string
    :return: bool
    """

    # 定义一个检查标识
    check_result = True
    sleep(3)

    if checks:
        check_list = checks.split(chr(10))    # 第一次使用换行拆分比对预期结果单元格内容

        for i in range(len(check_list)):

            log.info("开始处理 {0}".format(check_list[i]))
            set_global_var("EndTime", datetime.now().strftime('%Y%m%d%H%M%S'), False)
            if check_list[i].strip() == "":
                # 为空不匹配，默认成功
                check_result = True
            else:
                my_list = check_list[i].split('|')   # 将数据以竖线分割
                compare_item = my_list[0]       # CheckData

                if compare_item == "CheckData":
                    db_schema_table = my_list[1]
                    # log.info("db_schema_table: {}".format(db_schema_table))
                    # ${Database}.main.tn_process_conf_info
                    tmp = db_schema_table.split(".")
                    table_name = tmp[-1]
                    schema = tmp[-2]
                    db = ".".join(tmp[: -2])
                    if schema == "nu":
                        table_name = schema + '.' + table_name
                        schema = "sso"

                    count = my_list[2]
                    data = "|".join(my_list[3:])

                    # 自动替换${xx}变量
                    db = replace_global_var(db)
                    log.info("db: {}".format(db))
                    log.info("schema: {}".format(get_schema(schema)))
                    data = replace_global_var(data)
                    log.info("data: {}".format(data))

                    # 对于匹配字段里有～的，替换成换行
                    data = data.replace("~", r"\r\n")

                    check_result = check_db_data(db, schema, table_name, data, count)
                    if not check_result.get("status"):
                        store_error_code("{0}表数据不匹配，{1}".format(table_name, check_result.get("data")))
                        check_result = False
                        break

                elif compare_item == "CheckMsg":
                    # 校验弹出框信息
                    check_result = check_msg(msg=my_list[1])
                    if not check_result:
                        store_error_code("ErrorMsg不匹配，弹出框返回: {}".format(get_global_var("ResultMsg")))
                        break

                elif compare_item == "CheckDownloadFile":
                    # 检验下载文件名
                    my_list = check_list[i].split('|', 2)
                    sleep(5)
                    check_result = exist_download_file(filename=my_list[1], file_suffix=my_list[2])
                    if not check_result:
                        store_error_code("下载文件名不匹配")
                        break

                elif compare_item == "CheckFile":
                    # 文件目录管理判断上传文件是否正确
                    if my_list[1] != get_global_var("CheckFileName"):
                        check_result = False
                        store_error_code("文件名比对失败，实际文件名: {0}".format(get_global_var("CheckFileName")))
                        break
                    else:
                        check_result = True

                elif compare_item == "NoCheck":
                    # 不校验，只要前面步骤不报错，直接通过
                    log.info("本条匹配项不做匹配，跳过")
                    pass

                elif compare_item == "Wait":
                    sleep_time = int(my_list[1])
                    log.info("Sleep {} seconds".format(sleep_time))
                    sleep(sleep_time)

                elif compare_item == "GetData":
                    # GetData|${Database}.main|select xx from xx|NodeID
                    # 将sql查询到的结果，赋值给新变量名NodeID，匹配结果中，以${NodeID}使用变量的值
                    db_tmp = my_list[1].split(".")

                    schema = db_tmp[-1]
                    db = ".".join(db_tmp[: -1])
                    # schema = get_schema(schema)
                    # 如果没创建nu，使用sso登录，但sql语句里需要主动加上nu.前缀
                    if schema == "nu":
                        schema = "sso"
                    log.info("db: {}".format(db))
                    log.info("schema: {}".format(get_schema(schema)))
                    sql = my_list[2]
                    # 自动替换${xx}变量
                    db = replace_global_var(db)
                    sql = replace_global_var(sql)

                    sql_util = SQLUtil(db=db, schema=schema)
                    sql_result = sql_util.select(sql)
                    # 将查到的结果，存入全局变量
                    set_global_var(my_list[3].strip(), sql_result)

                else:
                    log.error("非法比对函数: {0}".format(compare_item))
                    store_error_code("无法找到对应比对函数{0}".format(compare_item))
                    check_result = False
                    break

    # 判断返回结果
    return check_result
