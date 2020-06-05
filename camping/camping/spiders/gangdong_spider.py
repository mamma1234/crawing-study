# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from camping.items import CampingItem

from datetime import date
from datetime import timedelta
import calendar

def getSaturday():
    
    today = date.today()
    thisyear = today.year
    thismonth = today.month
    nextyear, nextmonth = calendar._nextmonth(year=thisyear, month=thismonth)
    # print(nextyear, nextmonth)

    thissaturday=[]
    nextsaturday=[]

    cal = calendar.monthcalendar(thisyear, thismonth)
    for week in cal:
        if week[calendar.SATURDAY]:
            print('%2s: %2s' % (str(thismonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            thissaturday.append({'year':thisyear, 'month': thismonth, 'day':week[calendar.SATURDAY]})

    cal = calendar.monthcalendar(nextyear, nextmonth)
    for week in cal:
        if week[calendar.SATURDAY]:
            print('%2s: %2s' % (str(nextmonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            nextsaturday.append({'year':nextyear, 'month': nextmonth, 'day':week[calendar.SATURDAY]})

    return thissaturday, nextsaturday

class GangdongSpider(scrapy.Spider):
    name = 'gangdong_spider'
    allowed_domains = ['camp.xticket.kr']
    start_urls = ['https://camp.xticket.kr/web/main?shopEncode=5f9422e223671b122a7f2c94f4e15c6f71cd1a49141314cf19adccb98162b5b0']

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

# find_element_by_name('HTML_name')
# find_element_by_id('HTML_id')
# find_element_by_xpath('/html/body/some/xpath')
# find_element_by_css_selector('#css > div.selector')
# find_element_by_class_name('some_class_name')
# find_element_by_tag_name('h1')
# find_elements_by_css_selector('#css > div.selector')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(1)


        try:
            self.browser.find_element_by_css_selector("#notice_layer_582 > div > div > div > fieldset > ul > li > button").click()
        except Exception as identifier:
            print("Processing Exception:", identifier)

                                            # //*[@id="calendarTable"]/tbody/tr[2]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[3]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[4]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[5]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[6]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[7]/td[7]/a
        # thissaturday, nextsaturday = getSaturday()
        # print(thissaturday, nextsaturday)
        emptys=[]
        for loop in [1, 2]:
            if loop == 2:
                css = '#contents > div.aside > div.calendar_box > div.calendar_paginate_box > ul.calendar_paginate > li.next > a'
                self.browser.find_element_by_css_selector(css).click()
                # self.browser.implicitly_wait(5)
                time.sleep(2)

            weeks = [2,3,4,5,6,7] #주차
            Saturday = 7 #7 토요일
            for week in weeks:
                try:
                    print('======================>', week)
                    path = '//*[@id="calendarTable"]/tbody/tr['+str(week)+']/td['+str(Saturday)+']/a'
                    self.browser.find_element_by_xpath(path).click()
                    time.sleep(1)
                    # self.browser.implicitly_wait(2)
                    # print(click)

                    # time.sleep(5)
                    
            
                    path = '//*[@id="가족캠핑장"]'
                    self.browser.find_element_by_xpath(path).click()
                    time.sleep(1)
                    empty = self.search()
                    emptys.extend(empty)

                    path = '//*[@id="오토캠핑장"]'
                    self.browser.find_element_by_xpath(path).click()
                    time.sleep(1)
                    empty = self.search()
                    emptys.extend(empty)

                    path = '//*[@id="매화나무캠핑장"]'
                    self.browser.find_element_by_xpath(path).click()
                    time.sleep(1)
                    empty = self.search()
                    emptys.extend(empty)


                except Exception as identifier:
                    print("Processing Exception:", identifier)
                    # pass





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

    def search(self):
        emptys = []

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

                empty = CampingItem()
                empty['day']=day
                empty['row']=row
                emptys.append(empty)

        return emptys