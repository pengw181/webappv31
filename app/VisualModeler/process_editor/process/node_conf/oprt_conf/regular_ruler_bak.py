# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/21 上午10:20

from time import sleep
from common.page.func.regexp import regular_cube
from common.page.func.input import set_textarea
from common.log.logger import log
from common.variable.global_variable import *


def regular_ruler(begin_line, enable_magic, cols, split_type, split, advance, regular, sample_data):
    """
    :param begin_line: 解析开始行，必填
    :param enable_magic: 是否通过正则匹配数据列, bool
    :param cols: 列总数，是否通过正则匹配数据列为False时必填
    :param split_type: 拆分方式，文本/正则
    :param split: 拆分符，非必填
    :param advance: 高级配置，字典，非必填
    :param regular: 正则配置，是否通过正则匹配数据列为True或拆分方式为正则时必填，字典
    :param sample_data: 样例数据，textarea，文本，必填
    """
    browser = get_global_var("browser")
    # 解析开始行
    if begin_line:
        browser.find_element_by_xpath(
            "//*[contains(text(),'解析开始行')]/..//following-sibling::span//input[1]").send_keys(begin_line)
        log.info("设置解析开始行: {0}".format(begin_line))
        sleep(1)

    # 是否通过正则匹配数据列
    add_flag = False
    js = 'return $(".isMagic")[0].checked;'
    status = browser.execute_script(js)
    log.info("【通过正则匹配数据列】勾选状态: {0}".format(status))
    # 聚焦元素
    magic_click = browser.find_element_by_xpath("//*[@class='isMagic']")
    browser.execute_script("arguments[0].scrollIntoView(true);", magic_click)
    if enable_magic:
        if not status:
            magic_click.click()
            sleep(1)
        log.info("勾选【通过正则匹配数据列】")

        # 通过正则匹配数据列
        confirm_selector = "//*[@id='regexpregex_advCfg']"
        add_flag = regular_cube(confirm_selector=confirm_selector, set_type=regular.get("设置方式"),
                                regular_name=regular.get("正则模版名称"), advance_mode=regular.get("高级模式"),
                                regular=regular.get("标签配置"), expression=regular.get("表达式"))

    else:
        if status:
            magic_click.click()
            log.info("取消勾选【通过正则匹配数据列】")
        else:
            log.info("【通过正则匹配数据列】标识为否，不开启")

        # 列总数
        if cols:
            browser.find_element_by_xpath(
                "//*[contains(text(),'列总数')]/..//following-sibling::span//input[1]").send_keys(cols)
            log.info("设置列总数: {0}".format(cols))
            sleep(1)

        # 拆分方式
        if split_type == "文本":
            # 通过文本拆分
            browser.find_element_by_xpath("//*[@class='textSplit']").click()
            sleep(1)

            # 拆分符
            if split:
                browser.find_element_by_xpath(
                    "//*[contains(text(),'列分隔符')]/..//following-sibling::span//input[1]").send_keys(split)
                log.info("设置拆分符: {0}".format(split))
                sleep(1)
                add_flag = False
        else:
            # 通过正则拆分
            browser.find_element_by_xpath("//*[@class='regexpSplit']").click()
            sleep(1)
            confirm_selector = "//*[@id='regexpregex_advCfg']"
            add_flag = regular_cube(confirm_selector=confirm_selector, set_type=regular.get("设置方式"),
                                    regular_name=regular.get("正则模版名称"), advance_mode=regular.get("高级模式"),
                                    regular=regular.get("标签配置"), expression=regular.get("表达式"))

    if add_flag:
        # 切换到节点iframe
        browser.switch_to.frame(browser.find_element_by_xpath(get_global_var("NodeIframe")))
        # 切换到操作配置iframe
        browser.switch_to.frame(browser.find_element_by_xpath(get_global_var("OptIframe")))
        # 切换到运算配置iframe
        browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'operateVar.html')]"))
        # 切换到正则运算iframe
        browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'operateCfgRegular.html')]"))

    # 高级配置
    if advance:
        regular_advance()

    # 输入样例数据
    if sample_data:
        textarea = browser.find_element_by_xpath(
            "//*[@id='tableExampleDataregex_advCfg']/following-sibling::span/textarea")
        browser.execute_script("arguments[0].scrollIntoView(true);", textarea)
        set_textarea(textarea=textarea, msg=sample_data)
        sleep(1)

    # 格式化结果
    format_ele = browser.find_element_by_xpath("//*[text()='效果预览']/following-sibling::div[2]/a")
    browser.execute_script("arguments[0].scrollIntoView(true);", format_ele)
    format_ele.click()
    sleep(1)


def regular_advance():
    pass


def regular_fetch(default_config, fetch_config):
    """
    :param default_config: 默认值配置，字典，非必填
    :param fetch_config: 取值规则，字典，非必填

    {
        "默认值配置": {
            "默认值": "0",
            "行": "3",
            "列": "4"
        },
        "取值规则": {
            "行": "3",
            "列": "4"
        }
    }
    """
    browser = get_global_var("browser")
    fetch_ele = browser.find_element_by_xpath("//*[text()='取值配置']")
    browser.execute_script("arguments[0].scrollIntoView(true);", fetch_ele)
    log.info("开始取值配置")
    # 默认值配置
    if default_config:
        # 默认值
        if default_config.__contains__("默认值"):
            default_var = default_config.get("默认值")
            browser.find_element_by_xpath(
                "//*[@name='outDefaultVal']/preceding-sibling::input").clear()
            browser.find_element_by_xpath(
                "//*[@name='outDefaultVal']/preceding-sibling::input").send_keys(default_var)
            log.info("设置默认值: {0}".format(default_var))
        # 行
        if default_config.__contains__("行"):
            default_row = default_config.get("行")
            browser.find_element_by_xpath(
                "//*[@name='outRowDefault']/preceding-sibling::input").clear()
            browser.find_element_by_xpath(
                "//*[@name='outRowDefault']/preceding-sibling::input").send_keys(default_row)
            log.info("设置行: {0}".format(default_row))
        # 列
        if default_config.__contains__("列"):
            default_col = default_config.get("列")
            browser.find_element_by_xpath(
                "//*[@name='outColDefault']/preceding-sibling::input").clear()
            browser.find_element_by_xpath(
                "//*[@name='outColDefault']/preceding-sibling::input").send_keys(default_col)
            log.info("设置列: {0}".format(default_col))

    # 取值规则
    if fetch_config:
        # 行
        if fetch_config.__contains__("行"):
            fetch_row = fetch_config.get("行")
            browser.find_element_by_xpath(
                "//*[@name='resultRow']/preceding-sibling::input").clear()
            browser.find_element_by_xpath(
                "//*[@name='resultRow']/preceding-sibling::input").send_keys(fetch_row)
            log.info("设置行: {0}".format(fetch_row))
        # 列
        if fetch_config.__contains__("列"):
            fetch_col = fetch_config.get("列")
            browser.find_element_by_xpath(
                "//*[@name='resultCol']/preceding-sibling::input").clear()
            browser.find_element_by_xpath(
                "//*[@name='resultCol']/preceding-sibling::input").send_keys(fetch_col)
            log.info("设置列: {0}".format(fetch_col))
    sleep(1)
