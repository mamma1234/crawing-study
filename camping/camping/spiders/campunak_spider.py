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
        if week[calendar.SATURDAY]:
            # print('%2s: %2s' % (str(thismonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            thissaturday.append({'year':thisyear, 'month': thismonth, 'day':week[calendar.SATURDAY]})

    cal = calendar.monthcalendar(nextyear, nextmonth)
    for week in cal:
        if week[calendar.SATURDAY]:
            # print('%2s: %2s' % (str(nextmonth).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            nextsaturday.append({'year':nextyear, 'month': nextmonth, 'day':week[calendar.SATURDAY]})

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
        time.sleep(5)

        # self.browser.switch_to_frame(0)
        # self.browser.find_element_by_xpath('//*[@id="ContentMain_txtSdate"]').click()
        
        # self.browser.find_element_by_name('ctl00$ContentMain$txtSdate').click()
        date = self.browser.find_element_by_xpath("//div[@class='input _date-depart']/div[@class='ui-calendar']/input").click()

        # self.browser.find_element_by_xpath('//*[@id="ContentMain_txtSdate"]').send_keys('06192020')
        # self.browser.find_element_by_xpath('//*[@id="ContentMain_txtSdate"]').send_keys('06')
        # self.browser.find_element_by_xpath('//*[@id="ContentMain_txtSdate"]').send_keys('19')
        time.sleep(5)
        # self.browser.find_element_by_xpath('//*[@id="ContentMain_txtEdate"]').send_keys('06202020')


        # time.sleep(5)


        # self.browser.find_element_by_xpath('//*[@id="ContentMain_aSite"]').click()
        # element = WebDriverWait(self.browser, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/div[5]')) 
        # )  


        time.sleep(5)




        main_window_handle = self.browser.current_window_handle

        self.browser.find_element_by_xpath('//*[@id="imgLogin"]').click()
        element = WebDriverWait(self.browser, 20).until(
            # EC.presence_of_element_located((By.ID, "loginWrap"))
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginAllWrap"]/div[2]/iframe[starts-with(@src, "https://accounts.interpark.com/authorize/ticket-pc")]'))
            
        )  
        self.browser.switch_to_frame(0)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[starts-with(@src, 'http://thunder/spidio.net/CF9F4DA6B7533431/devinfo/devdect')]")))

#loginAllWrap > div.leftLoginBox > iframe
# https://accounts.interpark.com/authorize/ticket-pc?origin=https%3A%2F%2Fticket%2Einterpark%2Ecom%2FGate%2FTPLoginConfirmGate%2Easp%3FGroupCode%3D%26Tiki%3D%26Point%3D%26PlayDate%3D%26PlaySeq%3D%26HeartYN%3D%26TikiAutoPop%3D%26BookingBizCode%3D%26MemBizCD%3DWEBBR%26CPage%3DB%26GPage%3Dhttp%253A%252F%252Fticket%252Einterpark%252Ecom%252F&postProc=IFRAME
        # time.sleep(5)
        self.browser.find_element_by_xpath('/html/body/form[1]/div/div/div[1]/ul/li[1]/div/input').send_keys('mamma0911')
        self.browser.find_element_by_xpath('//*[@id="userPwd"]').send_keys('qkrghwls0!')
        self.browser.find_element_by_xpath('//*[@id="btn_login"]').click()

        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "DT_Rarea"))
        )  
        self.browser.find_element_by_xpath('/html/body/div[9]/div[2]/div[3]/div/div[2]/div/div[2]/div[5]/a').click()

        
        signin_window_handle = None
        while not signin_window_handle:
            for handle in self.browser.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break
        self.browser.switch_to.window(signin_window_handle)

        self.browser.find_element_by_xpath('//*[@id="divBookNotice"]/div/div/span/a/img').click()


        # thissaturday, nextsaturday = getSaturday()

        emptys=[]
        # for loop in [2]:
        for loop in [1, 2]:
            if loop == 2:
                css = '#BookingDateTime > a'
                self.browser.find_element_by_css_selector(css).click()
                # self.browser.implicitly_wait(5)
                # thissaturday = nextsaturday
                time.sleep(1)

            weeks = [1,2,3,4,5] #주차
            Saturday = 5 #7 토요일
            for week in reversed(weeks):
                try:
                    print('======================>', week)
                    
                    path = '//*[@id="BookingDateTime"]/div/table/tbody/tr['+str(week)+']/td['+str(Saturday)+']/a'
                    self.browser.find_element_by_xpath(path).click()
                    time.sleep(1)

                    select = Select(self.browser.find_element_by_xpath('//*[@id="SelectCheckIn"]'))
                    # select.selectByVisibleText("Banana");
                    select.select_by_index(1)
                    element = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="SeatRemainNotice"]/dl[1]'))
                    )  

                    

                    # self.browser.implicitly_wait(2)
                    # print(click)

                    # time.sleep(5)
                    empty = self.search()
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

    def search(self):
        emptys = []

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)

        
        emptycnt1 = selector.xpath('//*[@id="SeatRemainNotice"]/dl[1]/dd/em/text()').extract()
        emptycnt2 = selector.xpath('//*[@id="SeatRemainNotice"]/dl[2]/dd/em/text()').extract()
        
        print(emptycnt1, emptycnt2)

        if emptycnt1 != '0' or emptycnt2 != '0':
            day = selector.xpath('//td/a[@id="CellPlayDate" and @class="selOn"]/@onclick').extract()
            print(day)
            # print('click =============>', day[0], '<=============')
            # rows = selector.xpath('//*[@id="contents"]/div[3]/div[2]/div/img/@alt').extract()
            
            
            # groups = [1,2,3,4]
            groups = [1]
            for group in groups:
                # self.browser.switch_to.default_content()
                self.browser.switch_to_frame('ifrmSeat')

                self.browser.find_element_by_xpath('//*[@id="Map"]/area['+str(group)+']').click()
                element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="MainMap"]'))
                )  
                self.browser.switch_to.default_content()
                self.browser.switch_to_frame('ifrmSeat')

                html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
                selector = Selector(text=html)
                rows = selector.xpath('/html/body/table/tbody/tr/td/div/div/img[@class="stySeat"]')
                # rows = selector.xpath('/html/body/table/tbody/tr/td/div/div/img[@class="stySelectSeat"]')

                
                try:
                    for row in reversed(rows):
                        print(row)
                        # row.select

                        alt = row.xpath('@alt').extract()
                        # id = row.xpath('@id').extract()
                        # print(alt, ":", id)
                        # if "시설 약도" not in alt[0] and "예약완료" not in alt[0]:
                        #     # emptys.append({'day':day, 'row': row})

                        empty = CampingItem()
                        empty['day']=day
                        empty['group']=group
                        empty['row']=alt
                        emptys.append(empty)
        # //*[@id="SID0"]
                        # self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td/div/div/img[@class="stySelectSeat"] and @id="'+str(id)+'"]').click()
                        self.browser.find_element_by_xpath('//*[@id="map"]/img[@class="stySeat" and @alt="'+alt[0]+'"]').click()                
                        self.browser.find_element_by_xpath('//*[@id="NextStepImage"]').click()
                        # element = WebDriverWait(self.browser, 10).until(
                        #     EC.presence_of_element_located((By.XPATH, '//*[@id="layer1"]'))
                        # )  
                        time.sleep(2)
                        element = WebDriverWait(self.browser, 10).until(
                            EC.visibility_of_element_located((By.ID, "divBookStep"))
                        #     EC.presence_of_element_located((By.ID, "divBookStep"))
                        # #     EC.presence_of_element_located((By.XPATH, '//*[@id="ifrmBookStep"]'))
                        )
                        self.browser.switch_to.default_content()
                        self.browser.switch_to_frame('ifrmBookStep') #ifrmBookStep
                        # self.browser.find_element_by_xpath('//*[@id="PriceType"]').click()
                        self.browser.find_element_by_css_selector("input[type='radio'][value='1']").click()
                        # self.browser.find_element_by_xpath('//*[@id="li1"]/span[1]/label').click()
                        # self.browser.find_element_by_xpath('//*[@id="PriceType"]').click()
                        
                        self.browser.find_element_by_xpath('//*[@id="NextStepImage"]').click()
                        time.sleep(2)
                                                        
                                                        

                        # return emptys
                except Exception as identifier:
                    print("Processing Exception:", identifier)
                    pass

                # self.browser.switch_to.default_content()
            
        return emptys