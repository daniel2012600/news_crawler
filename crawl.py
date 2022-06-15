
# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
import scrapy.utils.misc
import scrapy.core.scraper

from news_crawler.spiders.wz_news_api import WzNewsApiSpider
from news_crawler import items
from news_crawler import settings
from news_crawler import middlewares
from news_crawler import pipelines
import time
import os
import re
import pymysql
from datetime import datetime

def warn_on_generator_with_return_value_stub(spider, callable):
    pass

scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub

if __name__ == '__main__':
    # 建立log資料夾
    today = datetime.now()
    file_name = f"wz_news_{today.year}_{today.month}_{today.day}.log"
    # 啟動 scrapy 爬蟲
    process = CrawlerProcess({
        'BOT_NAME': settings.BOT_NAME ,
        'SPIDER_MODULES': settings.SPIDER_MODULES,
        'NEWSPIDER_MODULE':settings.NEWSPIDER_MODULE,
        'ROBOTSTXT_OBEY':False,
        'DOWNLOAD_DELAY':0.20,
        'LOG_FILE': f"./logs/{file_name}",
        'LOG_LEVEL' : 'ERROR',
        'ITEM_PIPELINES': {
            'news_crawler.pipelines.NewsCrawlerPipeline': 300,
            }
        })

    process.crawl(WzNewsApiSpider) 
    process.start()