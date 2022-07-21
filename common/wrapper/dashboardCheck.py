# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2022/5/26 上午10:54

from common.variable.globalVariable import get_global_var
from common.page.func.pageMaskWait import page_wait
from common.page.script.css import setVisible


# 关闭并进入仪表盘配置页面
def closeAndEnterDashboard(func):
    def wrapper(*args, **kwargs):
        browser = get_global_var("browser")
        # noinspection PyBroadException
        try:
            browser.find_element_by_xpath("//*[@class='my_dashboard']//*[@class='dashboard-title']")
            class_name = "index-menu"
            setVisible(browser, class_name)
            browser.find_element_by_xpath("//*[@class='index-menu']/a[@class='close']").click()
            page_wait(5)
        except Exception:
            pass
        return func(*args, **kwargs)
    return wrapper
