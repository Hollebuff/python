# -*- coding:utf-8 -*-
import re, scrapy, random, time
import requests
import xlrd
from mganji.items import MganjiItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
# import win_unicode_console
# win_unicode_console.enable()
# 代理IP爬虫优质版，实现获取最新代理IP请求页面，并过滤掉不合格、失效代理IP
# 2018年9月29日


class ganji(scrapy.Spider):
    name = 'mganji'
    # start_urls = ['https://3g.ganji.com/foshan_zhuangxiu/', 'https://3g.ganji.com/zunyi_zhuangxiu/']
    alloed_domain = ['ganji.com']
    items = MganjiItem()
    count = 0
    user_agent_list = [
        "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m1 metal Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; m1 metal Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7",
        "Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
        "Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3",
        "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3",
        "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 5X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.2",
        "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 5.1; OPPO R9tm Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)",
        "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.1.1)",
        "Mozilla/5.0 (Linux; Android 6.0; MX6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; PRO 6 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 5.1; OPPO R9tm Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)",
        "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.4.950 Mobile Safari/537.36"

    ]
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': '3g.ganji.com'
    }

    def start_requests(self):           # get_info  get_company
        path = 'E:/爬虫_装修公司资料/赶集网装修公司.xlsx'
        # 打开Excel
        workbook = xlrd.open_workbook(path)
        data_sheet = workbook.sheets()[0]  # 通过索引获取
        # 尝试获取5行看看 (9, 11) 获取：第9行、第10行
        for row_list in range(301, 360):
            rows = data_sheet.row_values(row_list)  # 获取第n行数据
            city_company_url = rows[2]
            nub = rows[3]
            ua = random.choice(self.user_agent_list)
            self.header['User-Agent'] = ua
            yield scrapy.Request(url=city_company_url, callback=self.get_company, headers=self.header,
                                 meta={'nub': nub}, errback=self.geterrback, dont_filter=False)

    def get_company(self, response):
        rsp_url = response.url
        ua = random.choice(self.user_agent_list)
        nub = response.meta['nub']
        self.header['User-Agent'] = ua
        company_htmls = response.xpath('//div[@class="server fuwu-list-quick"]')
        for company_html in company_htmls:
            company_urls = company_html.xpath('./a[1]/@href').extract_first()
            tels = company_html.xpath('./a[2]/@href').extract_first()
            company_url = 'https:' + company_urls
            # if re.search(r'.*?end=end$', company_url):
            #     pass
            # else:
            tel = tels.replace('tel:', '')
            # print(self.count, company_url, tel)
            yield scrapy.Request(url=company_url, callback=self.get_info, headers=self.header,
                                 meta={'tel': tel}, errback=self.geterrback, dont_filter=False)

        # 翻页
        page_html = response.xpath('//a[@class="page-down"]/@href').extract_first()
        print(page_html)
        if len(page_html) > 0:
            page = 'https://3g.ganji.com' + page_html
            page_nubs = page_html.split('/')
            page_nub = page_nubs[3].replace('o', '')
            # print(nub, page_nubs, page_nub, page_html, page)
            if int(nub) > int(page_nub):
                self.header['Referer'] = rsp_url
                yield scrapy.Request(url=page, callback=self.get_company, headers=self.header,
                                     meta={'nub': nub}, errback=self.geterrback, dont_filter=False)
            else:
                print('超过限定页面数', page_nub)

    # 信息
    def get_info(self, response):
        company_url = response.url
        self.count += 1
        # 城市名
        city_name = response.xpath('//a[@class="city-change city-change-active"]/span/text()').extract_first()

        company_adds = response.xpath('//div[@class="business-info"]/table'
                                      '//tr/th[contains(text(), "店铺地址")]/following-sibling::td/text()').extract_first()
        company_add = company_adds.replace('-', '').replace(' ', '')
        linkman = response.xpath('//div[@class="business-info"]/table'
                                 '//tr/th[contains(text(), "联系人")]/following-sibling::td/text()').extract_first()
        tel = response.meta['tel']
        # company_name = response.xpath('//div[@class="car-tit"]/text()').extract_first()

        company_h1 = response.xpath('//h1/text()').extract_first()
        xinxi_name_html = response.xpath('//span[@class="portion"]/text()').extract_first()
        pattern = u"[\u4e00-\u9fa5]{4,12}公司|[\u4e00-\u9fa5]{4,12}公司有限公司|" \
                  u"[\u4e00-\u9fa5]{3,12}装饰 |[\u4e00-\u9fa5]{2,6}装饰设计工程有限公司|[\u4e00-\u9fa5]{2,8}装饰设计有限公司"
        regex = re.compile(pattern)
        # 信息介绍
        if company_h1 is None:
            if xinxi_name_html is None:
                company_namea = 'company_nam_kong'
                # print('无信息、无h1', 'aa' * 60)
                # print(self.count, company_url, city_name, company_add, company_namea, linkman, tel)
                self.items['id'] = self.count
                self.items['company_url'] = company_url
                self.items['city_name'] = city_name
                self.items['company_add'] = company_add
                self.items['company_name'] = company_namea
                self.items['linkman'] = linkman
                self.items['tel'] = tel
                yield self.items
                pass
            else:
                company_reg = regex.findall(xinxi_name_html)
                if len(company_reg) == 0:
                    company_nameb = 'company_nam_kong'
                    # print('有信息找不到、无h1', 'bb' * 60)
                    # print(self.count, company_url, city_name, company_add, company_nameb, linkman, tel)
                    self.items['id'] = self.count
                    self.items['company_url'] = company_url
                    self.items['city_name'] = city_name
                    self.items['company_add'] = company_add
                    self.items['company_name'] = company_nameb
                    self.items['linkman'] = linkman
                    self.items['tel'] = tel
                    yield self.items
                    pass
                else:
                    company_named = '|'.join(company_reg)
                    # print('有信息找到、无h1', 'cc' * 60)
                    # print(self.count, company_url, city_name, company_reg, company_add, company_named, linkman, tel)
                    self.items['id'] = self.count
                    self.items['company_url'] = company_url
                    self.items['city_name'] = city_name
                    self.items['company_add'] = company_add
                    self.items['company_name'] = company_named
                    self.items['linkman'] = linkman
                    self.items['tel'] = tel
                    yield self.items
                    pass
        else:
            # print('有h1', 'dd' * 60)
            # print(self.count, company_url, city_name, company_add, company_h1, linkman, tel)
            self.items['id'] = self.count
            self.items['company_url'] = company_url
            self.items['city_name'] = city_name
            self.items['company_add'] = company_add
            self.items['company_name'] = company_h1
            self.items['linkman'] = linkman
            self.items['tel'] = tel
            yield self.items
            pass

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
            # fromurl = response.meta['city_name']
            self.items['id'] = self.count
            self.items['company_url'] = response.url
            self.items['city_name'] = 'null'  # 解析页面，也就是来源页面
            self.items['company_add'] = 'null'
            self.items['company_name'] = str(response.status)
            self.items['linkman'] = 'null'
            self.items['tel'] = 'null'
            yield self.items
            print('>>' * 65)
            print('--来源--', '--请求--', response.url, '--状态码--', response.status)
            self.logger.error('HTTP请求错误 on %s，状态码%s', response.url, response.status)

        elif failure.check(DNSLookupError):  # 解析域名错误
            # this is the original request
            request = failure.request
            self.items['id'] = self.count
            self.items['company_url'] = request.url
            self.items['city_name'] = 'null'
            self.items['company_add'] = 'null'
            self.items['company_name'] = '111111'
            self.items['linkman'] = 'null'
            self.items['tel'] = 'null'
            yield self.items
            self.logger.error('解析错误111111>>>>>>DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):  # 请求超时
            request = failure.request
            self.items['id'] = self.count
            self.items['company_url'] = request.url
            self.items['city_name'] = 'null'
            self.items['company_add'] = 'null'
            self.items['company_name'] = '999999'
            self.items['linkman'] = 'null'
            self.items['tel'] = 'null'
            yield self.items
            self.logger.error('请求超时999999》》》》》》TimeoutError on %s', request.url)
