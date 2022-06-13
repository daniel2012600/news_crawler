
# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy.utils.misc
import scrapy.core.scraper


from news_crawler.spiders import wz_news_api
import news_crawler.items
import news_crawler.settings
import news_crawler.middlewares
import news_crawler.pipelines
import time
from pathlib import Path
import re
import pymysql



def warn_on_generator_with_return_value_stub(spider, callable):
    pass

scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub

scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub



if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(wz_news_api.WzNewsApiSpider) 
    process.start()