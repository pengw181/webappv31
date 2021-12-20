# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 上午11:48

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from app.VisualModeler.main.menu.tab_xpath import tab_xpath as visual_tab
from app.Crawler.main.menu.tab_xpath import tab_xpath as crawler_tab
from common.variable.global_variable import *
from common.log.logger import log
from config.loads import properties


class TabHandles:

    def __init__(self):
        self.browser = get_global_var("browser")

        self.table_handles = get_global_var("TableHandles")
        if self.table_handles is None:
            self.table_handles = {}

    def save(self, title):
        if properties.get("application") == "visualmodeler":
            tab_xpath = visual_tab
        elif properties.get("application") == "crawler":
            tab_xpath = crawler_tab
        else:
            tab_xpath = None
        if title not in self.table_handles.keys():
            self.table_handles[title] = tab_xpath.get(title)
            set_global_var("TableHandles", self.table_handles)
            log.info("tab列表增加: %s, %s" % (title, tab_xpath.get(title)))
        log.info("当前tab句柄信息: {0}".format(get_global_var("TableHandles")))

    def switch(self, title):
        try:
            self.browser.find_element(By.XPATH, self.table_handles.get(title)).click()
            log.info("切换到tab页: {0}，{1}".format(title, self.table_handles.get(title)))
        except NoSuchElementException:
            raise "tab {0} 不存在！！！".format(title)
