# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from scrapy import signals
import fake_useragent
import requests
import json
import random
import os
import time

class SriScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SriScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    #随机跟换user-agent
    def __init__(self,crawler):
        super(RandomUserAgentMiddleware,self).__init__()
        self.ua = fake_useragent.UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')#从setting文件中读取RANDOM_UA_TYPE值

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):  ###系统电泳函数
        def get_ua():
            return getattr(self.ua,self.ua_type)
        # user_agent_random=get_ua()
        request.headers.setdefault('User-Agent',get_ua())
        pass


class ChangeProxy(object):
    #运行这一部分代码就已经把ip地址改变了
    def __init__(self):
        #get_url为申请Ip的APi接口
        self.get_url= 'http://120.79.85.144/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=0&fa=0&dt=0&groupid=0&fetch_key=&qty=4&time=1&port=1&format=json&ss=5&css=&dt=0&pro=&city=&usertype=6'
        #通过访问temp_url测试申请Ip有效性
        self.temp_url = 'http://www.sse.com.cn/disclosure/listedinfo/regular/'
        #IP池
        self.ip_list = []
        #选用Ip在Ip池中的位置
        self.ip_pos = 0
        #定时器
        self.pre = time.time()
        self.late = time.time()

    def getIPData(self):
        '''这部分获得ip值，先清空原有的ip值'''
        temp_data = requests.get(url=self.get_url).text
        #输出请求到的ip列表
        print(json.loads(temp_data))
        #将申请到的Ip逐个放入IP池
        for eve_ip in json.loads(temp_data)["data"]:
            self.ip_list.append({
                "ip" : eve_ip["IP"],
                "port" : eve_ip["Port"],
            })
        #迭代申请
        if (len(self.ip_list) < 3):
            self.getIPData()

    def changeProxy(self, request):
        ''' 修改代理ip'''
        #在IP池中随机获取一个ip
        r = random.random()
        self.ip_pos = (int)(r * len(self.ip_list))
        request.meta['proxy'] = 'http://' + str(self.ip_list[self.ip_pos]["ip"]) + ':' \
                                + str(self.ip_list[self.ip_pos]["port"])

    def process_request(self, request, spider):
        self.late = time.time()
        if len(self.ip_list) < 3:
            time.sleep(2)
            self.getIPData()
        elif self.late - self.pre > 600:
            self.pre = self.late
            self.ip_list.clear()
            self.getIPData()


class SeleniumStocksscrapyaderMiddlewDownloare(object):

    def process_request(self, request, spider):
        driver = spider.driver
        time.sleep(1)
        page_text = driver.page_source

        return HtmlResponse(url=driver.current_url, body=page_text, encoding='utf8', request=request)