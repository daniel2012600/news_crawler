# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from news_crawler import settings
import pymysql

class NewsCrawlerPipeline:

    def __init__(self):
 
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DATABASE,
            user=settings.MYSQL_USERNAME,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8'
        )
 
        self.cursor = self.connect.cursor()
 
    def process_item(self, item, spider):
        try:
            ret = self.cursor.fetchone()
            if ret :
                print(item['news_title']+'***********資料重複！***************')
            else:
                        
                sql = 'INSERT INTO new_table(id, news_title, title_pic, news_content, publish_date)VALUES(%s,%s,%s,%s,%s) '
        
                data = (item['id'], item['news_title'], item['title_pic'], item['news_content'], item['publish_date'])
        
                self.cursor.execute(sql, data)
        
                return item
        except Exception as error:
            print('error')

    def close_spider(self, spider):
        self.connect.commit()
        self.connect.close()