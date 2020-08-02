# -*- coding: utf-8 -*-
import scrapy
import pymysql
import os
from SRI_pdfdownload.items import *

def mysqlfetchalllink(db, table):
    obj = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=db)
    cursor = obj.cursor()
    sql = "select link from `{0}`.`{1}`;".format(db, table)
    cursor.execute(sql)
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    obj.close()
    return result

class ShSpiderSpider(scrapy.Spider):
    name = 'sh_spider'

    def start_requests(self):
        # 获取下载链接
        links_of_annual = mysqlfetchalllink('sh', 'sh_annual')
        links_of_first = mysqlfetchalllink('sh', 'sh_first')
        links_of_mid = mysqlfetchalllink('sh', 'sh_mid')
        links_of_third = mysqlfetchalllink('sh', 'sh_third')
        tables = []
        tables.append(links_of_annual)
        tables.append(links_of_first)
        tables.append(links_of_mid)
        tables.append(links_of_third)

        mapping = {
            0 : "sh_annual",
            1 : "sh_first",
            2 : "sh_mid",
            3 : "sh_third"
        }

        mapping2 = {
            0 : self.parse0,
            1 : self.parse1,
            2 : self.parse2,
            3 : self.parse3
        }
        for cnt, table in zip(range(0, 4), tables):
            for link in table:
                id = link.split('/')[-1]
                if not os.path.exists('F:/pythonprojects/data/{0}/{1}'.format(mapping[cnt], id.strip())):
                    yield scrapy.Request(url=link, callback=mapping2[cnt], dont_filter=True)

    def parse0(self, response):
        item = SriAnnualItem()
        item['content'] = response.body
        item['link'] = response.url
        yield item

    def parse1(self, response):
        item = SriFirstItem()
        item['content'] = response.body
        item['link'] = response.url
        yield item

    def parse2(self, response):
        item = SriMidItem()
        item['content'] = response.body
        item['link'] = response.url
        yield item

    def parse3(self, response):
        item = SriThirdItem()
        item['content'] = response.body
        item['link'] = response.url
        yield item

