# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from joongrangsoop.items import JoongrangsoopItem


class Joongrangsoop2SpiderSpider(scrapy.Spider):
    name = 'joongrangsoop2_spider'
    allowed_domains = ['reservation.nowonsc.kr']
    start_urls = ['https://reservation.nowonsc.kr/member/login']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('C:\\github\\chromedriver.exe')


    def parse1(self, response):
        for colum in response.xpath('//*[@id="contents"]/div[3]/div[2]/div/img').getall():
            print("------------------------------")
            print(colum)
            print("******************************")
        pass


    def parse2(self, response):
        self.browser.get(response.url)
        time.sleep(10)
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        rows = selector.xpath('//*[@id="contents"]/div[3]/div[2]/div/img').extract()

        for colum in rows:
            print("------------------------------")
            print(colum)
            print("******************************")
        #self.browser.quit()
        pass

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(1)
                                            # //*[@id="calendarTable"]/tbody/tr[2]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[3]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[4]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[5]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[6]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[7]/td[7]/a
        emptys=[]
        weeks = [2,3,4,5,6,7] #주차
        Saturday = 7 #토요일
        for week in weeks:
            try:
                # print('index', index)
                path = '//*[@id="calendarTable"]/tbody/tr['+str(week)+']/td['+str(Saturday)+']/a'
                self.browser.find_element_by_xpath(path).click()
                # print(click)

                # time.sleep(5)
                
                html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
                selector = Selector(text=html)

                day = selector.xpath('//*[@class="select_day"]/a/text()').extract()
                # print('click =============>', day[0], '<=============')
                rows = selector.xpath('//*[@id="contents"]/div[3]/div[2]/div/img/@alt').extract()
                # print(rows)
                for row in rows:
                    if "시설 약도" not in row and "예약완료" not in row:
                        # print(row)
                        # emptys.append({'day':day, 'row': row})

                        empty = JoongrangsoopItem()
                        empty['day']=day
                        empty['row']=row
                        emptys.append(empty)

            except Exception as identifier:
                print("Processing Exception:", identifier)
                pass

 

        print('emptys:', emptys)
        # elements1 = self.browser.find_elements_by_xpath('//*[@id="contents"]/div[3]/div[2]/div/img').get_attribute('alt')
        # for element1 in elements1:
        #     print(element1)

        # elements = self.browser.find_elements_by_xpath('//*[@id="contents"]/div[3]/div[2]/div/img')
        # print(elements)
        # for element in elements:
        #     print(element)
            # print('test')
            # alt = element.get_attribute('alt')
            # if "예약완료" in alt:
            #     print("예약완료", alt)
            # else:
            #     print("예약불가", alt)

        # html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        # selector = Selector(text=html)
        # rows = selector.xpath('//*[@id="contents"]/div[3]/div[2]/div/img').extract()

        # for colum in rows:
        #     print("------------------------------")
        #     print(colum)
        #     # if "예약완료" in colum:
        #     #     print('예약완료')
        #     # else:
        #     #     print('예약가능')
        #     #     print(colum)
        #     print("******************************")
        self.browser.quit()
        return emptys
        # pass
