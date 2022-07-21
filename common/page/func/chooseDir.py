# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午4:11

from selenium.common.exceptions import NoSuchElementException
from time import sleep
from common.log.logger import log
from common.variable.globalVariable import *


def choose_ftp_dir(path):
    """
    :param path: 类似根目录-pw-AI
    :return: 点击
    """
    browser = get_global_var("browser")
    path_level = path.split("-")
    sleep(1)
    for level in path_level:
        # 如果当前不是输入的目录最后一层，点击前面的+，否则点击目录名
        if level != path_level[-1]:
            elements = browser.find_elements_by_xpath(
                "//*[contains(@id,'_easyui_tree_')]/*[text()='{0}']/preceding-sibling::span[2]".format(level))
        else:
            elements = browser.find_elements_by_xpath("//*[contains(@id,'_easyui_tree_')]/*[text()='{0}']".format(level))
        sleep(1)
        # 点击当前可见元素
        choose_finished = False
        for e in elements:
            if e.is_displayed():
                browser.execute_script("arguments[0].scrollIntoView(true);", e)
                e.click()
                choose_finished = True
                break
        if not choose_finished:
            raise NoSuchElementException("未找到目录: {0}".format(level))
        else:
            sleep(2)


def choose_file_dir(dir_name):
    """
    :param dir_name: 目录名
    :return: 点击
    """
    browser = get_global_var("browser")
    dir_element = browser.find_elements_by_xpath(
        "//*[@class='tree-node']/*[@class='tree-title' and text()='{0}']".format(dir_name))
    for element in dir_element:
        if element.is_displayed():
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            log.info("选择目录: {0}".format(dir_name))
            break
