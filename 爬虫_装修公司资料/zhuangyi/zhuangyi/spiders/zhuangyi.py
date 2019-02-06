# -*- coding:utf-8 -*-
import random
import re, scrapy
from zhuangyi.items import ZhuangyiItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
# import win_unicode_console
# win_unicode_console.enable()
# 怎么解决IP被限制问题呢？
# http://webapi.http.zhimacangku.com/getip?num=50&type=1&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=3&sb=0&pb=4&mr=1&regions=


class zhuangyi(scrapy.Spider):
    name = 'zhuangyi'
    start_urls = ['http://www.zhuangyi.com/csfz/']
    # start_urls = ['http://0795.zhuangyi.com/zsgs/']
    # start_urls = ['http://www.291988.zhuangyi.com/']
    alloed_domain = ['zhuangyi.com']
    count = 0
    items = ZhuangyiItem()
    just = '深圳'
    company_name = '装一网有限公司'
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）",
        "Mozilla/5.0 (compatible; YodaoBot/1.0;http://www.yodao.com/help/webmaster/spider/;)",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Sogou Pic Spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8;baidu Transcoder)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        " Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729)"
    ]

    # def start_requests(self):           # get_info  get_company
    #     url = 'http://ip.chinaz.com/getip.aspx'
    #     for i in range(1, 4):
    #         yield scrapy.Request(url=url, callback=self.parse, meta={'city_name': self.just,
    #                                                                        'company_name': self.company_name,
    #                                                                        'company_url_page': url.replace('/zsgs/','')})
    #     # for url in self.start_urls:
    #     #     yield scrapy.Request(url=url, callback=self.get_company, meta={'city_name': self.just,
    #     #                                                                    'company_name': self.company_name,
    #     #                                                                    'company_url_page': url.replace('/zsgs/', '')})

    # 获取所有城市  574    紫阳 http://zyx.zhuangyi.com
    def parse(self, response):
        all_city_urls = response.xpath("//div[@id='cl2']/dl/span[@class='ct_main']//dd/a")
        for city_urls in all_city_urls:
            ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
            header = {
                'User-Agent': ua
            }
            # print(city_urls)
            # self.count += 1
            city_url = city_urls.xpath('./@href').extract_first()
            city_name = city_urls.xpath('./text()').extract_first()

            # 排除特殊字符
            if city_name != "更多" and city_url != "javascript:;":
                city_wzurl = city_url + "/zsgs/"
                # print(self.count, city_name, city_url)
                yield scrapy.Request(url=city_wzurl, dont_filter=False, callback=self.get_company,
                                     meta={'city_name': city_name,
                                           'company_url_page': city_url}, errback=self.geterrback, headers=header)
        #         # pass

    # 解析装修公司首页  http://bj.zhuangyi.com/zsgs/        /zsgs/pn-18/
    def get_company(self, response):
        # print(response.url)
        city_name = response.meta['city_name']
        company_url_page = response.meta['company_url_page']
        # 公司名称、URL
        company_html = response.xpath("//ul/li/span[@class='l_txt fl']/p[@class='li_tle']/b/a")
        for company_urls in company_html:
            ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
            header = {
                'User-Agent': ua
            }
            company_name = company_urls.xpath('./text()').extract_first()
            company_url = company_urls.xpath('./@href').extract_first()
            # self.count += 1
            # print(ua)
            # print(self.count, company_name, company_url)
            yield scrapy.Request(url=company_url, dont_filter=False, callback=self.get_info,
                                 meta={'city_name': city_name,
                                       'company_name': company_name}, errback=self.geterrback, headers=header)

        # 翻页
        pages = response.xpath('//div[@class="paginator"]/a[last()-1]/@href').extract_first()
        if pages is None:
            pass
            # print('没有翻页-----------', response.url)
        else:
            ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
            header = {
                'User-Agent': ua
            }
            page = company_url_page + pages
            # print('--' * 65)
            # print(page, company_url_page, pages)
            yield scrapy.Request(url=page, dont_filter=False, callback=self.get_company,
                                 meta={'city_name': city_name,
                                       'company_url_page': company_url_page}, errback=self.geterrback, headers=header)

    def get_info(self, response):
        self.count += 1
        rsp_info = response.url
        # 城市
        city_name = response.meta['city_name']
        # 公司名称
        company_name = response.meta['company_name']

        # 地址
        company_add = response.xpath("//p[@class='s_add']/span/text()").extract_first()

        # 电话
        tels = response.xpath("//div[@class='new_sdcs clear_bor']/p[@class='s_tel s_bor']/text()").extract_first()
        # tel = re.findall(r'(\d{5,12})\s?(.{0,4})|(\d{3}-\d{3}\d{3})', tels)
        # 市辖区
        city_md = re.findall(r'(..区|县)', company_add)
        if len(city_md) == 0:
            city_mdk = 'md_kong'
            # print('--' * 65)
            # print(self.count, rsp_info, city_name, city_mdk, company_add.strip(), company_name, tels)
            self.items['id'] = self.count
            self.items['company_url'] = rsp_info
            self.items['city_name'] = city_name
            self.items['city_md'] = city_mdk
            self.items['company_add'] = company_add.replace('\r\n                ', '')
            self.items['company_name'] = company_name
            self.items['tel'] = tels
            yield self.items
        else:
            # print('**'*85)
            # print(self.count, rsp_info, city_name, city_md[0], company_add.strip(), company_name, tels)
            self.items['id'] = self.count
            self.items['company_url'] = rsp_info
            self.items['city_name'] = city_name
            self.items['city_md'] = city_md[0]
            self.items['company_add'] = company_add.replace('\r\n                ', '')
            self.items['company_name'] = company_name
            self.items['tel'] = tels
            yield self.items

    # 错误处理
    def geterrback(self, failure):
        # pass
        # log all failures
        self.count += 1
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            fromurl = response.meta['city_name']
            self.items['id'] = self.count
            self.items['company_url'] = response.url
            self.items['city_name'] = fromurl  # 解析页面，也就是来源页面
            self.items['city_md'] = 'null'   # 请求页面
            self.items['company_name'] = str(response.status)
            self.items['company_add'] = 'null'
            self.items['tel'] = 'null'
            yield self.items
            print('>>' * 65)
            print('--来源--', fromurl, '--请求--', response.url, '--状态码--', response.status)
            self.logger.error('HTTP请求错误 on %s，状态码%s', response.url, response.status)

        elif failure.check(DNSLookupError):  # 解析域名错误
            # this is the original request
            request = failure.request
            self.items['id'] = self.count
            self.items['company_url'] = request.url
            self.items['city_name'] = request.meta['city_name']
            self.items['city_md'] = 'null'
            self.items['company_name'] = '111111'
            self.items['company_add'] = 'null'
            self.items['tel'] = 'null'
            yield self.items
            self.logger.error('解析错误111111>>>>>>DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):  # 请求超时
            request = failure.request
            self.items['id'] = self.count
            self.items['company_url'] = request.url
            self.items['city_name'] = request.meta['city_name']
            self.items['city_md'] = 'null'
            self.items['company_name'] = '999999'
            self.items['company_add'] = 'null'
            self.items['tel'] = 'null'
            yield self.items
            self.logger.error('请求超时999999》》》》》》TimeoutError on %s', request.url)
