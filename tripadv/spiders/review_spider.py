# -*- coding: utf-8 -*-
"""


Created on Wed Jun 14 11:11:41 2017

@author: giotto
"""
from traceback import format_exc
from scrapy import Request
from scrapy.conf import settings
from pymongo import MongoClient
from scrapy.spiders import CrawlSpider
from tripadv.items import Review_Item
from geopy.geocoders import Nominatim
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
logger = logging.getLogger('Review_spider')


class Review_spider(CrawlSpider):

    name = "review_hunter"

    def __init__(self, country=None, city=None, schema=None):
        self.geolocator = Nominatim()
        mongo_credentials = settings['MONGODB']
        client = MongoClient(mongo_credentials)
        db = client.tripadvisor
        self.hotels_collection = db.hotels
        self.allowed_domains = ["tripadvisor.com"]

    def start_requests(self):
        '''called only once implicitly it yields the first request to parse
        which will eventually keep on yielding similar ones'''
        url_target = self.review_target_finder()
        if url_target:
            logger.debug(str(url_target))

            yield Request(url_target,
                          # it lets re-perform the same request
                          dont_filter=True,
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [301, 302]
                          },

                          callback=self.parse,)

    def review_target_finder(self):
        room =\
            next(self.hotels_collection.
                 aggregate([{'$match': {
                     '$or': [{'updates.reviews_updated':
                              {'$exists': 0}},
                             {'updates.reviews_updated':
                              {'$lt': datetime.now() +
                               relativedelta(weeks=-2)}},
                             ],
                 }},
                     {'$project': {'hotel_url': 1}},
                     {'$sample': {'size': 1}}, ]))
        if room:
            room["hotel_url"]
            return room["hotel_url"]
        else:
            logger.debug(
                'hotel_target_finder did not find any available target')

    def parse(self, response):
        current_url = response.url
        item = Review_Item()
        response.xpath('//div[@class="reviewSelector"]')

        page_number = int(
            response.xpath(
                '//div[@class="pageNumbers"]/a/@data-page-number'
            ).extract()[-1])
        for page_number in range(page_number - 1):
            next_url =\
                (current_url.split('-Reviews-')[0] +
                 '-Reviews-or' + str((page_number + 1) * 5) +
                 '-' + current_url.split('-Reviews-')[1])
            yield Request(next_url,
                          # it lets re-perform the same request
                          dont_filter=True,
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [301, 302]
                          },

                          callback=self.parse,)
