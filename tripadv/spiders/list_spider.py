# -*- coding: utf-8 -*-
"""


Created on Wed Jun 14 11:11:41 2017

@author: giotto
"""
from scrapy.spiders import CrawlSpider
from scrapy import Request
from tripadv.items import List_Item
import logging
from scrapy.utils.log import configure_logging
import os
import time
import sys

logger = logging.getLogger('List_spider')


class List_spider(CrawlSpider):
    name = "list_hunter"
    cwd = str(os.getcwd())
    if sys.argv[0] == 'shell':
        log_file_name = str(time.strftime("%Y%m%d_")) + 'tripadv.log'
    else:
        log_file_name = str(time.strftime("%Y%m%d_")
                            ) + sys.argv[1] + '_tripadv.log'
    if '/root' in cwd or '/home/complus' in cwd:
        full_log_file_name = '/home/complus/python_log_files/' + log_file_name
    elif '/giotto' in cwd:
        full_log_file_name = (
            '/home/giotto/Dropbox/scraping/' +
            log_file_name)
    else:
        full_log_file_name = log_file_name

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=full_log_file_name,
        filemode='a',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG
    )

    def __init__(self, country=None, city=None, schema_name=None):
        # def __init__(self, country="Greece", city="rhodes"):
        self.page_count = 0
        self.allowed_domains = ["tripadvisor.com"]
        self.base_url = "https://www.tripadvisor.com"
        self.start_urls = [

            "/Hotels-g187323-Berlin-Hotels.html",
            "/Hotels-g187323-c2-Berlin-Hotels.html",
            "/Hotels-g187323-c3-Berlin-Hotels.html",
            "/Hotels-g187331-Hamburg-Hotels.html",
            "/Hotels-g187331-c2-Hamburg-Hotels.html",
            "/Hotels-g187331-c3-Hamburg-Hotels.html",
            "/Hotels-g187371-Cologne_North_Rhine_Westphalia-Hotels.html",
            "/Hotels-g187371-c2-Cologne_North_Rhine_Westphalia-Hotels.html",
            "/Hotels-g187371-c3-Cologne_North_Rhine_Westphalia-Hotels.html",
            "/Hotels-g187309-Munich_Upper_Bavaria_Bavaria-Hotels.html",
            "/Hotels-g187309-c2-Munich_Upper_Bavaria_Bavaria-Hotels.html",
            "/Hotels-g187309-c3-Munich_Upper_Bavaria_Bavaria-Hotels.html",

            "/Hotels-g187337-Frankfurt_Hesse-Hotels.html",
            "/Hotels-g187337-c2-Frankfurt_Hesse-Hotels.html",
            "/Hotels-g187337-c3-Frankfurt_Hesse-Hotels.html",

            "/Hotels-g187291-Stuttgart_Baden_Wurttemberg-Hotels.html",
            "/Hotels-g187291-c2-Stuttgart_Baden_Wurttemberg-Hotels.html",
            "/Hotels-g187291-c3-Stuttgart_Baden_Wurttemberg-Hotels.html",

            "/Hotels-g1053658-Luechow_Lower_Saxony-Hotels.html",
            "/Hotels-g1053658-c2-Luechow_Lower_Saxony-Hotels.html",
            "/Hotels-g1053658-c3-Luechow_Lower_Saxony-Hotels.html",

            "/Hotels-g642012-Dannenberg_Lower_Saxony-Hotels.html",
            "/Hotels-g642012-c2-Dannenberg_Lower_Saxony-Hotels.html",
            "/Hotels-g642012-c3-Dannenberg_Lower_Saxony-Hotels.html",

        ]
        self.start_urls = [self.base_url + url for url in self.start_urls]

    def parse(self, response):
        # ??
        hotels = response.xpath('//div[@class="hotel_content easyClear sem"]')
        # hotels = response.xpath('//div[@class="listing_title"]')
        for hotel in hotels:
            item = List_Item()
            item["hotel_id"] =\
                long(hotel.xpath('.//span/@data-id').extract()[0])
            item["hotel_url"] = (self.base_url +
                                 hotel.xpath('.//a[@target="_blank"]/@href').
                                 extract()[0])
            item["hotel_name"] =\
                hotel.xpath(
                    './/a[@class="property_title"]/text()').extract()[0]
            yield item

        page_navigator =\
            response.xpath(
                '//div[@class="unified pagination standard_pagination"]/a/@href'
            ).extract()
        if len(page_navigator) == 1:
            if "-oa30-" in page_navigator[0]:
                next_page = self.base_url + page_navigator[0]
                yield Request(next_page,
                              meta={'dont_redirect': True,
                                    'handle_httpstatus_list':
                                    [301, 302]},
                              callback=self.parse)
            else:
                pass
        elif len(page_navigator) == 0:
            pass
        else:
            next_page = self.base_url + page_navigator[1]
            yield Request(next_page,
                          meta={'dont_redirect': True,
                                'handle_httpstatus_list':
                                [301, 302]},
                          callback=self.parse)
