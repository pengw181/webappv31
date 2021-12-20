# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午11:35

from time import sleep
from common.page.func.alert_box import BeAlertBox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.log.logger import log
from common.variable.global_variable import *


def email_fetch(opt, target_var, var_name, var_type, attach_type, file_name, value_type):
    """
    :param opt: 操作
    :param target_var: 目标变量
    :param var_name: 变量名称
    :param var_type: 变量类型
    :param attach_type: 附件类型
    :param file_name: 文件名
    :param value_type: 赋值方式

    # 添加
    {
        "操作": "添加",
        "变量名称": "附件内容",
        "变量类型": "附件",
        "附件类型": "xlsx",
        "文件名": "abc",
        "赋值方式": "替换"
    }

    # 修改
    {
        "操作": "修改",
        "目标变量": "附件内容",
        "变量名称": "附件内容1",
        "变量类型": "附件",
        "附件类型": "xls",
        "文件名": "abcd",
        "赋值方式": "替换"
    }

    # 删除
    {
        "操作": "删除",
        "目标变量": "附件内容1"
    }

    """
    browser = get_global_var("browser")
    if opt == "添加":
        browser.find_element_by_xpath("//*[@onclick='addEMailGetInfo()']//*[text()='添加']").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='varName']/preceding-sibling::input")))

        # 变量名称
        if var_name:
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").send_keys(var_name)
            log.info("设置变量名称: {0}".format(var_name))
            sleep(1)

        # 变量类型
        if var_type:
            browser.find_element_by_xpath("//*[@name='varExpr']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'emailtype') and text()='{0}']".format(var_type)).click()
            log.info("设置变量类型: {0}".format(var_type))
            sleep(1)

        # 附件类型
        if attach_type:
            browser.find_element_by_xpath("//*[@name='attachtype']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'getattachtype') and text()='{0}']".format(attach_type)).click()
            log.info("设置附件类型: {0}".format(attach_type))
            sleep(1)

        # 文件名
        if file_name:
            browser.find_element_by_xpath("//*[@name='filename']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='filename']/preceding-sibling::input").send_keys(file_name)
            log.info("设置文件名: {0}".format(file_name))
            sleep(1)

        # 赋值方式
        if value_type:
            browser.find_element_by_xpath("//*[@name='valueType']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type)).click()
            log.info("设置赋值方式: {0}".format(value_type))
            sleep(1)

        # 点击保存
        browser.find_element_by_xpath("//*[@onclick='addEmailDataRow()']//*[text()='保存']").click()

        alert = BeAlertBox(back_iframe="default")
        msg = alert.get_msg()
        if alert.title_contains("操作成功"):
            log.info("保存取数配置成功")
        else:
            log.warn("保存取数配置失败，失败提示: {0}".format(msg))
        set_global_var("ResultMsg", msg, False)

    elif opt == "修改":
        browser.find_element_by_xpath("//*[@field='varName']//*[text()='{0}']".format(target_var)).click()
        sleep(1)
        browser.find_element_by_xpath("//*[@onclick='addEmailDataRow()']//*[text()='修改']").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='varName']/preceding-sibling::input")))

        # 变量名称
        if var_name:
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='varName']/preceding-sibling::input").send_keys(var_name)
            log.info("设置变量名称: {0}".format(var_name))
            sleep(1)

        # 变量类型
        if var_type:
            browser.find_element_by_xpath("//*[@name='varExpr']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'emailtype') and text()='{0}']".format(var_type)).click()
            log.info("设置变量类型: {0}".format(var_type))
            sleep(1)

        # 附件类型
        if attach_type:
            browser.find_element_by_xpath("//*[@name='attachtype']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'getattachtype') and text()='{0}']".format(attach_type)).click()
            log.info("设置附件类型: {0}".format(attach_type))
            sleep(1)

        # 文件名
        if file_name:
            browser.find_element_by_xpath("//*[@name='filename']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='filename']/preceding-sibling::input").send_keys(file_name)
            log.info("设置文件名: {0}".format(file_name))
            sleep(1)

        # 赋值方式
        if value_type:
            browser.find_element_by_xpath("//*[@name='valueType']/preceding-sibling::input").click()
            browser.find_element_by_xpath(
                "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type)).click()
            log.info("设置赋值方式: {0}".format(value_type))
            sleep(1)

        # 点击保存
        browser.find_element_by_xpath("//*[@onclick='addFetchVar()']//*[text()='保存']").click()

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
        browser.find_element_by_xpath("//*[@onclick='del_getdata_email();']//*[text()='删除']").click()

        alert = BeAlertBox(back_iframe="default")
        msg = alert.get_msg()
        if alert.title_contains("您确定需要删除{0}吗".format(target_var), auto_click_ok=False):
            alert.click_ok()

            alert = BeAlertBox(back_iframe=False)
            msg = alert.get_msg()
            if alert.title_contains("删除成功"):
                log.info("删除取数配置成功")
            else:
                log.warn("删除取数配置失败，失败提示: {0}".format(msg))
        else:
            log.warn("删除取数配置失败，失败提示: {0}".format(msg))
        set_global_var("ResultMsg", msg, False)

    # 切换到节点iframe
    browser.switch_to.frame(browser.find_element_by_xpath(get_global_var("NodeIframe")))
    # 切换到取数配置iframe
    browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'busi_email_node')]"))