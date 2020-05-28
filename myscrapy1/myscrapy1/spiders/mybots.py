# -*- coding: utf-8 -*-
import scrapy
import time
from myscrapy1.items import Myscrapy1Item
from selenium import webdriver
from scrapy.selector import Selector

class MybotsSpider(scrapy.Spider):
    name = 'mybots'
    # start_urls = ['http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=732/']
    # allowed_domains = ['news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=732']
    # start_urls = ['http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=732']
    allowed_domains = ['premierleague.com']
    start_urls = ['https://www.premierleague.com/tables?co=1&se=42&mw=-1&ha=-1']


    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('C:\\github\\chromedriver.exe')


    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        rows = selector.xpath('//*[@id="mainContent"]/div/div[1]/div[3]/div/div/table/tbody/tr[not(@class="expandable")]')
        self.browser.quit()
 
        items=[]        
        for row in rows:
            item = Myscrapy1Item()
            item['title']=row.xpath('./td[3]/a/span[2]/text()')[0].extract()
            item['author']=row.xpath('./td[2]/span[1]/text()')[0].extract()
            item['preview']=row.xpath('./td[4]/text()')[0].extract()
            items.append(item)
 
        print(items)
        print('parse finish@@@@@@@@@@@@@@@@@@@')
        return items

    def parse_back(self, response):
        # pass
        titles=response.xpath('//*[@id="main_content"]/div[2]/ul/li/dl/dt[2]/a/text()').extract()
        authors=response.css('.writing::text').extract()
        previews=response.css('.lede::text').extract()
        
        items=[]
        for itemidx in range(len(titles)):
            item=Myscrapy1Item()
            item['title']=titles[itemidx].strip()
            item['author']=authors[itemidx].strip()
            item['preview']=previews[itemidx].strip()
            items.append(item)

        print('parse finish@@@@@@@@@@@@@@@@@@@')
        return items
