# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2022/5/13 下午5:15

from app.Dashboard.dashboard.dashboard import Dashboard
from app.Dashboard.dashboard.editDashboard import DefaultDashboard, MyDashboard
from app.Dashboard.image.image import Image
from app.Dashboard.dictionary.dictionary import Dictionary
from app.Dashboard.dataInterface.interface import CustomizeInterface
from app.VisualModeler.doctorwho.doctorWho import DoctorWho
from common.page.func.pageMaskWait import page_wait


class Monitor(Dashboard):

    def __init__(self):
        DoctorWho().choose_menu("个人中心-我的监控")
        page_wait()
        self.iframe_xpath = "//iframe[contains(@src, '/VisualModeler/html/personalcenter/myMonitor.html')]"
        super().__init__(self.iframe_xpath)

    def clickButton(self, buttonName):
        """
        # 点击按钮
        :param buttonName: 按钮
        :return:
        """
        self.click(buttonName)

    def showDashboard(self, dashboardName):
        """
        # 预览仪表盘
        :param dashboardName: 仪表盘名称
        :return:
        """
        self.show(dashboardName)

    @staticmethod
    def setDefaultDashboard(dashboardInfo):
        """
        # 默认仪表盘
        :param dashboardInfo: 仪表盘配置
        """
        dashboard = DefaultDashboard()
        dashboard_name = dashboardInfo.get("仪表盘名称")
        subtitle = dashboardInfo.get("仪表盘副标题")
        remark = dashboardInfo.get("备注")
        theme = dashboardInfo.get("主题样式")
        show_title = dashboardInfo.get("显示标题")
        carousel = dashboardInfo.get("启用轮播")
        carousel_interval = dashboardInfo.get("轮播间隔")

        dashboard.edit(dashboard_name, subtitle, remark, theme, show_title, carousel, carousel_interval)

    @staticmethod
    def setMyDashboard(dashboardInfo):
        """
        # 我的仪表盘
        :param dashboardInfo: 仪表盘配置
        """
        dashboard = MyDashboard()
        dashboard_name = dashboardInfo.get("仪表盘名称")
        subtitle = dashboardInfo.get("仪表盘副标题")
        remark = dashboardInfo.get("备注")
        theme = dashboardInfo.get("主题样式")
        show_title = dashboardInfo.get("显示标题")
        carousel = dashboardInfo.get("启用轮播")
        carousel_interval = dashboardInfo.get("轮播间隔")

        dashboard.edit(dashboard_name, subtitle, remark, theme, show_title, carousel, carousel_interval)

    def addDashboard(self, dashboardInfo):
        """
        # 添加仪表盘
        :param dashboardInfo: 仪表盘配置
        """
        self.add(dashboardInfo)

    def editDashboard(self, dashboardName, dashboardInfo):
        """
        # 编辑仪表盘
        :param dashboardName: 仪表盘名称
        :param dashboardInfo: 仪表盘配置
        """
        self.edit(dashboardName, dashboardInfo)

    def deleteDashboard(self, dashboardName):
        """
        # 删除仪表盘
        :param dashboardName: 仪表盘名称
        """
        self.delete(dashboardName)

    @staticmethod
    def addImage(imageInfo):
        """
        # 添加图像
        :param imageInfo: 图像配置
        """
        image = Image()
        imageName = imageInfo.get("图像名称")
        catalog = imageInfo.get("主题分类")
        interface = imageInfo.get("数据接口")
        imageType = imageInfo.get("图像类型")
        dataSource = imageInfo.get("数据源配置")
        style = imageInfo.get("样式配置")

        image.add(imageName, catalog, interface, imageType, dataSource, style)

    @staticmethod
    def addDictionary(dictionaryInfo):
        """
        # 添加字典
        :param dictionaryInfo: 字典配置
        """
        dictionary = Dictionary()
        dictionary.add(dictionaryInfo)

    def addInImage(self, dashboardName, imageList):
        """
        # 仪表盘加入图像
        :param dashboardName: 仪表盘名称
        :param imageList: 图像列表
        """
        self.bind(dashboardName, imageList)

    @staticmethod
    def fieldConversion(tableName, conversion):
        """
        # 字段类型转化
        :param tableName: 表中文名称
        :param conversion: 转化配置，数组
        """
        interface = CustomizeInterface()
        interface.fieldConversion(tableName, conversion)

    @staticmethod
    def fieldClassify(tableName, xList, yList, gList):
        """
        # 字段分类
        :param tableName: 表中文名称
        :param xList: 维度字段，数组
        :param yList: 度量字段，数组
        :param gList: 分组字段，数组
        """
        interface = CustomizeInterface()
        interface.fieldClassify(tableName, xList, yList, gList)
