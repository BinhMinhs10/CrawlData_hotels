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
        assert(splash:wait(6))
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
        for href in hrefs: #[0:8]
            request = scrapy.Request(response.urljoin(href), callback=self.parse_list)
            request.meta['destination'] = href
            yield request
    
    def parse_list(self, response):
        destination = response.meta['destination']
        for href in response.css('div.hotel-item__wrapper a.hotel-item__a::attr(href)').getall():
            # Khong dung if ngay dc vì 
            request = SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_detail,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )
            #request.meta['destination'] = destination
            yield request
            
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