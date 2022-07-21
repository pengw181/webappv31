# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 上午11:22

from config.loads import properties
from gooflow.controller import case_run
from common.variable.globalVariable import *


def main():

    # runAllTest为true时，runTestLevel不生效；runAllTest为false时，只执行runTestLevel指定级别的用例
    properties["runAllTest"] = True
    # 用例执行失败，是否继续执行下一条
    properties["continueRunWhenError"] = False
    # 设置测试用例覆盖级别
    properties["runTestLevel"] = ["高", "中", "低"]

    # 常用变量赋值
    set_global_var("BelongID", "440100")
    set_global_var("DomainID", "AiSeeCore")
    set_global_var("LoginUser", "pw")
    set_global_var("LoginPwd", "1qazXSW@")
    set_global_var("Belong", "广州市")
    set_global_var("Domain", "广州核心网")

    # 开始运行，第一个数字为读取第几个测试用例文件（从1开始），第二个数字为读取测试用例的第几行（从1开始）
    case_run(15, 14)


if __name__ == "__main__":
    main()
