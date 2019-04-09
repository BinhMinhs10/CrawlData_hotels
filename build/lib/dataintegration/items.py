# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    destination = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    room_type = scrapy.Field()
    room_size = scrapy.Field()
    price_per_night = scrapy.Field()
    benefits = scrapy.Field()
    rating = scrapy.Field()
   

