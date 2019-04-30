# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from dataintegration.items import HotelItem
from dataintegration.items import RoomItem


class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['booking.com']
    custom_settings = {
       'IMAGES_STORE' : 'images/booking/'
    }

    start_urls = ['https://www.booking.com/searchresults.vi.html?label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuALvl5XmBcACAQ&lang=vi&sid=d329c175be2f8d73877c0ecc3395ca01&sb=1&src=hotel&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Fvn%2Fsalsa-2-hotel.vi.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuALvl5XmBcACAQ%3Bsid%3Dd329c175be2f8d73877c0ecc3395ca01%3Ball_sr_blocks%3D42904711_125357920_2_0_0%3Bcheckin%3D2019-05-01%3Bcheckout%3D2019-05-31%3Bdest_id%3D-3712125%3Bdest_type%3Dcity%3Bdist%3D0%3Bgroup_adults%3D2%3Bhapos%3D5%3Bhighlighted_blocks%3D42904711_125357920_2_0_0%3Bhpos%3D5%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsr_order%3Dpopularity%3Bsrepoch%3D1556433906%3Bsrpvid%3Dfc772f7949bc0190%3Btype%3Dtotal%3Bucfs%3D1%26%3B&highlighted_hotels=429047&hp_sbox=1&ss=%C4%90%C3%A0+N%E1%BA%B5ng&is_ski_area=0&ssne=%C4%90%C3%A0+N%E1%BA%B5ng&ssne_untouched=%C4%90%C3%A0+N%E1%BA%B5ng&dest_id=-3712125&dest_type=city&checkin_year=2019&checkin_month=5&checkin_monthday=15&checkout_year=2019&checkout_month=5&checkout_monthday=16&group_adults=2&group_children=0&no_rooms=1&from_sf=1']

    script = """
    function main(splash)
        local url = splash.args.url
        assert(splash:go(url))
        assert(splash:wait(1))
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
        for row in response.css('div.sr_item.sr_item_new'):
            link = row.css('a.hotel_name_link.url::attr(href)').get().strip()
            if not row.css('div.sr--soldout-content'):
                request = SplashRequest(
                    url=response.urljoin(link),
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
        
        hotel = HotelItem()
        hotel['link'] = response.url
        hotel['destination'] = 'ĐN' #response.meta['destination']
        hotel['name'] = response.css('h2#hp_hotel_name::text').getall()[1].strip()
        hotel['rating'] = extract_with_css('i span.invisible_spoken::text')
        hotel['address'] = extract_with_css('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip::text')

        image_url = response.css('img.hotel::attr(src)').get(default='')
        hotel['image_urls'] = [image_url]

        hotel['rooms'] = response.css('div.hprt-price-price').getall()
        yield hotel