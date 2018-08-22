# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.conf import settings
from pymongo import MongoClient
from items import List_Item, Hotel_Item
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class MongoDBPipeline(object):

    def __init__(self):

        mongo_credentials = settings['MONGODB']
        client = MongoClient(mongo_credentials)
        db = client.tripadvisor
        self.hotels_collection = db.hotels

    def process_item(self, item, spider):
        if isinstance(item, List_Item):
            self.hotels_collection.\
                update_one({'_id': item['hotel_id']},
                           {'$set':
                            {'hotel_name': item["hotel_name"],
                             'hotel_url': item["hotel_url"],
                             "updates":
                             {"insert_time": datetime.utcnow(), }}},
                           upsert=True)
            return item

        if isinstance(item, Hotel_Item):
            self.hotels_collection.\
                update_one({'_id': item['hotel_id']},
                           {'$set':
                            {
                                # 'location.address.street': item["street"],
                                'location.address.postcode': item["postcode"],
                                'location.address.city': item["city"],
                                'location.address.country': item["country"],
                            }},
                           )

            if "street" in item:
                self.hotels_collection.\
                    update_one({'_id': item['hotel_id']},
                               {'$set':
                                {'location.address.street': item["street"],
                                 }},
                               )

            if "latitude" in item:
                self.hotels_collection.\
                    update_one({'_id': item['hotel_id']},
                               {'$set':
                                {'location.coordinates.latitude':
                                    item["latitude"],
                                 'location.coordinates.longitude':
                                    item["longitude"],
                                 }},
                               )

            if "reviews_count" in item:
                self.hotels_collection.\
                    update_one({'_id': item['hotel_id']},
                               {'$set':
                                {'reviews_count': item["reviews_count"], }})

            if "overall_rating" in item:
                self.hotels_collection.\
                    update_one({'_id': item['hotel_id']},
                               {'$set':
                                {'overall_rating': item["overall_rating"], }})

            return item
