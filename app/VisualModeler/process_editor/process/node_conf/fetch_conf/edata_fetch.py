# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午11:32

from time import sleep
from common.page.func.alert_box import BeAlertBox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.page.func.page_mask_wait import page_wait
from common.log.logger import log
from common.variable.global_variable import *


def edata_fetch(opt, target_var, var_name, obj_type, result_type, cmd_name, value_type):
    """
    # 添加
    {
        "操作": "添加",
        "变量名称": "格式化二维表结果",
        "对象类型": "网元",
        "结果类型": "格式化二维表结果",
        "指令": "全部指令",
        "赋值方式": "替换"
    }

    # 修改
    {
        "操作": "修改",
        "目标变量": "格式化二维表结果",
        "变量名称": "解析结果",
        "对象类型": "网元",
        "结果类型": "解析结果",
        "指令": "全部指令",
        "赋值方式": "替换"
    }

    # 删除
    {
        "操作": "删除",
        "目标变量": "解析结果"
    }

    """
    browser = get_global_var("browser")
    page_wait()
    if opt == "添加":
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='addDataVarBtn']//*[text()='添加']")))
        browser.find_element_by_xpath("//*[@id='addDataVarBtn']//*[text()='添加']").click()
        sleep(2)
        browser.switch_to.frame(
            browser.find_element_by_xpath("//iframe[contains(@src,'getdataEdataCustomNodeEdit.html?type=add')]"))
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='varName']/preceding-sibling::input")))
        log.info("添加取数配置")

        # 变量名称
        if var_name:
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").send_keys(var_name)
            log.info("设置变量名称: {0}".format(var_name))
            sleep(1)

        # 对象类型
        if obj_type:
            browser.find_element_by_xpath("//*[@name='objType']/preceding-sibling::input").click()
            browser.find_element_by_xpath("//*[contains(@id,'objType') and text()='{0}']".format(obj_type)).click()
            log.info("设置对象类型: {0}".format(obj_type))
            sleep(1)

        # 结果类型
        if result_type:
            browser.find_element_by_xpath("//*[@name='resultType']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'resultType') and text()='{0}']".format(result_type)).click()
            log.info("设置结果类型: {0}".format(result_type))
            sleep(1)

        # 指令
        if cmd_name:
            browser.find_element_by_xpath("//*[@id='cmdId']/following-sibling::span/input[1]").click()
            browser.find_element_by_xpath("//*[contains(@id,'cmdId') and text()='{0}']".format(cmd_name)).click()
            log.info("设置指令: {0}".format(cmd_name))
            sleep(1)

        # 赋值方式
        if value_type:
            browser.find_element_by_xpath("//*[@name='valueType']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'valuetype_cmd') and text()='{0}']".format(value_type)).click()
            log.info("设置赋值方式: {0}".format(value_type))
            sleep(1)

        # 点击保存
        browser.find_element_by_xpath("//*[@id='saveBtn']//*[text()='保存']").click()

        alert = BeAlertBox(back_iframe="default")
        msg = alert.get_msg()
        if alert.title_contains("操作成功"):
            log.info("保存取数配置成功")
        else:
            log.warn("保存取数配置失败，失败提示: {0}".format(msg))
        set_global_var("ResultMsg", msg, False)

    elif opt == "修改":
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@field='varName']//*[text()='{0}']".format(target_var))))
        browser.find_element_by_xpath("//*[@field='varName']//*[text()='{0}']".format(target_var)).click()
        sleep(1)
        browser.find_element_by_xpath("//*[@onclick='edit_getdata_cmdvar();']//*[text()='修改']").click()
        sleep(1)
        browser.switch_to.frame(
            browser.find_element_by_xpath("//iframe[contains(@src,'getdataEdataCustomNodeEdit.html?type=edit')]"))
        wait = WebDriverWait(browser, 10)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='varName']/preceding-sibling::input")))
        log.info("修改取数配置")

        # 变量名称
        if var_name:
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").send_keys(var_name)
            log.info("设置变量名称: {0}".format(var_name))
            sleep(1)

        # 对象类型
        if obj_type:
            browser.find_element_by_xpath("//*[@name='objType']/preceding-sibling::input").click()
            browser.find_element_by_xpath("//*[contains(@id,'objType') and text()='{0}']".format(obj_type)).click()
            log.info("设置对象类型: {0}".format(obj_type))
            sleep(1)

        # 结果类型
        if result_type:
            browser.find_element_by_xpath("//*[@name='resultType']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'resultType') and text()='{0}']".format(result_type)).click()
            log.info("设置结果类型: {0}".format(result_type))
            sleep(1)

        # 指令
        if cmd_name:
            browser.find_element_by_xpath("//*[@id='cmdId']/following-sibling::span/input[1]").click()
            browser.find_element_by_xpath("//*[contains(@id,'cmdId') and text()='{0}']".format(cmd_name)).click()
            log.info("设置指令: {0}".format(cmd_name))
            sleep(1)

        # 赋值方式
        if value_type:
            browser.find_element_by_xpath("//*[@name='valueType']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type)).click()
            log.info("设置赋值方式: {0}".format(value_type))
            sleep(1)

        # 点击保存
        browser.find_element_by_xpath("//*[@id='saveBtn']//*[text()='保存']").click()

        alert = BeAlertBox(back_iframe="default")
        msg = alert.get_msg()
        if alert.title_contains("操作成功"):
            log.info("保存取数配置成功")
        else:
            log.warn("保存取数配置失败，失败提示: {0}".format(msg))
        set_global_var("ResultMsg", msg, False)

    else:
        browser.find_element_by_xpath("//*[@field='varName']//*[text()='{0}']".format(target_var)).click()
        sleep(1)
        browser.find_element_by_xpath("//*[@onclick='del_getdata_cmdvar();']//*[text()='删除']").click()
        log.info("删除取数配置")

        alert = BeAlertBox(back_iframe="default")
        msg = alert.get_msg()
        if alert.title_contains("您确定需要删除{0}吗".format(target_var), auto_click_ok=False):
            alert.click_ok()

            alert = BeAlertBox(back_iframe=False)
            msg = alert.get_msg()
            if alert.title_contains("操作成功"):
                log.info("删除取数配置成功")
            else:
                log.warn("删除取数配置失败，失败提示: {0}".format(msg))
        else:
            log.warn("删除取数配置失败，失败提示: {0}".format(msg))
        set_global_var("ResultMsg", msg, False)

    # 切换到节点iframe
    browser.switch_to.frame(browser.find_element_by_xpath(get_global_var("NodeIframe")))
    # 切换到取数配置iframe
    browser.switch_to.frame(browser.find_element_by_xpath("//iframe[@id='getdata_edata_custom_node']"))
