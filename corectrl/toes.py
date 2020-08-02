""""""
import os
import pymysql
import time
from pdf_to_txt import pdf2txt
from es_functions import ReportRemoteEs
from Mysql_functions import ReportLocalDB
from elasticsearch import Elasticsearch
def mysqlfetchalllink(db, table):
    obj = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=db)
    sql = "select link from `{0}`.`{1}`;".format(db, table)
    cursor = obj.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    obj.close()
    return result

def es_getall_links(index):
    es = Elasticsearch(
        ['es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com'],
        http_auth=('elastic', 'HYS526956h'),
        port=9200,
        use_ssl=False
    )

    qbody = {
        "query" : {
            "match_all" : {}
        },
        "_source" : ['link'],
        "size" : 10000
    }

    res_of_es = es.search(index=index, body=qbody)
    dics = res_of_es['hits']['hits']
    links = []
    for dic in dics:
        links.append(dic['_source']['link'])

    return links

def rpt_update():
    tables = ['sh_annual', 'sh_first', 'sh_mid', 'sh_third']
    for table in tables:
        #获取数据库所有内容
        links_db = set(mysqlfetchalllink('sh', table))
        #获取es所有Link内容
        links_es = set(es_getall_links(table))
        links = links_db - links_es
        for link in links:
            url = 'F:/pythonprojects/data/{0}/{1}'.format(table,link.split('/')[-1])
            if os.path.exists(url):
                # 1、pdf转txt
                content = pdf2txt(url=url)
                # 2、确认添加体
                db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='sh')
                cursor = db.cursor()
                sql = 'select * from `{0}`.`{1}` where link = "{2}";'.format('sh', table, link)
                cursor.execute(sql)
                result = cursor.fetchall()[0]
                body = {}
                body['code'] = result[1]
                body['title'] = result[2]
                body['date'] = time.time()
                body['link'] = result[4]
                body['content'] = content
                # 3、添加
                es.add(index=table, body=body)

if __name__ == "__main__":
    links_db = set(mysqlfetchalllink('test', 'sh_annual'))
    links_es = set(es_getall_links('sh_annual'))
    links = links_db - links_es
    print('1' , len(links_db))
    print('2' , len(links_es))
    print(links, len(links))


