# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/13 下午5:35

from common.variable.globalVariable import *
from app.VisualModeler.main.run.servers import actions as visual_actions
from app.Crawler.main.run.servers import actions as crawler_actions
from app.AiSee.main.run.servers import actions as aisee_actions
from app.AlarmPlatform.main.run.servers import actions as alarm_actions


def server_run(func, param):
    """
    根据系统名称，到指定系统的目录下加载操作方法
    :param func: 操作
    :param param: 参数
    """
    application = get_global_var("Application")

    if application == "VisualModeler":
        run_flag = visual_actions(func, param)
    elif application == "Crawler":
        run_flag = crawler_actions(func, param)
    elif application == "AiSee":
        run_flag = aisee_actions(func, param)
    elif application == "AlarmPlatform":
        run_flag = alarm_actions(func, param)
    else:
        raise Exception("非法的application名称: {}".format(application))

    return run_flag


# action = server_run()

