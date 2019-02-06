# -*- coding:utf-8 -*-
import re, scrapy, random, xlrd
import time
from tobato.items import TobatoItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
# import win_unicode_console
# win_unicode_console.enable()
# 代理ip失效处理参考文章：
# https://blog.csdn.net/xudailong_blog/article/details/80153387
# https://blog.csdn.net/qq_33854211/article/details/78535963
# https://blog.csdn.net/sc_lilei/article/details/80702449
# https://blog.csdn.net/on_the_road_2018/article/details/80985524


class totato(scrapy.Spider):
    name = 'tobato'
    # start_urls = ['http://www.to8to.com/index.html']
    # start_urls = ['http://bj.to8to.com/company/']
    # start_urls = ['http://kunshan.to8to.com/company/']
    # start_urls = ['http://fs.to8to.com/zs/8617777/']
    # , 'http://shenz.qizuang.com/company/', 'http://wh.qizuang.com/company/'
    alloed_domain = ['to8to.com']
    count = 0
    # just = '北京'
    items = TobatoItem()
    # company_name = '北京xxx有限公司'
    header = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.5",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]

    def start_requests(self):           # get_info  get_company     'company_name': self.company_name,
        path = 'E:/爬虫_装修公司资料/土巴兔装修公司.xlsx'
        count = 0
        # 打开Excel
        workbook = xlrd.open_workbook(path)
        data_sheet = workbook.sheets()[1]  # 通过索引获取
        # 尝试获取5行看看 (9, 11) 获取：第9行、第10行
        for row_list in range(1, 2):
            # count += 1
            rows = data_sheet.row_values(row_list)  # 获取第n行数据
            city_name = rows[1]
            city_company_url = rows[2]
            page_nub = rows[3]
            host_url = rows[4]
            ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
            self.header['User-Agent'] = ua
            self.header['Host'] = host_url
            # self.header['Referer'] = referer
            # for url in self.start_urls:
            yield scrapy.Request(url=city_company_url, callback=self.get_company,
                                 meta={'city_name': city_name,
                                       'page_nub': page_nub,
                                       'city_referer_url': city_company_url,
                                       'host_url': host_url}, errback=self.geterrback, headers=self.header)

    # 获取所有城市
    def parse(self, response):
        all_citys = response.xpath("//div[@class='cs_zs']/div[@class='xzcs_dt']/a")
        for all_city in all_citys:
            ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
            header = {
                'User-Agent': ua
            }
            # self.count += 1
            # 城市名称
            city_name = all_city.xpath("./text()").extract()[0]
            # 城市链接
            city_url = all_city.xpath("./@href").extract()[0]
            company_url = city_url + 'company/'
            yield scrapy.Request(url=company_url, dont_filter=False, callback=self.get_company,
                                 meta={'city_name': city_name, 'rsp_page': company_url}, errback=self.geterrback, headers=header)
            # print(self.count, city_name, company_url)

    # 解析公司列表
    def get_company(self, response):
        rsp_get_companyurl = response.url
        ua = random.choice(self.user_agent_list)  # 随机抽取User-Agent
        rsp_city_referer_url = response.meta['city_referer_url']
        host_url = response.meta['host_url']
        self.header['Host'] = host_url
        self.header['User-Agent'] = ua
        self.header['Referer'] = rsp_city_referer_url
        # 翻页限制
        rsp_page = response.meta['page_nub']
        res_meta = response.meta['city_name']
        # res_company = response.meta['rsp_page']
        # 装修公司 全称、URL、 电话
        company_urls = response.xpath("//ul[@class='company-data-list']/li[@class='company-data ']/a")
        for jt_company_urls in company_urls:
            company_name = jt_company_urls.xpath("./div[@class='company__data']/p[@class='company__name']/span/text()").extract_first()
            jt_company_url = jt_company_urls.xpath('./@href').extract_first()
            company_tel_ft = jt_company_urls.xpath("./div[@class='company__data']/p[@class='company__phone']/text()").extract_first()
            if company_tel_ft is None:
                company_tels = 'tel_kong'
                # self.count += 1
                pass
                # print(self.count, res_meta, company_name, jt_company_url, company_tels)
                yield scrapy.Request(url=jt_company_url, dont_filter=False, callback=self.get_info,
                                     meta={'city_name': res_meta,
                                           'company_name': company_name,
                                           'company_tel': company_tels}, errback=self.geterrback, headers=self.header)
            else:
                # self.count += 1
                pass
                company_tel = company_tel_ft.replace('-', "")
                # print(self.count, res_meta, company_name, jt_company_url, company_tel)
                yield scrapy.Request(url=jt_company_url, dont_filter=False, callback=self.get_info,
                                     meta={'city_name': res_meta,
                                           'company_name': company_name,
                                           'company_tel': company_tel}, errback=self.geterrback, headers=self.header)
        # 翻页
        company_pages = response.xpath("//div[@class='pages']/a[last()]")
        for pages in company_pages:
            self.header['Referer'] = rsp_get_companyurl
            page_href = pages.xpath('./@href').extract_first()
            page_text = pages.xpath('./text()').extract_first()
            page_urla = page_href.rsplit('company/')
            page_url = page_urla[1].replace('list_', '').replace('.html', '')
            if int(page_url) < int(rsp_page):
                # print(page_text)
                if page_text == '下一页':
                    # print('翻页', page_href)
                    pass
                    # print(company_pages)
                    yield scrapy.Request(url=page_href, dont_filter=False, callback=self.get_company,
                                         meta={'city_name': res_meta,
                                               'page_nub': rsp_page,
                                               'city_referer_url': rsp_city_referer_url,
                                               'host_url': host_url}, errback=self.geterrback, headers=self.header)
                else:
                    pass

    # 获取最终数据
    def get_info(self, response):
        rsp_info = response.url
        # 城市
        city_meta = response.meta['city_name']
        # 公司名称
        company_name = response.meta['company_name'].strip()
        # print(city_meta, rsp_info, company_name)
        # 电话
        company_tel = response.meta['company_tel']
        self.count += 1
        # 公司地址
        company_add = response.xpath("//p[@class='address']/text()").extract_first()
        if company_add is None:
            company_add = 'add_kong'
            city_md = 'md_kong'
            # print('``'*70)
            # print(self.count, rsp_info, city_meta, city_md, company_add, company_name, company_tel)
            self.items['id'] = self.count
            self.items['company_url'] = rsp_info
            self.items['city_name'] = city_meta
            self.items['city_md'] = city_md
            self.items['company_add'] = company_add
            self.items['company_name'] = company_name
            self.items['tel'] = company_tel
            yield self.items
        else:
            # 市辖区
            city_allmd = response.xpath("//p[@class='address']/text()").extract_first()
            city_md = re.findall(r'..区|县', city_allmd)
            if len(city_md) == 0:
                city_mdk = 'md_kong'
                # print('--'*65)
                # print(self.count, rsp_info, city_meta, city_mdk, company_add, company_name, company_tel)
                self.items['id'] = self.count
                self.items['company_url'] = rsp_info
                self.items['city_name'] = city_meta
                self.items['city_md'] = city_mdk
                self.items['company_add'] = company_add
                self.items['company_name'] = company_name
                self.items['tel'] = company_tel
                yield self.items
            else:
                # print('**'*85)
                # print(self.count, rsp_info, city_meta, city_md[0], company_add, company_name, company_tel)
                self.items['id'] = self.count
                self.items['company_url'] = rsp_info
                self.items['city_name'] = city_meta
                self.items['city_md'] = city_md[0]
                self.items['company_add'] = company_add
                self.items['company_name'] = company_name
                self.items['tel'] = company_tel
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
