import pymysql

class ReportLocalDB():

    def __init__(self, db, user="root", password="123456", port=3306, host="localhost"):
        self.db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
        self.cursor=self.db.cursor()

    #增
    def add(self, db, table, insert_content):
        try:
            sql = "insert into `{0}`.`{1}`".format(db, table)
            sql = sql + insert_content
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            print("数据库添加失败\n")

    #删
    def delete(self):
        pass

    #改
    def updata(self, db, table, set, condition):
        result = None
        try:
            sql = "UPDATE `{0}`.`{1}`".format(db, table)   #SET `title_code` = '山' WHERE `id` = '9';
            sql += set + condition
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            return False

        return True

    #查
    def findall(self, db, table):
        try:
            sql = "select * from `{0}`.`{1}`".format(db, table)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            print("查找表所有数据失败")

    def find(self, db, table, condition):
        try:
            sql = "select * from `{0}`.`{1}`".format(db, table)
            sql = sql+condition
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as e:
            print("Exception", e)
            print("查找单个数据失败\n")

        return False


if __name__ == "__main__":
    obj = ReportLocalDB("fromfrontend")
    result = obj.find('fromfrontend', 'keywordsinfo', condition='')
    print(result)