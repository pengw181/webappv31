# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午11:05

from app.VisualModeler.doctorwho.doctorWho import DoctorWho
from time import sleep
from common.page.func.alertBox import BeAlertBox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from common.page.func.pageMaskWait import page_wait
from common.log.logger import log
from common.variable.globalVariable import *


class Database:

    def __init__(self):
        self.browser = get_global_var("browser")
        DoctorWho().choose_menu("常用信息管理-数据库管理")
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(
            "//iframe[contains(@src, '/VisualModeler/html/commonInfo/dbCfg.html')]"))
        sleep(1)

    def choose(self, db_name):
        """
        :param db_name: 数据库名称
        """
        self.browser.find_element_by_xpath("//*[@name='dbName']/preceding-sibling::input").send_keys(db_name)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        self.browser.find_element_by_xpath(
            "//*[contains(@id,'dbCfg_info_tab_')]//*[text()='{0}']".format(db_name)).click()
        log.info("已选择: {0}".format(db_name))

    def add(self, db_name, db_driver, db_url, username, pwd, belong_type, data_type):
        """
        :param db_name: 数据库名称
        :param db_driver: 数据库驱动
        :param db_url: 数据库URL
        :param username: 用户名
        :param pwd: 密码
        :param belong_type: 归属类型
        :param data_type: 数据类型
        """
        log.info("开始添加数据")
        self.browser.find_element_by_xpath("//*[text()='添加']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'dbCfgEdit.html?type=add')]")))
        sleep(1)
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='dbName']/preceding-sibling::input")))

        self.database_page(db_name=db_name, db_driver=db_driver, db_url=db_url, username=username, pwd=pwd,
                           belong_type=belong_type, data_type=data_type)
        alert = BeAlertBox()
        msg = alert.get_msg()
        if alert.title_contains("保存成功"):
            log.info("数据 {0} 添加成功".format(db_name))
        else:
            log.warn("数据 {0} 添加失败，失败提示: {1}".format(db_name, msg))
        set_global_var("ResultMsg", msg, False)

    def update(self, obj, db_name, db_driver, db_url, username, pwd, belong_type, data_type):
        """
        :param obj: 数据库名称
        :param db_name: 数据库名称
        :param db_driver: 数据库驱动
        :param db_url: 数据库URL
        :param username: 用户名
        :param pwd: 密码
        :param belong_type: 归属类型
        :param data_type: 数据类型
        """
        log.info("开始修改数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='修改']").click()

        # 鉴于数据权限问题，在修改/删除数据时，需要判断是否有弹出框提示无权操作
        alert = BeAlertBox(back_iframe=False, timeout=2)
        if alert.exist_alert:
            set_global_var("ResultMsg", alert.get_msg(), False)
        else:
            wait = WebDriverWait(self.browser, 10)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'dbCfgEdit.html?type=edit')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='dbName']/preceding-sibling::input")))

            self.database_page(db_name=db_name, db_driver=db_driver, db_url=db_url, username=username, pwd=pwd,
                               belong_type=belong_type, data_type=data_type)
            alert = BeAlertBox()
            msg = alert.get_msg()
            if alert.title_contains("保存成功"):
                log.info("{0} 修改成功".format(obj))
            else:
                log.warn("{0} 修改失败，失败提示: {1}".format(obj, msg))
            set_global_var("ResultMsg", msg, False)

    def database_page(self, db_name, db_driver, db_url, username, pwd, belong_type, data_type):
        """
        :param db_name: 数据库名称
        :param db_driver: 数据库驱动
        :param db_url: 数据库URL
        :param username: 用户名
        :param pwd: 密码
        :param belong_type: 归属类型
        :param data_type: 数据类型
        """
        # 数据库名称
        if db_name:
            self.browser.find_element_by_xpath("//*[@name='dbName']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='dbName']/preceding-sibling::input").send_keys(db_name)
            log.info("设置数据库名称: {0}".format(db_name))

        # 数据库驱动
        if db_driver:
            self.browser.find_element_by_xpath("//*[@name='dbDriver']/preceding-sibling::input").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'dbDriver') and text()='{0}']".format(db_driver)).click()
            log.info("设置数据库驱动: {0}".format(db_driver))

        # 数据库URL
        if db_url:
            self.browser.find_element_by_xpath("//*[@name='dbUrl']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='dbUrl']/preceding-sibling::input").send_keys(db_url)
            log.info("设置数据库URL: {0}".format(db_url))

        # 用户名
        if username:
            self.browser.find_element_by_xpath("//*[@name='username']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='username']/preceding-sibling::input").send_keys(username)
            log.info("设置用户名: {0}".format(username))

        # 密码
        if pwd:
            try:
                # 判断是否是修改密码
                self.browser.find_element_by_xpath(
                    "//*[@id='pwd']/following-sibling::span//a[contains(@class, 'edit')]").click()
            except NoSuchElementException:
                pass
            self.browser.find_element_by_xpath("//*[@name='pwd']/preceding-sibling::input").send_keys(pwd)
            sleep(1)
            log.info("设置密码: {0}".format(pwd))

        # 归属类型
        if belong_type:
            self.browser.find_element_by_xpath("//*[@name='belongType']/preceding-sibling::input").click()
            belong_type = "外部库"
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'belongType') and text()='{0}']".format(belong_type)).click()
            log.info("设置归属类型: {0}".format(belong_type))

        # 数据类型
        if data_type:
            self.browser.find_element_by_xpath("//*[@name='dataTypeId']/preceding-sibling::input").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type)).click()
            log.info("设置数据类型: {0}".format(data_type))

        # 提交
        self.browser.find_element_by_xpath("//*[@id='submitBtn']//*[text()='提交']").click()

    def test(self, obj):
        """
        :param obj: 数据库名称
        """
        log.info("开始测试数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='修改']").click()

        # 鉴于数据权限问题，在修改/删除数据时，需要判断是否有弹出框提示无权操作
        alert = BeAlertBox(back_iframe=False, timeout=2)
        exist = alert.exist_alert
        if exist:
            set_global_var("ResultMsg", alert.get_msg(), False)
        else:
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'dbCfgEdit.html?type=edit')]")))

            self.browser.find_element_by_xpath("//*[@id='testBtn']//*[text()='测试']").click()
            alert = BeAlertBox(back_iframe=True, timeout=60)
            msg = alert.get_msg()
            if alert.title_contains("测试成功"):
                log.info("{0} 测试成功".format(obj))
            else:
                log.warn("{0} 测试失败，测试返回结果: {1}".format(obj, msg))
            set_global_var("ResultMsg", msg, False)

    def delete(self, obj):
        """
        :param obj: 数据库名称
        """
        log.info("开始删除数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='删除']").click()

        alert = BeAlertBox(back_iframe=False)
        msg = alert.get_msg()
        if alert.title_contains(obj, auto_click_ok=False):
            alert.click_ok()
            sleep(1)
            alert = BeAlertBox(back_iframe=False)
            msg = alert.get_msg()
            if alert.title_contains("操作成功"):
                log.info("{0} 删除成功".format(obj))
            else:
                log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        else:
            log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        set_global_var("ResultMsg", msg, False)

    def data_clear(self, obj, fuzzy_match=False):
        """
        :param obj: 数据库名称
        :param fuzzy_match: 模糊匹配
        """
        # 用于清除数据，在测试之前执行, 使用关键字开头模糊查询
        self.browser.find_element_by_xpath("//*[@name='dbName']/preceding-sibling::input").clear()
        self.browser.find_element_by_xpath("//*[@name='dbName']/preceding-sibling::input").send_keys(obj)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        fuzzy_match = True if fuzzy_match == "是" else False
        if fuzzy_match:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='dbName']/*[contains(@class,'dbName') and starts-with(text(),'{0}')]".format(obj))
        else:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='dbName']/*[contains(@class,'dbName') and text()='{0}']".format(obj))
        if len(record_element) > 0:
            exist_data = True

            while exist_data:
                pe = record_element[0]
                search_result = pe.text
                pe.click()
                log.info("选择: {0}".format(search_result))
                # 删除
                self.browser.find_element_by_xpath("//*[text()='删除']").click()
                alert = BeAlertBox(back_iframe=False)
                msg = alert.get_msg()
                if alert.title_contains("您确定需要删除{0}吗".format(search_result), auto_click_ok=False):
                    alert.click_ok()
                    alert = BeAlertBox(back_iframe=False)
                    msg = alert.get_msg()
                    if alert.title_contains("成功"):
                        log.info("{0} 删除成功".format(search_result))
                        page_wait()
                        if fuzzy_match:
                            # 重新获取页面查询结果
                            record_element = self.browser.find_elements_by_xpath(
                                "//*[@field='dbName']/*[contains(@class,'dbName') and text()='{0}']".format(
                                    obj))
                            if len(record_element) > 0:
                                exist_data = True
                            else:
                                # 查询结果为空,修改exist_data为False，退出循环
                                log.info("数据清理完成")
                                exist_data = False
                        else:
                            break
                    else:
                        raise Exception("删除数据时出现未知异常: {0}".format(msg))
                else:
                    # 无权操作
                    log.warn("{0} 清理失败，失败提示: {1}".format(obj, msg))
                    set_global_var("ResultMsg", msg, False)
                    break
        else:
            # 查询结果为空,结束处理
            log.info("查询不到满足条件的数据，无需清理")
