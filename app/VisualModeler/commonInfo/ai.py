# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午10:52

from app.VisualModeler.doctorwho.doctor_who import DoctorWho
from time import sleep
from common.page.func.alert_box import BeAlertBox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.page.func.page_mask_wait import page_wait
from common.log.logger import log
from common.variable.global_variable import *


class AI:

    def __init__(self):
        self.browser = get_global_var("browser")
        DoctorWho().choose_menu("常用信息管理-AI模型管理")
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(
            "//iframe[contains(@src, '/VisualModeler/html/commonInfo/algorithm.html')]"))
        page_wait()
        sleep(1)

    def choose(self, ai_model):
        self.browser.find_element_by_xpath("//*[@name='modelName']/preceding-sibling::input").send_keys(ai_model)
        self.browser.find_element_by_xpath("//*[@id='queryButton']//*[text()='查询']").click()
        page_wait()
        self.browser.find_element_by_xpath(
            "//*[contains(@id,'templetManage')]/*[@field='modelName']/*[text()='{0}']".format(ai_model)).click()
        log.info("已选择: {0}".format(ai_model))

    def add(self, application_mode, algorithm, model_name, model_desc, train_scale, test_scale, timeout, file_name,
            params, col_sets, use_train, use_test):
        """
        :param application_mode: 应用模式
        :param algorithm: 算法名称
        :param model_name: 模型名称
        :param model_desc: 模型描述
        :param train_scale: 训练比例
        :param test_scale: 测试比例
        :param timeout: 超时时间
        :param file_name: 模型数据
        :param params: 参数设置
        :param col_sets: 列设置
        :param use_train: 是否训练， bool
        :param use_test: 是否测试， bool
        """
        log.info("开始添加数据")
        self.browser.find_element_by_xpath("//*[text()='添加']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'algorithmEdit.html')]")))
        sleep(1)
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='applicationMode']/preceding-sibling::input")))

        # 应用模式
        if application_mode:
            self.browser.find_element_by_xpath("//*[@id='applicationMode']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'applicationMode') and text()='{0}']".format(application_mode)).click()
            log.info("设置应用模式: {0}".format(application_mode))

        # 算法名称
        if algorithm:
            self.browser.find_element_by_xpath("//*[@id='algorithm']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'algorithm') and text()='{0}']".format(algorithm)).click()
            log.info("设置算法名称: {0}".format(algorithm))

        # 模型名称
        if model_name:
            self.browser.find_element_by_xpath("//*[@name='modelName']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='modelName']/preceding-sibling::input").send_keys(model_name)
            log.info("设置模型名称: {0}".format(model_name))

        # 模型描述
        if model_desc:
            self.browser.find_element_by_xpath("//*[@name='modelDesc']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='modelDesc']/preceding-sibling::input").send_keys(model_desc)
            log.info("设置模型描述: {0}".format(model_desc))

        # 训练比例
        if train_scale:
            self.browser.find_element_by_xpath("//*[@id='algorithm']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'algorithm') and text()='{0}']".format(train_scale)).click()
            log.info("设置训练比例: {0}".format(train_scale))

        # 测试比例
        if test_scale:
            self.browser.find_element_by_xpath(
                "//*[@id='algorithm']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'algorithm') and text()='{0}']".format(test_scale)).click()
            log.info("设置测试比例: {0}".format(test_scale))

        # 算法名称
        if algorithm:
            self.browser.find_element_by_xpath(
                "//*[@id='algorithm']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'algorithm') and text()='{0}']".format(algorithm)).click()
            log.info("设置算法名称: {0}".format(algorithm))

        # TODO

        # 保存
        self.browser.find_element_by_xpath("//*[@id='saveBtn']//*[text()='保存']").click()
        alert = BeAlertBox(self.browser)
        msg = alert.get_msg()
        if alert.title_contains("保存成功"):
            log.info("{0} 添加成功".format(model_name))
        else:
            log.warn("{0} 添加失败，失败提示: {1}".format(model_name, msg))
        set_global_var("ResultMsg", msg, False)

    def update(self, obj, field_name):
        log.info("开始修改数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='修改']").click()

        # 鉴于数据权限问题，在修改/删除数据时，需要判断是否有弹出框提示无权操作
        alert = BeAlertBox(back_iframe=False, timeout=2)
        if alert.exist_alert:
            set_global_var("ResultMsg", alert.get_msg(), False)
        else:
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'addTempletManageInfo.html')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='tempTypeNameInfo']/preceding-sibling::input")))

            # 专业领域名称
            if field_name:
                self.browser.find_element_by_xpath(
                    "//*[@name='tempTypeNameInfo']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@name='tempTypeNameInfo']/preceding-sibling::input").send_keys(field_name)
                log.info("设置专业领域名称: {0}".format(field_name))

            # 保存
            self.browser.find_element_by_xpath("//*[@id='saveBtn']//*[text()='保存']").click()
            alert = BeAlertBox(self.browser)
            msg = alert.get_msg()
            if alert.title_contains("保存成功"):
                log.info("{0} 修改成功".format(obj))
            else:
                log.warn("{0} 修改失败，失败提示: {1}".format(obj, msg))
            set_global_var("ResultMsg", msg, False)

    def delete(self, obj):
        log.info("开始删除数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='删除']").click()

        alert = BeAlertBox(back_iframe=False)
        msg = alert.get_msg()
        if alert.title_contains(obj, auto_click_ok=False):
            alert.click_ok()
            alert = BeAlertBox(back_iframe=False)
            msg = alert.get_msg()
            if alert.title_contains("成功"):
                log.info("{0} 删除成功".format(obj))
            else:
                log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        else:
            # 无权操作
            log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        set_global_var("ResultMsg", msg, False)

    def data_clear(self, obj, fuzzy_match=False):
        # 用于清除数据，在测试之前执行, 使用关键字开头模糊查询
        self.browser.find_element_by_xpath("//*[@name='tempTypeName']/preceding-sibling::input").clear()
        self.browser.find_element_by_xpath("//*[@name='tempTypeName']/preceding-sibling::input").send_keys(obj)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        if fuzzy_match:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='tempTypeName']/*[contains(@class,'tempTypeName')]/*[starts-with(text(),'{0}')]".format(obj))
        else:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='tempTypeName']/*[contains(@class,'tempTypeName')]/*[text()='{0}']".format(obj))
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
                if alert.title_contains("您确定需要删除{0}吗".format(obj), auto_click_ok=False):
                    alert.click_ok()
                    alert = BeAlertBox(back_iframe=False)
                    msg = alert.get_msg()
                    if alert.title_contains("成功"):
                        log.info("{0} 删除成功".format(search_result))
                        page_wait()
                        if fuzzy_match:
                            # 重新获取页面查询结果
                            record_element = self.browser.find_elements_by_xpath(
                                "//*[@field='tempTypeName']/*[contains(@class,'tempTypeName')]/*[starts-with(text(),'{0}')]".format(
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

        else:
            # 查询结果为空,结束处理
            log.info("查询不到满足条件的数据，无需清理")
            pass
