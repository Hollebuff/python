# -*- coding:utf-8 -*-
import random
import re
import requests
import time


def get_api(url, header):
    try:
        # 请求代理ip的API，获取ip
        proxy_html = requests.get(url=url, headers=header)
        api_ip = proxy_html.content.decode('utf8')
        print(api_ip)
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


def random_ip(proxies):
    proxy = random.choice(proxies).strip()
    return proxy


def main():
    ip_set = set()
    write_path = 'E:/爬虫_装修公司资料/tobato/iplist.txt'
    header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
    # 西瓜代理
    url = 'http://api3.xiguadaili.com/ip/?tid=558519336478218&num=5&category=2&sortby=time&filter=on'
    while len(ip_set) < 30000:
        print('等待中', '~~'*30)
        time.sleep(5)
        ip_html = get_api(url=url, header=header)
        ip_contents = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', ip_html)
        for ip_content in ip_contents:
            # time.sleep(2)
            write_ip(write_path, ip_content + '\n')


if __name__ == '__main__':
    main()
