# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午11:19

from app.VisualModeler.doctorwho.doctorWho import DoctorWho
from time import sleep
from common.page.func.alertBox import BeAlertBox
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from common.page.func.pageMaskWait import page_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.log.logger import log
from common.variable.globalVariable import *


class Mail:

    def __init__(self):
        self.browser = get_global_var("browser")
        DoctorWho().choose_menu("常用信息管理-邮箱管理")
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(
            "//iframe[contains(@src, '/VisualModeler/html/commonInfo/emailCfg.html')]"))
        page_wait()
        sleep(1)

    def choose(self, mail_addr):
        """
        :param mail_addr: 邮箱地址
        """
        self.browser.find_element_by_xpath("//*[@name='mailAddr']/preceding-sibling::input").send_keys(mail_addr)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        self.browser.find_element_by_xpath(
            "//*[contains(@id,'emailCfg')]//*[text()='{0}']".format(mail_addr)).click()
        log.info("已选择: {0}".format(mail_addr))

    def add(self, mail_addr, mail_type, data_type, send_protocol, send_server, send_port, receive_protocol,
            receive_server, receive_port, username, pwd, proxy_name, platf_account):
        """
        :param mail_addr: 邮箱地址
        :param mail_type: 邮箱类型
        :param data_type: 数据类型
        :param send_protocol: 发送协议类型
        :param send_server: 发送服务器地址
        :param send_port: 发送端口
        :param receive_protocol: 接收协议类型
        :param receive_server: 接收服务器地址
        :param receive_port: 接收端口
        :param username: 账号
        :param pwd: 密码或授权码
        :param proxy_name: 代理名称
        :param platf_account: 平台账号
        """
        log.info("开始添加数据")
        self.browser.find_element_by_xpath("//*[text()='添加']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'emailCfgEdit.html?type=save')]")))
        sleep(1)
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='mailAddr']/preceding-sibling::input")))

        self.mail_page(mail_addr=mail_addr, mail_type=mail_type, data_type=data_type, send_protocol=send_protocol,
                       send_server=send_server, send_port=send_port, receive_protocol=receive_protocol,
                       receive_server=receive_server, receive_port=receive_port, username=username, pwd=pwd,
                       proxy_name=proxy_name, platf_account=platf_account)
        alert = BeAlertBox()
        msg = alert.get_msg()
        if alert.title_contains("成功"):
            log.info("数据 {0} 添加成功".format(mail_addr))
        else:
            log.warn("数据 {0} 添加失败，失败提示: {1}".format(mail_addr, msg))
        set_global_var("ResultMsg", msg, False)

    def update(self, obj, mail_addr, mail_type, data_type, send_protocol, send_server, send_port, receive_protocol,
               receive_server, receive_port, username, pwd, proxy_name, platf_account):
        """
        :param obj: 邮箱地址
        :param mail_addr: 邮箱地址
        :param mail_type: 邮箱类型
        :param data_type: 数据类型
        :param send_protocol: 发送协议类型
        :param send_server: 发送服务器地址
        :param send_port: 发送端口
        :param receive_protocol: 接收协议类型
        :param receive_server: 接收服务器地址
        :param receive_port: 接收端口
        :param username: 账号
        :param pwd: 密码或授权码
        :param proxy_name: 代理名称
        :param platf_account: 平台账号
        """
        log.info("开始修改数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='修改']").click()

        # 鉴于数据权限问题，在修改/删除数据时，需要判断是否有弹出框提示无权操作
        alert = BeAlertBox(back_iframe=False, timeout=1)
        exist = alert.exist_alert
        if exist:
            set_global_var("ResultMsg", alert.get_msg(), False)
        else:
            wait = WebDriverWait(self.browser, 10)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'emailCfgEdit.html?type=edit')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='mailAddr']/preceding-sibling::input")))

            self.mail_page(mail_addr=mail_addr, mail_type=mail_type, data_type=data_type, send_protocol=send_protocol,
                           send_server=send_server, send_port=send_port, receive_protocol=receive_protocol,
                           receive_server=receive_server, receive_port=receive_port, username=username, pwd=pwd,
                           proxy_name=proxy_name, platf_account=platf_account)
            alert = BeAlertBox()
            msg = alert.get_msg()
            if alert.title_contains("成功"):
                log.info("{0} 修改成功".format(mail_addr))
            else:
                log.warn("{0} 修改失败，失败提示: {1}".format(mail_addr, msg))
            set_global_var("ResultMsg", msg, False)

    def mail_page(self, mail_addr, mail_type, data_type, send_protocol, send_server, send_port, receive_protocol,
                  receive_server, receive_port, username, pwd, proxy_name, platf_account):
        """
        :param mail_addr: 邮箱地址
        :param mail_type: 邮箱类型
        :param data_type: 数据类型
        :param send_protocol: 发送协议类型
        :param send_server: 发送服务器地址
        :param send_port: 发送端口
        :param receive_protocol: 接收协议类型
        :param receive_server: 接收服务器地址
        :param receive_port: 接收端口
        :param username: 账号
        :param pwd: 密码或授权码
        :param proxy_name: 代理名称
        :param platf_account: 平台账号
        """
        # 邮箱地址
        if mail_addr:
            self.browser.find_element_by_xpath("//*[@name='mailAddr']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='mailAddr']/preceding-sibling::input").send_keys(mail_addr)
            log.info("设置邮箱地址: {0}".format(mail_addr))

        # 邮箱类型
        if mail_type:
            self.browser.find_element_by_xpath("//*[@name='cfgType']/preceding-sibling::input").click()

            # 确认是否已选择了接收邮箱，如果已选择，则先勾掉
            mail_type_element = self.browser.find_element_by_xpath("//*[contains(@id,'cfgType') and text()='接收邮箱']")
            if mail_type_element.get_attribute("class").find("selected") > -1:
                mail_type_element.click()

            # 确认是否已选择了发送邮箱，如果已选择，则先勾掉
            mail_type_element = self.browser.find_element_by_xpath("//*[contains(@id,'cfgType') and text()='发送邮箱']")
            if mail_type_element.get_attribute("class").find("selected") > -1:
                mail_type_element.click()

            # 确认是否已选择了联系人，如果已选择，则先勾掉
            mail_type_element = self.browser.find_element_by_xpath("//*[contains(@id,'cfgType') and text()='联系人']")
            if mail_type_element.get_attribute("class").find("selected") > -1:
                mail_type_element.click()

            for _mail_type in mail_type:
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'cfgType') and text()='{0}']".format(_mail_type)).click()
            sleep(1)
            self.browser.find_element_by_xpath("//*[@name='cfgType']/preceding-sibling::input").click()
            log.info("设置邮箱类型: {0}".format(",".join(mail_type)))

        # 数据类型
        if data_type:
            self.browser.find_element_by_xpath("//*[@name='dataTypeId']/preceding-sibling::input").click()
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.visibility_of_element_located((
                By.XPATH, "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type))))
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type)).click()
            log.info("设置数据类型: {0}".format(data_type))

        # 发送协议类型
        if send_protocol:
            self.browser.find_element_by_xpath("//*[@name='protocolType']/preceding-sibling::input").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'protocolType') and text()='{0}']".format(send_protocol)).click()
            log.info("设置发送协议类型: {0}".format(send_protocol))

        # 发送服务器地址
        if send_server:
            self.browser.find_element_by_xpath("//*[@name='serverName']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='serverName']/preceding-sibling::input").send_keys(
                send_server)
            log.info("设置发送服务器地址: {0}".format(send_server))

        # 发送端口
        if send_port:
            self.browser.find_element_by_xpath("//*[@name='sendPort']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='sendPort']/preceding-sibling::input").send_keys(send_port)
            log.info("设置发送端口: {0}".format(send_port))

        # 接收协议类型
        if receive_protocol:
            self.browser.find_element_by_xpath("//*[@name='receiveProtocolType']/preceding-sibling::input").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'receiveProtocolType') and text()='{0}']".format(receive_protocol)).click()
            log.info("设置接收协议类型: {0}".format(receive_protocol))

        # 接收服务器地址
        if receive_server:
            self.browser.find_element_by_xpath("//*[@name='receiveServerName']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='receiveServerName']/preceding-sibling::input").send_keys(receive_server)
            log.info("设置接收服务器地址: {0}".format(receive_server))

        # 接收端口
        if receive_port:
            self.browser.find_element_by_xpath("//*[@name='receivePort']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='receivePort']/preceding-sibling::input").send_keys(
                receive_port)
            log.info("设置接收端口: {0}".format(receive_port))

        # 账号
        if username:
            self.browser.find_element_by_xpath("//*[@name='mailAccount']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='mailAccount']/preceding-sibling::input").send_keys(username)
            log.info("设置账号: {0}".format(username))

        # 密码或授权码
        if pwd:
            try:
                # 判断是否是修改密码
                self.browser.find_element_by_xpath(
                    "//*[@id='pwd']/following-sibling::span//a[contains(@class, 'edit')]").click()
            except NoSuchElementException:
                pass
            self.browser.find_element_by_xpath("//*[@name='pwd']/preceding-sibling::input").send_keys(pwd)
            sleep(1)
            log.info("设置密码或授权码: {0}".format(pwd))

        # 代理名称
        if proxy_name:
            if proxy_name == "" or proxy_name == "无":
                log.info("无需配置代理")
            else:
                self.browser.find_element_by_xpath("//*[@name='proxyId']/preceding-sibling::input").click()
                try:
                    proxy_element = self.browser.find_element_by_xpath(
                        "//*[contains(@id,'proxyId') and text()='{0}']".format(proxy_name))
                    action = ActionChains(self.browser)
                    action.move_to_element(proxy_element).perform()
                    self.browser.find_element_by_xpath(
                        "//*[contains(@id,'proxyId') and text()='{0}']".format(proxy_name)).click()
                    log.info("设置代理名称: {0}".format(proxy_name))
                except NoSuchElementException:
                    raise NoSuchElementException("找不到指定代理: {0}".format(proxy_name))

        # 平台账号
        if platf_account:
            plate_account_element = self.browser.find_element_by_xpath(
                "//*[@name='isPlatfAccount']/preceding-sibling::input")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", plate_account_element)
            plate_account_element.click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'isPlatfAccount') and text()='{0}']".format(platf_account)).click()
            log.info("设置平台账号: {0}".format(platf_account))

        # 提交
        self.browser.find_element_by_xpath("//*[@id='submitBtn']//*[text()='提交']").click()

    def test(self, obj):
        """
        :param obj: 邮箱地址
        """
        log.info("开始测试数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='修改']").click()

        # 鉴于数据权限问题，在修改/删除数据时，需要判断是否有弹出框提示无权操作
        alert = BeAlertBox(back_iframe=False, timeout=1)
        exist = alert.exist_alert
        if exist:
            set_global_var("ResultMsg", alert.get_msg(), False)
        else:
            wait = WebDriverWait(self.browser, 10)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'emailCfgEdit.html?type=edit')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='mailAddr']/preceding-sibling::input")))

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
        :param obj: 邮箱地址
        """
        log.info("开始删除数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='删除']").click()

        alert = BeAlertBox(back_iframe=False, timeout=2)
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
            log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        set_global_var("ResultMsg", msg, False)

    def data_clear(self, obj, fuzzy_match=False):
        """
        :param obj: 邮箱地址
        :param fuzzy_match: 模糊匹配
        """
        # 用于清除数据，在测试之前执行, 使用关键字开头模糊查询
        self.browser.find_element_by_xpath("//*[@name='mailAddr']/preceding-sibling::input").clear()
        self.browser.find_element_by_xpath("//*[@name='mailAddr']/preceding-sibling::input").send_keys(obj)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        fuzzy_match = True if fuzzy_match == "是" else False
        if fuzzy_match:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='mailAddr']/*[contains(@class,'mailAddr') and starts-with(text(),'{0}')]".format(obj))
        else:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='mailAddr']/*[contains(@class,'mailAddr') and text()='{0}']".format(obj))
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
                                "//*[@field='mailAddr']/*[contains(@class,'mailAddr') and starts-with(text(),'{0}')]".format(
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
