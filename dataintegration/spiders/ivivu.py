# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from dataintegration.items import HotelItem
from dataintegration.items import RoomItem


class IvivuSpider(scrapy.Spider):
    name = 'ivivu'
    start_urls = ['http://ivivu.com/']

    custom_settings = {
       'IMAGES_STORE' : 'images/ivivu/'
    }
    
    script = """
    function main(splash)
        local url = splash.args.url
        assert(splash:go(url))
        assert(splash:runjs("$('.btn-load-more').click();"))
        assert(splash:wait(6))
        assert(splash:runjs("$('.btn-load-more').click();"))
        return {
            html = splash:html(),
            url = splash:url(),
        }
    end
    """
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('div.super-card:not([class*="lazy"]) a::attr(href)').getall()[5:7]
        hrefs.append(response.css('div.super-card:not([class*="lazy"]) a::attr(href)').getall()[1])
        print(hrefs)
        for href in hrefs:
            request = SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_list,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )
            request.meta['destination'] = href
            yield request
        
    def parse_list(self, response):

        for row in response.css('div.hotel-item__wrapper '):

            hotel = HotelItem()
            hotel['link'] = response.urljoin(row.css('a.hotel-item__a::attr(href)').get())
            hotel['destination'] = response.meta['destination']
            hotel['name'] = row.css('p.name.limit-length::text').get().strip()
            if not row.css('span.review-score::text'):
                hotel['rating'] = 10
            else:
                hotel['rating'] = row.css('span.review-score::text').get()
            hotel['address'] = row.css('p.address.limit-length::text').getall()[1].strip()
            
            attributes = []
            for attr in row.css('div.pill-item::text').getall():
                attributes.append( attr.strip() )
            hotel['benefits'] = attributes

            rooms = []
            
            roomitem = RoomItem()
            roomitem['room_type'] = row.css('div.pricing__room_name b::text').get(default='')
            roomitem['price_per_night'] = row.css('p.price.primary span.price-num::text').get(default='')
            if roomitem is not None :
                rooms.append(dict(roomitem))
            hotel['rooms'] = rooms
            #hotel['benefits'] = response.css('div.pad-lr-15.txt-justify p::text').getall()        
            #hotel['star'] = 5
            
            #image_url = response.css('img.img-responsive::attr(src)').get(default='')
            #hotel['image_urls'] = [image_url]

            yield hotel
            
    def parse_detail(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        if response.css('table.room-rate-table'):
            hotel = HotelItem()
            hotel['link'] = response.url
            #hotel['destination'] = response.meta['destination']
            hotel['name'] = extract_with_css('span#hotel-name-detail::text')
            hotel['rating'] = extract_with_css('span.score::text')
            hotel['address'] = response.css('p.address::text').getall()[1].strip()
            hotel['benefits'] = response.css('div.pad-lr-15.txt-justify p::text').getall()        
            hotel['star'] = 5
            
            image_url = response.css('img.img-responsive::attr(src)').get(default='')
            hotel['image_urls'] = [image_url]
            
            rooms = []
            for row in response.css('tbody.ng-scope'):
                roomitem = RoomItem()
                roomitem['room_type'] = row.css('tr.room-item p.room__title::text').get(default='')
                roomitem['price_per_night'] = row.css('tr.room-item p.rate__price::text').get(default='')
                roomitem['room_size'] = row.css('div.room__description p.ng-scope::text').get(default='')
                if roomitem is not None :
                    rooms.append(dict(roomitem))
            # if image_url != '':
            # Error
            hotel['rooms'] = rooms
            yield hotel
        else: 
            print( response.url + ' : Sold out\n')