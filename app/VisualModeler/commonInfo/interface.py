# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/8/24 上午11:47

from app.VisualModeler.doctorwho.doctorWho import DoctorWho
from time import sleep
from common.page.func.alertBox import BeAlertBox
from common.page.func.input import set_textarea
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from common.page.func.pageMaskWait import page_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pykeyboard import PyKeyboard
from common.log.logger import log
from common.variable.globalVariable import *


class Interface:

    def __init__(self):
        self.browser = get_global_var("browser")
        DoctorWho().choose_menu("常用信息管理-第三方接口管理")
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(
            "//iframe[contains(@src, '/VisualModeler/html/commonInfo/interfaceCfg.html')]"))
        page_wait()
        sleep(1)

    def choose(self, interface_name):
        """
        :param interface_name: 接口名称
        """
        self.browser.find_element_by_xpath("//*[@name='interfaceName']/preceding-sibling::input").send_keys(interface_name)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        self.browser.find_element_by_xpath(
            "//*[@field='interfaceName']//*[@data-mtips='{0}']".format(interface_name)).click()
        log.info("已选择: {0}".format(interface_name))

    def add(self, interface_name, interface_type, interface_url, data_type, interface_namespace, interface_method,
            request_type, timeout, proxy_name, result_sample, request_header, request_parameter, request_body):
        """
        :param interface_name: 接口名称
        :param interface_type: 接口类型
        :param interface_url: 接口url，支持变量，一维数组，首个值为url，后面为变量样例值
        :param data_type: 数据类型
        :param interface_namespace: 接口空间名
        :param interface_method: 接口方法名
        :param request_type: 请求方式
        :param timeout: 超时时间
        :param proxy_name: 代理名称
        :param result_sample: 返回结果样例，字典，包含：结果类型和结果样例
        :param request_header: 接口请求头，数组，每一个值包含：参数名称，参数类型，参数默认值
        :param request_parameter: 接口参数，数组，每一个值包含：参数名称，参数类型，参数样例值
        :param request_body: 请求体内容，字典，包含：请求体内容类型和请求体内容
        """
        log.info("开始添加数据")
        self.browser.find_element_by_xpath("//*[text()='添加']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'interfaceCfgEdit.html?type=add')]")))
        sleep(1)
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='interfaceName']/preceding-sibling::input")))

        self.interface_page(interface_name=interface_name, interface_type=interface_type, interface_url=interface_url,
                            data_type=data_type, interface_namespace=interface_namespace, interface_method=interface_method,
                            request_type=request_type, timeout=timeout, proxy_name=proxy_name, result_sample=result_sample,
                            request_header=request_header, request_parameter=request_parameter, request_body=request_body)
        alert = BeAlertBox()
        msg = alert.get_msg()
        if alert.title_contains("成功"):
            log.info("数据 {0} 添加成功".format(interface_name))
        else:
            log.warn("数据 {0} 添加失败，失败提示: {1}".format(interface_name, msg))
        set_global_var("ResultMsg", msg, False)

    def update(self, obj, interface_name, interface_type, interface_url, data_type, interface_namespace, interface_method,
               request_type, timeout, proxy_name, result_sample, request_header, request_parameter, request_body):
        """
        :param obj: 目标接口
        :param interface_name: 接口名称
        :param interface_type: 接口类型
        :param interface_url: 接口url，支持变量，一维数组，首个值为url，后面为变量样例值
        :param data_type: 数据类型
        :param interface_namespace: 接口空间名
        :param interface_method: 接口方法名
        :param request_type: 请求方式
        :param timeout: 超时时间
        :param proxy_name: 代理名称
        :param result_sample: 返回结果样例，字典，包含：结果类型和结果样例
        :param request_header: 接口请求头，数组，每一个值包含：参数名称，参数类型，参数默认值
        :param request_parameter: 接口参数，数组，每一个值包含：参数名称，参数类型，参数样例值
        :param request_body: 请求体内容，字典，包含：请求体内容类型和请求体内容
        """
        log.info("开始修改数据")
        self.choose(obj)
        self.browser.find_element_by_xpath("//*[text()='修改']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'interfaceCfgEdit.html?type=edit')]")))
        sleep(1)
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='interfaceName']/preceding-sibling::input")))

        self.interface_page(interface_name=interface_name, interface_type=interface_type, interface_url=interface_url,
                            data_type=data_type, interface_namespace=interface_namespace,
                            interface_method=interface_method,
                            request_type=request_type, timeout=timeout, proxy_name=proxy_name,
                            result_sample=result_sample,
                            request_header=request_header, request_parameter=request_parameter,
                            request_body=request_body)
        alert = BeAlertBox()
        msg = alert.get_msg()
        if alert.title_contains("成功"):
            log.info("数据 {0} 修改成功".format(interface_name))
        else:
            log.warn("数据 {0} 修改失败，失败提示: {1}".format(interface_name, msg))
        set_global_var("ResultMsg", msg, False)

    def test(self, obj):
        """
        :param obj: 接口名称
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
                By.XPATH, "//iframe[contains(@src,'interfaceCfgEdit.html?type=edit')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='interfaceName']/preceding-sibling::input")))

            self.browser.find_element_by_xpath("//*[@id='testBtn']//*[text()='测试']").click()
            alert = BeAlertBox(back_iframe=True, timeout=60)
            msg = alert.get_msg()
            if alert.title_contains("测试成功"):
                log.info("{0} 测试成功".format(obj))
            else:
                log.warn("{0} 测试失败，测试返回结果: {1}".format(obj, msg))
            set_global_var("ResultMsg", msg, False)

    def interface_page(self, interface_name, interface_type, interface_url, data_type, interface_namespace, interface_method,
                       request_type, timeout, proxy_name, result_sample, request_header, request_parameter, request_body):
        """
        :param interface_name: 接口名称
        :param interface_type: 接口类型
        :param interface_url: 接口url，支持变量，一维数组，首个值为url，后面为变量样例值
        :param data_type: 数据类型
        :param interface_namespace: 接口空间名
        :param interface_method: 接口方法名
        :param request_type: 请求方式
        :param timeout: 超时时间
        :param proxy_name: 代理名称
        :param result_sample: 返回结果样例，字典，包含：结果类型和结果样例
        :param request_header: 接口请求头，数组，每一个值包含：参数名称，参数类型，参数默认值
        :param request_parameter: 接口参数，数组，每一个值包含：参数名称，参数类型，参数样例值
        :param request_body: 请求体内容，字典，包含：请求体内容类型和请求体内容
        """
        # 接口名称
        if interface_name:
            self.browser.find_element_by_xpath("//*[@name='interfaceName']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='interfaceName']/preceding-sibling::input").send_keys(interface_name)
            log.info("设置接口名称: {0}".format(interface_name))

        # 接口类型
        if interface_type:
            self.browser.find_element_by_xpath(
                "//*[@id='interfaceEdit_form']//*[@id='interfaceType']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'interfaceType') and text()='{0}']".format(interface_type)).click()
            log.info("设置接口类型: {0}".format(interface_type))

        # 接口url
        if interface_url:
            self.browser.find_element_by_xpath("//*[@name='interfaceUrl']/preceding-sibling::input").clear()
            url = interface_url[0]

            # 输入url
            self.browser.find_element_by_xpath(
                "//*[@name='interfaceUrl']/preceding-sibling::input").send_keys(url)
            log.info("设置接口url: {0}".format(url))

            # 输入回车键，出现变量列表
            if len(interface_url) > 1:
                url_params = interface_url[1:]
                k = PyKeyboard()
                k.press_keys(['Return'])
                sleep(1)

                i = 0
                for p in url_params:
                    self.browser.find_element_by_xpath(
                        "//*[@id='urlVar{0}']/following-sibling::span/input[1]".format(i)).send_keys(p)
                    log.info("设置接口url变量{0}样例值{1}".format(i + 1, p))
                    i += 1
            else:
                pass

        # 数据类型
        if data_type:
            self.browser.find_element_by_xpath("//*[@id='dataTypeId']/following-sibling::span//a").click()
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.visibility_of_element_located((
                By.XPATH, "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type))))
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type)).click()
            log.info("设置数据类型: {0}".format(data_type))

        # 接口空间名
        if interface_namespace:
            self.browser.find_element_by_xpath("//*[@name='interfaceNs']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='interfaceNs']/preceding-sibling::input").send_keys(interface_namespace)
            log.info("设置接口空间名: {0}".format(interface_namespace))

        # 接口方法名
        if interface_method:
            self.browser.find_element_by_xpath("//*[@name='interfaceMethod']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='interfaceMethod']/preceding-sibling::input").send_keys(interface_method)
            log.info("设置接口方法名: {0}".format(interface_method))

        # 请求方式
        if request_type:
            self.browser.find_element_by_xpath("//*[@id='requestType']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'requestType') and text()='{0}']".format(request_type)).click()
            log.info("设置请求方式: {0}".format(request_type))

        # 超时时间
        if timeout:
            self.browser.find_element_by_xpath("//*[@name='connectTimeout']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='connectTimeout']/preceding-sibling::input").send_keys(timeout)
            log.info("设置超时时间: {0}".format(timeout))

        # 代理名称
        if proxy_name:
            if proxy_name == "" or proxy_name == "无":
                log.info("无需配置代理")
            else:
                self.browser.find_element_by_xpath("//*[@id='proxyId']/following-sibling::span//a").click()
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

        # 返回结果样例
        if result_sample:
            # 结果类型
            if result_sample.__contains__("结果类型"):
                result_sample_type = result_sample.get("结果类型")
                self.browser.find_element_by_xpath("//*[@id='resultType']/following-sibling::span//a").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'resultType') and text()='{0}']".format(result_sample_type)).click()
                log.info("设置结果类型: {0}".format(result_sample_type))
            # 结果样例
            if result_sample.__contains__("结果样例"):
                result_sample_content = result_sample.get("结果样例")
                result_sample_content_textarea = self.browser.find_element_by_xpath(
                    "//*[@id='resultSample']/following-sibling::span//textarea")
                if isinstance(result_sample_content, dict) or isinstance(result_sample_content, str):
                    # json或字符串
                    result_sample_content_textarea.send_keys(result_sample_content)
                else:
                    # xml文本
                    set_textarea(textarea=result_sample_content_textarea, msg=result_sample_content)
                log.info("设置结果样例: {0}".format(result_sample_content))

        # 接口请求头
        if request_header:
            i = 1
            title_element = self.browser.find_element_by_xpath("//*[@class='title' and text()='接口请求头']")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", title_element)
            for h in request_header:
                if isinstance(h, dict):
                    # 点击+
                    self.browser.find_element_by_xpath("//*[@id='headerBtn']").click()
                    request_header_name = ""
                    for key, value in h.items():
                        # 参数名称
                        if key == "参数名称":
                            self.browser.find_element_by_xpath(
                                "//*[@id='interface_headerBtn{0}']//*[@name='paramName']/preceding-sibling::input".format(
                                    i)).send_keys(value)
                            request_header_name = value
                        # 参数类型
                        if key == "参数类型":
                            self.browser.find_element_by_xpath(
                                "//*[@id='interface_headerBtn{0}']//*[@comboname='paramType']/following-sibling::span//a".format(
                                    i)).click()
                            p_type_ele = self.browser.find_elements_by_xpath(
                                "//*[contains(@id,'_easyui_combobox') and text()='{0}']".format(value))
                            for e in p_type_ele:
                                if e.is_displayed():
                                    e.click()
                                    break
                        # 参数默认值
                        if key == "参数默认值":
                            self.browser.find_element_by_xpath(
                                "//*[@id='interface_headerBtn{0}']//*[@name='paramSample']/preceding-sibling::input".format(
                                    i)).send_keys(value)
                    log.info("接口请求头 {0} 已配置".format(request_header_name))
                    i += 1
                else:
                    raise KeyError("接口请求头格式错误")

        # 接口参数
        if request_parameter:

            # 获取序号
            i = 1
            flag = True
            while flag:
                try:
                    self.browser.find_element_by_xpath("//*[@id='interface_headerBtn{0}']".format(i))
                    i += 1
                except NoSuchElementException:
                    flag = False

            title_element = self.browser.find_element_by_xpath("//*[@class='title' and text()='接口参数']")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", title_element)
            for p in request_parameter:
                if isinstance(p, dict):
                    # 点击+
                    self.browser.find_element_by_xpath("//*[@id='paramBtn']").click()
                    request_param_name = ""
                    for key, value in p.items():
                        # 参数名称
                        if key == "参数名称":
                            self.browser.find_element_by_xpath(
                                "//*[@id='interface_paramBtn{0}']//*[@name='paramName']/preceding-sibling::input".format(
                                    i)).send_keys(value)
                            request_param_name = value
                        # 参数类型
                        if key == "参数类型":
                            self.browser.find_element_by_xpath(
                                "//*[@id='interface_paramBtn{0}']//*[@comboname='paramType']/following-sibling::span//a".format(
                                    i)).click()
                            p_type_ele = self.browser.find_elements_by_xpath(
                                "//*[contains(@id,'_easyui_combobox') and text()='{0}']".format(value))
                            for e in p_type_ele:
                                if e.is_displayed():
                                    e.click()
                                    break
                        # 参数值样例
                        if key == "参数值样例":
                            self.browser.find_element_by_xpath(
                                "//*[@id='interface_paramBtn{0}']//*[@name='paramSample']/preceding-sibling::input".format(
                                    i)).send_keys(value)
                    log.info("接口请求参数 {0} 已配置".format(request_param_name))
                    i += 1
                else:
                    raise KeyError("接口请求参数格式错误")

        # 请求体内容
        if request_body:
            title_element = self.browser.find_element_by_xpath("//*[@class='title' and text()='请求体内容']")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", title_element)
            # 结果类型
            if request_body.__contains__("请求体内容类型"):
                request_body_type = request_body.get("请求体内容类型")
                self.browser.find_element_by_xpath("//*[@id='requestBodyType']/following-sibling::span//a").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'requestBodyType') and text()='{0}']".format(request_body_type)).click()
                log.info("设置请求体内容类型: {0}".format(request_body_type))
            # 请求体内容
            if request_body.__contains__("请求体内容"):
                request_body_content = request_body.get("请求体内容")
                request_body_content_textarea = self.browser.find_element_by_xpath(
                    "//*[@id='requestBody']/following-sibling::span//textarea")
                if isinstance(request_body_content, str):
                    # json或字符串
                    request_body_content_textarea.send_keys(request_body_content)
                else:
                    # xml文本
                    set_textarea(textarea=request_body_content_textarea, msg=request_body_content)
                log.info("设置请求体内容: {0}".format(request_body_content))

        # 提交
        self.browser.find_element_by_xpath("//*[@id='submitBtn']//*[text()='提交']").click()

    def delete(self, obj):
        """
        :param obj: 接口名称
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
        :param obj: 接口名称
        :param fuzzy_match: 模糊匹配
        """
        # 用于清除数据，在测试之前执行, 使用关键字开头模糊查询
        self.browser.find_element_by_xpath("//*[@name='interfaceName']/preceding-sibling::input").clear()
        self.browser.find_element_by_xpath("//*[@name='interfaceName']/preceding-sibling::input").send_keys(obj)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        fuzzy_match = True if fuzzy_match == "是" else False
        if fuzzy_match:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='interfaceName']//*[starts-with(@data-mtips,'{}')]".format(obj))
        else:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='interfaceName']//*[@data-mtips='{}']".format(obj))
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
                                "//*[@field='interfaceName']//*[starts-with(@data-mtips,'{}')]".format(obj))
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
