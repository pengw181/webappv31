# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/29 下午5:14

from common.log.logger import log
from app.AiSee.main.login_page import login
from common.variable.global_variable import *
from config.loads import properties
from app.com.login.loads import login_config
from app.com.login.statics_login import login_tool
from app.AiSee.main.main_page import AiSee
from app.VisualModeler.doctorwho.doctor_who import DoctorWho
from common.page.handle.windows import WindowHandles
from selenium.common.exceptions import NoSuchElementException


# 定义一个自动检测登录vm的装饰器
def auto_enter_vm(func):
    def wrapper(*args, **kwargs):
        if func.__name__ in ['LoginAiSee', 'EnterDomain']:
            pass
        else:
            browser = get_global_var("browser")
            try:
                browser.find_element_by_xpath("//*[@id='userName']")
            except AttributeError:
                log.info("当前未登录，自动执行登录操作")
                arg1 = {
                    "操作": "LoginAiSee",
                    "参数": {
                        "用户名": get_global_var("LoginUser"),
                        "密码": get_global_var("LoginPwd")
                    }
                }
                username = arg1.get("参数").get("用户名")
                password = arg1.get("参数").get("密码")
                login(username, password)

                arg2 = {
                    "操作": "EnterDomain",
                    "参数": {
                        "归属": get_global_var("Belong"),
                        "领域明细": get_global_var("Domain")
                    }
                }
                action = AiSee()
                action.close_tips()
                belong = arg2.get("参数").get("归属")
                domain = arg2.get("参数").get("领域明细")
                action.enter_domain(belong, domain)
            except NoSuchElementException:
                if browser.current_window_handle == get_global_var("WinHandles").get("流程图编辑器"):
                    log.info("当前处于流程图编辑器窗口")
                    pass
                else:
                    log.info("当前已登录，未进入领域，自动进入广州核心网")
                    arg2 = {
                        "操作": "EnterDomain",
                        "参数": {
                            "归属": get_global_var("Belong"),
                            "领域明细": get_global_var("Domain")
                        }
                    }
                    action = AiSee()
                    belong = arg2.get("参数").get("归属")
                    domain = arg2.get("参数").get("领域明细")
                    action.enter_domain(belong, domain)
        return func(*args, **kwargs)

    return wrapper


# 定义一个自动检测登录aisee的装饰器
def auto_login_aisee(func):
    def wrapper(*args, **kwargs):
        if func.__name__ in ['LoginAiSee']:
            pass
        else:
            browser = get_global_var("browser")
            try:
                browser.find_element_by_xpath("//*[@id='userName']")
            except AttributeError:
                log.info("当前未登录，自动执行登录操作")
                arg1 = {
                    "操作": "LoginAiSee",
                    "参数": {
                        "用户名": get_global_var("LoginUser"),
                        "密码": get_global_var("LoginPwd")
                    }
                }
                username = arg1.get("参数").get("用户名")
                password = arg1.get("参数").get("密码")
                login(username, password)
            except NoSuchElementException:
                log.info("用户当前已登录")
        return func(*args, **kwargs)

    return wrapper


# 定义一个自动检测登录的装饰器
def auto_login_tool(func):
    def wrapper(*args, **kwargs):
        browser = get_global_var("browser")
        try:
            browser.find_element_by_xpath("//*[@menuid='CrawlerApp1000']")
        except AttributeError:
            log.info("当前未登录，自动执行登录操作")
            arg1 = {
                "系统": properties.get("app"),
                "用户名": login_config.get("username"),
                "密码": login_config.get("password"),
                "应用跳转url": login_config.get("redirect_url"),
                "appId": login_config.get("appid"),
                "领域明细": login_config.get("domain_detail"),
                "dsKey": login_config.get("dskey"),
                "客户": login_config.get("custom"),
                "签名秘钥": login_config.get("signature"),
                "语言": login_config.get("language"),
                "登录方式": login_config.get("login_type")
            }
            login_tool(system_name=arg1.get("系统"), username=arg1.get("用户名"), password=arg1.get("密码"),
                       redirect_url=arg1.get("应用跳转url"), appId=arg1.get("appId"), domain_detail=arg1.get("领域明细"),
                       dsKey=arg1.get("dsKey"), custom=arg1.get("客户"), signature=arg1.get("签名秘钥"),
                       language=arg1.get("语言"))

        return func(*args, **kwargs)

    return wrapper


# 定义一个自动从vm进入告警平台的装饰器
def login_alarm_via_vm(func):
    def wrapper(*args, **kwargs):
        browser = get_global_var("browser")
        try:
            browser.find_element_by_xpath("//*[@menuid='CrawlerApp1000']")
        except AttributeError:
            DoctorWho().choose_menu("告警-告警平台")
            # 切换到告警平台窗口
            current_win_handle = WindowHandles()
            current_win_handle.save("告警平台")
            current_win_handle.switch("告警平台")

        return func(*args, **kwargs)

    return wrapper
