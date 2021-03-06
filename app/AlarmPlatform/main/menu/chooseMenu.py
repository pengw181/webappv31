# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/12/27 上午11:27

from common.variable.globalVariable import *
from common.log.logger import log
from .menuXpath import *
from time import sleep
from selenium.common.exceptions import NoSuchElementException


def choose_menu(menu_path):
    browser = get_global_var("browser")
    menu_list = str(menu_path).split("-")
    first_menu = menu_list[0]
    second_menu = menu_list[1]

    try:
        browser.find_element_by_xpath(first_menu_xpath.get(first_menu)).click()
        log.info("点击一级菜单: {0}".format(first_menu))
        sleep(1)

        if second_menu:
            second_menu_element = browser.find_element_by_xpath(second_menu_xpath.get(second_menu))
            browser.execute_script("arguments[0].scrollIntoView(true);", second_menu_element)
            second_menu_element.click()
            log.info("点击二级菜单: {0}".format(second_menu))
            sleep(1)

        return True
    except NoSuchElementException:
        return False
