import os
import time
import pymysql
import smtplib
import zipfile
from email.header import Header  # 定义邮件标题
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart

def send_email(exchange, session, lists, receiver, keyword1, keyword2):
    ''' file_path为要邮件发送的文件路径, receiver为用户邮箱'''
    try:
        table = exchange + '_' + session
        now = time.strftime("%Y-%m-%d", time.localtime())

        user = "13336130340@163.com"
        password = "hys526956h"
        smtpserver = 'smtp.163.com'
        sender = "13336130340@163.com"
        receive = receiver

        # 邮件对象:
        msg = MIMEMultipart()
        msg['From'] = "13336130340@163.com"
        msg['To'] = receiver
        msg['Subject'] = Header("【帮我盯着】{}最新报表".format(now), 'utf-8').encode()

        #文字内容
        message = MIMEText('    [帮我盯着]\n    您的搜索关键词为:\n        '
                           '关键词1:{0}\n        关键词2:{1}\n'.format(keyword1, keyword2) +
                           '        替您找到与相关的文件,已放到附件中，可点击下载\n', 'plain', 'utf-8')


        #附件内容
        zip = zipfile.ZipFile('帮我盯着.zip', 'w', zipfile.ZIP_DEFLATED)
        zip.close()

        if lists:
            for list in lists:

                file_path = "F:/pythonprojects/data/{}/".format(table) + list['link'].split('/')[-1].strip()

                if os.path.exists(file_path):

                    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=exchange)
                    cursor = db.cursor()
                    sql = "select * from {0} where link = '{1}'".format(table, list['link'].strip())
                    cursor.execute(sql)
                    ll = cursor.fetchall()[0]
                    db.close()

                    zip = zipfile.ZipFile('帮我盯着.zip', 'a', zipfile.ZIP_DEFLATED)
                    zip.write(file_path, ll[1] + ll[2] + '.pdf')
                    zip.close()

            content = open("帮我盯着.zip", 'rb').read()
            filemsg = MIMEBase("application", 'zip')
            filemsg.set_payload(content)
            encode_base64(filemsg)
            filemsg.add_header('Content-Disposition', 'attachment', filename="{}最新报表".format(now) + '.zip')

            #添加
            msg.attach(filemsg)
            msg.attach(message)

            #发送
            smtp = smtplib.SMTP_SSL(smtpserver, 465)
            smtp.helo(smtpserver)
            smtp.ehlo(smtpserver)  # 服务器返回结果确认
            smtp.login(user, password)  # 登录邮箱服务器用户名和密码
            print("开始发送邮件...")
            smtp.sendmail(sender, receive, msg.as_string())
            smtp.quit()
            print("邮件发送完成！")

            return True

        else:
            print("传递的链接信息无内容\n")
            return False

    except Exception as e:
        print("Exception", e)


if __name__ == "__main__":
    lists = [{
        "link" : "http://www.sse.com.cn/disclosure/listedinfo/announcement/c/2020-07-16/603039_20200716_4.pdf",
    }, {
        "link" : "http://www.sse.com.cn/disclosure/listedinfo/announcement/c/2020-07-15/600179_20200715_7.pdf"
    }]
    send_email('sh', 'annual', lists, "384746875@qq.com", "key1", "key2")


















    # if lists:
    #     for list in lists:
    #
    #         file_path = r"F:/pythonprojects/data/{}/".format(table) + list['link'].split('/')[-1].strip()
    #
    #         if os.path.exists(file_path):
    #             content = open(file_path, 'rb').read()  # 读取内容
    #             filemsg = MIMEBase("application", 'zip')
    #             filemsg.set_payload(content)
    #             encode_base64(filemsg)
    #
    #             db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=exchange)
    #             cursor = db.cursor()
    #             sql = "select * from {0} where link = '{1}'".format(table, list['link'].strip())
    #             cursor.execute(sql)
    #             ll = cursor.fetchall()[0]
    #             db.close()
    #             msg['Subject'] = Header("【帮我盯着】{}".format(ll[1] + ll[2]), 'utf-8').encode()
    #
    #             filemsg.add_header('Content-Disposition', 'attachment', filename=ll[1] + ll[2] + '.zip')
    #
    #             msg.attach(filemsg)
    #             msg.attach(message)
    #
    #         else:
    #             print("pdf文件仍未下载\n")
    #             return False