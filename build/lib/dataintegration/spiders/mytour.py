# -*- coding: utf-8 -*-
import scrapy
from dataintegration.items import HotelItem
from scrapy_splash import SplashRequest



class MytourSpider(scrapy.Spider):
    name = 'mytour'
    start_urls = ['http://mytour.vn/']

    
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
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
            
            
    def parse(self, response):
        for href in response.css('a.events-tracking::attr(href)').getall()[1:13]:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_list)
            
    def parse_list(self, response):
        
        destination = response.css('h1.title-lg a::text').get()
        
        for href in response.css('h2.title-sm a::attr(href)').getall():
            
            request = SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_detail,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )
            # request = scrapy.Request(response.urljoin(href), callback=self.parse_detail)
            request.meta['destination'] = destination
            yield request

        # print('NEXT PAGE-------------------------------')
        for nextp in response.css('a[aria-label*=Next]::attr(href)').getall():
            yield scrapy.Request(response.urljoin(nextp), callback=self.parse_list)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        item = HotelItem()
        item['link'] = response.url
        item['destination'] = response.meta['destination']
        item['name'] = extract_with_css('h1#hotel-name::text')
        item['rating'] = extract_with_css('span.rate::text')
        item['address'] = extract_with_css('p.text-df span.gray::text')
        attributes = []
        for attr in response.css('li span.attribute-value::text').getall():
           attributes.append(attr)
        item['benefits'] = attributes
        type_name = ''
        for row in response.css('tr:not([class*="rate-box"])'):
            isname = row.css('td.title-room a.product-name::text').get()
            if isname != None:
                type_name = row.css('td.title-room a.product-name::text').get()   
            else:
                price = row.css('p.price strong::text').get(default=None)
                size = row.css('p[title*="tích"]::text').getall()
                if price != None and size != None:
                    item['room_type'] = type_name.strip()
                    item['price_per_night'] = price.strip()
                    item['room_size'] = size
                    yield item