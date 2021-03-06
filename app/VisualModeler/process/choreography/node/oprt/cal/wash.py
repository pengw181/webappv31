# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午10:43

from time import sleep
from common.page.func.processVar import choose_var
from common.page.func.regexp import regular_cube
from common.variable.globalVariable import *
from common.log.logger import log
from common.page.func.alertBox import BeAlertBox


def wash(output_var, input_var, value_type, wash_direction, time_wash, key_wash):
    # 清洗筛选运算
    """
    :param output_var: 变量名称，必填
    :param input_var: 输入变量，必填
    :param value_type: 赋值方式，替换/追加，非必填
    :param wash_direction: 筛选方向，正向/反向，非必填
    :param time_wash: 按时间筛选，字典，非必填
    :param key_wash: 按关键字/变量筛选，字典，非必填

    {
        "变量名称": "清洗筛选运算结果",
        "输入变量": "时间",
        "赋值方式": "替换",
        "筛选方向": "正向",
        "按时间筛选": {
            "flag": "是",
            "时间格式": "yyyy-MM-dd",
            "间隔": "-1",
            "单位": "日",
            "语言": "中文"
        },
        "按关键字/变量筛选": {
            "flag": "是",
            "筛选配置": [
                {
                    "类型": "变量",
                    "值": "时间"
                },
                {
                    "类型": "关键字",
                    "值": {
                        "设置方式": "选择",
                        "正则模版名称": "pw按时间拆分"
                    }
                },
                {
                    "类型": "关键字",
                    "值": {
                        "设置方式": "添加",
                        "正则模版名称": "pw自动化正则模版-清洗筛选运算",
                        "高级模式": "否",
                        "标签配置": [
                            {
                                "标签": "自定义文本",
                                "值": "pw",
                                "是否取值": "黄色"
                            },
                            {
                                "标签": "任意字符",
                                "值": "1到多个",
                                "是否取值": "绿色"
                            },
                            {
                                "标签": "自定义文本",
                                "值": "test",
                                "是否取值": "无"
                            }
                        ]
                    }
                }
            ]
        }
    }

    """
    browser = get_global_var("browser")
    # 切换到清洗筛选运算iframe
    browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'operateCfgWash.html')]"))

    # 变量名称
    if output_var:
        browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").send_keys(output_var)
        log.info("设置输出变量名称: {0}".format(output_var))
        sleep(1)

    # 输入变量
    if input_var:
        browser.find_element_by_xpath("//*[@id='dataH_inputVarName']/following-sibling::span//a").click()
        choose_var(var_name=input_var)
        sleep(1)

    # 赋值方式
    if value_type:
        elements = browser.find_elements_by_xpath("//*[@name='valueType']/preceding-sibling::input")
        for e1 in elements:
            if e1.is_displayed():
                e1.click()
                elements = browser.find_elements_by_xpath(
                    "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type))
                for e2 in elements:
                    if e2.is_displayed():
                        e2.click()
                        log.info("设置赋值方式: {0}".format(value_type))
                        sleep(1)
                        break

    # 筛选方向
    if wash_direction:
        browser.find_element_by_xpath("//*[text()='{0}']/preceding-sibling::input[1]".format(wash_direction)).click()
        log.info("设置筛选方向: {0}".format(wash_direction))
        sleep(1)

    # 按时间筛选
    if time_wash:
        if time_wash.get("flag") == "是":
            flag = True
        else:
            flag = False
        time_wash_action(enable_flag=flag, time_format=time_wash.get("时间格式"), time_interval=time_wash.get("间隔"),
                         time_unit=time_wash.get("单位"), language=time_wash.get("语言"))

    # 按关键字/变量筛选
    if key_wash:
        if key_wash.get("flag") == "是":
            flag = True
        else:
            flag = False
        key_wash_action(enable_flag=flag, filter_set=key_wash.get("筛选配置"))

    # 返回到上层iframe
    browser.switch_to.parent_frame()


def time_wash_action(enable_flag, time_format, time_interval, time_unit, language):
    """
    :param enable_flag: flag，bool
    :param time_format: 时间格式
    :param time_interval: 间隔
    :param time_unit: 单位
    :param language: 语言

    {
        "flag": "是",
        "时间格式": "yyyy-MM-dd",
        "间隔": "-1",
        "单位": "日",
        "语言": "中文"
    }
    """
    browser = get_global_var("browser")
    js = 'return $("#isTime")[0].checked;'
    status = browser.execute_script(js)
    log.info("【按时间筛选】勾选状态: {0}".format(status))
    # 聚焦元素
    time_wash_click = browser.find_element_by_xpath("//*[@id='isTime']")
    browser.execute_script("arguments[0].scrollIntoView(true);", time_wash_click)
    if enable_flag:
        if not status:
            time_wash_click.click()
        log.info("开启【按时间筛选】")

        # 时间格式
        if time_format:
            browser.find_element_by_xpath("//*[@name='format']/preceding-sibling::span//a").click()
            browser.find_element_by_xpath("//*[contains(@id,'format') and text()='{0}']".format(time_format)).click()
            log.info("设置时间格式: {0}".format(time_format))
            sleep(1)

        # 间隔
        if time_interval:
            browser.find_element_by_xpath("//*[@name='interval']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='interval']/preceding-sibling::input").send_keys(time_interval)
            log.info("设置间隔: {0}".format(time_interval))
            sleep(1)

        # 单位
        if time_unit:
            browser.find_element_by_xpath("//*[@id='unit']/following-sibling::span[1]//a").click()
            browser.find_element_by_xpath("//*[contains(@id,'unit') and text()='{0}']".format(time_unit)).click()
            log.info("设置单位: {0}".format(time_unit))
            sleep(1)

        # 语言
        if language:
            browser.find_element_by_xpath("//*[@id='language']/following-sibling::span[1]//a").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'language') and text()='{0}']".format(language)).click()
            log.info("设置语言: {0}".format(language))
            sleep(1)

    else:
        if status:
            # 如果flag为否，但当前已勾选，则再点击一次，取消勾选
            time_wash_click.click()
            log.info("关闭【按时间筛选】")
        else:
            log.info("【按时间筛选】标识为否，不开启")


def key_wash_action(enable_flag, filter_set):

    """
    :param enable_flag: flag，bool
    :param filter_set: 筛选配置，数组

    {
        "flag": "是",
        "筛选配置": [
            {
                "类型": "变量",
                "值": "时间"
            },
            {
                "类型": "关键字",
                "值": {
                    "设置方式": "选择",
                    "正则模版名称": "pw按时间拆分"
                }
            },
            {
                "类型": "关键字",
                "值": {
                    "设置方式": "添加",
                    "正则模版名称": "pw自动化正则模版-清洗筛选运算",
                    "高级模式": "否",
                    "标签配置": [
                        {
                            "标签": "自定义文本",
                            "值": "pw",
                            "是否取值": "黄色"
                        },
                        {
                            "标签": "任意字符",
                            "值": "1到多个",
                            "是否取值": "绿色"
                        },
                        {
                            "标签": "自定义文本",
                            "值": "test",
                            "是否取值": "无"
                        }
                    ]
                }
            }
        ]
    }
    """
    browser = get_global_var("browser")
    js = 'return $("#isKewWordOrVar")[0].checked;'
    status = browser.execute_script(js)
    log.info("【按关键字/变量筛选】勾选状态: {0}".format(status))
    # 聚焦元素
    key_wash_click = browser.find_element_by_xpath("//*[@id='isKewWordOrVar']")
    browser.execute_script("arguments[0].scrollIntoView(true);", key_wash_click)
    if enable_flag:
        if not status:
            key_wash_click.click()
        log.info("开启【按关键字/变量筛选】")

        key_wash_set = filter_set
        key_num = 1
        for key in key_wash_set:
            key_type = key.get("类型")
            key_value = key.get("值")

            if key_num > 1:
                # 点击一次添加关键字或变量
                browser.find_element_by_xpath("//*[@onclick='addKeyOrVar()']//*[text()='添加关键字或变量']").click()
                sleep(1)
            # 点击类型下拉框
            browser.find_element_by_xpath("//*[@id='type{0}']/following-sibling::span[1]//a".format(key_num)).click()
            # 选择类型
            browser.find_element_by_xpath(
                "//*[contains(@id,'type{0}') and text()='{1}']".format(key_num, key_type)).click()
            if key_type == "变量":
                # 选择变量
                browser.find_element_by_xpath(
                    "//*[@id='dataH_inputVar{0}Name']/following-sibling::span//a".format(key_num)).click()
                choose_var(var_name=key_value)
            else:
                browser.find_element_by_xpath(
                    "//*[@id='keyExpr{0}']/following-sibling::span[1]//a".format(key_num)).click()
                # 切换到清洗筛选正则iframe
                browser.switch_to.frame(browser.find_element_by_xpath("//*[contains(@src,'operateWashRegexBox.html')]"))
                sleep(1)
                # 开始配置正则
                confirm_selector = "//*[@id='regexDiv']"
                regular_cube(confirm_selector=confirm_selector, set_type=key_value.get("设置方式"),
                             regular_name=key_value.get("正则模版名称"), advance_mode=key_value.get("高级模式"),
                             regular=key_value.get("标签配置"), expression=key_value.get("表达式"))
                if key_value.get("设置方式") == "添加":
                    alert = BeAlertBox(back_iframe="default")
                    msg = alert.get_msg()
                    if alert.title_contains("成功"):
                        log.info("保存正则模版成功")
                        # 切换到节点iframe
                        browser.switch_to.frame(browser.find_element_by_xpath(get_global_var("NodeIframe")))
                        # 切换到操作配置iframe
                        browser.switch_to.frame(browser.find_element_by_xpath(get_global_var("OptIframe")))
                        # 切换到运算配置iframe
                        browser.switch_to.frame(
                            browser.find_element_by_xpath("//iframe[contains(@src,'operateVar.html')]"))
                        # 切换到清洗筛选运算iframe
                        browser.switch_to.frame(
                            browser.find_element_by_xpath("//iframe[contains(@src,'operateCfgWash.html')]"))
                    else:
                        log.warn("保存正则模版失败，失败提示: {0}".format(msg))
                    set_global_var("resultMsg", msg, False)
                else:
                    # 返回上层iframe
                    browser.switch_to.parent_frame()
                # 关闭正则模版窗口
                browser.find_element_by_xpath("//*[text()='正则魔方']/following-sibling::div/a[2]").click()
            # 更新key_num
            key_num += 1
            sleep(1)

    else:
        if status:
            # 如果flag为否，但当前已勾选，则再点击一次，取消勾选
            key_wash_click.click()
            log.info("关闭【按关键字/变量筛选】")
        else:
            log.info("【按关键字/变量筛选】标识为否，不开启")