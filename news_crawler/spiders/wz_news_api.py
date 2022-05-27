import scrapy
import time # 引入time

class WzNewsApiSpider(scrapy.Spider):
    name = 'wz_news_api'
    allowed_domains = ['pwa.zhibo16.live']
    start_urls = [f'https://pwa.zhibo16.live/pwa-api/index.php?']

    def parse(self, response):
        # g=H5&m=News&a=newsDetail&_={self.time_trans(time_params)}

        pass
    # 轉換日期格式至UNIX
    def time_trans(qurey_date):
        struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        return time_stamp
