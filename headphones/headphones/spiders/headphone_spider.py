# -*- coding: utf-8 -*-
import scrapy


class HeadphoneSpiderSpider(scrapy.Spider):
    name = 'headphone_spider'
    allowed_domains = ['https://www.amazon.com/s/ref=nb_sb_noss_2']
    start_urls = ['https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=headphones&rh=i%3Aaps%2Ck%3Aheadphones&ajr=2']

    def parse(self, response):
        img_urls = response.css('img::attr(src)').extract()
        with open('urls.txt', 'w') as f:
            for u in img_urls:
                f.write(u + "\n")
