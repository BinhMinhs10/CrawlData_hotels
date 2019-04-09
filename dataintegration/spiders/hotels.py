# -*- coding: utf-8 -*-
import scrapy
from dataintegration.items import HotelItem
from dataintegration.items import RoomItem

class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    # start_urls = ['https://vi.hotels.com/search.do?resolved-location=CITY%3A1633619%3AUNKNOWN%3AUNKNOWN&destination-id=1633619&q-destination=Th%C3%A0nh%20ph%E1%BB%91%20H%E1%BB%93%20Ch%C3%AD%20Minh,%20Vi%E1%BB%87t%20Nam&q-check-in=2019-04-09&q-check-out=2019-04-10&q-rooms=1&q-room-0-adults=2&q-room-0-children=0']
    start_urls=['https://vi.hotels.com/search.do?resolved-location=CITY%3A1634382%3AUNKNOWN%3AUNKNOWN&destination-id=1634382&q-destination=H%C3%A0%20N%E1%BB%99i,%20Vi%E1%BB%87t%20Nam&q-check-in=2019-04-12&q-check-out=2019-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0']
    count = 2
    def parse(self, response):
        for row in response.css('li.hotel'):
            href = row.css('h3.p-name a::attr(href)').get()
            if not row.css('p.sold-out-message'):
                yield response.follow(href, callback=self.parse_detail) 
        # count = 150 voi HCM
        if self.count < 50:
            self.count += 1
            href = str(self.start_urls[0]) + "&pn=" + str(self.count) 
            yield response.follow(href, callback=self.parse)
    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        hotel = HotelItem()
        hotel['link'] = response.url
        hotel['destination'] = 'khách sạn Hà Nội'
        hotel['name'] = extract_with_css('div.vcard h1::text')
        hotel['star'] = extract_with_css('div.vcard span.star-rating-text::text')
        hotel['address'] = extract_with_css('span.postal-addr::text')
        attributes = []
        for attr in response.css('div#overview-section-4 ul li::text').getall():
           attributes.append(attr)
        hotel['benefits'] = attributes
        for room in response.css('li.room.cont'):
            roomitem = RoomItem()
            image_url = room.css('div.room-image a.room-images-link::attr(href)').get(default='')
            hotel['image_urls'] = [image_url]
            roomitem['room_type'] = room.css('h3 span::text').get().strip()
            roomitem['room_size'] = room.css('span.occupancy-info strong::text').get().strip()
            if room.css('div.price strong::text'):
                roomitem['price_per_night'] = room.css('div.price strong::text').get().strip()
            else:
                roomitem['price_per_night'] = room.css('div.price ins.current-price::text').get().strip()
            hotel['rooms'] = dict(roomitem)
            yield hotel
