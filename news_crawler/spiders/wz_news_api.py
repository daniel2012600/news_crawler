# -*- coding: utf-8 -*-
import scrapy
import time # 引入time
from scrapy.exceptions import CloseSpider
from ..settings import DEFAULT_REQUEST_HEADERS
from pathlib import Path
import re


class WzNewsApiSpider(scrapy.Spider):
    name = 'wz_news_api'
    id_value = 32290 # 預設爬取ＩＤ

    def __init__(self):
        self.time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.url = f"https://pwa.zhibo16.live/pwa-api/index.php?g=H5&m=News&a=newsDetail&_={self.time_trans(self.time_params)}"

    def start_requests(self):
        log_dir = Path('./logs/')
        last_craw_id = self.check_log_data(log_dir)
        # 檢視是否有上次爬取的ＩＤ·若沒有則用預設的
        self.id_value = int(last_craw_id) if last_craw_id != '' else self.id_value
        
        yield scrapy.FormRequest(self.url, formdata={ 'id': str(self.id_value)  }, headers =  DEFAULT_REQUEST_HEADERS )

    def parse(self, response):
        print("######################")
        print(f"目前爬的ＩＤ：{self.id_value}")
        print("######################")
        resource_json = response.json()   
        if resource_json['data']['detail']['post_title'] != '':
            # 建立容器·將要擷取的資訊放進去
            NewsCrawlerItem = {
            "id" : self.id_value,
            "news_title" : resource_json['data']['detail']['post_title'],
            "title_pic" : resource_json['data']['detail']['smeta']['thumb'],
            "news_content" : resource_json['data']['detail']['post_content'],
            "publish_date" : resource_json['data']['detail']['publishtime']
            }
            yield NewsCrawlerItem

        else:
            # 確認沒有爬到底了·則關閉爬蟲
            self.logger.error(f"最後爬取ＩＤ：{self.id_value}")
            raise CloseSpider('close it')

        self.id_value += 1
        yield scrapy.FormRequest(self.url, formdata={ 'id': str(self.id_value)  }, callback = self.parse , dont_filter = True, headers =  DEFAULT_REQUEST_HEADERS)

    # 轉換日期格式至UNIX
    def time_trans(self, qurey_date):
        struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        return time_stamp

    # 爬取前確定ＬＯＧ是否有上次爬取的ＩＤ
    def check_log_data(self, log_dir):
        last_craw_id = ''
        try:
            if log_dir.exists():
                # 確定此次爬蟲是否為當天首次爬蟲·如果是就去看看前一天爬的是否有最後爬取的ＩＤ
                with open(Path(list(log_dir.iterdir())[-1]),'r') as f:
                    last_craw_data = f.readlines()
                    r = re.compile(".*最後爬取ＩＤ：")
                    newlist = list(filter(r.match, last_craw_data)) 
                    if newlist:
                        last_craw_id = newlist[-1].split('最後爬取ＩＤ：')[-1]
                    else:
                        with open(Path(list(log_dir.iterdir())[-2]),'r') as f:
                            last_craw_data = f.readlines()     
                            newlist = list(filter(r.match, last_craw_data)) 
                            last_craw_id = newlist[-1].split('最後爬取ＩＤ：')[-1] 
        except:
            pass            

        return last_craw_id

