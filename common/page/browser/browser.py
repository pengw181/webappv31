# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/10 下午5:10


from selenium import webdriver
from common.log.logger import log
from common.variable.global_variable import *
from config.loads import properties


def init_browser():
    log.info("开始初始化浏览器.")
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': properties.get("downLoadPath")}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(properties.get("chromeDriverPath"), chrome_options=options)
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': properties.get("downLoadPath")}}
    browser.execute("send_command", params)
    log.info("浏览器初始化完成，浏览器信息: {}".format(browser))
    set_global_var("browser", browser)
    return browser
