# -*- coding: utf-8 -*-
import scrapy
from dataintegration.items import HotelItem
from scrapy_splash import SplashRequest


class IvivuSpider(scrapy.Spider):
    name = 'ivivu'
    start_urls = ['http://ivivu.com/']

    # custom_settings = {
	# 	'FEED_URI': "aliexpress_%(time)s.json",
	# 	'FEED_FORMAT' : "json"
	# }
    script = """
    function main(splash)
        local url = splash.args.url
        assert(splash:go(url))
        assert(splash:wait(8))
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
        for href in response.css('div.super-card:not([class*="lazy"]) a::attr(href)').getall()[0:8]:
            destination = href
            request = scrapy.Request(response.urljoin(href), callback=self.parse_list_destination)
            request.meta['destination'] = destination
            yield request
    
    def parse_list_destination(self, response):

        destination = response.meta['destination']
        for href in response.css('a.hotel-item__a::attr(href)').getall():
            request = SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_detail,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )
            request.meta['destination'] = destination
            yield request
         
    def parse_detail(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        ht = HotelItem()
        ht['link'] = response.url
        ht['destination'] = response.meta['destination']
        ht['name'] = extract_with_css('span#hotel-name-detail::text')
        ht['rating'] = extract_with_css('span.score::text')
        ht['address'] = response.css('p.address::text').getall()[1].strip()
        # yield {'html': response.css('tbody.ng-scope').getall()}
        for row in response.css('tbody.ng-scope'):
            ht['room_type'] = row.css('tr.room-item p.room__title::text').get(default='')
            ht['price_per_night'] = row.css('tr.room-item p.rate__price::text').get(default='')
            ht['room_size'] = row.css('div.room__description p.ng-scope::text').getall()
            yield ht

        