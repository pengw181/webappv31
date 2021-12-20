# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/7/20 下午4:18

from common.page.func.level import cmd_node_choose_level, cmd_node_choose_member
from app.VisualModeler.process_editor.process.node_conf.business_conf.cmd_param import cmd_node_param_set
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.page.func.alert_box import BeAlertBox
from common.page.func.process_var import choose_var
from common.page.func.page_mask_wait import page_wait
from common.log.logger import log
from common.variable.global_variable import *


def cmd_business(node_name, mem_filter, ne_filter, choose_type, scene, config, advance_set):
    """
    :param node_name: 节点名称
    :param mem_filter: 成员选择
    :param ne_filter: 网元选择
    :param choose_type: 选择方式
    :param scene: 场景标识
    :param config: 配置，字典
    :param advance_set: 高级配置，字典

    # 按网元添加
    {
        "节点名称": "自动化指令节点名称",
        "成员选择": "",
        "网元选择": "",
        "选择方式": "网元",
        "场景标识": "无",
        "配置": {
            "层级": "4G,4G_MME"，
            "层级成员": ["GKF_MME_华为_SE2900_02", "GKF_MME_华为_SE2900_03"],
            "网元类型": "MME",
            "厂家": "华为",
            "设备型号": "SE2900"
            "网元": ["GKF_MME_华为_SE2900_02", "GKF_MME_华为_SE2900_03"],
            "指令": {
                "pw指令2_df": {
                    "解析模版": "pw解析模版解析df",
                    "参数设置": ""
                },
                "pw测试指令传参最大值": {
                    "解析模版": "",
                    "参数设置": {
                        "模式": "独立模式",
                        "参数": "参数1,参数2"
                    }
                },
                "pw二维表传参指令": {
                    "解析模版": "pw解析ping返回4参数",
                    "参数设置": {
                        "模式": "二维表模式",
                        "参数": {
                            "选择变量": "参数1",
                            "对象设置": "[1]",
                            "参数1": "[2],a",
                            "参数2": "[3],b"
                        }
                    }
                }
            }
        },
        "高级配置": {
            "flag": "是",
            "超时时间": "600",
            "超时重试次数": ""
        }
    }

    # 按网元类型添加
    {
        "节点名称": "自动化指令节点名称",
        "成员选择": "",
        "网元选择": "",
        "选择方式": "网元类型",
        "场景标识": "无",
        "配置": {
            "层级": "4G,4G_MME",
            "成员名称": "MME",
            "状态": "带业务",
            "层级成员个数": "是",
            "网元类型": "MME",
            "厂家": "华为",
            "设备型号": "SE2900",
            "网元个数": "是",
            "指令": {
                "pw指令2_df": {
                    "解析模版": "pw解析模版解析df",
                    "参数设置": ""
                },
                "pw测试指令传参最大值": {
                    "解析模版": "",
                    "参数设置": {
                        "模式": "独立模式",
                        "参数": "参数1,参数2"
                    }
                },
                "pw二维表传参指令": {
                    "解析模版": "pw解析ping返回4参数",
                    "参数设置": {
                        "模式": "二维表模式",
                        "参数": {
                            "选择变量": "参数1",
                            "对象设置": "[1]",
                            "参数1": "[2],a",
                            "参数2": "[3],b"
                        }
                    }
                }
            }
        },
        "高级配置": {
            "flag": "是",
            "超时时间": "600",
            "超时重试次数": "2"
        }
    }
    """
    browser = get_global_var("browser")
    page_wait()
    # 设置节点名称
    if node_name:
        browser.find_element_by_xpath("//*[@name='node_name']/preceding-sibling::input[1]").clear()
        browser.find_element_by_xpath("//*[@name='node_name']/preceding-sibling::input[1]").send_keys(node_name)
        log.info("设置节点名称: {0}".format(node_name))
        sleep(1)

    # 成员选择
    if mem_filter:
        browser.find_element_by_xpath("//*[@id='dataH_filterMbrVarName']/following-sibling::span//a").click()
        choose_var(var_name=mem_filter)
        log.info("成员选择,变量: {0}".format(mem_filter))
        sleep(1)

    # 网元选择
    if ne_filter:
        browser.find_element_by_xpath("//*[@id='dataH_filterVarName']/following-sibling::span//a").click()
        choose_var(var_name=ne_filter)
        log.info("网元选择,变量: {0}".format(ne_filter))
        sleep(1)

    # 设置选方式
    if choose_type:
        browser.find_element_by_xpath("//*[@name='selMode']/preceding-sibling::input[1]").click()
        browser.find_element_by_xpath("//*[contains(@id,'selMode') and text()='{0}']".format(choose_type)).click()
        log.info("选择方式: {0}".format(choose_type))
        sleep(1)

    # 场景标识
    if scene:
        browser.find_element_by_xpath("//*[@name='scene_flag']/preceding-sibling::input[1]").click()
        browser.find_element_by_xpath("//*[contains(@id,'scene_flag') and text()='{0}']".format(scene)).click()
        log.info("设置场景标识: {0}".format(scene))
        sleep(1)

    # 配置，配置完成后返回到业务配置iframe
    if config:
        browser.find_element_by_xpath("//*[@id='add_retrieve']//*[text()='添加']").click()
        sleep(2)

        # 开始进行配置，分网元和网元类型两种方式
        if choose_type == "网元":
            add_by_ne(level=config.get("层级"), level_member=config.get("层级成员"), ne_type=config.get("网元类型"),
                      vendor=config.get("厂家"), model=config.get("设备型号"), ne_list=config.get("网元"),
                      cmd_set=config.get("指令"))
        else:
            if config.get("层级成员个数") == "是":
                show_member = True
            else:
                show_member = False

            if config.get("网元个数") == "是":
                show_ne = True
            else:
                show_ne = False

            add_by_ne_type(level=config.get("层级"), member_name=config.get("成员名称"), status=config.get("状态"),
                           show_member=show_member, ne_type=config.get("网元类型"), vendor=config.get("厂家"),
                           model=config.get("设备型号"), show_ne=show_ne, cmd_set=config.get("指令"))
        page_wait()
    else:
        log.info("未加入节点配置")

    # 设置高级配置
    if advance_set:
        if advance_set.get("flag") == "是":
            timeout = advance_set.get("超时时间")
            retry_times = advance_set.get("超时重试次数")
            try:
                enable_click = browser.find_element_by_xpath(
                    "//*[@onclick='show_advanced_mode($(this))']//*[text()='开启高级模式']")
                enable_click.click()
                log.info("开启【高级配置】")
            except NoSuchElementException:
                pass

            browser.find_element_by_xpath("//*[@name='cmd_timeout']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='cmd_timeout']/preceding-sibling::input").send_keys(timeout)
            browser.find_element_by_xpath("//*[@name='try_time']/preceding-sibling::input").clear()
            browser.find_element_by_xpath("//*[@name='try_time']/preceding-sibling::input").send_keys(retry_times)
            log.info("设置高级模式")
            sleep(1)
        else:
            try:
                browser.find_element_by_xpath("//*[@onclick='show_advanced_mode($(this))']//*[text()='开启高级模式']")
            except NoSuchElementException:
                disable_click = browser.find_element_by_xpath(
                    "//*[@onclick='show_advanced_mode($(this))']//*[text()='关闭高级模式']")
                disable_click.click()
                log.info("关闭【高级配置】")

    # 获取节点名称
    node_name = browser.find_element_by_xpath(
        "//*[@name='node_name']/preceding-sibling::input[1]").get_attribute("value")

    # 保存节点
    browser.find_element_by_xpath("//*[@id='save_retrieve']//*[text()='保存']").click()
    log.info("保存节点")

    alert = BeAlertBox(back_iframe="default")
    msg = alert.get_msg()
    if alert.title_contains("操作成功"):
        log.info("保存节点成功")
    else:
        log.warn("保存节点失败，失败提示: {0}".format(msg))
    set_global_var("ResultMsg", msg, False)

    # 刷新页面，返回画流程图
    browser.refresh()
    return node_name


def add_by_ne_type(level, member_name, status, show_member, ne_type, vendor, model, show_ne, cmd_set):
    """
    :param level: 层级，父子层级以逗号分隔，必填
    :param member_name: 成员名称，关键字，非必填
    :param status: 状态，非必填
    :param show_member: 层级成员个数，bool，非必填
    :param ne_type: 网元类型，必填
    :param vendor: 厂家，必填
    :param model: 设备型号，必填
    :param show_ne: 网元个数，bool，非必填
    :param cmd_set: 指令，字典，必填

    # 按网元类型添加
    {
        "层级": "核心网分类,核心网分类_MME"，
        "成员名称": "GKF",
        "状态": "带业务",
        "层级成员个数": "是",
        "网元类型": "MME",
        "厂家": "华为",
        "设备型号": "SE2900"
        "网元个数": "是",
        "指令": {
            "pw指令2_df": {
                "解析模版": "pw解析模版解析df",
                "参数设置": ""
            },
            "pw测试指令传参最大值": {
                "解析模版": "",
                "参数设置": {
                    "模式": "独立模式",
                    "参数": "参数1,参数2"
                }
            },
            "pw二维表传参指令": {
                "解析模版": "pw解析ping返回4参数",
                "参数设置": {
                    "模式": "二维表模式",
                    "参数": {
                        "选择变量": "参数1",
                        "对象设置": "[1]",
                        "参数1": "[2],a",
                        "参数2": "[3],b"
                    }
                }
            }
        }
    }
    """
    browser = get_global_var("browser")
    # 进入网元类型配置iframe
    browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'./cmdNodeType.html?')]"))
    # 等待页面加载
    wait = WebDriverWait(browser, 30)
    wait.until(ec.element_to_be_clickable((
        By.XPATH, "//*[@id='level_id_path']/following-sibling::span//*[contains(@id,'_textbox_input')]")))
    page_wait()

    # 层级
    if level:
        browser.find_element_by_xpath("//*[@id='level_id_path']/following-sibling::span//a").click()
        cmd_node_choose_level(level=level)
        log.info("选择层级: {0}".format(level))
        sleep(1)

    # 成员名称
    if member_name:
        browser.find_element_by_xpath("//*[@name='netunit_name']/preceding-sibling::input").clear()
        browser.find_element_by_xpath("//*[@name='netunit_name']/preceding-sibling::input").send_keys(member_name)
        log.info("设置成员名称: {0}".format(member_name))
        sleep(1)

    # 状态
    if status:
        browser.find_element_by_xpath("//*[@name='state_id']/preceding-sibling::input").click()
        browser.find_element_by_xpath("//*[contains(@id,'state_id') and text()='{0}']".format(status)).click()
        log.info("设置状态: {0}".format(status))
        sleep(2)

    # 查看层级成员个数
    if show_member:
        browser.find_element_by_xpath("//*[@onclick='getLevelMemberDetail()']").click()
        # 切换到弹出列表iframe
        browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'levelMemberList.html?')]"))
        # 等待弹出框加载完成
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@field='netunit_name']//*[text()='网元名称']")))
        # 查看停留3秒后，返回上层iframe继续配置,并关闭窗口
        log.info("查看层级成员个数详情")
        sleep(3)
        browser.switch_to.parent_frame()
        browser.find_element_by_xpath(
            "//*[text()='层级成员列表']/following-sibling::div/a[contains(@class,'close')]").click()

    # 网元类型
    if ne_type:
        browser.find_element_by_xpath("//*[@name='child_level_id']/preceding-sibling::input").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//*[contains(@id, 'child_level_id') and text()='{0}']".format(ne_type))))
        browser.find_element_by_xpath("//*[contains(@id,'child_level_id') and text()='{0}']".format(ne_type)).click()
        log.info("选择网类型: {0}".format(ne_type))
        sleep(1)

    # 选择厂家
    if vendor:
        browser.find_element_by_xpath("//*[@name='vendor_id']/preceding-sibling::input").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//*[contains(@id, 'vendor_id_') and text()='{0}']".format(vendor))))
        browser.find_element_by_xpath("//*[contains(@id, 'vendor_id_') and text()='{0}']".format(vendor)).click()
        log.info("选择厂家: {0}".format(vendor))
        sleep(1)

    # 选择设备型号
    if model:
        browser.find_element_by_xpath("//*[@name='netunit_model_id']/preceding-sibling::input").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//*[contains(@id, 'netunit_model_id') and text()='{0}']".format(model))))
        browser.find_element_by_xpath("//*[contains(@id, 'netunit_model_id') and text()='{0}']".format(model)).click()
        log.info("选择设备型号: {0}".format(model))
        sleep(1)

    # 查看网元个数
    if show_ne:
        browser.find_element_by_xpath("//*[@onclick='getNetunitDetail()']").click()
        # 切换到弹出列表iframe
        browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@src,'levelMemberList.html?')]"))
        # 等待弹出框加载完成
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@field='netunit_name']//*[text()='网元名称']")))
        # 查看停留3秒后，返回上层iframe继续配置,并关闭窗口
        log.info("查看网元个数详情")
        sleep(3)
        browser.switch_to.parent_frame()
        browser.find_element_by_xpath(
            "//*[text()='网元列表']/following-sibling::div/a[contains(@class,'close')]").click()

    # 选择指令集
    if cmd_set:
        log.info("开始配置指令集")
        for cmd_name in cmd_set.keys():

            # 勾选指令
            cmd_click = browser.find_element_by_xpath(
                "//*[@field='cmdName']//*[text()='{0}']/../preceding-sibling::td[1]//input".format(cmd_name))
            browser.execute_script("arguments[0].scrollIntoView(true);", cmd_click)
            cmd_click.click()
            log.info("选择指令集: {0}".format(cmd_name))
            cmd_info = cmd_set.get(cmd_name)

            # 选择解析模版
            if cmd_info.__contains__("解析模版"):
                analyzer = cmd_info.get("解析模版")
                if analyzer:
                    log.info("开始选择解析模版")
                    sleep(1)
                    # 点开下拉框
                    browser.find_element_by_xpath(
                        "//*[@field='cmdName']//*[text()='{0}']/../following-sibling::td[1]//span/a".format(
                            cmd_name)).click()
                    try:
                        browser.find_element_by_xpath(
                            "//*[contains(@id,'analyzerID_') and text()='{0}']".format(analyzer)).click()
                        log.info("选择解析模版: {0}".format(analyzer))
                    except NoSuchElementException:
                        log.error("所选解析模版不在列表中，指令集: {0}, 解析模版: {1}".format(cmd_name, analyzer))
                        raise

            # 指令参数设置
            if cmd_info.__contains__("参数设置"):
                param_set = cmd_info.get("参数设置")
                if param_set:
                    log.info("指令参数设置")
                    sleep(1)
                    # 点击参数设置
                    browser.find_element_by_xpath(
                        "//*[@field='cmdName']//*[text()='{0}']/../following-sibling::td[5]//a".format(cmd_name)).click()
                    cmd_node_param_set(param_mode=param_set.get("模式"), params=param_set.get("参数"))
                else:
                    log.info("此指令不需配置参数")
                    continue

    # 保存配置
    browser.find_element_by_xpath("//*[@id='submitBtn']//*[text()='提交']").click()
    log.info("保存配置")

    alert = BeAlertBox(back_iframe="default")
    msg = alert.get_msg()
    if alert.title_contains("保存成功"):
        log.info("保存配置成功")

        # 重新进入iframe
        browser.switch_to.frame(
            browser.find_element_by_xpath(get_global_var("NodeIframe")))
        browser.switch_to.frame(
            browser.find_element_by_xpath("//iframe[@id='busi_cmd_node']"))
    else:
        log.warn("保存配置失败，失败提示: {0}".format(msg))
    set_global_var("ResultMsg", msg, False)


def add_by_ne(level, level_member, ne_type, vendor, model, ne_list, cmd_set):
    """
    :param level: 层级，父子层级之间以逗号分隔，必填
    :param level_member: 层级成员，多个成员以逗号分隔，必填
    :param ne_type: 网元类型，必填
    :param vendor: 厂家，必填
    :param model: 设备型号，必填
    :param ne_list: 网元，数组，必填
    :param cmd_set: 指令，字典，必填

    # 按网元添加
    {
        "层级": "核心网分类,核心网分类_MME"，
        "层级成员": "GKF_MME_华为_SE2900_02,GKF_MME_华为_SE2900_03",
        "网元类型": "MME",
        "厂家": "华为",
        "设备型号": "SE2900"
        "网元": "GKF_MME_华为_SE2900_02,GKF_MME_华为_SE2900_03",
        "指令": {
            "pw指令2_df": {
                "解析模版": "pw解析模版解析df",
                "参数设置": {}
            },
            "pw测试指令传参最大值": {
                "解析模版": "",
                "参数设置": {
                    "模式": "独立模式",
                    "参数": "参数1,参数2"
                }
            },
            "pw二维表传参指令": {
                "解析模版": "pw解析ping返回4参数",
                "参数设置": {
                    "模式": "二维表模式",
                    "参数": {
                        "选择变量": "参数1",
                        "对象设置": "[1]",
                        "参数1": "[2],a",
                        "参数2": "[3],b"
                    }
                }
            }
        }
    }
    """
    browser = get_global_var("browser")
    # 进入网元配置iframe
    wait = WebDriverWait(browser, 30)
    wait.until(ec.frame_to_be_available_and_switch_to_it((
        By.XPATH, "//iframe[contains(@src, './cmdNodeNetunit.html?')]")))
    log.info("开始配置指令网元信息")
    sleep(2)

    # 选择层级
    if level:
        browser.find_element_by_xpath("//*[@id='cmd_table_codtion']/span/span/a").click()
        cmd_node_choose_level(level=level)
        log.info("选择层级: {0}".format(level))
        sleep(1)

    # 选择层级成员
    if level_member:
        browser.find_element_by_xpath("//*[@id='netunit_id']/following-sibling::span[1]/span/a").click()
        cmd_node_choose_member(member_list=level_member)
        browser.find_element_by_xpath("//*[@id='netunit_id']/following-sibling::span[1]/span/a").click()
        log.info("选择层级成员: {0}".format(level_member))
        sleep(1)

    # 选择网元类型
    if ne_type:
        browser.find_element_by_xpath("//*[@id='child_level_id']/following-sibling::span[1]/span/a").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//*[contains(@id, 'child_level_id_') and text()='{0}']".format(ne_type))))
        browser.find_element_by_xpath("//*[contains(@id, 'child_level_id_') and text()='{0}']".format(ne_type)).click()
        log.info("选择网元类型: {0}".format(ne_type))
        sleep(1)

    # 选择厂家
    if vendor:
        browser.find_element_by_xpath("//*[@id='vendor_id']/following-sibling::span[1]/span/a").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//*[contains(@id, 'vendor_id_') and text()='{0}']".format(vendor))))
        browser.find_element_by_xpath("//*[contains(@id, 'vendor_id_') and text()='{0}']".format(vendor)).click()
        log.info("选择厂家: {0}".format(vendor))
        sleep(1)

    # 选择设备型号
    if model:
        browser.find_element_by_xpath("//*[@id='netunit_model_id']/following-sibling::span[1]/span/a").click()
        wait = WebDriverWait(browser, 30)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//*[contains(@id, 'netunit_model_id_') and text()='{0}']".format(model))))
        browser.find_element_by_xpath("//*[contains(@id, 'netunit_model_id_') and text()='{0}']".format(model)).click()
        log.info("选择设备型号: {0}".format(model))

    # 选择网元
    if ne_list:
        need_wait = True
        for ne in ne_list:
            if need_wait:
                # 等待加载出网元和指令
                wait = WebDriverWait(browser, 30)
                wait.until(ec.element_to_be_clickable((
                    By.XPATH, "//*[@field='childNetunitName']//*[text()='{0}']".format(ne))))
                need_wait = False
            try:
                browser.find_element_by_xpath("//*[@field='childNetunitName']//*[text()='{0}']".format(ne)).click()
                log.info("选择网元: {0}".format(ne))
            except NoSuchElementException:
                raise

    # 选择指令集
    if cmd_set:
        for cmd_name in cmd_set:

            # 勾选指令
            cmd_click = browser.find_element_by_xpath(
                "//*[@field='cmdName']//*[text()='{0}']/../preceding-sibling::td[1]//input".format(cmd_name))
            browser.execute_script("arguments[0].scrollIntoView(true);", cmd_click)
            cmd_click.click()
            log.info("选择指令集: {0}".format(cmd_name))
            cmd_info = cmd_set.get(cmd_name)

            # 选择解析模版
            if cmd_info.__contains__("解析模版"):
                analyzer = cmd_info.get("解析模版")
                if analyzer:
                    log.info("开始选择解析模版")
                    sleep(1)
                    # 点开下拉框
                    browser.find_element_by_xpath(
                        "//*[@field='cmdName']//*[text()='{0}']/../following-sibling::td[1]//span/a".format(
                            cmd_name)).click()
                    sleep(1)
                    ana_element = browser.find_elements_by_xpath(
                        "//*[contains(@id,'analyzerID_') and text()='{0}']".format(analyzer))
                    if len(ana_element) > 0:
                        for element in ana_element:
                            if element.is_displayed():
                                element.click()
                                log.info("选择解析模版: {0}".format(cmd_name))
                                break
                    else:
                        raise KeyError("解析模版不存在")

            # 指令参数设置
            if cmd_info.__contains__("参数设置"):
                param_set = cmd_info.get("参数设置")
                if param_set:
                    log.info("指令参数设置")
                    sleep(1)
                    # 点击参数设置
                    browser.find_element_by_xpath(
                        "//*[@field='cmdName']//*[text()='{0}']/../following-sibling::td[5]//a".format(cmd_name)).click()
                    cmd_node_param_set(param_mode=param_set.get("模式"), params=param_set.get("参数"))
                else:
                    log.info("此指令不需配置参数")
                    continue

    # 保存配置
    browser.find_element_by_xpath("//*[@id='submitBtn']//*[text()='提交']").click()
    log.info("保存配置")

    alert = BeAlertBox(back_iframe="default")
    msg = alert.get_msg()
    if alert.title_contains("操作成功"):
        log.info("保存配置成功")

        # 重新进入iframe
        browser.switch_to.frame(
            browser.find_element_by_xpath(get_global_var("NodeIframe")))
        browser.switch_to.frame(
            browser.find_element_by_xpath("//iframe[@id='busi_cmd_node']"))
    else:
        log.warn("保存配置失败，失败提示: {0}".format(msg))
    set_global_var("ResultMsg", msg, False)
