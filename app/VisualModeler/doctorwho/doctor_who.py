# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午2:50

from common.page.handle.windows import WindowHandles
from common.page.handle.tab import TabHandles
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from app.VisualModeler.main.menu.menu_xpath import *
from time import sleep
from common.log.logger import log
from common.variable.global_variable import *


class DoctorWho:

    def __init__(self):
        self.browser = get_global_var("browser")
        self.current_win_handle = WindowHandles()
        log.info("进入领域后，保存新窗口句柄")

        # 关闭多余窗口
        self.current_win_handle.close(title="流程图编辑器")
        self.current_win_handle.close(title="告警平台")

        # 切换到vm窗口
        self.current_win_handle.save("vm")
        self.current_win_handle.switch("vm")
        # log.info("tab : {}".format(get_global_var("TableHandles")))
        if bool(get_global_var("TableHandles")):
            self.browser.refresh()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@mid='PersonalCenter1001']//*[text()='个人中心']")))

    def choose_menu(self, menu_path):
        menu_list = str(menu_path).split("-")
        first_menu = menu_list[0]
        second_menu = menu_list[1]
        current_tab_handle = TabHandles()

        try:
            first_menu_element = self.browser.find_element_by_xpath(first_menu_xpath.get(first_menu))
            self.browser.execute_script("arguments[0].scrollIntoView(true);", first_menu_element)
            first_menu_element.click()
            log.info("点击一级菜单: {0}".format(first_menu))
            sleep(1)

            if second_menu:
                second_menu_element = self.browser.find_element_by_xpath(second_menu_xpath.get(second_menu))
                self.browser.execute_script("arguments[0].scrollIntoView(true);", second_menu_element)
                second_menu_element.click()
                log.info("点击二级菜单: {0}".format(second_menu))
                sleep(1)

                # 如果打开的二级菜单是在当前页面，在点击二级菜单后需要保存tab句柄
                if second_menu not in ("云平台", "告警", "OA审批平台"):
                    if second_menu not in ["文件目录管理"]:
                        current_tab_handle.save(second_menu)
                        current_tab_handle.switch(second_menu)
                    else:
                        # 文件目录管理特殊处理
                        third_menu = menu_list[2]
                        third_menu_element = self.browser.find_element_by_xpath(third_menu_xpath.get(third_menu))
                        self.browser.execute_script("arguments[0].scrollIntoView(true);", third_menu_element)
                        third_menu_element.click()
                        log.info("点击三级菜单: {0}".format(third_menu))
                        sleep(1)
                        current_tab_handle.save(third_menu)
                        current_tab_handle.switch(third_menu)
                else:
                    # 如果打开的二级菜单是新开标签，如：告警、OA审批平台、云平台，在点击二级菜单后需要保存windows句柄
                    self.current_win_handle.save(second_menu)
                    self.current_win_handle.switch(second_menu)
                    sleep(3)
            return True
        except NoSuchElementException:
            return False

    def logout(self):

        try:
            self.browser.find_element_by_xpath("//*[@id='logout']").click()
        except NoSuchElementException:
            raise
