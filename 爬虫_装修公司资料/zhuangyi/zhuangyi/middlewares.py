# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
from scrapy import signals
from zhuangyi.proxy import *


class MyproxiesSpiderMiddleware(object):
    # 重写下载中间件，获取ip、删除旧的IP，获取新的IP

    def __init__(self, ip=''):
        self.ip = ip
        self.delete_ip = set()

    def process_request(self, request, spider):
        while len(self.delete_ip) < 5000:
            get_api_content = get_api()
            if get_api_content is None:
                time.sleep(3)
                pass
            else:
                write_ip(get_api_content)
                get_text_ip = reader_ip()
                rd_ip = random_ip(get_text_ip)
                self.delete_ip.add(rd_ip)
                request.meta["proxy"] = "http://" + rd_ip
                # print('---' * 50)
                print("this is ip:" + rd_ip)

    def process_response(self, request, response, spider):
        # 对返回的response处理
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200 and response.status == 403:
            # shibai = response.meta['proxy']
            get_text_ip = reader_ip()
            rd_ip = random_ip(get_text_ip)
            print('--'*50)
            print("this is response ip:" + rd_ip)
            # 对当前reque加上代理
            request.meta['proxy'] = rd_ip
            return request
        return response
        # pass

    # def get_random_proxy(self):
    #     # '''随机从文件中读取proxy'''
    #     while 1:
    #         with open('./ip.txt', 'r') as f:
    #             proxies = f.readlines()
    #         if proxies:
    #             break
    #         else:
    #             time.sleep(1)
    #     proxy = random.choice(proxies).strip()
    #     return proxy

    # def __init__(self, ip=''):
    #     self.ip = ip
    #
    # def process_request(self, request, spider):
    #     thisip = random.choice(IPPOOL)
    #     request.meta["proxy"] = "http://" + thisip["ipaddr"]
    #     # print('---' * 50)
    #     print("this is ip:" + thisip["ipaddr"])


class ZhuangyiSpiderMiddleware(object):
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

        # Should return either None or an iterable of Response, dict
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


class ZhuangyiDownloaderMiddleware(object):
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
