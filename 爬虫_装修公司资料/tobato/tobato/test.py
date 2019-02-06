# -*- coding:utf-8 -*-
import random
import re
import requests
import time
import xlrd
# from scrapy.downloadermiddlewares.retry import RetryMiddleware
# 请求API 获取代理 IP


def get_api(url, header):
    try:
        # 请求代理ip的API，获取ip
        proxy_html = requests.get(url=url, headers=header)
        # proxy_html.encoding = 'utf-8'
        # 问题：Can't convert 'bytes' object to str implicitly   直接转换成str类型
        # api_ip = proxy_html.content.decode('raw_unicode_escape')
        api_ip = proxy_html.content.decode('utf8')
        # print(api_ip)
        return api_ip
    except Exception as e:
        print(e)


# 检查代理IP可用性
def check_ip(baidu_url, ip, timeout):
    ip_html = requests.get(url=baidu_url, proxies=ip, timeout=timeout)
    if ip_html == 200:
        return ip
    else:
        pass


def write_ip(write_path, ip):
    # ip写入txt文档中
    with open(write_path, 'a', encoding='utf-8') as write_ip:
        try:
            write_ip.write(ip)
            print('写入IP', ip)
            # write_ip.close()
        except Exception as e:
            print(e)


def reader_ip(reader_path):
    with open(reader_path, 'r') as f:
        proxies = f.readlines()
        return proxies


def reader_excel():
    path = 'E:/爬虫_装修公司资料/土巴兔装修公司.xlsx'
    count = 0
    # 打开Excel
    workbook = xlrd.open_workbook(path)
    data_sheet = workbook.sheets()[0]  # 通过索引获取
    for row_list in range(2, 228):
        count += 1
        rows = data_sheet.row_values(row_list)  # 获取第n行数据
        return rows
        # city_name = rows[1]
        # city_company_url = rows[2]
        # page_nub = int(rows[3])
        # print(count, city_name, city_company_url, page_nub)


def random_ip(proxies):
    proxy = random.choice(proxies).strip()
    return proxy


def main():
    ip_set = set()
    write_path = 'E:/爬虫_装修公司资料/tobato/iplist.txt'
    reader_path = 'E:/爬虫_装修公司资料/tobato/iplist.txt'
    header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
    # 私人代理
    # url = 'http://39.108.59.38:7777/Tools/proxyIP.ashx?Type=090bc2b2a902e7f1aa540bab05a2135b&Order=29825&cache=0&qty=5'
    # 快代理
    url = 'http://dps.kdlapi.com/api/getdps/?orderid=943784354993129&num=10&pt=1&dedup=1&format=json&sep=1'
    # 西瓜代理
    # url = 'http://api3.xiguadaili.com/ip/?tid=558519336478218&num=10&category=2&sortby=time&filter=on'
    while len(ip_set) < 30000:
        print('等待中', '~~'*30)
        time.sleep(5)
        ip_html = get_api(url=url, header=header)
        # print('~~~', ip_html)
        ip_contents = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', ip_html)
        for ip_content in ip_contents:
            # time.sleep(2)
            write_ip(write_path, ip_content + '\n')
            # proxys = reader_ip(reader_path)
            # print(proxys[-5:])
            # ip = random_ip(proxys[-5:])
            # print('>>>', ip)
            # print('-----', ip_content)
            # proxy_ip = 'https://' + ip_content
            # # print(proxy_ip)
            # proxies = {"https": proxy_ip, }
            # try:
            #     ip_html = requests.get(url=baidu_url, proxies=proxies, timeout=timeout)
            #     # print(ip_html)
            #     if ip_html.status_code == 200:
            #         # print('写入数据')
            #         write_ip(write_path, ip_content + '\n')
            #     else:
            #         pass
            # except Exception as e:
            #     print(e)
    # else:
    #     break


if __name__ == '__main__':
    main()
