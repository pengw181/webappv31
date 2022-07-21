# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2022/4/25 下午3:10

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.variable.globalVariable import *
from common.log.logger import log
from common.page.func.input import set_textarea
from common.page.func.loadDictionary import load_dictionary
from common.page.func.pageMaskWait import page_wait
from common.page.func.alertBox import BeAlertBox
from common.wrapper.dashboardCheck import closeAndEnterDashboard
from time import sleep


@closeAndEnterDashboard
class Dictionary:

    def __init__(self):
        self.browser = get_global_var("browser")
        page_wait(5)
        wait = WebDriverWait(self.browser, 10)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[text()='字典管理']")))
        self.browser.find_element_by_xpath("//*[text()='字典管理']").click()
        sleep(1)

    def add(self, dict_list):
        num = 1
        for dictionary in dict_list:
            if not isinstance(dictionary, dict):
                raise TypeError
            dict_name = dictionary.get("字典名称")
            catalog = dictionary.get("主题分类")
            interface = dictionary.get("数据接口")
            dict_item = dictionary.get("字典项")

            # 点击添加
            self.browser.find_element_by_xpath("//*[@title='添加字典']").click()
            row_xpath = "//*[contains(@id,'dictionaryTab')][{0}]".format(num)
            sleep(1)

            # 字典名称
            if dict_name:
                self.browser.find_element_by_xpath(row_xpath + "/td[2]//input[contains(@id,'textbox')]").clear()
                self.browser.find_element_by_xpath(
                    row_xpath + "/td[2]//input[contains(@id,'textbox')]").send_keys(dict_name)
                log.info("设置字典名称: {0}".format(dict_name))

            # 主题分类
            if catalog:
                self.browser.find_element_by_xpath(row_xpath + "/td[3]//a").click()
                catalog_elements = self.browser.find_elements_by_xpath(
                    "//*[contains(@id,'combobox') and text()='{0}']".format(catalog))
                if len(catalog_elements) == 0:
                    raise NoSuchElementException
                for element in catalog_elements:
                    if element.is_displayed():
                        element.click()
                        log.info("设置主题分类: {0}".format(catalog))
                        sleep(1)
                        break

            # 数据接口
            if interface:
                self.browser.find_element_by_xpath(row_xpath + "/td[4]//a").click()
                interface_elements = self.browser.find_elements_by_xpath(
                    "//*[contains(@id,'combobox') and text()='{0}']".format(interface))
                if len(interface_elements) == 0:
                    raise NoSuchElementException
                for element in interface_elements:
                    if element.is_displayed():
                        element.click()
                        log.info("设置数据接口: {0}".format(interface))
                        sleep(1)
                        break

            # 字典项
            if dict_item:
                textarea = self.browser.find_element_by_xpath("//*[@id='dictionaryText']")
                if isinstance(dict_item, str):
                    # 文件名
                    content = load_dictionary(dict_item)
                else:
                    # 数组
                    content = dict_item
                set_textarea(textarea=textarea, msg=content)
                sleep(1)

            # 保存
            self.browser.find_element_by_xpath("//*[@title='保存字典']").click()
            alert = BeAlertBox()
            msg = alert.get_msg()
            if alert.title_contains("确定保存字典【{0}】吗".format(dict_name), auto_click_ok=False):
                alert.click_ok()
                log.info("保存字典【{0}】成功".format(dict_name))
                msg = "操作成功"
                sleep(3)
            else:
                log.warn("保存字典失败，失败提示: {0}".format(msg))
            set_global_var("ResultMsg", msg, False)
            num += 1
        set_global_var("ResultMsg", "操作成功", False)