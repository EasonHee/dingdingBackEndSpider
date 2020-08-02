from .items import *
import pymysql
import os
class SriPdfdownloadPipeline:

    def process_item(self, item, spider):
        folder = ''
        if isinstance(item, SriAnnualItem):
            folder = 'sh_annual'
        elif isinstance(item, SriMidItem):
            folder = 'sh_mid'
        elif isinstance(item, SriFirstItem):
            folder = 'sh_first'
        elif isinstance(item, SriThirdItem):
            folder = 'sh_third'

        print('\n', "PipeLine处理SriMidItem : {}".format(item['link']), '\n')
        #文件名
        id = item['link'].split('/')[-1]
        #存放路径
        url = 'F:/pythonprojects/data/{0}/{1}'.format(folder, id)
        with open(url, 'wb') as fp:
            fp.write(item['content'])
