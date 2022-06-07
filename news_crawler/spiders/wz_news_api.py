# -*- coding: utf-8 -*-
import scrapy
import time # 引入time
from scrapy.exceptions import CloseSpider
import json
from scrapy.http import JsonRequest
from ..settings import DEFAULT_REQUEST_HEADERS

class WzNewsApiSpider(scrapy.Spider):
    name = 'wz_news_api'
    id_value = 32080
    
    def __init__(self):
        self.lastime_cawler_date = "2022-05-12 14:02:00"
        self.time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.url = f"https://pwa.zhibo16.live/pwa-api/index.php?g=H5&m=News&a=newsDetail&_={self.time_trans(self.time_params)}"

    def start_requests(self):
        yield scrapy.FormRequest(self.url, formdata={ 'id': str(self.id_value)  }, headers =  DEFAULT_REQUEST_HEADERS )

    def parse(self, response):
       
        resource_json = response.json()   
        
        if resource_json['data']['detail']['post_title'] != '':
            # 用發布日期判斷新聞是否已經爬過了
            publishtime = resource_json['data']['detail']['publishtime']
            print(publishtime)
            if self.time_trans(self.lastime_cawler_date) < self.time_trans(publishtime):
                NewsCrawlerItem = {
                "id" : self.id_value,
                "news_title" : resource_json['data']['detail']['post_title'],
                "title_pic" : resource_json['data']['detail']['smeta']['thumb'],
                "news_content" : resource_json['data']['detail']['post_content'],
                "publish_date" : publishtime
                }

                yield NewsCrawlerItem
            else:
                pass
        else:
            raise CloseSpider('close it')


        self.id_value += 1

        yield scrapy.FormRequest(self.url, formdata={ 'id': str(self.id_value)  }, callback = self.parse , dont_filter = True)

    # 轉換日期格式至UNIX
    def time_trans(self, qurey_date):
        struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        return time_stamp

