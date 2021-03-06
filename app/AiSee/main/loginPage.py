# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午2:28

from time import sleep
from common.page.handle.windows import WindowHandles
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.log.logger import log
from common.variable.globalVariable import *
from config.loads import properties
from common.page.browser.browser import init_browser
from common.page.func.pageMaskWait import page_wait


class LoginPage:

    username = (By.ID, "userId")
    password = (By.ID, "password")
    okButton = (By.ID, "loginButton")

    def __init__(self):
        self.browser = init_browser()
        self.browser.get(properties.get("pageUrl"))
        self.browser.maximize_window()

        # https高级
        if str(properties.get("pageUrl")).startswith("https"):
            self.browser.find_element_by_xpath(
                "//*[text()='返回安全连接']/following-sibling::button[2][contains(text(),'高级')]").click()
            self.browser.find_element_by_xpath("//*[@id='proceed-link']").click()

        # 等待页面加载
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@class='autoLoadImg_companyInLogin']")))

    def set_username(self, username):
        name = self.browser.find_element(*LoginPage.username)
        name.send_keys(username)

    def set_password(self, password):
        pwd = self.browser.find_element(*LoginPage.password)
        pwd.send_keys(password)

    def click_ok(self):
        button = self.browser.find_element(*LoginPage.okButton)
        button.click()

    def get_login_status(self):
        try:
            self.browser.find_element(*LoginPage.username)
            return False
        except NoSuchElementException:
            return True


def login(username, password):

    # 是否关闭谷歌进程, IOS下无效，Windows下可以关闭所有谷歌进程
    # os.app('TASKKILL /F /IM chrome.exe 1>nul')

    login_action = LoginPage()
    login_action.set_username(username)
    login_action.set_password(password)
    login_action.click_ok()
    log.info("#######################欢迎登录AiSee系统#######################")
    log.info("登录用户名：%s, 用户密码：%s" % (get_global_var("LoginUser"), get_global_var("LoginPwd")))
    page_wait()
    sleep(1)
    current_win_handle = WindowHandles()
    current_win_handle.save("首页")
    return True
