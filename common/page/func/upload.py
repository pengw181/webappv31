# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午6:31

from pykeyboard import PyKeyboard
from time import sleep
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from common.log.logger import log
from common.variable.global_variable import *
from config.loads import properties

# Used for Mac


def upload(file_name, input_id='filebox_file_id_2'):
    browser = get_global_var("browser")
    if not properties.get("uploadPath").endswith("/"):
        properties["uploadPath"] += "/"
    path = properties.get("uploadPath") + file_name
    log.info("上传文件路径: {0}".format(path))
    k = PyKeyboard()
    upload_action(path=path)

    flag = False
    retry_time = 1
    max_try_times = 3
    while not flag:
        if retry_time < max_try_times:
            # 未达到最大重试次数
            action = ActionChains(browser)
            action.move_to_element(browser.find_element_by_xpath(
                "//*[@id='{0}']/preceding-sibling::input".format(input_id))).perform()
            js = 'return $("#{0}")[0].files[0].name;'.format(input_id)
            try:
                upload_file_name = browser.execute_script(js)
                log.info("当前上传文件: {0}".format(upload_file_name))
                flag = True
            except JavascriptException:
                # 文件上传失败，重试
                log.info("文件上传失败，开始第{0}次重试".format(retry_time))
                k.press_keys(['Return'])
                sleep(1)
                upload_action(path=path)
                retry_time += 1
        else:
            raise Exception("尝试{0}次均上传文件不成功".format(max_try_times))


def upload_action(path):
    k = PyKeyboard()
    k.press_keys(['Command', 'shift', 'g'])
    k.release_key('Command')
    sleep(1)
    k.type_string(path)
    sleep(1)
    k.tap_key('Return')
    # k.press_keys(['Return'])
    # 这里会自动读取文件内容，需要时间比较长
    sleep(2)
    k.tap_key('Return')
    # k.press_keys(['Return'])
    sleep(1)


def upload_file(file_name, input_id='filebox_file_id_2'):
    browser = get_global_var("browser")
    if not properties.get("uploadPath").endswith("/"):
        properties["uploadPath"] += "/"
    path = properties.get("uploadPath") + file_name
    log.info("上传文件路径: {0}".format(path))
    k = PyKeyboard()
    k.press_keys(['Command', 'shift', 'g'])
    k.release_key('Command')
    k.press_keys(['backspace'])
    k.release_key('backspace')
    sleep(1)
    k.type_string(path)
    sleep(1)
    # 确认文件
    k.press_keys(['Return'])
    sleep(3)
    # 确认上传
    k.press_keys(['Return'])
    sleep(1)
    # 检测文件是否已经上传到输入框
    try:
        js = 'return $("#{}")[0].files[0].name;'.format(input_id)
        uploaded_file_name = browser.execute_script(js)
        log.info("已上传文件: {}".format(uploaded_file_name))
    except JavascriptException:
        sleep(2)
        k.press_keys(['Return'])
        try:
            js = 'return $("#{}")[0].files[0].name;'.format(input_id)
            uploaded_file_name = browser.execute_script(js)
            log.info("已上传文件: {}".format(uploaded_file_name))
        except JavascriptException:
            raise Exception("上传文件不成功")
