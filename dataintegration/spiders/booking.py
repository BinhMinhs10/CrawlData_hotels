# -*- coding: utf-8 -*-
import scrapy
from dataintegration.items import HotelItem

class BookingSpider(scrapy.Spider):
    name = 'booking'
    start_urls = ['https://www.booking.com/searchresults.vi.html?label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAIDuALy6YXlBcACAQ&lang=vi&sid=a609978e73b2bd1bad339faf8275158c&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAIDuALy6YXlBcACAQ%3Bsid%3Da609978e73b2bd1bad339faf8275158c%3Btmpl%3Dsearchresults%3Bac_click_type%3Db%3Bac_position%3D0%3Bcheckin_month%3D4%3Bcheckin_monthday%3D6%3Bcheckin_year%3D2019%3Bcheckout_month%3D4%3Bcheckout_monthday%3D7%3Bcheckout_year%3D2019%3Bclass_interval%3D1%3Bdest_id%3D230%3Bdest_type%3Dcountry%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcountry%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dindex%3Bsrc_elem%3Dsb%3Bsrpvid%3Dc8ad109af400006b%3Bss%3DVi%25E1%25BB%2587t%2520Nam%3Bss_all%3D0%3Bss_raw%3Dviet%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ss=Hu%E1%BA%BF%2C+Th%E1%BB%ABa+Thi%C3%AAn+-+Hu%E1%BA%BF%2C+Vi%E1%BB%87t+Nam&is_ski_area=&ssne=Vi%C3%AA%CC%A3t+Nam&ssne_untouched=Vi%C3%AA%CC%A3t+Nam&checkin_year=2019&checkin_month=4&checkin_monthday=6&checkout_year=2019&checkout_month=4&checkout_monthday=7&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=hu%E1%BA%BF+&ac_position=0&ac_langcode=vi&ac_click_type=b&dest_id=-3715887&dest_type=city&iata=HUI&place_id_lat=16.463661&place_id_lon=107.590012&search_pageview_id=c8ad109af400006b&search_selected=true&search_pageview_id=c8ad109af400006b&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0']

    def parse(self, response):
        for row in response.css('div.sr_item.sr_item_new'):
            item = HotelItem()
            item['name'] = row.css('span.sr-hotel__name::text').get().strip()
            link = row.css('a.hotel_name_link.url::attr(href)').get().strip()
            item['link'] = link
            item['rating'] = row.css('::attr(data-score)').get().strip()
            response.follow(link, callback=self.parse_detail)
            yield item
    def parse_detail(self, response):
        pass