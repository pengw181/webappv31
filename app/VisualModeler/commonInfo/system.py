# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午11:32

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


class ThirdSystem:

    def __init__(self):
        self.browser = get_global_var("browser")
        DoctorWho().choose_menu("常用信息管理-第三方系统管理")
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(
            "//iframe[contains(@src, '/VisualModeler/html/commonInfo/nodeVosLoginCfg.html')]"))
        page_wait()
        sleep(1)

    def choose(self, platform_name):
        """
        :param platform_name: 平台名称
        """
        self.browser.find_element_by_xpath("//*[@name='platform']/preceding-sibling::input").send_keys(platform_name)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        self.browser.find_element_by_xpath(
            "//*[contains(@id,'nodeVosLogin_info_tab_')]//*[text()='{0}']".format(platform_name)).click()
        log.info("已选择: {0}".format(platform_name))

    def add(self, platform, visit_url, network_tag, browser_type, browser_timeout, session_timeout, data_type,
            first_click_set, enable_proxy_set, enable_login_set):
        """
        :param platform: 平台名称
        :param visit_url: 平台地址
        :param network_tag: 平台网络标识
        :param browser_type: 浏览器类型
        :param browser_timeout: 浏览器超时时间
        :param session_timeout: 空闲刷新时间
        :param data_type: 数据类型
        :param first_click_set: 是否优先点击页面元素，字典
        :param enable_proxy_set: 是否启用代理，字典
        :param enable_login_set: 是否验证登录，字典
        """
        log.info("开始添加数据")
        self.browser.find_element_by_xpath("//*[text()='添加']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'nodeVosLoginCfgEdit.html?type=add')]")))
        sleep(1)
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='platform']/preceding-sibling::input")))

        self.system_page(platform=platform, visit_url=visit_url, network_tag=network_tag, browser_type=browser_type,
                         browser_timeout=browser_timeout, session_timeout=session_timeout, data_type=data_type,
                         first_click_set=first_click_set, enable_proxy_set=enable_proxy_set, enable_login_set=enable_login_set)
        alert = BeAlertBox()
        msg = alert.get_msg()
        if alert.title_contains("成功"):
            log.info("数据 {0} 添加成功".format(platform))
        else:
            log.warn("数据 {0} 添加失败，失败提示: {1}".format(platform, msg))
        set_global_var("ResultMsg", msg, False)

    def system_page(self, platform, visit_url, network_tag, browser_type, browser_timeout, session_timeout, data_type,
                    first_click_set, enable_proxy_set, enable_login_set):
        """
        :param platform: 平台名称
        :param visit_url: 平台地址
        :param network_tag: 平台网络标识
        :param browser_type: 浏览器类型
        :param browser_timeout: 浏览器超时时间
        :param session_timeout: 空闲刷新时间
        :param data_type: 数据类型
        :param first_click_set: 是否优先点击页面元素，字典
        :param enable_proxy_set: 是否启用代理，字典
        :param enable_login_set: 是否验证登录，字典
        """
        # 平台名称
        if platform:
            self.browser.find_element_by_xpath("//*[@name='platform']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='platform']/preceding-sibling::input").send_keys(platform)
            log.info("设置平台名称: {0}".format(platform))

        # 平台地址
        if visit_url:
            self.browser.find_element_by_xpath("//*[@name='visitUrl']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath("//*[@name='visitUrl']/preceding-sibling::input").send_keys(visit_url)
            log.info("设置平台地址: {0}".format(visit_url))

        # 平台网络标识
        if network_tag:
            self.browser.find_element_by_xpath("//*[@comboname='platformNwTag']/following-sibling::span//a").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'combobox') and text()='{0}']".format(network_tag)).click()
            log.info("设置平台网络标识: {0}".format(network_tag))

        # 浏览器类型
        if browser_type:
            self.browser.find_element_by_xpath("//*[@name='browserType']/preceding-sibling::input").click()
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'browserType') and text()='{0}']".format(browser_type)).click()
            log.info("设置浏览器类型: {0}".format(browser_type))

        # 浏览器超时时间
        if browser_timeout:
            self.browser.find_element_by_xpath("//*[@name='browseTimeout']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='browseTimeout']/preceding-sibling::input").send_keys(browser_timeout)
            log.info("设置浏览器超时时间: {0}".format(browser_timeout))

        # 空闲刷新时间
        if session_timeout:
            self.browser.find_element_by_xpath("//*[@name='sessionTimeout']/preceding-sibling::input").clear()
            self.browser.find_element_by_xpath(
                "//*[@name='sessionTimeout']/preceding-sibling::input").send_keys(session_timeout)
            log.info("设置空闲刷新时间: {0}".format(session_timeout))

        # 数据类型
        if data_type:
            self.browser.find_element_by_xpath("//*[@name='dataTypeId']/preceding-sibling::input").click()
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.visibility_of_element_located((
                By.XPATH, "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type))))
            self.browser.find_element_by_xpath(
                "//*[contains(@id,'dataTypeId') and text()='{0}']".format(data_type)).click()
            log.info("设置数据类型: {0}".format(data_type))

        # 是否优先点击页面元素
        if first_click_set:
            if first_click_set.get("flag") == "是":
                flag = True
            else:
                flag = False

            # 登录失败是否重试优先点击页面元素
            if first_click_set.get("登录失败是否重试优先点击页面元素") == "是":
                retry_flag = True
            else:
                retry_flag = False
            self.first_click_element(enable_flag=flag, retry_first_click_flag=retry_flag,
                                     element_set=first_click_set.get("点击元素标识"))

        # 是否启用代理
        if enable_proxy_set:
            if enable_proxy_set.get("flag") == "是":
                flag = True
            else:
                flag = False
            self.enable_proxy(enable_flag=flag, proxy_name=enable_proxy_set.get("代理名称"))

        # 是否验证登录
        if enable_login_set:
            if enable_login_set.get("flag") == "是":
                flag = True
            else:
                flag = False
            self.enable_login(enable_flag=flag, username_tag=enable_login_set.get("用户名标识"),
                              username_tag_type=enable_login_set.get("用户名标识类型"),
                              username=enable_login_set.get("账号"),
                              pwd_tag=enable_login_set.get("密码标识"),
                              pwd_tag_type=enable_login_set.get("密码标识类型"),
                              pwd=enable_login_set.get("密码"),
                              login_tag=enable_login_set.get("登录按钮标识"),
                              login_tag_type=enable_login_set.get("登录按钮标识类型"),
                              login_failed_tag=enable_login_set.get("登录异常标识"),
                              login_failed_tag_type=enable_login_set.get("登录异常标识类型"),
                              login_failed_tips=enable_login_set.get("登录异常输出"),
                              enter_after_login_set=enable_login_set.get("是否在输入账号密码后运行"),
                              verification_set=enable_login_set.get("是否开启验证码"),
                              phone_code_set=enable_login_set.get("是否开启手机验证码"))

        # 提交
        self.browser.find_element_by_xpath("//*[@id='submitBtn']//*[text()='提交']").click()

    # 是否优先点击页面元素
    def first_click_element(self, enable_flag, retry_first_click_flag, element_set):
        """
        :param enable_flag: flag, bool，必填
        :param retry_first_click_flag: 登录失败是否重试优先点击页面元素, bool，必填
        :param element_set: 点击元素标识， 数组，必填
        """
        js = 'return $("#isFirstClickEle")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【是否优先点击页面元素】勾选状态: {0}".format(status))

        # 聚焦元素
        first_click_element = self.browser.find_element_by_xpath("//*[@for='isFirstClickEle']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", first_click_element)

        if enable_flag:
            if not status:
                first_click_element.click()
                log.info("开启【是否优先点击页面元素】")
            else:
                # 先把已配置数据删除
                exist_flag = True
                i = 3
                while exist_flag:
                    try:
                        delete_element = self.browser.find_element_by_xpath(
                            "//*[@id='isFirstClickEleDiv']/div[{0}]//*[@onclick='removeItem($(this))']".format(i))
                        delete_element.click()
                        i += 1
                    except NoSuchElementException:
                        exist_flag = False

            retry_js = 'return $("#retryFirstClickTag")[0].checked;'
            retry_status = self.browser.execute_script(retry_js)
            log.info("【登录失败是否重试优先点击页面元素】勾选状态: {0}".format(retry_status))

            retry_click_element = self.browser.find_element_by_xpath("//*[@for='retryFirstClickTag']")
            # 如果登录失败是否重试优先点击页面元素未勾选，先勾选
            if retry_first_click_flag:
                if not retry_status:
                    retry_click_element.click()
                log.info("开启【登录失败是否重试优先点击页面元素】")
            else:
                if retry_status:
                    # 如果flag为否，但当前已勾选，则再点击一次，取消勾选
                    retry_click_element.click()
                    log.info("关闭【登录失败是否重试优先点击页面元素】")
                else:
                    log.info("【登录失败是否重试优先点击页面元素】标识为否，不开启")
            sleep(1)

            log.info("开始配置是否优先点击页面元素")
            i = 2
            j = 1
            for elem_ident, elem_type in element_set:
                if i <= len(element_set) + 1:

                    # 聚焦到每一行
                    input_element = self.browser.find_element_by_xpath(
                        "//*[@id='isFirstClickEleDiv']/div[{0}]//*[@name='labelCode']/preceding-sibling::input[1]".format(
                            i))
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", input_element)

                    # 清空输入框
                    self.browser.find_element_by_xpath(
                        "//*[@id='isFirstClickEleDiv']/div[{0}]//*[@name='labelCode']/preceding-sibling::input[1]".format(
                            i)).clear()

                    # 输入框输入
                    self.browser.find_element_by_xpath(
                        "//*[@id='isFirstClickEleDiv']/div[{0}]//*[@name='labelCode']/preceding-sibling::input[1]".format(
                            i)).send_keys(elem_ident)

                    # 点击下拉框
                    self.browser.find_element_by_xpath(
                        "//*[@id='isFirstClickEleDiv']/div[{0}]//*[@name='labelCodeType']/preceding-sibling::input[1]".format(
                            i)).click()

                    # 下拉框选择
                    if i == 2:
                        self.browser.find_element_by_xpath(
                            "//*[contains(@id,'eleTypeFirst') and text()='{0}']".format(elem_type)).click()
                        i += 1
                    else:
                        try:
                            element = self.browser.find_element_by_xpath(
                                "//*[contains(@id,'labelCodeType_addClkEle{0}') and text()='{1}']".format(
                                    j, elem_type))
                            element.click()
                            j += 1
                        except NoSuchElementException:
                            j += 1
                            self.browser.find_element_by_xpath(
                                "//*[contains(@id,'labelCodeType_addClkEle{0}') and text()='{1}']".format(
                                    j, elem_type)).click()
                        finally:
                            i += 1
                    sleep(1)
                    log.info("【是否优先点击页面元素】添加元素: {0}, {1}".format(elem_ident, elem_type))

                    if i <= len(element_set) + 1:
                        self.browser.find_element_by_xpath("//*[@id='addClkEle']").click()
                else:
                    break
            sleep(1)
        else:
            if status:
                # 如果flag为否，但当前已勾选，则再点击一次，取消勾选
                first_click_element.click()
                log.info("关闭【是否优先点击页面元素】")
            else:
                log.info("【是否优先点击页面元素】标识为否，不开启")

    # 是否启用代理
    def enable_proxy(self, enable_flag, proxy_name):
        """
        :param enable_flag: flag, bool，必填
        :param proxy_name: 代理名称, 非必填
        """
        js = 'return $("#isProxy")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【是否启用代理】勾选状态: {0}".format(status))
        # 聚焦元素
        enable_proxy_element = self.browser.find_element_by_xpath("//*[@for='isProxy']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", enable_proxy_element)

        if enable_flag:
            if not status:
                # 如果未勾选，先勾选
                enable_proxy_element.click()
                log.info("开启【启用代理】")

            log.info("开始配置代理")

            # 点击下拉框
            self.browser.find_element_by_xpath("//*[@name='proxyId']/preceding-sibling::input").click()
            sleep(1)
            try:
                proxy_element = self.browser.find_element_by_xpath(
                    "//*[contains(@id,'proxyId') and text()='{0}']".format(proxy_name))
                sleep(1)
                action = ActionChains(self.browser)
                action.move_to_element(proxy_element).perform()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'proxyId') and text()='{0}']".format(proxy_name)).click()
                log.info("已选择代理: {0}".format(proxy_name))
            except NoSuchElementException:
                raise NoSuchElementException("找不到指定代理: {0}".format(proxy_name))
        else:
            if status:
                # 如果flag为否，但当前已勾选，则再点击一次，取消勾选
                enable_proxy_element.click()
                log.info("关闭【是否启用代理】")
            else:
                log.info("【是否启用代理】 标识为否，不开启")

    # 是否验证登录
    def enable_login(self, enable_flag, username_tag, username_tag_type, username, pwd_tag, pwd_tag_type, pwd, login_tag,
                     login_tag_type, login_failed_tag, login_failed_tag_type, login_failed_tips, enter_after_login_set,
                     verification_set, phone_code_set=None):
        """
        :param enable_flag: flag, bool，必填
        :param username_tag: 用户名标识，必填
        :param username_tag_type: 用户名标识类型，非必填
        :param username: 账号，必填
        :param pwd_tag: 密码标识， 必填
        :param pwd_tag_type: 密码标识类型，非必填
        :param pwd: 密码，必填
        :param login_tag: 登录按钮标识，非必填
        :param login_tag_type: 登录按钮标识类型，非必填
        :param login_failed_tag: 登录异常标识，非必填
        :param login_failed_tag_type: 登录异常标识类型，非必填
        :param login_failed_tips: 登录异常输出，非必填
        :param enter_after_login_set: 是否在输入账号密码后运行，字典，非必填
        :param verification_set: 是否开启验证码，字典，非必填
        :param phone_code_set: 是否开启手机验证码，字典，非必填

        {
            "flag": "是",
            "用户名标识": "userId",
            "用户名标识类型": "id",
            "账号": "pw",
            "密码标识": "password",
            "密码标识类型": "id",
            "密码": "1qazXSW#",
            "登录按钮标识": "loginButton",
            "登录按钮标识类型": "id",
            "登录异常标识": "//div[@id='errorTip']/span[contains(text(),'账号或密码错误')]",
            "登录异常标识类型": "xpath",
            "登录异常输出": "账号或密码错误",
            "是否在输入账号密码后运行": {
                "flag": "是",
                "点击元素标识": [["cc", "id"], ["dd", "xpath"]]
            },
            "是否开启验证码": {
                "flag": "是",
                "验证码输入标识": "ee",
                "验证码输入标识类型": "xpath",
                "验证码图片标识": "ff",
                "验证码图片标识类型": "id",
                "验证码识别模型": "网络资源验证码模型"
            },
            "是否开启手机验证码": {
                "flag": "是",
                "验证码输入标识": "ee",
                "验证码输入标识类型": "xpath",
                "手机验证码发送按钮标识": "ff",
                "手机验证码发送按钮标识类型": "id"
            }
        }
        """
        js = 'return $("#isValidLogin")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【是否验证登录】勾选状态: {0}".format(status))

        enable_login_element = self.browser.find_element_by_xpath("//*[@for='isValidLogin']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", enable_login_element)
        sleep(1)

        if enable_flag:

            # 如果未勾选，则勾选
            if not status:
                enable_login_element.click()
                log.info("开启【是否验证登录】")
                sleep(1)

            focus_element = self.browser.find_element_by_xpath(
                "//*[@id='isLoginDiv']//*[@name='loginErrOutput']/preceding-sibling::input")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", focus_element)
            sleep(1)

            log.info("开始配置登录信息")
            # 用户名标识
            if username_tag:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelUsername']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelUsername']/preceding-sibling::input").send_keys(username_tag)
                log.info("设置用户名标识: {0}".format(username_tag))

            # 用户名标识类型
            if username_tag_type:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelUsernameType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'labelUsernameType') and text()='{0}']".format(username_tag_type)).click()
                log.info("设置用户名标识类型: {0}".format(username_tag_type))

            # 账号
            if username:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='username']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='username']/preceding-sibling::input").send_keys(username)
                log.info("设置账号: {0}".format(username))

            # 密码标识
            if pwd_tag:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelPwd']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelPwd']/preceding-sibling::input").send_keys(pwd_tag)
                log.info("设置密码标识: {0}".format(pwd_tag))

            # 密码标识类型
            if pwd_tag_type:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelPwdType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'labelPwdType') and text()='{0}']".format(pwd_tag_type)).click()
                log.info("设置密码标识类型: {0}".format(pwd_tag_type))

            # 密码
            if pwd:
                update_pwd_element = self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='pwd']/preceding-sibling::span/a[1]")
                if update_pwd_element.get_attribute("class").find("edit") > -1:
                    # 修改密码
                    update_pwd_element.click()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='pwd']/preceding-sibling::input").send_keys(pwd)
                sleep(1)
                log.info("设置密码: {0}".format(pwd))

            # 登录按钮标识
            if login_tag:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelSubmitbtn']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelSubmitbtn']/preceding-sibling::input").send_keys(login_tag)
                log.info("设置登录按钮标识: {0}".format(login_tag))

            # 登录按钮标识类型
            if login_tag_type:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='labelSubmitType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'labelSubmitType') and text()='{0}']".format(login_tag_type)).click()
                log.info("设置登录按钮标识类型: {0}".format(login_tag_type))

            # 登录异常标识
            if login_failed_tag:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='loginErrCode']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='loginErrCode']/preceding-sibling::input").send_keys(
                    login_failed_tag)
                log.info("设置登录异常标识: {0}".format(login_failed_tag))

            # 登录异常标识类型
            if login_failed_tag_type:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='loginErrCodeType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'loginErrCodeType') and text()='{0}']".format(login_failed_tag_type)).click()
                log.info("设置登录异常标识类型: {0}".format(login_failed_tag_type))

            # 登录异常输出
            if login_failed_tips:
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='loginErrOutput']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isLoginDiv']//*[@name='loginErrOutput']/preceding-sibling::input").send_keys(
                    login_failed_tips)
                log.info("设置登录异常输出: {0}".format(login_failed_tips))

            # 是否在输入账号密码后运行
            if enter_after_login_set:
                if enter_after_login_set.get("flag") == "是":
                    flag = True
                else:
                    flag = False
                self.click_after_enter_pwd(enable_flag=flag, element_set=enter_after_login_set.get("点击元素标识"))

            # 是否开启验证码
            if verification_set:
                if verification_set.get("flag") == "是":
                    flag = True
                else:
                    flag = False
                self.valid_code(enable_flag=flag,
                                verification_tag=verification_set.get("验证码输入标识"),
                                verification_tag_type=verification_set.get("验证码输入标识类型"),
                                verification_img_tag=verification_set.get("验证码图片标识"),
                                verification_img_tag_type=verification_set.get("验证码图片标识类型"),
                                model=verification_set.get("验证码识别模型"))

            # 是否开启手机验证码
            if phone_code_set:
                if phone_code_set.get("flag") == "是":
                    flag = True
                else:
                    flag = False
                self.phone_code(enable_flag=flag,
                                verification_tag=phone_code_set.get("验证码输入标识"),
                                verification_tag_type=phone_code_set.get("验证码输入标识类型"),
                                verification_send_tag=phone_code_set.get("手机验证码发送按钮标识"),
                                verification_send_tag_type=phone_code_set.get("手机验证码发送按钮标识类型"))

        else:
            if status:
                enable_login_element.click()
                log.info("关闭【是否验证登录】")
            else:
                log.info("【是否验证登录】标识为否，不开启")

    # 是否在输入账号密码后运行
    def click_after_enter_pwd(self, enable_flag, element_set):
        """
        :param enable_flag: flag，bool，必填
        :param element_set: 点击元素标识，字典，必填
        """
        js = 'return $("#isInpAccLastClick")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【是否在输入账号密码后运行】勾选状态: {0}".format(status))

        after_pwd_element = self.browser.find_element_by_xpath("//*[@for='isInpAccLastClick']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", after_pwd_element)

        if enable_flag:
            if not status:
                after_pwd_element.click()
                log.info("开启【是否在输入账号密码后运行】")
            else:
                # 先将元素删除，保留一行
                for i in range(3, 10):
                    try:
                        delete_element = self.browser.find_element_by_xpath(
                            "//*[@id='isInpAccLastClickDiv']/div[{0}]//*[@onclick='removeItem($(this))']".format(i))
                        delete_element.click()
                    except NoSuchElementException:
                        break

            log.info("开始配置是否在输入账号密码后运行")
            i = 1
            j = 3
            for elem_ident, elem_type in element_set:
                if i <= len(element_set):

                    # 聚焦到元素
                    element = self.browser.find_element_by_xpath(
                        "//*[@id='isInpAccLastClickDiv']/div[{0}]//*[@name='labelCode']/preceding-sibling::input".format(
                            i))
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", element)

                    # 先清空输入框
                    self.browser.find_element_by_xpath(
                        "//*[@id='isInpAccLastClickDiv']/div[{0}]//*[@name='labelCode']/preceding-sibling::input".format(
                            i)).clear()

                    # 输入框输入
                    self.browser.find_element_by_xpath(
                        "//*[@id='isInpAccLastClickDiv']/div[{0}]//*[@name='labelCode']/preceding-sibling::input".format(
                            i)).send_keys(elem_ident)

                    # 点击下拉框
                    self.browser.find_element_by_xpath(
                        "//*[@id='isInpAccLastClickDiv']/div[{0}]//*[@name='labelCodeType']/preceding-sibling::input".format(
                            i)).click()
                    sleep(1)

                    # 下拉框选择值
                    if i == 1:
                        self.browser.find_element_by_xpath(
                            "//*[contains(@id,'eleTypeInp') and text()='{0}']".format(elem_type)).click()
                        i += 1
                    else:
                        self.browser.find_element_by_xpath(
                            "//*[contains(@id,'labelCodeType_addLstClk{0}') and text()='{1}']".format(
                                j, elem_type)).click()
                        i += 1
                        j += 1
                    sleep(1)
                    log.info("【是否在输入账号密码后运行】添加元素: {0}, {1}".format(elem_ident, elem_type))

                    # 点击加号新增一行元素
                    if i <= len(element_set):
                        self.browser.find_element_by_xpath("//*[@id='addLstClk']").click()
                else:
                    break
            sleep(1)
        else:
            if status:
                after_pwd_element.click()
                log.info("关闭【是否在输入账号密码后运行】")
            else:
                log.info("【是否在输入账号密码后运行】标识为否，不开启")

    # 是否启用验证码
    def valid_code(self, enable_flag, verification_tag, verification_tag_type, verification_img_tag,
                   verification_img_tag_type, model):
        """
        :param enable_flag: flag，bool，必填
        :param verification_tag: 验证码输入标识，必填
        :param verification_tag_type: 验证码输入标识类型，非必填
        :param verification_img_tag: 验证码图片标识，必填
        :param verification_img_tag_type: 验证码图片标识类型，非必填
        :param model: 验证码识别模型，非必填
        """
        js = 'return $("#isValidCode")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【是否启用验证码】勾选状态: {0}".format(status))

        enable_valid_code_element = self.browser.find_element_by_xpath("//*[@for='isValidCode']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", enable_valid_code_element)

        if enable_flag:
            if not status:
                enable_valid_code_element.click()
                log.info("开启【验证码】")

            model_element = self.browser.find_element_by_xpath("//*[@name='validCodeModel']/preceding-sibling::input")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", model_element)
            sleep(1)

            log.info("开始配置验证码")

            # 验证码输入标识
            if verification_tag:
                self.browser.find_element_by_xpath(
                    "//*[@id='isValidCodeDiv']/div[1]//*[@name='labelCode']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@id='isValidCodeDiv']/div[1]//*[@name='labelCode']/preceding-sibling::input").send_keys(
                    verification_tag)
                log.info("设置验证码输入标识: {0}".format(verification_tag))

            # 验证码输入标识类型
            if verification_tag_type:
                self.browser.find_element_by_xpath(
                    "//*[@id='isValidCodeDiv']/div[1]//*[@name='labelCodeType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'labelCodeType') and text()='{0}']".format(verification_tag_type)).click()
                log.info("设置验证码输入标识类型: {0}".format(verification_tag_type))

            # 验证码图片标识
            if verification_img_tag:
                self.browser.find_element_by_xpath("//*[@name='labelCodeImage']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath(
                    "//*[@name='labelCodeImage']/preceding-sibling::input").send_keys(verification_img_tag)
                log.info("设置验证码图片标识: {0}".format(verification_img_tag))

            # 验证码图片标识类型
            if verification_img_tag_type:
                self.browser.find_element_by_xpath("//*[@name='labelCodeImageType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'labelCodeImageType') and text()='{0}']".format(verification_img_tag_type)).click()
                log.info("设置验证码图片标识类型: {0}".format(verification_img_tag_type))

            # 验证码识别模型
            if model:
                self.browser.find_element_by_xpath("//*[@name='validCodeModel']/preceding-sibling::input").click()
                try:
                    valid_code_model_element = self.browser.find_element_by_xpath(
                        "//*[contains(@id,'validCodeModel') and text()='{0}']".format(model))
                    action = ActionChains(self.browser)
                    action.move_to_element(valid_code_model_element).perform()
                    self.browser.find_element_by_xpath(
                        "//*[contains(@id,'validCodeModel') and text()='{0}']".format(model)).click()
                    log.info("选择验证码模型: {0}".format(model))
                except NoSuchElementException:
                    raise NoSuchElementException("找不到指定验证码模型: {0}".format(model))

        else:
            if status:
                enable_valid_code_element.click()
                log.info("关闭【是否开启验证码】")
            else:
                log.info("【是否开启验证码】 标识为否，不开启")

    # 是否启用验证码
    def phone_code(self, enable_flag, verification_tag, verification_tag_type, verification_send_tag,
                   verification_send_tag_type):
        """
        :param enable_flag: flag，bool，必填
        :param verification_tag: 验证码输入标识，必填
        :param verification_tag_type: 验证码输入标识类型，非必填
        :param verification_send_tag: 手机验证码发送按钮标识，必填
        :param verification_send_tag_type: 手机验证码发送按钮标识类型，非必填
        """
        js = 'return $("#isPhoneCode")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【是否启用手机验证码】勾选状态: {0}".format(status))

        enable_phone_code_element = self.browser.find_element_by_xpath("//*[@for='isPhoneCode']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", enable_phone_code_element)

        if enable_flag:
            if not status:
                enable_phone_code_element.click()
                log.info("开启【手机验证码】")

            phone_element = self.browser.find_element_by_xpath(
                "//*[@id='isValidCodeDiv']/div[1]//*[@name='labelCode']/preceding-sibling::input")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", phone_element)
            sleep(1)

            log.info("开始配置手机验证码")

            # 验证码输入标识
            if verification_tag:
                self.browser.find_element_by_xpath("//*[@name='labelPhoneCode']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath("//*[@name='labelPhoneCode']/preceding-sibling::input").send_keys(
                    verification_tag)
                log.info("设置验证码输入标识: {0}".format(verification_tag))

            # 验证码输入标识类型
            if verification_tag_type:
                self.browser.find_element_by_xpath("//*[@name='labelPhoneCodeType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath(
                    "//*[contains(@id,'labelPhoneCodeType') and text()='{0}']".format(verification_tag_type)).click()
                log.info("设置验证码输入标识类型: {0}".format(verification_tag_type))

            # 手机验证码发送按钮标识
            if verification_send_tag:
                self.browser.find_element_by_xpath("//*[@name='labelPhoneCodeBtn']/preceding-sibling::input").clear()
                self.browser.find_element_by_xpath("//*[@name='labelPhoneCodeBtn']/preceding-sibling::input").send_keys(
                    verification_send_tag)
                log.info("设置手机验证码发送按钮标识: {0}".format(verification_send_tag))

            # 手机验证码发送按钮标识类型
            if verification_send_tag_type:
                self.browser.find_element_by_xpath("//*[@name='labelPhoneCodeBtnType']/preceding-sibling::input").click()
                self.browser.find_element_by_xpath("//*[contains(@id,'labelPhoneCodeBtnType') and text()='{0}']".format(
                    verification_send_tag_type)).click()
                log.info("设置手机验证码发送按钮标识类型: {0}".format(verification_send_tag_type))
        else:
            if status:
                enable_phone_code_element.click()
                log.info("关闭【手机验证码】")
            else:
                log.info("【是否开启手机验证码】 标识为否，不开启")

    def update(self, obj, platform, visit_url, network_tag, browser_type, browser_timeout, session_timeout, data_type,
               first_click_set, enable_proxy_set, enable_login_set):
        """
        :param obj: 平台名称
        :param platform: 平台名称
        :param visit_url: 平台地址
        :param network_tag: 平台网络标识
        :param browser_type: 浏览器类型
        :param browser_timeout: 浏览器超时时间
        :param session_timeout: 空闲刷新时间
        :param data_type: 数据类型
        :param first_click_set: 是否优先点击页面元素，字典
        :param enable_proxy_set: 是否启用代理，字典
        :param enable_login_set: 是否验证登录，字典
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
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'nodeVosLoginCfgEdit.html?type=edit')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='platform']/preceding-sibling::input")))

            self.system_page(platform=platform, visit_url=visit_url, network_tag=network_tag, browser_type=browser_type,
                             browser_timeout=browser_timeout, session_timeout=session_timeout, data_type=data_type,
                             first_click_set=first_click_set, enable_proxy_set=enable_proxy_set,
                             enable_login_set=enable_login_set)
            alert = BeAlertBox()
            msg = alert.get_msg()
            if alert.title_contains("保存成功"):
                log.info("{0} 修改成功".format(obj))
            else:
                log.warn("{0} 修改失败，失败提示: {1}".format(obj, msg))
            set_global_var("ResultMsg", msg, False)

    def test(self, obj):
        """
        :param obj: 平台名称
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
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.frame_to_be_available_and_switch_to_it((
                By.XPATH, "//iframe[contains(@src,'nodeVosLoginCfgEdit.html?type=edit')]")))
            sleep(1)
            wait = WebDriverWait(self.browser, 30)
            wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='platform']/preceding-sibling::input")))

            self.browser.find_element_by_xpath("//*[@id='testBtn']//*[text()='测试']").click()
            log.info("开始测试中...")
            alert = BeAlertBox(timeout=180)
            msg = alert.get_msg()
            if alert.title_contains("测试成功"):
                log.info("{0} 测试成功".format(obj))
            else:
                log.warn("{0} 测试失败，测试返回结果: {1}".format(obj, msg))
            set_global_var("ResultMsg", msg, False)

    def delete(self, obj):
        """
        :param obj: 平台名称
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
            if alert.title_contains("成功"):
                log.info("{0} 删除成功".format(obj))
            else:
                log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        else:
            log.warn("{0} 删除失败，失败提示: {1}".format(obj, msg))
        set_global_var("ResultMsg", msg, False)

    def data_clear(self, obj, fuzzy_match=False):
        """
        :param obj: 平台名称
        :param fuzzy_match: 模糊匹配
        """
        # 用于清除数据，在测试之前执行, 使用关键字开头模糊查询
        self.browser.find_element_by_xpath("//*[@name='platform']/preceding-sibling::input").clear()
        self.browser.find_element_by_xpath("//*[@name='platform']/preceding-sibling::input").send_keys(obj)
        self.browser.find_element_by_xpath("//*[@id='btn']//*[text()='查询']").click()
        page_wait()
        fuzzy_match = True if fuzzy_match == "是" else False
        if fuzzy_match:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='platform']/*[contains(@class,'platform')]/*[starts-with(text(),'{0}')]".format(obj))
        else:
            record_element = self.browser.find_elements_by_xpath(
                "//*[@field='platform']/*[contains(@class,'platform')]/*[text()='{0}']".format(obj))
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
                                "//*[@field='platform']/*[contains(@class,'platform')]/*[starts-with(text(),'{0}')]".format(
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
