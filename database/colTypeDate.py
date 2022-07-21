# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2022/6/22 上午10:44


def checkColTypeDate(col):
    """
    # 判断当前字段是否时间字段
    # create_time: True
    # create_date: True
    # try_time: False
    # cmd_timeout: False
    :return: True/False
    """
    col = str(col.upper())
    if (col[-4:] == "TIME" or col[-4:] == "DATE") and col.find("TRY") == -1:
        # create_time/create_date
        date_type = True
    elif col[-4:] == "TIME" and col.find("TRY") > -1:
        # try_time
        date_type = False
    else:
        # cmd_timeout
        date_type = False
    return date_type


if __name__ == "__main__":
    col_name = "try_time"
    print(checkColTypeDate(col_name))
