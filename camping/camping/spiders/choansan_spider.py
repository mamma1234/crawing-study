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
        # THURSDAY
        if week[calendar.SATURDAY]:
            # print('%2s: %2s' % (str(thismonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            thissaturday.append({'year':thisyear, 'month': thismonth, 'day':week[calendar.SATURDAY]})

    cal = calendar.monthcalendar(nextyear, nextmonth)
    for week in cal:
        if week[calendar.SATURDAY]:
            # print('%2s: %2s' % (str(nextmonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            nextsaturday.append({'year':nextyear, 'month': nextmonth, 'day':week[calendar.SATURDAY]})

    return thissaturday, nextsaturday


class ChoansanSpider(scrapy.Spider):
    name = 'choansan_spider'
    allowed_domains = ['reservation.nowonsc.kr']
    start_urls = ['https://reservation.nowonsc.kr/member/login']
    reserve_urls = ['https://reservation.nowonsc.kr/leisure/camping_date?cate1=2']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('C:\\github\\chromedriver.exe')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(2)
        # self.browser.implicitly_wait(3)
        
        self.browser.find_element_by_id("memberId").send_keys('mamma1234')
        self.browser.find_element_by_id("memberPassword").send_keys('qkrghwls0!')
        self.browser.find_element_by_css_selector("button[type='submit'].btn").click()
        # self.browser.get(self.reserve_urls)
        time.sleep(1)
        self.browser.implicitly_wait(3)
        self.browser.get('https://reservation.nowonsc.kr/leisure/camping_date?cate1=2')
        # time.sleep(3)
                                            # //*[@id="calendarTable"]/tbody/tr[2]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[3]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[4]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[5]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[6]/td[7]/a
                                            # //*[@id="calendarTable"]/tbody/tr[7]/td[7]/a
        thissaturday, nextsaturday = getSaturday()
        # print(thissaturday, nextsaturday)
        emptys=[]
            # 당월의 토요일 구하기
            # 다음달의 토요일 구하기
        # for loop in [2]:
        for loop in [1, 2]:
            if loop == 2:
                css = '#frm > div.cnt_wrap2 > div.left_menu > div.calendar_box2.type2.pj2 > div > div > div.clndr-control-button.rightalign'
                self.browser.find_element_by_css_selector(css).click()
                # self.browser.implicitly_wait(5)
                thissaturday = nextsaturday
                time.sleep(1)
            
            for saturday in thissaturday:
                try:
                    print('===========================', saturday, '=======================')

                    # str(saturday.month).zfill(2)
                    path = '//*[@id="td-'+str(saturday['year'])+'-'+ str(saturday['month']).zfill(2)+'-'+ str(saturday['day']).zfill(2)+'"]'
                    self.browser.find_element_by_xpath(path).click()
                    time.sleep(1)
                    # path = '//*[@id="td-2020-06-25"]'
                    # self.browser.find_element_by_xpath(path).click()
                    day = path

                    groups=[]
                    groups.append({'group':"village01", 'start': 39, 'end':66})
                    groups.append({'group':"village02", 'start': 66, 'end':72})
                    groups.append({'group':"village03", 'start': 72, 'end':91})
                    groups.append({'group':"village04", 'start': 91, 'end':94})

                    for group in groups:
                        empty = self.search(day, group["group"], group["start"], group["end"])
                        if len(empty) > 0:
                            emptys.extend(empty)

                        if len(emptys) > 0:
                            print('--------------------------------------------')
                            print('emptys:', emptys)
                            print('--------------------------------------------')
                            # pass
                            return emptys

                except Exception as identifier:
                    print("Processing Exception:", identifier)
                    pass


        # css = '#frm > div.cnt_wrap2 > div.left_menu > div.calendar_box2.type2.pj2 > div > div > div.clndr-control-button.rightalign'
        # self.browser.find_element_by_css_selector(css).click()
        # time.sleep(1)

        # for saturday in nextsaturday:
        #     try:
        #         print('===========================', saturday, '=======================')

        #         # str(saturday.month).zfill(2)
        #         path = '//*[@id="td-'+str(saturday['year'])+'-'+ str(saturday['month']).zfill(2)+'-'+ str(saturday['day']).zfill(2)+'"]'
        #         self.browser.find_element_by_xpath(path).click()
        #         time.sleep(1)
        #         # path = '//*[@id="td-2020-06-25"]'
        #         # self.browser.find_element_by_xpath(path).click()
        #         day = path

        #         group = "village01"
        #         start = 39
        #         end = 66
        #         empty = self.search(day, group, start, end)
        #         emptys.extend(empty)

        #         group = "village02"
        #         start = 66
        #         end = 72
        #         empty = self.search(day, group, start, end)
        #         emptys.extend(empty)

        #         group = "village03"
        #         start = 72
        #         end = 91
        #         empty = self.search(day, group, start, end)
        #         emptys.extend(empty)

        #         group = "village04"
        #         start = 91
        #         end = 94
        #         empty = self.search(day, group, start, end)
        #         emptys.extend(empty)

        #     except Exception as identifier:
        #         print("Processing Exception:", identifier)
        #         pass

        time.sleep(1)
        print('--------------------------------------------')
        print('emptys:', emptys)
        print('--------------------------------------------') 
        if len(emptys) == 0:
            self.browser.quit()
        return emptys


    def search(self, day, group, start, end):
        emptys = []
        print('---------------------->>', day, '**',group)
        self.browser.find_element_by_id(group).click()
        time.sleep(1)
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)

        prefix = ""
        test = '//*[@id="m_chk_'+str(start)+'"]/@data-cseq'
        check = selector.xpath(test).extract()
        if len(check) > 0:
            prefix = "m_"

        # print('prefix:',prefix)

        # self.browser.find_element_by_id(prefix+'chk_39').check()
        # time.sleep(1)
        # self.browser.find_element_by_id(prefix+'chk_39').click()
        # time.sleep(1)
        
        # self.browser.find_element_by_css_selector("input#"+prefix+"chk_39").click() 
        # time.sleep(1)
        # self.browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/form/div[1]/div[2]/div[2]/div/ul/li[1]/input').click()
        # self.browser.find_element_by_xpath('//*[@id="reserved_submit"]').click()
        # self.browser.find_element_by_xpath('//[@id="'+prefix+'chk_'+str(start)+'"]').check()
        # self.browser.find_elements_by_xpath("//input[@type='radio' and @id='"+prefix+"chk_"+str(start)+"']")[0].click()
        #m_chk_39

        for n in range(start, end): #39 ~ 65
            try:
                # print(n)
                path = '//*[@id="'+prefix+'chk_'+str(n)+'"]/@data-cseq'
                # print(path)
                rows = selector.xpath(path).extract()
                # print(rows)
                path2 = '//*[@id="'+prefix+'chk_'+str(n)+'"]/@disabled'
                rows2 = selector.xpath(path2).extract()

                path3 = '//*[@id="'+prefix+'chk_'+str(n)+'"]/@value'
                rows3 = selector.xpath(path3).extract()
                print(rows3, len(rows3))
                # print(rows2, len(rows2) )
                if len(rows2) < 1:
                    empty = CampingItem()
                    empty['day']=day
                    empty['group']=group
                    empty['row']=rows[0]
                    emptys.append(empty)
                    

                    self.browser.find_element_by_css_selector("input[type='radio'][value='"+rows3[0]+"']").click()
                    # self.browser.find_element_by_id(prefix+'chk_'+str(n)).click()
                    # self.browser.find_element_by_xpath('//[@id="'+prefix+'chk_'+str(n)+'"]').click()
                    self.browser.find_element_by_xpath('//*[@id="reserved_submit"]').click()
                    alert = self.browser.switch_to.alert
                    alert.accept()
                    # print('emptys:', emptys)
                    
                    # time.sleep(1)
                    return emptys
            except Exception as identifier:
                print("Processing Exception:", identifier)
                pass        

        return emptys