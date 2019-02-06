# -*- coding:utf-8 -*-
import random, re, scrapy, requests
from bs4 import BeautifulSoup
from qizhuang.items import QizhuangItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
# 市辖区可能是空的


class qizhuang(scrapy.Spider):
    name = 'qizhuang'
    start_urls = ['http://www.qizuang.com/city/']
    # start_urls = ['http://nn.qizuang.com/company/']
    # start_urls = ['http://wh.qizuang.com/company_home/83034/']
    alloed_domain = ['qizuang.com']
    count = 0
    just = '中国'
    items = QizhuangItem()
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0"
    ]
    ua = random.choice(user_agent_list)  # 随机抽取User-Agent
    header = {
        'User-Agent': ua
    }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.get_info, meta={'city_name': self.just})

    #  获取所有城市  638个
    def parse(self, response):
        city_lists = response.xpath("//div[@class='p2 clearfix']/div[@class='con1 acti']"
                                    "/div[@class='span1']/ul/li/a")
        for city_list in city_lists:
            # self.count += 1
            city_name = city_list.xpath('./text()').extract()
            city_url = city_list.xpath('./@href').extract()
            company_url = city_url[0] + 'company/'
            # print(self.count, city_name[0], city_url[0])
            yield scrapy.Request(url=company_url, dont_filter=False, callback=self.get_company,
                                 meta={'city_name': city_name[0]}, errback=self.geterrback)

    def get_company(self, response):
        rsp_company = response.meta['city_name']
        # 公司URL  10个
        info_urls = response.xpath("//div[@class='company_tituw f0']/a/@href").extract()
        for info_url in info_urls:
            # print('--'*80)
            # print(info_url)
            yield scrapy.Request(url=info_url, dont_filter=False, callback=self.get_info,
                                 meta={'city_name': rsp_company}, errback=self.geterrback)
        # 翻页
        pages = response.xpath("//div[@class='page']/a[last()]/@href").extract()
        # print(pages[0])
        if len(pages[0]) > 15:
            pass
            yield scrapy.Request(url=pages[0], dont_filter=False, callback=self.get_company,
                                 meta={'city_name': rsp_company}, errback=self.geterrback)
        else:
            pass

    def get_info(self, response):
        res_company_url = response.url
        # 城市名称
        city_name = response.meta['city_name']
        # 市辖区
        try:
            city_mds = response.xpath("//li[@class='att']/text()").extract_first()
            city_md = re.findall(r'(..区|县)', city_mds)
        except Exception as e:
            pass
        # 装修公司名称
        company_name = response.xpath("//h1/text()").extract_first().strip()
        # 电话
        tel = response.xpath("//li[@class='tel']/text()").extract_first()
        # 手机
        phone = response.xpath("//li[@class='mob']/text()").extract_first()

        # 公司地址,解决完整问题
        company_adds = response.xpath("//li[@class='att']/text()").extract_first()
        if company_adds is None:
            print('~~'*80)
            print(self.count, res_company_url, city_name, company_adds, company_name.strip(), tel, phone)
            pass
        else:
            self.count += 1
            if len(city_md) == 0:
                city_mds = 'kong'
                if re.findall(r'(\.\.\.)$', company_adds[0]):
                    add_about_url = res_company_url.replace("home", "about")
                    html = requests.get(url=add_about_url, headers=self.header)
                    html.encoding = "utf-8"
                    soup = BeautifulSoup(html.content, 'html.parser')
                    complete_adds = soup.find("ul", class_="c-about-info")
                    li_adds = complete_adds.findAll('li')
                    company_add = li_adds[1].get_text().replace('<span>公司地址：</span>', "").replace('公司地址：', '').strip()
                    if len(company_add) != 0:
                        # print('--' * 70)
                        # print(self.count, add_about_url, city_name, city_md, company_add, company_name, tel, phone)
                        self.items['id'] = self.count
                        self.items['company_url'] = res_company_url
                        self.items['city_name'] = city_name
                        self.items['city_md'] = city_mds
                        self.items['company_name'] = company_name
                        self.items['company_add'] = company_add
                        self.items['tel'] = tel
                        self.items['phone'] = phone
                        yield self.items
                    else:
                        # print(self.count, res_company_url, '详细页无地址', city_name, city_md, company_adds[0].strip(), company_name.strip(), tel, phone)
                        self.items['id'] = self.count
                        self.items['company_url'] = res_company_url
                        self.items['city_name'] = city_name
                        self.items['city_md'] = city_mds
                        self.items['company_name'] = company_name
                        self.items['company_add'] = company_adds
                        self.items['tel'] = tel
                        self.items['phone'] = phone
                        yield self.items
                else:
                    # print(self.count, res_company_url, '公司首页', city_name, city_md, company_adds[0].strip(), company_name.strip(), tel, phone)
                    self.items['id'] = self.count
                    self.items['company_url'] = res_company_url
                    self.items['city_name'] = city_name
                    self.items['city_md'] = city_mds
                    self.items['company_name'] = company_name
                    self.items['company_add'] = company_adds
                    self.items['tel'] = tel
                    self.items['phone'] = phone
                    yield self.items
            else:
                if re.findall(r'(\.\.\.)$', company_adds[0]):
                    add_about_url = res_company_url.replace("home", "about")
                    html = requests.get(url=add_about_url, headers=self.header)
                    html.encoding = "utf-8"
                    soup = BeautifulSoup(html.content, 'html.parser')
                    complete_adds = soup.find("ul", class_="c-about-info")
                    li_adds = complete_adds.findAll('li')
                    company_add = li_adds[1].get_text().replace('<span>公司地址：</span>', "").replace('公司地址：', '').strip()
                    if len(company_add) != 0:
                        # print('--' * 70)
                        # print(self.count, add_about_url, city_name, city_md, company_add, company_name, tel, phone)
                        self.items['id'] = self.count
                        self.items['company_url'] = res_company_url
                        self.items['city_name'] = city_name
                        self.items['city_md'] = city_md[0]
                        self.items['company_name'] = company_name
                        self.items['company_add'] = company_add
                        self.items['tel'] = tel
                        self.items['phone'] = phone
                        yield self.items
                    else:
                        # print(self.count, res_company_url, '详细页无地址', city_name, city_md, company_adds[0].strip(), company_name.strip(), tel, phone)
                        self.items['id'] = self.count
                        self.items['company_url'] = res_company_url
                        self.items['city_name'] = city_name
                        self.items['city_md'] = city_md[0]
                        self.items['company_name'] = company_name
                        self.items['company_add'] = company_adds
                        self.items['tel'] = tel
                        self.items['phone'] = phone
                        yield self.items
                else:
                    # print(self.count, res_company_url, '公司首页', city_name, city_md, company_adds[0].strip(), company_name.strip(), tel, phone)
                    self.items['id'] = self.count
                    self.items['company_url'] = res_company_url
                    self.items['city_name'] = city_name
                    self.items['city_md'] = city_md[0]
                    self.items['company_name'] = company_name
                    self.items['company_add'] = company_adds
                    self.items['tel'] = tel
                    self.items['phone'] = phone
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
            self.items['city_md'] = response.url   # 请求页面
            self.items['company_name'] = str(response.status)
            self.items['company_add'] = 'null'
            self.items['tel'] = 'null'
            self.items['phone'] = 'null'
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
            self.items['phone'] = 'null'
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
            self.items['phone'] = 'null'
            yield self.items
            self.logger.error('请求超时999999》》》》》》TimeoutError on %s', request.url)
