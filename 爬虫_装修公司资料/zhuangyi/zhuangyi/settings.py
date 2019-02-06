# -*- coding: utf-8 -*-

# Scrapy settings for zhuangyi project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhuangyi'

SPIDER_MODULES = ['zhuangyi.spiders']
NEWSPIDER_MODULE = 'zhuangyi.spiders'
REDIRECT_ENABLED = False
DOWNLOAD_TIMEOUT = 30

# 正则排除  \{\"ipaddr\"\: '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}
IPPOOL = [
            {"ipaddr": '180.105.248.151:22138'},
            {"ipaddr": '49.87.98.59:22148'},
            {"ipaddr": '47.100.249.202:22716'},
            {"ipaddr": '125.106.159.118:18481'},
            {"ipaddr": '124.229.244.187:16898'},
            {"ipaddr": '47.106.176.88:29473'},
            {"ipaddr": '47.92.242.25:17142'},
            {"ipaddr": '125.72.106.173:23603'},
            {"ipaddr": '106.56.102.156:15099'},
            {"ipaddr": '59.57.148.221:17723'},
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhuangyi (+ipaddr":'www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 同时请求数量
# CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 0.4
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# 对网站并发请求量
# CONCURRENT_REQUESTS_PER_DOMAIN = 5
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhuangyi.middlewares.ZhuangyiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'zhuangyi.middlewares.ZhuangyiDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'zhuangyi.middlewares.MyproxiesSpiderMiddleware': 400,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'zhuangyi.pipelines.ZhuangyiPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
