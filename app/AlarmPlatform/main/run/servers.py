# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/12/24 下午3:13

from app.com.wrapper.auto_login import auto_enter_vm, enter_platform


@auto_enter_vm
@enter_platform(platform="告警平台")
def actions(func, param):

    run_flag = True

    if func == "AddDatabase":
        pass

    return run_flag
