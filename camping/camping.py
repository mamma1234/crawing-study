from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from camping.spiders.choansan_spider import ChoansanSpider
from camping.spiders.gangdong_spider import GangdongSpider
from camping.spiders.joongrangsoop_spider import JoongrangsoopSpiderSpider
from camping.spiders.imjingak_spider import ImjingakSpider
from camping.spiders.pyeongtaek_spider import PyeongtaekSpider


from datetime import date
from datetime import timedelta
import calendar

# if __name__ == '__main__':



try:
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    # scheduler.add_job(process.crawl, 'interval', args=[ChoansanSpider], seconds=15)
    # scheduler.add_job(process.crawl, 'interval', args=[GangdongSpider], seconds=10)
    scheduler.add_job(process.crawl, 'interval', args=[JoongrangsoopSpiderSpider], seconds=15)
    # scheduler.add_job(process.crawl, 'interval', args=[ImjingakSpider], seconds=15)
    # scheduler.add_job(process.crawl, 'interval', args=[PyeongtaekSpider], seconds=15)
    scheduler.start()
    process.start(False)
except (KeyboardInterrupt, SystemExit):
    print("stop process")

def getSaturday():
    # today = date.today()
    # print(today)
    # print(today.weekday())
    # offset = (today.weekday() - 5)%7
    # print(offset)
    # print(timedelta(days=offset))

    # last_saturday = today - timedelta(days=offset)
    # print(last_saturday)

    today = date.today()
    thismonth = today.month
    thisyear = today.year
    # nextmonth = today.month +1 if today.month + 1 < 13 else 1

    for month in range(thismonth, thismonth+2):
        cal = calendar.monthcalendar(thisyear, month)

        # print(cal)
        # first_week  = cal[0]
        # second_week = cal[1]
        # third_week  = cal[2]

        for week in cal:
            # print(week[calendar.SATURDAY])
            # print('%3s: %2s' % (calendar.month_abbr[month], week[calendar.SATURDAY]))
            if week[calendar.SATURDAY]:
                print('%2s: %2s' % (str(month).zfill(2), str(week[calendar.SATURDAY]).zfill(2)))
            # for day in week:
                # print(day)
                # if day[calendar.SATURDAY]:
                #     print('%3s: %2s' % (calendar.month_abbr[month], day[calendar.SATURDAY]))
        # If a Saturday presents in the first week, the second Saturday
        # is in the second week.  Otherwise, the second Saturday must 
        # be in the third week.
        
        # if first_week[calendar.SATURDAY]:
        #     holi_day = second_week[calendar.SATURDAY]
        # else:
        #     holi_day = third_week[calendar.SATURDAY]


        # print('%3s: %2s' % (calendar.month_abbr[month], holi_day))


# getSaturday()