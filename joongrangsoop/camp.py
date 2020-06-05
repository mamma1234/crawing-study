from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from joongrangsoop.spiders.joongrangsoop_spider import JoongrangsoopSpiderSpider
from joongrangsoop.spiders.joongrangsoop2_spider import Joongrangsoop2SpiderSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[Joongrangsoop2SpiderSpider], seconds=10)
scheduler.start()
process.start(False)
