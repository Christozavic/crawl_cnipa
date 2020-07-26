# -*-coding:utf-8-*-
# 日期：2020-07-25，时间：16:23

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pdfkit
import time

CHROME_DRIVER = 'chromedriver.exe'
wk_path = r'C:\zzz\zzz_softs\wkhtmltopdf\bin\wkhtmltopdf.exe'
URL_CNIPA = 'http://sbj.cnipa.gov.cn/sbcx/'


class HandleWebDriver:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=self.chrome_options)
        self.driver.maximize_window()

    def handle_cnipa(self):
        self.driver.get(URL_CNIPA)
        time.sleep(2)
        self.driver.find_element_by_xpath('//p[@style="text-align: center"]/a').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//div[@class="left_side"]//li[2]').click()
        time.sleep(2)
        print(self.driver.page_source)

        # TODO: 反爬机制没有处理成功，暂时直接进入下一个步骤

        if WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.NAME, 'request:mn'))):
            input_keyword = input('请输入要查找的商标名称：')
            self.driver.find_element_by_name('request:mn').send_keys(input_keyword)
            self.driver.find_element_by_id('_searchButton').click()

            if WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, 'list_box'))):
                while True:
                    time.sleep(1)
                    # self.handle_parse(self.driver.page_source)
                    html_file = 'cnipa.html'
                    with open(html_file, 'a+') as f:
                        f.write(self.driver.page_source)
                    # 判断是否还有下一页
                    next_page = self.driver.find_element_by_xpath(
                        '//div[@id="mGrid_listGrid_paginator_0"]//li[@class="nextPage"]')
                    if next_page.text == '>':
                        next_page.click()
                    else:
                        config = pdfkit.configuration(wkhtmltopdf=wk_path)
                        pdf_file = "cnipa.pdf"
                        pdfkit.from_url(html_file, pdf_file, configuration=config)
            self.driver.quit()

    def handle_parse(self, page_source):
        # 解析页面数据
        # html_cnipa = etree.HTML(page_source)
        # all_div = html_cnipa.xpath('//div[@id="list_box"]//tr[@class="ng-scope"]')
        # info_list = []
        # for item in all_div:
        #     info = []
        #     info.append(item.xpath('./td[1]')[0])
        #     info.append(item.xpath('./td[2]')[0])
        #     info.append(item.xpath('./td[3]')[0])
        #     info.append(item.xpath('./td[4]')[0])
        #     info.append(item.xpath('./td[5]')[0])
        #     info.append(item.xpath('./td[6]')[0])
        #     info_list.append(info)
        pass


if __name__ == '__main__':
    test_selenium = HandleWebDriver()
    test_selenium.handle_cnipa()
