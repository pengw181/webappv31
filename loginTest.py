# -*- encoding: utf-8 -*-
# @Author: peng wei
# @Time: 2022/3/30 下午6:42

import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from common.page.browser.browser import init_browser
from time import sleep
from common.log.logger import log
from common.page.handle.windows import WindowHandles


def login_website(url):
    browser = init_browser()
    browser.get(url)
    browser.maximize_window()
    log.info("打开url: {0}".format(url))
    return browser


def qcc(qy):
    url = "https://www.qcc.com/?utm_source=baidu1&utm_medium=cpc&utm_term=pzsy"
    browser = login_website(url)
    windows = WindowHandles()
    windows.save("首页")

    # 输入企业名称
    browser.find_element(By.XPATH, "//*[@id='searchKey']").clear()
    browser.find_element(By.XPATH, "//*[@id='searchKey']").send_keys(qy)
    log.info("搜索: {0}".format(qy))

    # 点击查询
    browser.find_element(By.XPATH, "//*[text()='查一下']").click()
    sleep(3)

    # 获取企查查搜索结果
    qcc_find_element = browser.find_element(By.XPATH, "//*[@class='adsearch-list']//h4/span")
    qcc_find_num = int(qcc_find_element.get_attribute("innerHTML"))
    log.info("企查查找到{0}家企业".format(qcc_find_num))
    if qcc_find_num == 0:
        return "找不到企业记录"

    # 点击链接进入企业详情页面
    list_elements = browser.find_elements(By.XPATH, "//*[contains(@class,'tsd0')]/td[3]/div/div/span/a")
    # browser.find_element(By.XPATH, "//*[@class='tsd0'][1]/td[3]/div/div/span/a").click()
    num = 1
    max_access = 5  # 不登录最多只能查看5家
    qy_info = []
    for yq_element in list_elements:
        tmp = [qy]
        yq_element.click()
        log.info('进入企业详情介绍页面')
        sleep(3)

        # 切换窗口
        windows.save("业务详情页")
        windows.switch("业务详情页")

        # 序号
        log.info("序号: {0}".format(num))
        tmp.append(num)

        # 企业名称
        qy_title_element = browser.find_element(By.XPATH, "//*[@class='title']/div/span/h1")
        qy_title = qy_title_element.get_attribute("innerHTML")
        tmp.append(qy_title)
        log.info("企业名称: {0}".format(qy_title))

        # 企业状态
        qy_status_element = browser.find_element(By.XPATH, "//*[@class='title']/div/span/span")
        qy_status = qy_status_element.get_attribute("innerHTML")
        tmp.append(qy_status)
        log.info("企业状态: {0}".format(qy_status))

        # 法定代表人
        try:
            represent_element = browser.find_element(By.XPATH, "//*[@class='contact-info']/div[1]/span/span/span/span/a")
            represent = represent_element.get_attribute("innerText")
            represent = "无" if not represent else represent
        except NoSuchElementException:
            represent = "无"
        tmp.append(represent)
        log.info("法定代表人: {0}".format(represent))

        # 统一社会信用代码
        try:
            credit_element = browser.find_element(By.XPATH, "//*[@class='contact-info']/div[1]//span[2]/span/div/span[1]")
            credit = credit_element.get_attribute("innerText")
            credit = "无" if not credit else credit
        except NoSuchElementException:
            credit = "无"
        tmp.append(credit)
        log.info("统一社会信用代码: {0}".format(credit))

        # 电话
        try:
            phone_element = browser.find_element(By.XPATH, "//*[@class='contact-info']/div[2]/span[1]/span/span[2]")
            phone = phone_element.get_attribute("innerText")
            phone = "无" if not phone else phone
        except NoSuchElementException:
            phone = "无"
        tmp.append(phone)
        log.info("电话: {0}".format(phone))

        # 官网
        try:
            website_element = browser.find_element(By.XPATH, "//*[@class='contact-info']/div[2]/span[2]/span/a")
            website = website_element.get_attribute("innerText")
            website = "无" if not website else website
        except NoSuchElementException:
            website = "无"
        tmp.append(website)
        log.info("官网: {0}".format(website))

        # 邮箱
        try:
            email_element = browser.find_element(By.XPATH, "//*[@class='contact-info']/div[3]/span[1]/span/a")
            email = email_element.get_attribute("innerText")
            email = "无" if not email else email
        except NoSuchElementException:
            email = "无"
        tmp.append(email)
        log.info("邮箱: {0}".format(email))

        # 地址
        try:
            address_element = browser.find_element(By.XPATH, "//*[@class='contact-info']/div[3]/span[2]/div/span[1]/a/span")
            address = address_element.get_attribute("innerText")
            address = "无" if not address else address
        except NoSuchElementException:
            address = "无"
        tmp.append(address)
        log.info("地址: {0}\n".format(address))

        if num < min(qcc_find_num, max_access):
            # 关闭当前窗口
            browser.close()
            windows.switch("首页")
            num += 1
            qy_info.append(tmp)
            sleep(1)

    # 关闭
    browser.quit()

    return qy_info


def main1():
    name_list = ["湘邮科技", "百度"]
    result = []
    for name in name_list:
        result += qcc(name)
    log.info(result)
    # result = [['湘邮科技', 1, '湖南湘邮科技股份有限公司', '存续', '董志宏', '914300007225774774', '0731-8899****', ' www.copote.com', 'c****e@copote.com', '长沙市高新技术产业开发区麓谷基地玉兰路2号'],
    #           ['湘邮科技', 2, '湖南国邮传媒股份有限公司', '存续', '韩铸', '914301007722831511', '1807312****', ' http://www.postmeidia.com.cn', '9****1@qq.com', '长沙高新开发区玉兰路2号湘邮科技园研发大楼七楼'],
    #           ['湘邮科技', 3, '湖南湘邮科技股份有限公司福建分公司', '存续', '徐晖', '91350104MA8UAQ4C8C', '无', '无', '无', '福建省福州市仓山区临江街道工农街36-57号二楼186'],
    #           ['湘邮科技', 4, '湖南湘邮科技股份有限公司北京分公司', '存续', '姚琪', '91110102MA00D07TXL', '1511001****', '无', 'z****g@copote.com', '北京市丰台区南三环东路25号1幢一层至二层'],
    #           ['百度', 1, '企查查科技有限公司', '在业', '陈德强', '91320594088140947F', '0512-6251****', ' www.qcc.com', 'k****u@qichacha.com', '苏州工业园区东长路88号C1幢5层503室'],
    #           ['百度', 2, '百度在线网络技术（北京）有限公司', '存续', '崔珊珊', '91110108717743469K', '010-5992****', ' http://www.baidu.com', 's****r@baidu.com', '北京市海淀区上地十街10号百度大厦三层'],
    #           ['百度', 3, '百度（中国）有限公司', '存续', '沈抖', '91310000775785552L', '021-2068****', '无', 'w****5@baidu.com', '中国(上海)自由贸易试验区纳贤路701号1#楼3层'],
    #           ['百度', 4, '北京百度网讯科技有限公司', '存续', '梁志祥', '91110000802100433B', '010-5992****', ' http://www.baidu.com', 'u****o@baidu.com', '北京市海淀区上地十街10号百度大厦2层']]

    print(
        '{:<10} | {:^2} | {:<30} | {:^2} | {:^5} | {:^20} | {:^15} | {:^15} | {:^15}| {:40}'.format('关键字', '序号', '企业名称',
                                                                                                    '企业状态', '法定代表人',
                                                                                                    '信用代码', '联系电话',
                                                                                                    '企业官网', '企业邮箱',
                                                                                                    '企业地址'))
    fmt = '{:<10} | {:^2} | {:<30} | {:^2} | {:^5} | {:^20} | {:^15} | {:^15} | {:^15}| {:40}'
    for info in result:
        print(fmt.format(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9]))


def search(keyword):
    url = "https://www.baidu.com"
    browser = login_website(url)
    windows = WindowHandles()
    windows.save("百度首页")

    browser.find_element(By.XPATH, "//*[@id='kw']").clear()
    browser.find_element(By.XPATH, "//*[@id='kw']").send_keys(keyword)
    browser.find_element(By.XPATH, "//*[@id='su']").click()
    sleep(2)
    return browser


def weather():
    url = "http://www.weather.com.cn/"
    browser = login_website(url)
    windows = WindowHandles()
    windows.save("首页")
    sleep(1)

    # 获取当前城市名称
    city = browser.find_element(By.XPATH, "//*[@id='cityName']")
    city_name = city.get_attribute("innerHTML")

    # 点击获取【40天预报】
    browser.find_element(By.XPATH, "//*[@id='showCalendar']/div").click()
    windows.save("40天预报")
    windows.switch("40天预报")
    sleep(3)
    # 切换到7天
    browser.find_element(By.XPATH, "//*[@id='someDayNav']//a[text()='7天']").click()
    sleep(3)

    # 7天天气预报
    num = 7
    result = []
    for i in range(1, num+1):
        one_day = [city_name]
        day_xpath = "//*[@id='7d']/ul/li[{0}]".format(i)

        # date
        obj = browser.find_element(By.XPATH, day_xpath + "/h1")
        date = obj.get_attribute("innerHTML")
        one_day.append(date)

        # png1
        obj = browser.find_element(By.XPATH, day_xpath + "/big[1]")
        png1 = obj.get_attribute("class")
        one_day.append(png1)

        # png2
        obj = browser.find_element(By.XPATH, day_xpath + "/big[2]")
        png2 = obj.get_attribute("class")
        one_day.append(png2)

        # wea
        obj = browser.find_element(By.XPATH, day_xpath + "/p[@class='wea']")
        wea = obj.get_attribute("title")
        one_day.append(wea)

        # tem
        obj = browser.find_element(By.XPATH, day_xpath + "/p[@class='tem']")
        tem = obj.get_attribute("innerText")
        # 25/23℃
        patt = r'(-?\d+)/(-?\d+)℃'
        matchObj = re.match(patt, tem)
        if matchObj:
            low_tem = matchObj.group(1)
            high_tem = matchObj.group(2)
            one_day.append(low_tem)
            one_day.append(high_tem)
        else:
            raise Exception("no match")

        # win1
        obj = browser.find_element(By.XPATH, day_xpath + "/p[@class='win']/em/span[1]")
        win1 = obj.get_attribute("class")
        one_day.append(win1)

        # win2
        obj = browser.find_element(By.XPATH, day_xpath + "/p[@class='win']/em/span[2]")
        win2 = obj.get_attribute("class")
        one_day.append(win2)

        # win3
        obj = browser.find_element(By.XPATH, day_xpath + "/p[@class='win']/i")
        win3 = obj.get_attribute("innerText")
        one_day.append(win3)

        result.append(one_day)
    print(result)


if __name__ == "__main__":
    weather()

