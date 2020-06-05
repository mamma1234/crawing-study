# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from camping.items import CampingItem


class GangdongSpider(scrapy.Spider):
    name = 'gangdong_spider'
    allowed_domains = ['reservation.nowonsc.kr']
    start_urls = ['https://reservation.nowonsc.kr/member/login']
    reserve_urls = ['https://reservation.nowonsc.kr/leisure/camping_date?cate1=2']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('C:\\github\\chromedriver.exe')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(3)
        # self.browser.implicitly_wait(3)
        
        self.browser.find_element_by_id("memberId").send_keys('mamma1234')
        self.browser.find_element_by_id("memberPassword").send_keys('qkrghwls0!')
        self.browser.find_element_by_css_selector("button[type='submit'].btn").click()
        # self.browser.get(self.reserve_urls)
        self.browser.get('https://reservation.nowonsc.kr/leisure/camping_date?cate1=2')
        time.sleep(3)
                                            # //*[@id="calendarTable"]/tbody/tr[2]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[3]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[4]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[5]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[6]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[7]/td[7]/a
        emptys=[]
        try:
            # 당월의 토요일 구하기
            # 다음달의 토요일 구하기


            path = '//*[@id="td-2020-06-25"]'
            self.browser.find_element_by_xpath(path).click()
            day = path

            group = "village01"
            start = 39
            end = 66
            empty = self.search(day, group, start, end)
            emptys.extend(empty)

            group = "village02"
            start = 66
            end = 72
            empty = self.search(day, group, start, end)
            emptys.extend(empty)

            group = "village03"
            start = 72
            end = 91
            empty = self.search(day, group, start, end)
            emptys.extend(empty)

            group = "village04"
            start = 91
            end = 94
            empty = self.search(day, group, start, end)
            emptys.extend(empty)

        #     self.browser.find_element_by_id(group).click()
        #     html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        #     selector = Selector(text=html)
        #     for n in range(39, 66): #39 ~ 65
        #         try:
        #             # print(n)
        #             path = '//*[@id="chk_'+str(n)+'"]/@data-cseq'
        #             rows = selector.xpath(path).extract()
        #             # print(rows)
        #             path2 = '//*[@id="chk_'+str(n)+'"]/@disabled'
        #             rows2 = selector.xpath(path2).extract()
        #             # print(rows2, len(rows2) )
        #             if len(rows2) < 1:
        #                 empty = CampingItem()
        #                 empty['day']=day
        #                 empty['group']=group
        #                 empty['row']=rows[0]
        #                 emptys.append(empty)
        #         except Exception as identifier:
        #             print("Processing Exception:", identifier)
        #             pass

        #     group = "village02"
        #     self.browser.find_element_by_id(group).click()
        #     html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        #     selector = Selector(text=html)
        #     for n in range(66, 72): #39 ~ 65
        #         try:
        #             # print(n)
        #             path = '//*[@id="chk_'+str(n)+'"]/@data-cseq'
        #             rows = selector.xpath(path).extract()
        #             # print(rows)
        #             path2 = '//*[@id="chk_'+str(n)+'"]/@disabled'
        #             rows2 = selector.xpath(path2).extract()
        #             # print(rows2, len(rows2) )
        #             if len(rows2) < 1:
        #                 empty = CampingItem()
        #                 empty['day']=day
        #                 empty['group']=group
        #                 empty['row']=rows[0]
        #                 emptys.append(empty)
        #         except Exception as identifier:
        #             print("Processing Exception:", identifier)
        #             pass


        #     group = "village03"
        #     self.browser.find_element_by_id(group).click()
        #     html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        #     selector = Selector(text=html)
        #     for n in range(72, 91): #39 ~ 65
        #         try:
        #             # print(n)
        #             path = '//*[@id="chk_'+str(n)+'"]/@data-cseq'
        #             rows = selector.xpath(path).extract()
        #             # print(rows)
        #             path2 = '//*[@id="chk_'+str(n)+'"]/@disabled'
        #             rows2 = selector.xpath(path2).extract()
        #             # print(rows2, len(rows2) )
        #             if len(rows2) < 1:
        #                 empty = CampingItem()
        #                 empty['day']=day
        #                 empty['group']=group
        #                 empty['row']=rows[0]
        #                 emptys.append(empty)
        #         except Exception as identifier:
        #             print("Processing Exception:", identifier)
        #             pass

        #     group = "village04"
        #     self.browser.find_element_by_id(group).click()
        #     html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        #     selector = Selector(text=html)
        #     for n in range(91, 94): #39 ~ 65
        #         try:
        #             # print(n)
        #             path = '//*[@id="chk_'+str(n)+'"]/@data-cseq'
        #             rows = selector.xpath(path).extract()
        #             # print(rows)
        #             path2 = '//*[@id="chk_'+str(n)+'"]/@disabled'
        #             rows2 = selector.xpath(path2).extract()
        #             # print(rows2, len(rows2) )
        #             if len(rows2) < 1:
        #                 empty = CampingItem()
        #                 empty['day']=day
        #                 empty['group']=group
        #                 empty['row']=rows[0]
        #                 emptys.append(empty)
        #         except Exception as identifier:
        #             print("Processing Exception:", identifier)
        #             pass

        except Exception as identifier:
            print("Processing Exception:", identifier)
            pass

        time.sleep(3)
        print('emptys:', emptys)
        self.browser.quit()
        return emptys


    def search(self, day, group, start, end):
        emptys = []
        self.browser.find_element_by_id(group).click()
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        for n in range(start, end): #39 ~ 65
            try:
                # print(n)
                path = '//*[@id="chk_'+str(n)+'"]/@data-cseq'
                rows = selector.xpath(path).extract()
                # print(rows)
                path2 = '//*[@id="chk_'+str(n)+'"]/@disabled'
                rows2 = selector.xpath(path2).extract()
                # print(rows2, len(rows2) )
                if len(rows2) < 1:
                    empty = CampingItem()
                    empty['day']=day
                    empty['group']=group
                    empty['row']=rows[0]
                    emptys.append(empty)
            except Exception as identifier:
                print("Processing Exception:", identifier)
                pass        

        return emptys