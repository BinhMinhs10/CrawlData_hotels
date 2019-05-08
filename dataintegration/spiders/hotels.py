# -*- coding: utf-8 -*-
import scrapy
from dataintegration.items import HotelItem
from dataintegration.items import RoomItem

class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    #start_urls = ['https://vi.hotels.com/search.do?resolved-location=CITY%3A1633619%3AUNKNOWN%3AUNKNOWN&destination-id=1633619&q-destination=Th%C3%A0nh%20ph%E1%BB%91%20H%E1%BB%93%20Ch%C3%AD%20Minh,%20Vi%E1%BB%87t%20Nam&q-check-in=2019-04-09&q-check-out=2019-04-10&q-rooms=1&q-room-0-adults=2&q-room-0-children=0']
    
    start_urls = ['https://vi.hotels.com/search.do?resolved-location=CITY%3A1567225%3AUNKNOWN%3AUNKNOWN&destination-id=1567225&q-destination=%C4%90%C3%A0%20N%E1%BA%B5ng%20(v%C3%A0%20v%C3%B9ng%20ph%E1%BB%A5%20c%E1%BA%ADn),%20Vi%E1%BB%87t%20Nam&q-check-in=2019-05-09&q-check-out=2019-05-10&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
                'https://vi.hotels.com/search.do?resolved-location=CITY%3A1567425%3AUNKNOWN%3AUNKNOWN&destination-id=1567425&q-destination=%C4%90%C3%A0%20L%E1%BA%A1t,%20Vi%C3%AA%CC%A3t%20Nam&q-check-in=2019-05-09&q-check-out=2019-05-10&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
                'https://vi.hotels.com/search.do?resolved-location=CITY%3A1581970%3AUNKNOWN%3AUNKNOWN&destination-id=1581970&q-destination=Vu%CC%83ng%20Ta%CC%80u,%20Vi%C3%AA%CC%A3t%20Nam&q-check-in=2019-05-09&q-check-out=2019-05-10&q-rooms=1&q-room-0-adults=2&q-room-0-children=0']
    count = [2,2,2]
    custom_settings = {
       'IMAGES_STORE' : 'images/hotels/'
    }

    def parse(self, response):
        for key in range(len(self.start_urls)):
            for row in response.css('li.hotel'):
                href = row.css('h3.p-name a::attr(href)').get()
                if not row.css('p.sold-out-message'):
                    yield response.follow(href, callback=self.parse_detail) 
            # count = 150 voi HCM
            if self.count[key] < 70:
                self.count[key] += 1
                href = str(self.start_urls[key]) + "&pn=" + str(self.count[key]) 
                yield response.follow(href, callback=self.parse)
    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        hotel = HotelItem()
        hotel['link'] = response.url
        hotel['destination'] = 'Hotels.com'
        hotel['name'] = extract_with_css('div.vcard h1::text')
        hotel['star'] = extract_with_css('div.vcard span.star-rating-text::text')
        hotel['address'] = extract_with_css('span.postal-addr::text')
        attributes = []
        for attr in response.css('div#overview-section-4 ul li::text').getall():
           attributes.append(attr)
        hotel['benefits'] = attributes

        rooms = []
        for room in response.css('li.room.cont'):
            roomitem = RoomItem()
            image_url = room.css('div.room-image a.room-images-link::attr(href)').get(default='')
            #image_url = response.css("div.room-image img").re_first(r'url\(\'([^\'\)]+)')

            hotel['image_urls'] = [image_url]
            roomitem['room_type'] = room.css('h3 span::text').get().strip()
            roomitem['room_size'] = room.css('span.occupancy-info strong::text').get().strip()
            if room.css('div.price strong::text'):
                roomitem['price_per_night'] = room.css('div.price strong::text').get().strip()
            else:
                roomitem['price_per_night'] = room.css('div.price ins.current-price::text').get().strip()
            rooms.append(dict(roomitem))
        hotel['rooms'] = rooms
        yield hotel
