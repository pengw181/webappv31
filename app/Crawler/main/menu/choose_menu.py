# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/10 下午5:58

from common.page.handle.tab import TabHandles
from .menu_xpath import *
from common.log.logger import log
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from common.variable.global_variable import *


def choose_menu(menu_path):
    browser = get_global_var("browser")
    menu_list = str(menu_path).split("-")
    first_menu = menu_list[0]
    second_menu = menu_list[1]
    current_tab_handle = TabHandles()

    try:
        first_menu_element = browser.find_element_by_xpath(first_menu_xpath.get(first_menu))
        browser.execute_script("arguments[0].scrollIntoView(true);", first_menu_element)
        first_menu_element.click()
        log.info("点击一级菜单: {0}".format(first_menu))
        sleep(1)

        if second_menu:
            second_menu_element = browser.find_element_by_xpath(second_menu_xpath.get(second_menu))
            browser.execute_script("arguments[0].scrollIntoView(true);", second_menu_element)
            second_menu_element.click()
            log.info("点击二级菜单: {0}".format(second_menu))
            current_tab_handle.save(second_menu)
            current_tab_handle.switch(second_menu)
            sleep(1)

        return True
    except NoSuchElementException:
        return False
