# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午4:06

from common.page.func.alert_box import BeAlertBox
from time import sleep
from common.page.func.process_var import choose_var
from common.log.logger import log
from common.variable.global_variable import *


def ai_business(node_name, mode, algorithm, model, var_name, param_map, interval, advance_set):
    """
    :param node_name: 节点名称
    :param mode: 节点模式
    :param algorithm: 算法选择
    :param model: 模型
    :param var_name: 输入变量
    :param param_map: 对应关系配置，字典
    :param interval: 预测步长
    :param advance_set: 高级配置，字典

    {
        "操作": "NodeBusinessConf",
        "参数": {
            "流程名称": "pw自动化测试流程新",
            "节点类型": "AI节点",
            "节点名称": "AI节点",
            "业务配置": {
                "节点名称": "AI节点1",
                "节点模式": "pw测试脚本",
                "算法选择": "V 3",
                "模型": {}
            }
        }
    }

    """
    browser = get_global_var("browser")
    # 设置节点名称
    if node_name:
        browser.find_element_by_xpath("//*[@name='node_name']/preceding-sibling::input[1]").clear()
        browser.find_element_by_xpath("//*[@name='node_name']/preceding-sibling::input[1]").send_keys(node_name)
        log.info("设置节点名称: {0}".format(node_name))
        sleep(1)

    # 节点模式
    if mode:
        browser.find_element_by_xpath("//*[@name='node_model_id']/preceding-sibling::input").click()
        mode_element = browser.find_element_by_xpath("//*[contains(@id,'node_model_id') and text()='{0}']".format(mode))
        browser.execute_script("arguments[0].scrollIntoView(true);", mode)
        mode_element.click()
        log.info("设置节点模式: {0}".format(mode))
        sleep(1)

    # 算法选择
    if algorithm:
        browser.find_element_by_xpath("//*[@name='algorithmId']/preceding-sibling::input").click()
        algorithm_element = browser.find_element_by_xpath(
            "//*[contains(@id,'algorithmId') and text()='{0}']".format(algorithm))
        browser.execute_script("arguments[0].scrollIntoView(true);", algorithm_element)
        algorithm_element.click()
        log.info("设置算法选择: {0}".format(algorithm))
        sleep(1)

    # 模型
    if model:
        browser.find_element_by_xpath("//*[@name='algorithmModeId']/preceding-sibling::input").click()
        model_element = browser.find_element_by_xpath(
            "//*[contains(@id,'algorithmModeId') and text()='{0}']".format(model))
        browser.execute_script("arguments[0].scrollIntoView(true);", model_element)
        model_element.click()
        log.info("设置模型: {0}".format(model))
        sleep(1)

    # 输入变量
    if var_name:
        browser.find_element_by_xpath("//*[@id='dataH_inputVarName']/following-sibling::span//a").click()
        choose_var(var_name=var_name)
        log.info("设置输入变量: {0}".format(var_name))
        sleep(1)

    # 对应关系配置
    if param_map:
        log.info("开始配置脚本参数")
        num = 2
        for index, col_name in param_map:
            browser.find_element_by_xpath("//*[@name='relaCol{0}']/preceding-sibling::input".format(num)).clear()
            browser.find_element_by_xpath(
                "//*[@name='relaCol{0}']/preceding-sibling::input".format(num)).send_keys(index)
            browser.find_element_by_xpath(
                "//*[@id='cfgcoltype{0}']/following-sibling::span//input[1]".format(num)).click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'cfgcoltype{0}') and contains(text(),'{1}')]".format(num, col_name)).click()
            if num < len(param_map) + 1:
                browser.find_element_by_xpath(
                    "//*[@id='cfgcoltype{0}']/../following-sibling::div[1]/*[@onclick='addIrRelaItem(this)']".format(
                        num)).click()
            num += 1
            sleep(1)

    # 预测步长
    if interval:
        interval_element = browser.find_element_by_xpath("//*[@value='预测步长']/following-sibling::input[1]")
        browser.execute_script("arguments[0].scrollIntoView(true);", interval_element)
        interval_element.clear()
        interval_element.send_keys(interval)
        log.info("设置预测步长: {0}".format(interval))
        sleep(1)

    # 设置高级模式
    if advance_set:
        log.info("开启高级模式")
        timeout = advance_set.get("超时时间")
        retry_times = advance_set.get("超时重试次数")
        browser.find_element_by_xpath("//*[@onclick='toggleAdv($(this))']/span/span[1]").click()
        browser.find_element_by_xpath("//*[@name='aiTimeout']/preceding-sibling::input").clear()
        browser.find_element_by_xpath("//*[@name='aiTimeout']/preceding-sibling::input").send_keys(timeout)
        browser.find_element_by_xpath("//*[@name='tryTime']/preceding-sibling::input").clear()
        browser.find_element_by_xpath("//*[@name='tryTime']/preceding-sibling::input").send_keys(retry_times)
        sleep(1)

    # 获取节点名称
    node_name = browser.find_element_by_xpath(
        "//*[@name='node_name']/preceding-sibling::input[1]").get_attribute("value")

    # 保存业务配置
    browser.find_element_by_xpath("//*[@onclick='saveIRContent(true)']//*[text()='保存']").click()
    log.info("保存业务配置")

    alert = BeAlertBox(back_iframe="default")
    msg = alert.get_msg()
    if alert.title_contains("操作成功"):
        log.info("保存业务配置成功")
    else:
        log.warn("保存业务配置失败，失败提示: {0}".format(msg))
    set_global_var("ResultMsg", msg, False)

    # 刷新页面，返回画流程图
    browser.refresh()
    return node_name
