# -*- coding: utf-8 -*-

# Scrapy settings for tripadv project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
from config import access_codes

BOT_NAME = 'tripadv'

SPIDER_MODULES = ['tripadv.spiders']
NEWSPIDER_MODULE = 'tripadv.spiders'
MONGODB = [
    'mongodb://'+access_codes['MONGODB']['username']+':'+access_codes['MONGODB']['psw']+'@adriana:'+access_codes['MONGODB']['port'],
    'mongodb://'+access_codes['MONGODB']['username']+':'+access_codes['MONGODB']['psw']+'@annika:'+access_codes['MONGODB']['port'],
 ]
USER_AGENT_LIST_FILE = 'user_agents.txt'
DOWNLOAD_DELAY = 5
DOWNLOAD_TIMEOUT = 200

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
RANDOMIZE_DOWNLOAD_DELAY = True


# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'tripadv.middlewares.SpiderMiddleware': 543,
# }
# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'tripadv.middlewares.MyCustomDownloaderMiddleware': 543,
# }
# DOWNLOADER_CLIENTCONTEXTFACTORY = 'tripadv.middlewares.CustomContextFactory'

DOWNLOADER_MIDDLEWARES = {
    'tripadv.middlewares.RandomUserAgentMiddleware': 400,
    #  'tripadv.middlewares.ProxyMiddleware': 410,
    'tripadv.middlewares.LimitHandlerMiddleware': 650,

}
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'tripadv.pipelines.SomePipeline': 300,
#}
ITEM_PIPELINES = {
    'tripadv.pipelines.MongoDBPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED = False

# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
# LOG_FILE = str(time.strftime("%Y%m%d_"))+'intruder.log'
# 403 and 408 were not default here
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 408]
CLOSESPIDER_ERRORCOUNT = 1
RETRY_TIMES = 10
