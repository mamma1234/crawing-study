# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

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
        # if week[calendar.THURSDAY]:
        #     print('%2s: %2s' % (str(thismonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
        #     thissaturday.append({'year':thisyear, 'month': thismonth, 'day':week[calendar.THURSDAY], 'day2':week[calendar.FRIDAY]})

        if week[calendar.SATURDAY]:
            thissaturday.append({'year':thisyear, 'month': thismonth, 'day':week[calendar.SATURDAY], 'day2':week[calendar.SUNDAY]})

    cal = calendar.monthcalendar(nextyear, nextmonth)
    for week in cal:
        if week[calendar.SATURDAY]:
            # print('%2s: %2s' % (str(nextmonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            nextsaturday.append({'year':nextyear, 'month': nextmonth, 'day':week[calendar.SATURDAY], 'day2':week[calendar.SUNDAY]})

    return thissaturday, nextsaturday

class CampunakSpider(scrapy.Spider):
    name = 'campunak_spider'
    allowed_domains = ['www.campunak.co.kr']
    start_urls = ['https://www.campunak.co.kr/login.aspx?reurl=/Reservation2/Reservation_Site.aspx']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('C:\\github\\chromedriver.exe')


    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(1)


        self.browser.find_element_by_xpath('//*[@id="ContentMain_txtUserID"]').send_keys('mamma1234@naver.com')
        self.browser.find_element_by_xpath('//*[@id="ContentMain_txtUserPW"]').send_keys('7PhLU!LBr6d9Cn@')
        self.browser.find_element_by_xpath('//*[@id="ContentMain_btnMemberLogin"]').click()
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="txtMemberTel"]')) 
        )

        self.browser.get('https://www.campunak.co.kr/Reservation2/Reservation_Site.aspx')
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/div[5]')) 
        )  
        # time.sleep(5)

        print("data:", getSaturday())

        thissaturday, nextsaturday = getSaturday()
        thissaturday.extend(nextsaturday)
        now=date.today()

        emptys=[]
        for saturday in thissaturday:
            rflag = True
            try:
                print('saturday:', saturday)
                # print( now.year, now.month, now.day)
                if saturday['year'] >= now.year and saturday['month'] >= now.month and saturday['day'] >= now.day:
                    print('now over')
                else:
                    continue

                day = str(saturday['year'])+"-"+str(saturday['month']).zfill(2)+"-"+str(saturday['day']).zfill(2)
                day2 = str(saturday['year'])+"-"+str(saturday['month']).zfill(2)+"-"+str(saturday['day2']).zfill(2)
                self.browser.execute_script("document.getElementById('ContentMain_txtSdate').setAttribute('value','"+day+"')")
                self.browser.execute_script("document.getElementById('ContentMain_txtEdate').setAttribute('value','"+day2+"')")
                # self.browser.execute_script("__doPostBack('ctl00$ContentMain$txtSdate','')")
                self.browser.find_element_by_xpath('//*[@id="ContentMain_btnSearch"]').click()


                try:
                    alert = self.browser.switch_to.alert
                    alert.accept()
                    rflag = False
                except Exception as identifier:
                    print("Processing Exception:", identifier)  
                    pass

                print('rflag', rflag)

                if rflag == True:
                    # time.sleep(5)
                    empty = self.search(day)
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
                # pass

        print('--------------------------------------------')
        print('emptys:', emptys)
        print('--------------------------------------------')

        if len(emptys) == 0:
            self.browser.quit()
        return emptys
        # pass

    def search(self, day):
        emptys = []

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        
        groups = selector.xpath('//*[@id="ContentMain_divSiteOption"]/div[@class="site_choice"]')

# A, B 사이트 제외
        for group in groups[2:]:
            # print('group', group.extract())
            rows = group.xpath('ul/a')
            # print('rows', rows)
            
            try:
                for row in rows:
                    # print('row', row)
                    # row.select

                    alt = row.xpath('@href').extract()
                    id = row.xpath('@id').extract()
                    # print(alt, ":", id)
                    # if "시설 약도" not in alt[0] and "예약완료" not in alt[0]:
                    #     # emptys.append({'day':day, 'row': row})

                    if len(alt) > 0:
                        empty = CampingItem()
                        empty['day']=day
                        empty['group']=id[0] #group
                        empty['row']=alt
                        emptys.append(empty)

                        self.browser.execute_script(alt[0])
                        # print('data', empty)

                        element = WebDriverWait(self.browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="ContentMain_divRsrv"]')) 
                        )

                        self.browser.find_element_by_xpath('//*[@id="ContentMain_divRsrv"]/div[4]/label').click()
                        self.browser.find_element_by_xpath('//*[@id="ContentMain_divRsrv"]/div[5]/label').click()

                        # self.browser.find_element_by_xpath('//*[@id="ContentMain_btnPayNow"]').click()


                        time.sleep(5)

                        return emptys
            except Exception as identifier:
                print("Processing Exception:", identifier)
                pass

            # self.browser.switch_to.default_content()
        
        return emptys