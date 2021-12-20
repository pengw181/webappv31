# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 上午11:18

from common.variable.global_variable import *


def store_error_code(msg):
    if msg:
        if get_global_var("ErrorMsg") is None:
            set_global_var("ErrorMsg", msg, False)
        else:
            msg = str(get_global_var("ErrorMsg")) + '\n' + msg
            set_global_var("ErrorMsg", msg, False)
    return
