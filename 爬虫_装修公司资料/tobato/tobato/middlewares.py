# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils import defer
from twisted.internet.error import ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone
from tobato.test import *
logger = logging.getLogger(__name__)
# 请求超时的IP，直接替换掉，需要提高代码可用性、请求超时的处理未完善……
# 需要验证最新请求的代理iP是不是用刚刚请求api获取的？


class MyproxiesSpiderMiddleware(object):
    # 一些异常情况汇总
    EXCEPTIONS_TO_CHANGE = (
        defer.TimeoutError, TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost,
        TCPTimedOutError, ConnectionDone)

    def __init__(self, ip=''):
        self.ip = ip
        self.reader_path = 'E:/爬虫_装修公司资料/tobato/iplist.txt'
        self.proxys = reader_ip(self.reader_path)
        self.delete = set()

    def process_request(self, request, spider):
        # print(self.delete)
        # thisip = random_ip(self.proxys)
        thisip = random_ip(self.proxys[-20:])
        while thisip in self.delete:
            print('失效代理IP-----------aaa', thisip)
            # thisip = random_ip(self.proxys)
            thisip = random_ip(self.proxys[-5:])
            if thisip not in self.delete:
                print('正常代理IP-----------zzz', thisip)
                request.meta["proxy"] = "http://" + thisip
                break
        else:
            print("当前代理ip this is ip:" + thisip)
            request.meta["proxy"] = "http://" + thisip

    def process_response(self, request, response, spider):
        # 对返回的response处理
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            rsp_deleip = request.meta['proxy']
            self.delete.add(rsp_deleip)
            thisip = random_ip(self.proxys[-5:])
            # thisip = random_ip(self.proxys)
            print(response.status, '被拒绝访问--------------')
            if thisip in self.delete:
                print('失效代理IP------------age', thisip)
                pass
            else:
                print('--'*50)
                logger.warning("状态码非200，重新请求")
                print("this is response ip:" + thisip)
                # 对当前request加上代理
                request.meta['proxy'] = "https//" + thisip
                return request
        return response

    def process_exception(self, request, exception, spider):
        # 其他一些timeout之类异常判断后的处理，ip不可用删除即可
        if isinstance(exception, self.EXCEPTIONS_TO_CHANGE) and request.meta.get('proxy', False):
            delete_url = request.meta['proxy'].replace('http://', '')
            self.delete.add(delete_url)
            print("+++++++++++++++++++++++++{}不可用将被删除++++++++++++++++++++++++".format(delete_url))
            logger.debug("该代理Proxy {}失效或者请求超时{}.".format(request.meta['proxy'], exception))
            return request.replace(dont_filter=True)


class TobatoSpiderMiddleware(object):
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


class TobatoDownloaderMiddleware(object):
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
