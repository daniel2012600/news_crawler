import scrapy
import time # 引入time
from scrapy.exceptions import CloseSpider
import json

class WzNewsApiSpider(scrapy.Spider):
    name = 'wz_news_api'
    id_value = 31885

    def start_requests(self):
        time_params = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        url = f"https://pwa.zhibo16.live/pwa-api/index.php?g=H5&m=News&a=newsDetail&_={self.time_trans(time_params)}"
        print(self.id_value)
        yield scrapy.Request(url, method="POST", body=json.dumps({'id': self.id_value}) )

    def parse(self, response):

        resource_json = response.json()
        print("==============")
        print(resource_json)
        
        if resource_json['data']['detail']['post_title'] != '':
            # 用發布日期判斷新聞是否已經爬過了
            publishtime = resource_json['data']['detail']['publishtime']
            print("==============")
            print(publishtime)
            print(resource_json['data']['detail']['post_title'])
            print(self.id_value)
            print("==============")
            # if time_trans(lastime_cawler_date) < time_trans(publishtime):
                # data['id'] = self.id_value
                # data['news_title'] = resource_json['data']['detail']['post_title']
                # data['title_pic'] = resource_json['data']['detail']['smeta']['thumb']
                # data['news_content'] = resource_json['data']['detail']['post_content']
                # data['publish_date'] = publishtime
                # news_data.append(data)
            # else:
            #     pass
        else:
            print(2222222222222222)
            raise CloseSpider('close it')


        self.id_value += 1
        print(self.id_value)
        print("==============")

    # 轉換日期格式至UNIX
    def time_trans(self, qurey_date):
        struct_time = time.strptime(qurey_date, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        return time_stamp
