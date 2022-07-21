# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午10:48

from datetime import datetime
import json
from time import sleep
from app.AiSee.main.loginPage import login
from app.AiSee.main.mainPage import AiSee
from common.log.logger import log
from common.variable.globalVariable import *
from common.run.servers import server_run


def basic_run(steps):
    # 定义一个标识，True/False，用于判断步骤是否执行正确
    run_flag = False

    # 多个操作以至少3个横杆换行分割
    patt = r"-{3,}"
    step_list = re.split(patt, steps)

    for step_one in step_list:

        # 每一个操作格式：
        """
        {
            "操作": "xxx",
            "参数": {
                "xxx": "xxx",
                "xxx": "xxx"
            }  
        }          
        """

        # 开始执行，func为操作方法名
        step_one = str(step_one).strip()
        # 替换变量
        step_one = replace_global_var(step_one)
        log.info("步骤：\n%s" % json.dumps(json.loads(step_one), indent=4, ensure_ascii=False))
        func = eval(step_one).get("操作")
        param = eval(step_one).get("参数")
        log.info("开始执行操作： {0}".format(func))
        # log.info("参数： {0}".format(param))
        if func == "LoginAiSee":

            """
            {
                "操作": "LoginAiSee",
                "参数": {
                    "用户名": "pw",
                    "密码": "1qazXSW#"
                }  
            }  
            """
            username = param.get("用户名")
            password = param.get("密码")
            run_flag = login(username, password)
            sleep(2)

        elif func == "EnterDomain":

            """
            {
                "操作": "EnterDomain",
                "参数": {
                    "归属": "广州市",
                    "领域明细": "广州核心网"
                }  
            }
            """

            action = AiSee()
            belong = param.get("归属")
            domain = param.get("领域明细")
            run_flag = action.enter_domain(belong, domain)

        else:
            # 根据系统名称，选择执行具体业务操作
            """
            func = eval(step_one).get("操作")
            param = eval(step_one).get("参数")
            """
            run_flag = server_run(func, param)

    set_global_var("EndTime", datetime.now().strftime('%Y%m%d%H%M%S'), False)
    return run_flag


