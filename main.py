from data_crawler.stockSelect import selectStock
from data_crawler.crawlStock import crawlDailyStock
from data_crawler.getDateforCrawl import dateforGetData
from datetime import datetime

today = datetime.today().strftime(format="%Y%m%d")
todayWeek = datetime.today().weekday()+1 #抓出今日星期

datelist = dateforGetData(todayWeek, today)
dfStock = crawlDailyStock(datelist)


print(selectStock(dfStock, datelist))
