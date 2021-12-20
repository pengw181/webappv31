# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午9:17

from datetime import datetime
from common.log.logger import log
from common.variable.global_variable import *


def set_date(date_s, date_format="%Y-%m-%d"):
    """
    :param date_s: 字符串，2020-11-15
    :param date_format: 时间格式%Y-%m-%d %H:%M:%S
    :return:
    """
    browser = get_global_var("browser")
    # 解析date_s
    # date_s = "2019-02-27 17:50:30"
    time = datetime.strptime(date_s, date_format)

    year = time.date().year
    month = time.date().month
    day = time.date().day

    hour = time.hour
    minute = time.minute
    second = time.second

    # 点开年月
    m_y_ele = browser.find_elements_by_xpath("//*[@class='calendar-title']/span")
    for y in m_y_ele:
        if y.is_displayed():
            y.click()
            break

    # 设置年
    year_ele = browser.find_elements_by_xpath("//*[@class='calendar-menu-year']")
    for y in year_ele:
        if y.is_displayed():
            y.clear()
            y.send_keys(year)
            log.info("输入年: {0}".format(year))
            break

    # 设置月
    month_ele = browser.find_elements_by_xpath(
        "//*[contains(@class,'calendar-menu-month') and @abbr='{0}']".format(month))
    for m in month_ele:
        if m.is_displayed():
            m.click()
            log.info("点击月: {0}".format(month))
            break

    # 设置日
    day_ele = browser.find_elements_by_xpath(
        "//*[contains(@class,'calendar-day') and @abbr='{0},{1},{2}']".format(year, month, day))
    for d in day_ele:
        if d.is_displayed():
            d.click()
            log.info("点击日: {0}".format(day))
            break

    # 设置时分秒
    hms_ele = browser.find_elements_by_xpath(
        "//*[contains(@class,'timespinner-f')]/following-sibling::span//input[1]")
    for hms in hms_ele:
        if hms.is_displayed():
            hms.clear()
            _format = browser.find_elements_by_xpath(
                "//*[contains(@class,'timespinner-f')]/following-sibling::span//input[2]")
            for _ in _format:
                if _.is_displayed():
                    _hms = _.get_attribute("value")
                    h_len = _hms.split(":")
                    if len(h_len) == 2:
                        # 时:分
                        enter_time = "{0}:{1}".format(hour, minute)
                    else:
                        # 时:分:秒
                        enter_time = "{0}:{1}:{2}".format(hour, minute, second)
                    hms.send_keys(enter_time)
                    log.info("设置时分秒: {0}".format(enter_time))

                    # 点击确定
                    browser.find_element_by_xpath("//*[@class='datebox-button']//*[text()='确定']").click()
                    break
            break
