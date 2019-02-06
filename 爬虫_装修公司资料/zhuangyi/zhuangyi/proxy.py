# -*- coding：utf-8 -*-
import requests,  re, time, random
# 读取代理IP，去掉请求失败的IP
# http://39.108.59.38:7777/Tools/proxyIP.ashx?Type=c7fa0cd7d61f9832ebcecf737238d4c6&Order=59872&cache=0&qty=10

# 开始请求api
# ip写入txt文档
# 读取存储ip文档，代理请求目标网页 >>>
    # 如果response非200，写入delete 集合，再次获取文档的ip，并且删除保存在txt文档的ip数据， (获取到失败代理IP)
    # 如果该ip在delete文档中，再次选择和删除，最后请求
    #  如果txt文档为空的，再次请求api


def get_api():
    time.sleep(5)
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://39.108.59.38:7777/Tools/proxyIP.ashx?Type=c7fa0cd7d61f9832ebcecf737238d4c6&Order=59872&cache=0&qty=10'
    try:
        # 请求代理ip的API，获取ip
        proxy_html = requests.get(url=url, headers=header)
        # proxy_html.encoding = 'utf-8'
        # 问题：Can't convert 'bytes' object to str implicitly   直接转换成str类型
        api_ip = proxy_html.content.decode('raw_unicode_escape')
        # print(api_ip)
        return api_ip
    except Exception as e:
        print(e)


def write_ip(api_ip):
    # ip写入txt文档中
    with open('E:/爬虫_装修公司资料/zhuangyi/zhuangyi/iplist.txt', 'a', encoding='utf-8') as write_ip:
        try:
            write_ip.write(api_ip)
            print('写入IP', api_ip)
            write_ip.close()
        except Exception as e:
            print(e)


def reader_ip():
    with open('E:/爬虫_装修公司资料/zhuangyi/zhuangyi/iplist.txt', 'r') as f:
        proxies = f.readlines()
        return proxies
        # print(proxies[0:5])
        # for i in range(100):
        #     proxy = random.choice(proxies).strip()
        #     if proxy in old:
        #         print('已存在', proxy)
        #         pass
        #     else:
        #         old.add(proxy)
        #         print('未使用的~~~~~~~~', proxy)


def random_ip(proxies):
    proxy = random.choice(proxies).strip()
    return proxy


def main():
    pass
    # req_ip = set()
    # while len(req_ip) < 5000:
    #     ip_text = get_api()
    #     write_ip(ip_text)


if __name__ == '__main__':
    main()
    # ip = reader_ip()
    # print(ip)

