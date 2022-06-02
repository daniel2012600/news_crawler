# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    id = scrapy.Field()
    news_title = scrapy.Field()
    title_pic = scrapy.Field()
    news_content = scrapy.Field()
    publish_date = scrapy.Field()
