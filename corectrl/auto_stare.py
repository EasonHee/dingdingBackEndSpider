import time
from Mysql_functions import ReportLocalDB
from es_functions import ReportRemoteEs
from deliver_email import send_email
""""""""""""""""""""""上证"""""""""""""""""""""""

#年报
class Monitor():

    def monitor(self):

        try:
            #获取数据库存放所有 盯着功能 关键字信息
            obj = ReportLocalDB("fromfrontend")
            results = obj.find("fromfrontend", "keywordsinfo", condition='')

            #查找
            for result in results:

                #连接远程es
                remotees = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                                          http_auth=('elastic', "HYS526956h"), index='test')

                #查找
                body = {
                    "index" : "",
                    "title_code" : "",
                    "content" : "",
                }
                body['index'] = result[1] + "_" + result[2]
                body["title_code"] = result[3]
                body["content"] = result[4]

                responses = remotees.search(index=body['index'], title_code=body["title_code"], content=body["content"])
                print(responses)

                list = []
                for response in responses:
                    if response['date'] > float(result[6]):
                        list.append(response)

                # 发送
                if list and send_email(result[1], result[2], list, result[7], result[3], result[4]):
                    # 数据库修改
                    set = "SET update_date={}".format(time.time())
                    condition = "where id={}".format(result[0])
                    obj.updata('fromfrontend', 'keywordsinfo', set, condition)

        except Exception as e:
            print("Exception", e)

if __name__ == "__main__":
    remotees = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                              http_auth=('elastic', "HYS526956h"), index='test')
