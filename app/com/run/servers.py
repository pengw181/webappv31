# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/13 下午5:35

from config.loads import properties
from app.VisualModeler.main.run.servers import actions as visual_actions
from app.Crawler.main.run.servers import actions as crawler_actions
from app.AiSee.main.run.servers import actions as aisee_actions


def server_run(func, param):
    """
    根据系统名称，到指定系统的下加载操作方法
    :param func: 操作
    :param param: 参数
    """
    application = properties.get("application")

    if application == "visualmodeler":
        run_flag = visual_actions(func, param)
    elif application == "crawler":
        run_flag = crawler_actions(func, param)
    elif application == "aisee":
        run_flag = aisee_actions(func, param)
    else:
        raise Exception("非法的application名称: {}".format(application))

    return run_flag


# action = server_run()

