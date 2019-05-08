# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest

from dataintegration.items import HotelItem
from dataintegration.items import RoomItem

class MytourSpider(scrapy.Spider):
    name = 'mytour'
    start_urls = ['https://mytour.vn']
    #start_urls = ['https://web.archive.org/web/20190424015201/https://mytour.vn/']

    custom_settings = {
       'IMAGES_STORE' : 'images/mytour/'
    }
    
    script = """
    function main(splash)
        local url = splash.args.url
        assert(splash:go(url))
        assert(splash:wait(4))
        return {
            html = splash:html(),
            url = splash:url(),
        }
    end
    """

    script1 = """
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
        # for href in response.css('a.events-tracking::attr(href)').getall()[1:13]:
        hrefs = response.css('a.events-tracking::attr(href)').getall()[1:4]
        for href in hrefs:
            request = SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_list,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script1}}
                },
            )
            yield request
            
    def parse_list(self, response):
        
        destination = response.css('h1.title-lg a::text').get()
        
        for href in response.css('h2.title-sm a::attr(href)').getall():
            print('OK\n')
            request = SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_detail,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )
            
            request.meta['destination'] = destination
            yield request

        # print('NEXT PAGE-------------------------------')
        for nextp in response.css('a[aria-label*=Next]::attr(href)').getall():
            yield scrapy.Request(response.urljoin(nextp), callback=self.parse_list)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        hotel = HotelItem()
        hotel['link'] = response.url
        hotel['destination'] = 'Khách sạn Hồ Chí Minh' #response.meta['destination']
        hotel['name'] = extract_with_css('h1#hotel-name::text')
        hotel['rating'] = extract_with_css('span.rate::text')
        hotel['address'] = extract_with_css('p.text-df span.gray::text')
        attributes = []
        for attr in response.css('li span.attribute-value::text').getall():
           attributes.append(attr)
        hotel['benefits'] = attributes
        
        hotel['star'] = response.css('span.star span::attr(class)').get(default='')
        
        image_url = response.css('div.product-image img.img-responsive::attr(src)').get(default='')
        hotel['image_urls'] = [image_url]
        
        rooms = []
        type_name = ''
        for row in response.css('tr:not([class*="rate-box"])'):
            roomitem = RoomItem()
            isname = row.css('td.title-room a.product-name::text').get()
            if isname is not None:
                type_name = row.css('td.title-room a.product-name::text').get()   
            else:
                price = row.css('p.price strong::text').get(default=None)
                size = row.css('p[title*="tích"]::text').getall()
                if price is not None:
                    roomitem['room_type'] = type_name.strip()
                    roomitem['price_per_night'] = price.strip()
                    roomitem['room_size'] = size
                    if roomitem is not None :
                        rooms.append(dict(roomitem))
        if image_url != '':
            hotel['rooms'] = rooms
            yield hotel