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
from tripadv.items import Hotel_Item
from geopy.geocoders import Nominatim

import logging
logger = logging.getLogger('Hotel_spider')


class Hotel_spider(CrawlSpider):

    name = "hotel_hunter"

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
        url_target = self.hotel_target_finder()
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

    def hotel_target_finder(self):
        try:
            room =\
                next(self.hotels_collection.
                     aggregate([{'$match':
                                 {'location': {'$exists': 0}, }},
                                {'$project': {'hotel_url': 1}},
                                {'$sample': {'size': 1}}, ]))
            room["hotel_url"]
            return room["hotel_url"]
        except StopIteration:
            logger.debug(
                'hotel_target_finder did not find any available target')

    def parse(self, response):
        try:
            item = Hotel_Item()
            # hotel_id_raw =\
            #    response.xpath('//span/@data-id').extract()
            hotel_id_raw =\
                response.xpath('//div[@class="blRow"]/@data-locid').extract()
            if hotel_id_raw:
                item['hotel_id'] =\
                    long(hotel_id_raw[0])
                street_raw =\
                    response.xpath(
                        '//span[@class="street-address"]/text()'
                    ).extract()
                if street_raw:
                    item['street'] =\
                        street_raw[0].lower()

                item['city'] =\
                    (response.xpath('//span[@class="locality"]/text()'
                                    ).extract()[0].split(' ')[1].lower().
                     replace(',', ''))
                if item['city']:
                    pass
                else:
                    item['city'] =\
                        (response.xpath('//span[@class="locality"]/text()'
                                        ).extract()[0].split(' ')[0].lower().
                         replace(',', ''))

                #    response.xpath(
                #        '//span[@property="v:locality"]/text()'
                # ).extract()[0].lower()

                item['country'] =\
                    response.xpath('//span[@class="country-name"]/text()'
                                   ).extract()[0].lower()

                for script in\
                        response.xpath(
                        '//script[@type="text/javascript"]/text()').extract():
                    if 'lng: ' in script:
                        item["latitude"] =\
                            float(script.split('lat: ')[1].split(',')[0])
                        item["longitude"] =\
                            float(script.split('lng: ')[1].split(',')[0])
                if 'latitude' in item:
                    pass
                else:
                    if "street" in item:
                        address = (item['street'] + ' ' +
                                   item['city'] + ' ' +
                                   item['country'])
                    else:
                        address = (item['city'] + ' ' +
                                   item['country'])
                    location = (self.geolocator.geocode(address))
                    if location:
                        item["latitude"], item["longitude"] =\
                            location.latitude, location.longitude

                try:
                    item['postcode'] =\
                        int(response.xpath(
                            '//span[@class="locality"]/text()'
                        ).extract()[0].split(' ')[0])
                except:
                    location =\
                        self.geolocator.reverse(str(item["latitude"]) + ', ' +
                                                str(item["longitude"]),
                                                timeout=None,
                                                language='en')
                    postcode = location.raw['address']['postcode']
                    if ";" in postcode:
                        postcode = postcode.split(';')[0]
                    item['postcode'] = int(postcode)

                overall_rating_raw =\
                    response.xpath(
                        '//span[@class="overallRating"]/text()').extract()
                if overall_rating_raw:
                    item['overall_rating'] =\
                        float(overall_rating_raw[0])
                reviews_count_raw =\
                    response.xpath(
                        '//span[@property="v:count"]/text()').extract()
                if reviews_count_raw:
                    item["reviews_count"] = \
                        int(reviews_count_raw[0].split(
                            ' rev')[0].replace(',', ''))
                else:
                    item["reviews_count"] = 0
                yield item
            else:
                pass

            hotel_url = self.hotel_target_finder()
            if hotel_url:
                yield Request(hotel_url,
                              # it lets re-perform the same request
                              dont_filter=True,
                              meta={
                                  'dont_redirect': True,
                                  'handle_httpstatus_list': [301, 302, 404]
                              }, callback=self.parse,)

        except Exception:
            logger.error(format_exc())
            hotel_url = self.hotel_target_finder()
            if hotel_url:
                yield Request(hotel_url,
                              # it lets re-perform the same request
                              dont_filter=True,
                              meta={
                                  'dont_redirect': True,
                                  'handle_httpstatus_list': [301, 302, 404]
                              }, callback=self.parse,)
