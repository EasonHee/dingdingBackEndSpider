import pymysql
from .items import *


class SriScrapyPipeline:

    def __init__(self):

        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='sh')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        print('\n---------------理应写入一个数据数据库----------------\n')

        # 年报表 (id, code, title, date, link)
        if isinstance(item, SriAnnualItem):
            try:
                sql = "insert into sh.sh_annual(`code`, `title`, `date`, `link`) values(%s,%s,%s,%s);"
                self.cursor.execute(sql, (item['code'], item['title'], item['date'], item['link']))
                self.db.commit()
                return item
            except:
                print("pipeline SriAnnualItem存入数据库失败\n")

        # 中报表 (id, code, title, date, link)
        elif isinstance(item, SriMidItem):
            try:
                sql = "insert into sh.sh_mid(`code`, `title`, `date`, `link`) values(%s,%s,%s,%s);"
                self.cursor.execute(sql, (item['code'], item['title'], item['date'], item['link']))
                self.db.commit()
                return item
            except:
                print("pileline SirmidItem存入数据库失败\n")
        else:
            return item


    def close_spider(self, spider):
        self.db.close()