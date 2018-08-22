# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class List_Item(Item):
    # define the fields for your item here like:
    hotel_id = Field()
    hotel_url = Field()
    hotel_name = Field()
    pass


class Hotel_Item(Item):
    hotel_id = Field()
    street = Field()
    postcode = Field()
    city = Field()
    country = Field()
    overall_rating = Field()
    reviews_count = Field()
    latitude = Field()
    longitude = Field()
    pass


class Review_Item(Item):
    pass
