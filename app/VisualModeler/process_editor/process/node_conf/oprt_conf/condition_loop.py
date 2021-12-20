# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/11/9 下午4:54

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from common.page.func.process_var import choose_var, choose_inner_var
from common.page.func.alert_box import BeAlertBox
from common.page.func.input import set_textarea, set_text_enable_var
from app.VisualModeler.process_editor.process.node_conf.oprt_conf.function import FunctionWorker
from common.page.func.page_mask_wait import page_wait
from common.log.logger import log
from common.variable.global_variable import *


def condition(array, iframe_xpath_list=None, basic_cal=False):
    """
    # iframe_xpath_list用于添加条件表达式后，会自动保存，需要重新进入iframe继续操作
    [
        ["变量", "时间"],
        ["不等于", ""],
        ["空值", ""],
        ["与", ""],
        ["变量", "地点"],
        ["包含", ""],
        ["自定义值", "abc ddd"]
    ]

    [
        ["变量", {
            "变量名称": "时间变量",
            "时间格式": "yyyyMMddHHmmss",
            "间隔": "-1",
            "单位": "天",
            "语言": "中文"
        }],
        ["包含", ""],
        ["自定义值", "1115"]
    ]
    """
    browser = get_global_var("browser")
    # 切换到条件表达式配置页面iframe， 基础运算/过滤运算/动作的表达式在当前页面，不需要再跳转iframe
    if not basic_cal:
        browser.switch_to.frame(
            browser.find_element_by_xpath("//iframe[contains(@src,'controlCfgLogic.html')]"))
    # 等待页面加载
    page_wait()
    wait = WebDriverWait(browser, 30)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//*[text()='标签元素']")))

    for ele_tag, ele_value in array:
        # 将标签元素拖入表达式中
        element = browser.find_element_by_xpath("//*[text()='{0}']".format(ele_tag))
        expression_panel = browser.find_element_by_xpath("//*[@id='opera_sortable_0']")
        action = ActionChains(browser)
        action.drag_and_drop(element, expression_panel).perform()
        log.info("表达式加入 {0}".format(ele_tag))

        # 给标签设置值
        if ele_tag == "变量":
            var_name_tips = browser.find_elements_by_xpath("//*[contains(@id,'tip_pt_var')]")
            for vnt in var_name_tips:
                if vnt.get_attribute("title") == "":
                    vnt_id = vnt.get_attribute("id")[4:]
                    browser.find_element_by_xpath(
                        "//*[contains(@onclick,'chooseFunc') and contains(@onclick,'{0}')]".format(vnt_id)).click()
                    sleep(1)
                    break
            # 选择变量，自定义变量或系统内置变量
            try:
                # 如果包含属性"变量名称"，表示内置变量
                ele_value.get("变量名称")
                # 内置变量
                choose_inner_var(var_name=ele_value.get("变量名称"), time_format=ele_value.get("时间格式"),
                                 time_interval=ele_value.get("间隔"), time_unit=ele_value.get("单位"),
                                 language=ele_value.get("语言"))
            except AttributeError:
                choose_var(var_name=ele_value)

        elif ele_tag == "自定义值":
            text_tips = browser.find_elements_by_xpath("//*[contains(@id,'tip_pt_constant')]")
            for tt in text_tips:
                if tt.get_attribute("title") == "":
                    tt_id = tt.get_attribute("id")[4:]
                    browser.find_element_by_xpath(
                        "//*[contains(@onclick,'showText') and contains(@onclick,'{0}')]".format(tt_id)).click()
                    sleep(1)
                    break
            # 切换到输入自定义值iframe
            browser.switch_to.frame(
                browser.find_element_by_xpath("//iframe[contains(@src,'showCustom.html?')]"))
            sleep(1)
            text_area = browser.find_element_by_xpath("//*[@id='custom_content']")
            set_textarea(textarea=text_area, msg=ele_value)
            sleep(1)
            # 保存自定义值
            browser.find_element_by_xpath("//*[@onclick='save_custom();']//*[text()='保存']").click()
            # 返回到表达式iframe
            browser.switch_to.parent_frame()

        elif ele_tag == "变量索引":
            browser.find_element_by_xpath(
                "//*[contains(@id,'pt_index')]/following-sibling::span//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(ele_value)
            sleep(1)

        elif ele_tag == "函数":
            func_name_tips = browser.find_elements_by_xpath("//*[contains(@id,'tip_pt_func')]")
            for fnt in func_name_tips:
                if fnt.get_attribute("text") is None:
                    fnt_id = fnt.get_attribute("id")[4:]
                    browser.find_element_by_xpath(
                        "//*[contains(@onclick,'chooseFunc') and contains(@onclick,'{0}')]".format(fnt_id)).click()
                    sleep(1)
                    break
            # 选择函数
            func = FunctionWorker()
            func.run(var_name=ele_value.get("输入变量"), var_index=ele_value.get("数组索引"),
                     func_list=ele_value.get("函数处理列表"))

        elif ele_tag == "休眠":
            # input_xpath = "//*[@title='sleep']/following-sibling::div//*[@class='textbox-value' and @value='']/preceding-sibling::input"
            input_xpath = "//*[@title='sleep']/following-sibling::div//*[@class='textbox-value']/preceding-sibling::input"
            form_selector = "//*[@id='oprt_form']"
            set_text_enable_var(input_xpath=input_xpath, form_selector=form_selector, msg=ele_value)

        elif ele_tag == "置空":
            var_name_tips = browser.find_elements_by_xpath("//*[contains(@id,'tip_pt_var')]")
            for vnt in var_name_tips:
                log.info(vnt.get_attribute("text"))
                if vnt.get_attribute("text") is None:
                    vnt_id = vnt.get_attribute("id")[4:]
                    browser.find_element_by_xpath(
                        "//*[contains(@onclick,'chooseFunc') and contains(@onclick,'{0}')]".format(vnt_id)).click()
                    sleep(1)
                    break
            # 选择变量
            choose_var(var_name=ele_value)

        elif ele_tag == "总计(sum)":
            browser.find_element_by_xpath(
                "//*[@title='sum']/following-sibling::div//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(ele_value)

        elif ele_tag == "计数(count)":
            browser.find_element_by_xpath(
                "//*[@title='count']/following-sibling::div//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(ele_value)

        elif ele_tag == "最大值(max)":
            browser.find_element_by_xpath(
                "//*[@title='max']/following-sibling::div//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(ele_value)

        elif ele_tag == "最小值(min)":
            browser.find_element_by_xpath(
                "//*[@title='min']/following-sibling::div//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(ele_value)

        elif ele_tag == "平均值(avg)":
            browser.find_element_by_xpath(
                "//*[@title='avg']/following-sibling::div//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(ele_value)

        elif ele_tag == "分组连接":
            col, joiner = ele_value.split(",")
            # 第几列
            browser.find_element_by_xpath(
                "//*[@title='listagg']/following-sibling::div/span[1]//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(col)
            # 连接符
            browser.find_element_by_xpath(
                "//*[@title='listagg']/following-sibling::div/span[2]//*[@class='textbox-value' and "
                "@value='']/preceding-sibling::input").send_keys(joiner)

    log.info("表达式设置完成")
    sleep(1)

    if not basic_cal:
        # 保存表达式
        browser.find_element_by_xpath("//*[@onclick='saveExpr();']//*[text()='保存']").click()
        sleep(1)

        if not iframe_xpath_list:
            # 默认返回上层iframe，适用于在if里配置条件
            browser.switch_to.parent_frame()
        else:
            alert = BeAlertBox(back_iframe="default")
            msg = alert.get_msg()
            if alert.title_contains("成功"):
                log.info("保存条件成功")
            else:
                log.warn("保存条件失败，失败提示: {0}".format(msg))
            set_global_var("ResultMsg", msg, False)

            for frame_xpath in iframe_xpath_list:
                frame = browser.find_element_by_xpath(frame_xpath)
                browser.switch_to.frame(frame)
    else:
        # 基础运算不需要保存表达式，通过保存运算时保存
        sleep(1)


def var_loop(mode, var_name, loop_var_name, value_type, var_type="指令输出变量"):
    """
    :param mode: 模式
    :param var_type: 变量类型
    :param var_name: 变量选择
    :param loop_var_name: 循环行变量名称
    :param value_type: 赋值方式

    # 按变量列表循环
    """
    browser = get_global_var("browser")
    # 选择模式
    if mode:
        if mode == "自定义模式":
            browser.find_element_by_xpath("//*[@id='listBtn_mode1']").click()
        else:
            browser.find_element_by_xpath("//*[@id='listBtn_mode2']").click()
            # 选择变量类型,目前固定为指令输出变量
            if var_type:
                browser.find_element_by_xpath("//*[@name='vartype']/preceding-sibling::input").click()
                browser.find_element_by_xpath("//*[contains(@id,'vartype') and text()='{0}']".format(var_type)).click()
        log.info("设置模式: {0}".format(mode))
        sleep(1)

    # 选择变量
    if var_name:
        elements = browser.find_elements_by_xpath("//*[contains(text(),'变量选择')]/..//following-sibling::div//a")
        # 点击选择变量
        for e in elements:
            if e.is_displayed():
                e.click()
                break
        choose_var(var_name=var_name)
        log.info("设置变量: {0}".format(var_name))
        sleep(1)

    # 循环行变量名称
    if loop_var_name:
        elements = browser.find_elements_by_xpath("//*[@name='outVarName']/preceding-sibling::input")
        for e in elements:
            if e.is_displayed():
                e.clear()
                e.send_keys(loop_var_name)
                log.info("设置循环行变量名称: {0}".format(loop_var_name))
                sleep(1)
                break

    # 赋值方式
    if value_type:
        elements = browser.find_elements_by_xpath("//*[@name='valueType']/preceding-sibling::input")
        for e1 in elements:
            if e1.is_displayed():
                e1.click()
                elements = browser.find_elements_by_xpath(
                    "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type))
                for e2 in elements:
                    if e2.is_displayed():
                        e2.click()
                        log.info("设置赋值方式: {0}".format(value_type))
                        sleep(1)
                        break


def times_loop(loop_times, loop_var_name, value_type, next_condition, end_condition, common_tree, iframe_xpath_list):
    """
    :param loop_times: 循环次数
    :param loop_var_name: 循环变量名称
    :param value_type: 赋值方式
    :param next_condition: 跳至下一轮条件，数组
    :param end_condition: 结束循环条件，数组
    :param common_tree: bool
    :param iframe_xpath_list: 数组

    # 按次数循环
    """
    browser = get_global_var("browser")
    # 循环次数
    if loop_times:
        input_xpath = "//*[@id='cir_times']/following-sibling::span/input[1]"
        form_selector = "//"
        set_text_enable_var(input_xpath=input_xpath, form_selector=form_selector, msg=loop_times)
        log.info("设置循环次数: {0}".format(loop_times))
        sleep(1)

    # 循环变量名称
    if loop_var_name:
        browser.find_element_by_xpath(
            "//*[@name='outVarName_2']/preceding-sibling::input").send_keys(loop_var_name)
        log.info("设置循环变量名称: {0}".format(loop_var_name))
        sleep(1)

    # 赋值方式
    if value_type:
        elements = browser.find_elements_by_xpath("//*[@name='valueType']/preceding-sibling::input")
        for e1 in elements:
            if e1.is_displayed():
                e1.click()
                elements = browser.find_elements_by_xpath(
                    "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type))
                for e2 in elements:
                    if e2.is_displayed():
                        e2.click()
                        log.info("设置赋值方式: {0}".format(value_type))
                        sleep(1)
                        break

    # 跳至下一轮条件
    if next_condition:
        if common_tree:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('times_nextCondition');\"]//*[text()='修改']").click()
        else:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('times_nextCondition','1');\"]//*[text()='修改']").click()
        condition(array=next_condition, iframe_xpath_list=iframe_xpath_list)
        sleep(1)

    # 结束循环条件
    if end_condition:
        if common_tree:
            elements = browser.find_elements_by_xpath("//*[@onclick=\"showAdd('times_endCondition');\"]//*[text()='修改']")
            for element in elements:
                if element.is_displayed():
                    element.click()
                    break
        else:
            elements = browser.find_elements_by_xpath("//*[@onclick=\"showAdd('times_endCondition','1');\"]//*[text()='修改']")
            for element in elements:
                if element.is_displayed():
                    element.click()
                    break
        condition(array=end_condition, iframe_xpath_list=iframe_xpath_list)
        sleep(1)


def condition_loop(cir_condition, next_condition, end_condition, common_tree, iframe_xpath_list):
    """
    :param cir_condition: 跳至下一轮条件，数组
    :param next_condition: 结束循环条件，数组
    :param end_condition: 结束循环条件
    :param common_tree: bool
    :param iframe_xpath_list: 数组

    # 按条件循环
    """
    browser = get_global_var("browser")
    # 循环条件
    if cir_condition:
        if common_tree:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('circleCondition');\"]//*[text()='修改']").click()
        else:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('circleCondition','1');\"]//*[text()='修改']").click()
        condition(array=cir_condition, iframe_xpath_list=iframe_xpath_list)
        sleep(1)

    # 跳至下一轮条件
    if next_condition:
        if common_tree:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('nextCondition');\"]//*[text()='修改']").click()
        else:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('nextCondition','1');\"]//*[text()='修改']").click()
        condition(array=next_condition, iframe_xpath_list=iframe_xpath_list)
        sleep(1)

    # 结束循环条件
    if end_condition:
        if common_tree:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('endCondition');\"]//*[text()='修改']").click()
        else:
            browser.find_element_by_xpath("//*[@onclick=\"showAdd('endCondition','1');\"]//*[text()='修改']").click()
        condition(array=end_condition, iframe_xpath_list=iframe_xpath_list)
        sleep(1)


def step_loop(step_name, cir_var_name, value_type):
    """
    :param step_name: 步骤选择
    :param cir_var_name: 循环变量名称
    :param value_type: 赋值方式

    # 按步骤循环
    """
    browser = get_global_var("browser")
    # 步骤选择
    if step_name:
        browser.find_element_by_xpath("//*[@id='chooseStepName']/following-sibling::span//a").click()
        # 切换到选择步骤iframe
        browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'stepList.html?')]"))
        # 等待页面加载
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@name='stepName']/preceding-sibling::input")))
        # 查询步骤名称
        browser.find_element_by_xpath("//*[@name='stepName']/preceding-sibling::input").send_keys(step_name)
        browser.find_element_by_xpath("//*[@data-dg-query='#query_steps_tab']//*[text()='查询']").click()
        page_wait()
        browser.find_element_by_xpath(
            "//*[contains(@id,'query_steps')]//*[text()='{0}']".format(step_name)).click()
        # 点击保存
        browser.find_element_by_xpath("//*[@onclick='saveChooseStepCondition();']//*[text()='保存']").click()
        log.info("选择步骤: {0}".format(step_name))
        sleep(1)
        # 切换到步骤循环iframe
        browser.switch_to.parent_frame()

    # 循环变量名称
    if cir_var_name:
        browser.find_element_by_xpath("//*[@name='circleVarName_Step']/preceding-sibling::input").send_keys(cir_var_name)
        log.info("设置循环变量名称: {0}".format(cir_var_name))
        sleep(1)

    # 赋值方式
    if value_type:
        elements = browser.find_elements_by_xpath("//*[@name='valueType']/preceding-sibling::input")
        for e1 in elements:
            if e1.is_displayed():
                e1.click()
                elements = browser.find_elements_by_xpath(
                    "//*[contains(@id,'valuetype') and text()='{0}']".format(value_type))
                for e2 in elements:
                    if e2.is_displayed():
                        e2.click()
                        log.info("设置赋值方式: {0}".format(value_type))
                        sleep(1)
                        break
