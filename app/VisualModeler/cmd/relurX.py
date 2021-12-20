# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2021/9/17 下午4:56

from selenium.common.exceptions import NoSuchElementException
from common.page.func.alert_box import BeAlertBox
from common.page.func.input import set_textarea
from time import sleep
from app.VisualModeler.doctorwho.doctor_who import DoctorWho
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.page.func.page_mask_wait import page_wait
from common.log.logger import log
from common.variable.global_variable import *
from common.page.func.regexp import analyze_conf
from common.page.func.table_data import get_table_data2
from common.page.func.load_data import load_sample


class RulerX:

    def __init__(self):
        self.browser = get_global_var("browser")
        DoctorWho().choose_menu("指令配置-通用指令解析配置")
        page_wait()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src, '/VisualModeler/html/rulerx/rulerxTmpl.html')]")))
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='keyword']/following-sibling::span[1]/input[1]")))
        page_wait()
        self.analysis_name = None
        sleep(1)

    def choose(self, analyzer_name):
        """
        :param analyzer_name: 解析模版名称
        """
        try:
            self.browser.find_element_by_xpath("//*[@id='keyword']/following-sibling::span[1]/input[1]").clear()
            self.browser.find_element_by_xpath(
                "//*[@id='keyword']/following-sibling::span[1]/input[1]").send_keys(analyzer_name)
            page_wait()
            self.browser.find_element_by_xpath("//*[@id='rulerxTmpl-query']//*[text()='查询']").click()
            page_wait()
            self.browser.find_element_by_xpath(
                "//*[@field='analyzerName']/*[contains(@class,'analyzerName')]/*[text()='{}']".format(analyzer_name)).click()
            log.info("选择解析模版：{0}".format(analyzer_name))
        except NoSuchElementException:
            log.error("所选解析模版不存在, 解析模版名称: {0}".format(analyzer_name))

    def add(self, basic_cfg=None, result_format_cfg=None, segment_cfg=None, format_table_cfg=None, judge_ruler=None,
            judge_cfg=None):
        """
        :param basic_cfg: 基本信息配置
        :param result_format_cfg: 结果格式化配置
        :param segment_cfg: 分段规则配置
        :param format_table_cfg: 格式化二维表配置
        :param judge_ruler: 选择判断规则
        :param judge_cfg: 判断规则配置

        {
            "操作": "",
            "参数": {
                "基本信息配置": {
                    "模版名称": "",
                    "模版说明": ""
                },
                "结果格式化配置": {
                    "分段": "是",
                    "格式化成二维表": "是",
                },
                "分段规则配置": {
                    "段开始特征行": "",
                    "段结束特征行": "",
                    "样例数据": "",
                    "抽取每一段的头部字段": "否"

                },
                "格式化二维表配置": {
                    "解析开始行": "1",
                    "通过正则匹配数据列": "是",
                    "列总数": "",
                    "拆分方式": "",
                    "列分隔符": "",
                    "正则魔方": {
                        "设置方式": "添加",
                        "正则模版名称": "pw自动化正则模版",
                        "高级模式": "否",
                        "标签配置": [
                            {
                                "标签": "自定义文本",
                                "值": "pw",
                                "是否取值": "黄色"
                            },
                            {
                                "标签": "任意字符",
                                "值": "1到多个",
                                "是否取值": "绿色"
                            }
                        ]
                    },
                    "样例数据": ""
                },
                "选择判断规则": "二维表结果判断",
                "判断规则配置": {
                    "目标行": "",
                    "行结果关系": "",
                    "规则管理": [
                        {
                            "列名": "列1",
                            "关系": "不等于",
                            "匹配值": "0",
                            "条件满足时": "异常",
                            "匹配不到值时": "无数据进行规则判断",
                            "异常提示信息": ""
                        }
                    ]
                }
            }
        }
        """
        page_wait()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[text()='添加']")))
        self.browser.find_element_by_xpath("//*[text()='添加']").click()
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.frame_to_be_available_and_switch_to_it((
            By.XPATH, "//iframe[contains(@src,'rulerxTmplEditWin.html')]")))
        wait = WebDriverWait(self.browser, 30)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='analyzerName']/following-sibling::span/input[1]")))

        # 基本信息配置
        if basic_cfg:
            self.step_basic_info(analyzer_name=basic_cfg.get("模版名称"), remark=basic_cfg.get("模版说明"))
        # 点击下一步
        self.browser.find_element_by_xpath("//*[text()='下一步']").click()
        page_wait(timeout=3)

        # 结果格式化配置
        if result_format_cfg:
            self.step_result_format(enable_segment=result_format_cfg.get("分段"),
                                    enable_format_table=result_format_cfg.get("格式化成二维表"))
        # 点击下一步
        self.browser.find_element_by_xpath("//*[text()='下一步']").click()
        page_wait(timeout=3)

        # 分段规则配置
        if segment_cfg:
            self.step_segment()
            # 点击下一步
            self.browser.find_element_by_xpath("//*[text()='下一步']").click()
            page_wait(timeout=3)

        # 格式化二维表配置
        if format_table_cfg:
            self.step_format_table(begin_row=format_table_cfg.get("解析开始行"), enable_magic=format_table_cfg.get("通过正则匹配数据列"),
                                   total_columns=format_table_cfg.get("列总数"), row_split_type=format_table_cfg.get("拆分方式"),
                                   split_tag=format_table_cfg.get("列分隔符"), magic=format_table_cfg.get("正则魔方"),
                                   sample=format_table_cfg.get("样例数据"))
            # 点击下一步
            self.browser.find_element_by_xpath("//*[text()='下一步']").click()
            page_wait(timeout=3)

        # 选择判断规则
        if judge_ruler:
            self.step_choose_judge_ruler(judge_type=judge_ruler)
        # 点击下一步
        self.browser.find_element_by_xpath("//*[text()='下一步']").click()
        page_wait(timeout=3)

        # 判断规则配置
        if judge_cfg:
            self.step_judge_cfg(target_row=judge_cfg.get("目标行"), row_relation=judge_cfg.get("行结果关系"),
                                ruler_conf=judge_cfg.get("规则管理"))
        # 点击完成
        self.browser.find_element_by_xpath("//*[text()='完成']").click()
        alert = BeAlertBox(timeout=1)
        msg = alert.get_msg()
        if alert.title_contains("向导配置完成"):
            log.info("解析模版【{}】配置完成".format(self.analysis_name))
        else:
            log.warn("解析模版【{0}】配置失败，失败提示: {1}".format(self.analysis_name, msg))
        set_global_var("ResultMsg", msg, False)

    def step_basic_info(self, analyzer_name, remark):
        """
        # 基本信息配置
        :param analyzer_name: 模版名称
        :param remark: 模版说明
        """
        # 模版名称
        if analyzer_name:
            self.browser.find_element_by_xpath("//*[@id='analyzerName']/following-sibling::span/input[1]").clear()
            self.browser.find_element_by_xpath(
                "//*[@id='analyzerName']/following-sibling::span/input[1]").send_keys(analyzer_name)
            log.info("设置模版名称: {}".format(analyzer_name))

        # 模版说明
        if remark:
            remark_textarea = self.browser.find_element_by_xpath(
                "//*[@id='analyzerDesc']/following-sibling::span/textarea")
            set_textarea(textarea=remark_textarea, msg=remark)
            if isinstance(remark, list):
                log.info("设置模版说明: {}".format('\n'.join(remark)))
            else:
                log.info("设置模版说明: {}".format(remark))

        # 获取当前解析模版名称
        self.analysis_name = self.browser.find_element_by_xpath(
                "//*[@id='analyzerName']/following-sibling::span/input[2]").get_attribute("defaultValue")

    def step_result_format(self, enable_segment, enable_format_table):
        """
        :param enable_segment: 分段， 是/否
        :param enable_format_table: 格式化成二维表， 是/否
        """
        # 分段
        js = 'return $("#askSubsection")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【分段】勾选状态: {0}".format(status))

        enable_segment_element = self.browser.find_element_by_xpath("//*[@id='askSubsection']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", enable_segment_element)

        if enable_segment == "是":
            if not status:
                enable_segment_element.click()
                log.info("勾选【分段】")
        else:
            if status:
                enable_segment_element.click()
                log.info("取消勾选【分段】")
            else:
                log.info("【分段】设置为否，不勾选")

        # 格式化成二维表
        js = 'return $("#askTable")[0].checked;'
        status = self.browser.execute_script(js)
        log.info("【格式化成二维表】勾选状态: {0}".format(status))

        enable_format_table_element = self.browser.find_element_by_xpath("//*[@id='askTable']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", enable_format_table_element)

        if enable_format_table == "是":
            if not status:
                enable_format_table_element.click()
                log.info("勾选【格式化成二维表】")
        else:
            if status:
                enable_format_table_element.click()
                log.info("取消勾选【格式化成二维表】")
            else:
                log.info("【格式化成二维表】设置为否，不勾选")

    def step_segment(self):
        pass

    def step_format_table(self, begin_row=None, enable_magic=None, total_columns=None, row_split_type=None,
                          split_tag=None, magic=None, sample=None):
        """
        # 格式化二维表配置
        :param begin_row: 解析开始行
        :param enable_magic: 通过正则匹配数据列，是/否
        :param total_columns: 列总数
        :param row_split_type: 拆分方式，文本/正则
        :param split_tag: 列分隔符
        :param magic: 正则魔方，开启通过正则匹配数据列或拆分方式为正则时使用
        :param sample: 样例数据，指定resources下的文件名，自动从文件加载并填充
        """
        # 正则配置
        add_flag = analyze_conf(begin_row=begin_row, enable_magic=enable_magic, total_columns=total_columns,
                                row_split_type=row_split_type, split_tag=split_tag, magic=magic)
        if add_flag:
            # 向上返回2级，切换到解析模版配置iframe
            self.browser.switch_to.parent_frame()
            self.browser.switch_to.parent_frame()
            alert = BeAlertBox(back_iframe=False)
            msg = alert.get_msg()
            if alert.title_contains("成功"):
                log.info("保存正则模版成功")
                # 切换到正则魔方配置iframe
                self.browser.switch_to.frame(
                    self.browser.find_element_by_xpath("//iframe[contains(@src,'rulerxTmplEditWin.html')]"))
            else:
                log.warn("保存正则模版失败，失败提示: {0}".format(msg))
            set_global_var("ResultMsg", msg, False)

        # 样例数据
        if sample:
            sample_data = load_sample(sample_file_name=sample)
            sample_textarea = self.browser.find_element_by_xpath(
                "//*[@id='tableExampleDatatableFormatCfgDiv']/following-sibling::span/textarea")
            set_textarea(textarea=sample_textarea, msg=sample_data)
            log.info("样例数据填充完成")
            sleep(1)

        # 点击效果预览
        self.browser.find_element_by_xpath("//*[@id='tableFormatCfgDiv']//*[@class='formatBtn']").click()
        page_wait(timeout=5)
        sleep(1)
        # 如果出现弹出框，则表示预览异常
        alert = BeAlertBox(timeout=1)
        if alert.exist_alert:
            msg = alert.get_msg()
            raise Exception(msg)
        else:
            log.info("解析规则预览正常")
            # 切换到通用指令解析配置页面
            self.browser.switch_to.frame(self.browser.find_element_by_xpath("//iframe[contains(@src,'rulerxTmplEditWin.html')]"))
            table_xpath = "//*[@id='issuingCmdIframeTabletableFormatCfgDiv']/following-sibling::div[1]//*[@class='format_tab']"
            data = get_table_data2(table_xpath=table_xpath, return_column=True)
            log.info("预览结果: {}".format(data))

    def step_choose_judge_ruler(self, judge_type):
        """
        # 选择判断规则
        :param judge_type: 选择判断规则，只能选一个
        :return: 单击
        """
        # 选择判断规则
        self.browser.find_element_by_xpath(
            "//*[@name='judgeType']/following-sibling::span[text()='{}']".format(judge_type)).click()

    def step_judge_cfg(self, target_row, row_relation, ruler_conf):
        """
        # 判断规则配置
        :param target_row: 目标行
        :param row_relation: 行结果关系
        :param ruler_conf: 规则管理，数组
        :return: 每次添加一个规则
        """
        page_wait(timeout=3)
        sleep(1)
        # 目标行
        if target_row:
            self.browser.find_element_by_xpath(
                "//*[@name='tableTargetRowSel']/../../*[contains(text(),'{}')]".format(target_row)).click()
            log.info("设置目标行: {}".format(target_row))

        # 行结果关系
        if row_relation:
            self.browser.find_element_by_xpath(
                "//*[@name='tableRowRelation']/../../*[contains(text(),'{}')]".format(row_relation)).click()
            log.info("设置行结果关系: {}".format(row_relation))

        # 变量配置

        # 规则管理
        if ruler_conf:
            i = 1
            for rule in ruler_conf:
                add_element = self.browser.find_element_by_xpath("//*[@id='tableRuleMgr']//*[@data-mtips='添加一套规则']")
                self.browser.execute_script("arguments[0].scrollIntoView(true);", add_element)
                add_element.click()
                log.info("设置规则{}".format(i))
                self.ruler(left_value=rule.get("列名"), relation=rule.get("关系"), right_value=rule.get("匹配值"),
                           when_matched=rule.get("条件满足时"), when_not_matched=rule.get("匹配不到值时"),
                           error_tips=rule.get("异常提示信息"), row_num=i)
                i += 1

        # 解析结果预览
        self.browser.find_element_by_xpath("//*[text()='解析结果预览']/following-sibling::div/a").click()
        page_wait()
        alert = BeAlertBox(timeout=10)
        if alert.exist_alert:
            msg = alert.get_msg()
            log.info("解析结果预览失败，预览提示: {}".format(msg))
            raise Exception(msg)
        else:
            # 切换到通用指令解析配置页面
            self.browser.switch_to.frame(
                self.browser.find_element_by_xpath("//iframe[contains(@src, 'rulerxTmplEditWin.html')]"))
            analysis_result_element = self.browser.find_element_by_xpath(
                "//*[contains(@class,'analysisResult')]/following-sibling::span/input")
            analysis_result = analysis_result_element.get_attribute("defaultValue")
            log.info("解析结果预览成功，解析结果: {}".format(analysis_result))

    def ruler(self, left_value, relation, right_value, row_num, when_matched=None, when_not_matched=None, error_tips=None):
        """
        :param left_value: 列名
        :param relation: 关系
        :param right_value: 匹配值
        :param when_matched: 条件满足时
        :param when_not_matched: 匹配不到值时
        :param error_tips: 异常提示信息
        :param row_num: 规则N
        :return:
        """
        parent_ruler_xpath = "//*[@class='cfg_box_row singleRule'][{}]".format(row_num)
        rule_element = self.browser.find_element_by_xpath("//*[@class='rowRuleDiv']")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", rule_element)

        # 列名
        if left_value:
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[contains(@class,'leftValue')]/following-sibling::span//a").click()
            elements = self.browser.find_elements_by_xpath(
                "//*[contains(@id,'_combobox_') and text()='{}']".format(left_value))
            for element in elements:
                if element.is_displayed():
                    element.click()
                    log.info("规则{0}选择列名: {1}".format(row_num, left_value))
                    break

        # 关系
        if relation:
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[contains(@class,'operator')]/following-sibling::span//a").click()
            elements = self.browser.find_elements_by_xpath(
                "//*[contains(@id,'_combobox_') and text()='{}']".format(relation))
            for element in elements:
                if element.is_displayed():
                    element.click()
                    log.info("规则{0}选择关系: {1}".format(row_num, relation))
                    break

        # 匹配值
        if right_value:
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[contains(@class,'rightValue')]/following-sibling::span//a").click()
            elements = self.browser.find_elements_by_xpath(
                "//*[contains(@id,'_combobox_') and text()='{}']".format(right_value))
            if len(elements) == 0:
                # 如果下拉框没有预期的值，则在输入框手动输入
                self.browser.find_element_by_xpath(
                    parent_ruler_xpath + "//*[contains(@class,'rightValue')]/following-sibling::span//a").click()
                self.browser.find_element_by_xpath(
                    parent_ruler_xpath + "//*[contains(@class,'rightValue')]/following-sibling::span/input[1]").clear()
                self.browser.find_element_by_xpath(
                    parent_ruler_xpath + "//*[contains(@class,'rightValue')]/following-sibling::span/input[1]").send_keys(
                    right_value)
                log.info("规则{0}输入匹配值: {1}".format(row_num, right_value))
            else:
                for element in elements:
                    if element.is_displayed():
                        element.click()
                        log.info("规则{0}选择匹配值: {1}".format(row_num, right_value))
                        break

        # 条件满足时
        if when_matched:
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[contains(@class,'meetResult')]/following-sibling::span//a").click()
            elements = self.browser.find_elements_by_xpath(
                "//*[contains(@id,'_combobox_') and text()='{}']".format(when_matched))
            for element in elements:
                if element.is_displayed():
                    element.click()
                    log.info("规则{0}选择条件满足时: {1}".format(row_num, when_matched))
                    break

        # 匹配不到值时
        if when_not_matched:
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[contains(@class,'unFoundResult')]/following-sibling::span//a").click()
            elements = self.browser.find_elements_by_xpath(
                "//*[contains(@id,'_combobox_') and text()='{}']".format(when_not_matched))
            for element in elements:
                if element.is_displayed():
                    element.click()
                    log.info("规则{0}选择匹配不到值时: {1}".format(row_num, when_not_matched))
                    break

        # 异常提示信息
        if error_tips:
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[text()='异常提示信息']/following-sibling::span/input[1]").clear()
            self.browser.find_element_by_xpath(
                parent_ruler_xpath + "//*[text()='异常提示信息']/following-sibling::span/input[1]").send_keys(error_tips)
            log.info("规则{0}设置异常提示信息: {1}".format(row_num, error_tips))

        # 规则N配置完成
        log.info("规则{}配置完成".format(row_num))
        sleep(1)
