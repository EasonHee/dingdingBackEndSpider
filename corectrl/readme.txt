V1.0
1、
完成es_funcitons中的ReportRemoteEs类，
是连接远程elasticsearch的类，暂时完成的是查找功能，
    def search(self, index, title_code="", content="",content_max_length=300, link="",
               start='', size='10', highlight=True, raw = False):
               raw=True返回es返回的数据， raw=False返回处理后的数据

               需要调整的地方：try, exception

2、完成Mysql的添加和查找，
    def findall(self, db, table): //返回表中所有内容
    def find(self, db, table, condition):   //condition为sql语言 where给出条件
    def add(self, db, table, insert_content):   //添加的内容 还没有测试
    add测试成功
3、def an_rpt_updata(cir_bg_time):   //cir_bg_time为每次循环的开始时间，用于判断是否有新数据加入数据库
    成功测试将数据加入到远程es的test索引


V1.1
1、爬虫的功能
动态爬取网页内容，先点击进入到特定页面，获取页面数据，若这些内容不在本地的数据库中，则将它们爬取下来，如果已经存在于
本地的数据库中，则说明接下来的内容，在之前的爬取中，就已经爬取到了，则停止运行。
2、获取pdf部分功能
获取响应数据库中的所有记录，对比每一条记录，若本地没有此pdf文件则进行下载，若有则查看下一个
3、es函数
通过传递的时间参数，可知是否有新的数据进入数据库，则尝试更新到es
判断本地是否有此pdf和es是否已经有相应的内容，若本地有且远程没有，则进行转换
4、盯着
将所有的关键词信息提取出来，逐个进行es查找，如果找到，则通过比较时间字段，判断是否为新到数据,若是
则放到列表中，之后针对这个列表进行发邮件

BUG的地方：如果es更新时，pdf文件不存在怎么办?
盯着：若es的更新出现问题，记录存在数据库中，不存在es中，则会导致，部分数据错过时间后，就不可能再发给用户。

待改进：
爬虫直接爬全部，根据标题字段进行分类
getpdf部分也可以进行整合到一起
toes也可以整合到一起

