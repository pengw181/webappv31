# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午6:31

from pykeyboard import PyKeyboard
from time import sleep
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from common.log.logger import log
from common.variable.globalVariable import *
from config.loads import properties

# Used for Mac


def upload(file_name, catalog=None, input_id='filebox_file_id_2'):
    browser = get_global_var("browser")
    if not properties.get("uploadPath").endswith("/"):
        properties["uploadPath"] += "/"
    if catalog:
        path = properties.get("uploadPath") + catalog + "/" + file_name
    else:
        path = properties.get("uploadPath") + file_name
    log.info("上传文件路径: {0}".format(path))
    browser.find_element_by_xpath("//*[@id='{0}']".format(input_id)).send_keys(path)
    # k = PyKeyboard()
    # upload_action(path=path)
    #
    # flag = False
    # try_time = 1
    # max_try_times = 3
    # while not flag:
    #     if try_time < max_try_times:
    #         # 未达到最大重试次数
    #         action = ActionChains(browser)
    #         action.move_to_element(browser.find_element_by_xpath(
    #             "//*[@id='{0}']/preceding-sibling::input".format(input_id))).perform()
    #         js = 'return $("#{0}")[0].files[0].name;'.format(input_id)
    #         try:
    #             upload_file_name = browser.execute_script(js)
    #             log.info("当前上传文件: {0}".format(upload_file_name))
    #             flag = True
    #         except JavascriptException:
    #             # 文件上传失败，重试
    #             log.warn("文件上传失败，开始第{0}次重试".format(try_time))
    #             sleep(1)
    #             k.press_keys(['Return'])
    #             sleep(1)
    #             upload_action(path=path)
    #             try_time += 1
    #     else:
    #         raise Exception("尝试{0}次均上传文件不成功".format(max_try_times))


def upload_action(path):
    k = PyKeyboard()
    k.press_keys(['Command', 'shift', 'g'])
    k.release_key('Command')
    sleep(1)
    k.type_string(path)
    sleep(3)
    k.tap_key('Return')
    # k.press_keys(['Return'])
    # 这里会自动读取文件内容，需要时间比较长
    sleep(3)
    k.tap_key('Return')
    # k.press_keys(['Return'])
    sleep(1)
