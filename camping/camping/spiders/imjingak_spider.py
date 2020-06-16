# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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


class ImjingakSpider(scrapy.Spider):
    name = 'imjingak_spider'
    allowed_domains = ['reservation.nowonsc.kr']
    start_urls = ['http://imjingakcamping.co.kr/resv/res_01.html']
    reserve_urls = ['http://imjingakcamping.co.kr/resv/res_02.html']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('C:\\github\\chromedriver.exe')

    def parse(self, response):
        self.browser.get(response.url)
        # time.sleep(2)

        # html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        # selector = Selector(text=html)

        # self.browser.implicitly_wait(3)

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
                # css = '#contents > div > div.cal_wrap > div.item_month > a.btn_cal.next'
                # self.browser.find_element_by_css_selector(css).click()
                # self.browser.implicitly_wait(5)
                thissaturday = nextsaturday
                time.sleep(1)
            
            for saturday in thissaturday:
                try:
                    print('===========================', saturday, '=======================')
                    day = saturday

                    # print(self.start_urls)
                    # str(saturday.month).zfill(2)
                    # http://imjingakcamping.co.kr/resv/res_01.html?checkdate=2020-06-20
                    path = self.start_urls[0]+'?checkdate='+str(saturday['year'])+'-'+ str(saturday['month']).zfill(2)+'-'+ str(saturday['day']).zfill(2)
                    self.browser.implicitly_wait(3)
                    self.browser.get(path)
                                
                    # path = '//*[@id="contents"]/div//span/a[@data-date="'+str(saturday['year'])+'-'+ str(saturday['month']).zfill(2)+'-'+ str(saturday['day']).zfill(2)+'"]'
                    # self.browser.find_element_by_xpath(path).click()
                    
                    time.sleep(1)

                    html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
                    selector = Selector(text=html)

                    # time.sleep(5)


                    element = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.ID, "ijgFoot"))
                    )
                    
                    text1 = selector.xpath('//*[@id="contents"]/div/div[4]/table/tbody/tr/td[1]/text()').extract()
                    text2 = selector.xpath('//*[@id="contents"]/div/div[4]/table/tbody/tr/td[2]/text()').extract()
                    text6 = selector.xpath('//*[@id="contents"]/div/div[4]/table/tbody/tr/td[5]/text()').extract()

        # site_ph = //*[@id="contents"]/div/div[8]/div[1]/button[2]
        # site_hl = //*[@id="contents"]/div/div[8]/div[1]/button[3]
        
                        # //*[@id="site_ph"]/div[1]/span
                        # //*[@id="site_hl"]/div[1]/span
                        # //*[@id="site_rca"]/div[1]
                        # self.browser.execute_script('openSite(event, \'site_ph\')')

                        # //*[@id="contents"]/div/div[8]/div[1]/button[2]

                    place1 = text1[0].split('/')[0].strip()
                    if place1 != '0':
                        # print(text1[0].split('/')[0].strip())
                        empty = self.search(day, '평화캠핑존', 'site_ph', '//*[@id="contents"]/div/div[8]/div[1]/button[2]')
                        if len(empty) > 0:
                            emptys.extend(empty)

                            return emptys
                            


                    place2 = text2[0].split('/')[0].strip()
                    if place2 != '0':
                        # print(text2[0].split('/')[0].strip())
                        empty = self.search(day, '힐링캠핑존', 'site_hl', '//*[@id="contents"]/div/div[8]/div[1]/button[3]')
                        if len(empty) > 0:
                            emptys.extend(empty)

                            return emptys

                    # place6 = text6[0].split('/')[0].strip()
                    # if place6 != '0':
                    #     # print(text6[0].split('/')[0].strip())
                    #     empty = self.search(day, '렌탈캠핑존 A', 'site_rca', '//*[@id="contents"]/div/div[8]/div[1]/button[6]')   
                    #     if len(empty) > 0:
                    #         emptys.extend(empty)

                    #         return emptys

                    # return None

                    # path = '//*[@id="td-2020-06-25"]'
                    # self.browser.find_element_by_xpath(path).click()
                    # day = path

                    # groups=[]
                    # groups.append({'group':"village01", 'start': 39, 'end':66})
                    # groups.append({'group':"village02", 'start': 66, 'end':72})
                    # groups.append({'group':"village03", 'start': 72, 'end':91})
                    # groups.append({'group':"village04", 'start': 91, 'end':94})

                    # for group in groups:
                    #     empty = self.search(day, group["group"], group["start"], group["end"])
                    
                    if len(emptys) > 0:
                        print('--------------------------------------------')
                        print('emptys:', emptys)
                        print('--------------------------------------------')
                        # pass
                        return emptys


                except Exception as identifier:
                    print("Processing Exception:", identifier)
                    pass

        time.sleep(1)
        print('--------------------------------------------')
        print('emptys:', emptys)
        print('--------------------------------------------') 
        if len(emptys) == 0:
            self.browser.quit()
        return emptys


    def search(self, day, group, zone, button):
        emptys = []
        print('---------------------->>', day, '**',button)

        self.browser.find_element_by_xpath(button).click()
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )  
        # time.sleep(3)

        

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)

        rows = selector.xpath('//*[@id="'+zone+'"]/div')

        # print(rows)
        
        for row in rows:
            # print(row)
            spantext = row.xpath('span/text()').extract()
            print(day, zone, spantext)

            if len(spantext) == 0:
                inputid = row.xpath('input/@id').extract()
                inputvalue = row.xpath('input/@value').extract()
                print(inputid, inputvalue)

                
                empty = CampingItem()
                empty['day']=day
                empty['group']=group
                empty['row']=inputvalue
                emptys.append(empty)

                # check = self.browser.find_element_by_id(inputid[0])
                # if check.get_attribute("checked") == "true":
                #     check.click()
                    
                # 동의 버튼
                self.browser.find_element_by_xpath('//*[@id="contents"]/div/div[7]/label').click() 
                element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.ID, "contents"))
                ) 
                self.browser.implicitly_wait(1)
                

                # self.browser.find_element_by_xpath('//*[@id="site_rca"]/div[2]/label[@for="rc_a_02"]').click()
                # self.browser.find_element_by_xpath('//*[@id="site_rca"]/div[2]/label').click()
                # self.browser.find_element_by_xpath('//*[@id="site_rca"]/div/lable[@for="rc_a_02"]').click()
                self.browser.find_element_by_xpath('//*[@id="'+zone+'"]/div[@class="check_comn '+inputvalue[0]+'"]/label[@for="'+inputvalue[0]+'"]').click()
                element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.ID, "reservForm"))
                ) 
                self.browser.implicitly_wait(1)

                # 인원수
                select = Select(self.browser.find_element_by_xpath('//*[@id="reservForm"]/div[1]/div/table/tbody/tr[1]/td[4]/select'))
                # select.selectByVisibleText("Banana");
                select.select_by_index(4)
                # 예약버튼
                self.browser.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[9]/div[2]/button').click()
                element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.ID, "order_info"))
                ) 
                self.browser.implicitly_wait(1)


                # self.browser.findElement(By.name("r_name")).sendKeys("박대규")		
                # self.browser.findElement(By.name("r_hp")).sendKeys("01022610993")		
                # self.browser.findElement(By.name("r_email")).sendKeys("박대규")		
                # self.browser.findElement(By.name("r_jumin1")).sendKeys("박대규")		
                # self.browser.findElement(By.name("r_car[]")).sendKeys("박대규")		

                self.browser.find_element_by_name("r_name").send_keys('박대규')
                self.browser.find_element_by_name("r_hp").send_keys('01022610993')
                self.browser.find_element_by_name("r_email").send_keys('mamma1234@naver.com')
                self.browser.find_element_by_name("r_jumin1").send_keys('750911')
                self.browser.find_element_by_name("r_car[]").send_keys('275주6654')


                self.browser.find_element_by_xpath('//*[@id="order_info"]/div[13]/label').click()
                self.browser.find_element_by_xpath('//*[@id="order_info"]/div[15]/label').click()
                self.browser.find_element_by_xpath('//*[@id="order_info"]/div[16]/label').click()

                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.username[name='username'][placeholder='Enter your username']"))).send_keys("Gen Tan")

                # //*[@id="reservForm"]/div[1]/div/table/tbody/tr[1]/td[4]/select/option[5]

                # select = Select(self.browser.find_element_by_xpath('//*[@id="reservForm"]/div[1]/div/table/tbody/tr[1]/td[4]/select'))
                # # select.selectByVisibleText("Banana");
                # select.selectByIndex(4)
                
                # self.browser.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[9]/div[2]/button').click()


                # self.browser.find_element_by_xpath('//*[@id="contents"]/div/div[7]/label/em').click()

                    # //*[@id="site_rca"]/div[2]
                # self.browser.find_element_by_css_selector('//*[@id="site_rca"]/div[2]/label').click()
                # selenium.check("//input[@name=’checkboxes[]’ and @value=’cb3’]");

                
                # self.browser.find_element_by_css_selector('//*[@id="site_rca"]/div[2]/label').click()
                # self.browser.find_element_by_css_selector("input[type='checkbox'][value='rc_a_02']").click()
                # self.browser.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[7]/div[2]/input').click()
                # self.browser.find_element_by_xpath('//*[@id="'+zone+'"]/div//*[@id="rc_a_02"]').click()
                # self.browser.find_element_by_xpath('//*[@id="'+inputid[0]+'"]').click()
                # self.browser.implicitly_wait(5)
                # time.sleep(20)

                return emptys

        return emptys