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


    start_urls = ['https://www.booking.com/searchresults.vi.html?aid=398480&label=metatrivago-hotel-426918_xqdz-66a478a6363b883e5fe2a7108e907955_los-1_nrm-1_gstadt-2_gstkid-0_curr-vnd_lang-vi_itt-0_trvlp-a_losb-losb1_bw-17_bwb-bwb15_trvbm-a_split-00000a_defdate-0&lang=vi&sid=a609978e73b2bd1bad339faf8275158c&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D398480%3Blabel%3Dmetatrivago-hotel-426918_xqdz-66a478a6363b883e5fe2a7108e907955_los-1_nrm-1_gstadt-2_gstkid-0_curr-vnd_lang-vi_itt-0_trvlp-a_losb-losb1_bw-17_bwb-bwb15_trvbm-a_split-00000a_defdate-0%3Bsid%3Da609978e73b2bd1bad339faf8275158c%3Btmpl%3Dsearchresults%3Bac_click_type%3Db%3Bac_position%3D0%3Bcheckin_month%3D5%3Bcheckin_monthday%3D23%3Bcheckin_year%3D2019%3Bcheckout_month%3D5%3Bcheckout_monthday%3D24%3Bcheckout_year%3D2019%3Bcity%3D-3733750%3Bclass_interval%3D1%3Bdest_id%3D-3712045%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Bhighlighted_hotels%3D426918%3Biata%3DDLI%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bsrpvid%3Def07665f19ec00e8%3Bss%3D%25C4%2590%25C3%25A0%2520L%25E1%25BA%25A1t%252C%2520L%25C3%25A2m%2520%25C4%2590%25E1%25BB%2593ng%252C%2520Vi%25E1%25BB%2587t%2520Nam%3Bss_all%3D0%3Bss_raw%3D%25C4%2590%25C3%25A0%2520l%25E1%25BA%25A1t%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3DVu%25CC%2583ng%2520Ta%25CC%2580u%3Bssne_untouched%3DVu%25CC%2583ng%2520Ta%25CC%2580u%26%3B&highlighted_hotels=426918&ss=%C4%90%C3%A0+N%E1%BA%B5ng%2C+Th%C3%A0nh+ph%E1%BB%91+%C4%90%C3%A0+N%E1%BA%B5ng%2C+Vi%E1%BB%87t+Nam&is_ski_area=&ssne=%C4%90%C3%A0+L%E1%BA%A1t&ssne_untouched=%C4%90%C3%A0+L%E1%BA%A1t&city=-3712045&checkin_year=2019&checkin_month=5&checkin_monthday=23&checkout_year=2019&checkout_month=5&checkout_monthday=24&group_adults=2&group_children=0&no_rooms=1&from_sf=1&search_pageview_id=ef07665f19ec00e8&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0&ac_position=1&ac_langcode=vi&ac_click_type=b&dest_id=-3712125&dest_type=city&iata=DAD&place_id_lat=16.068366&place_id_lon=108.219195&search_pageview_id=ef07665f19ec00e8&search_selected=true&ss_raw=%C4%90%C3%A0+',
                'https://www.booking.com/searchresults.vi.html?aid=398480&label=metatrivago-hotel-426918_xqdz-66a478a6363b883e5fe2a7108e907955_los-1_nrm-1_gstadt-2_gstkid-0_curr-vnd_lang-vi_itt-0_trvlp-a_losb-losb1_bw-17_bwb-bwb15_trvbm-a_split-00000a_defdate-0&lang=vi&sid=d329c175be2f8d73877c0ecc3395ca01&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D398480%3Blabel%3Dmetatrivago-hotel-426918_xqdz-66a478a6363b883e5fe2a7108e907955_los-1_nrm-1_gstadt-2_gstkid-0_curr-vnd_lang-vi_itt-0_trvlp-a_losb-losb1_bw-17_bwb-bwb15_trvbm-a_split-00000a_defdate-0%3Bsid%3Dd329c175be2f8d73877c0ecc3395ca01%3Btmpl%3Dsearchresults%3Bcheckin%3D2019-05-23%3Bcheckout%3D2019-05-24%3Bcity%3D-3714993%3Bclass_interval%3D1%3Bdest_id%3D-3714993%3Bdest_type%3Dcity%3Bgroup_adults%3D2%3Bhighlighted_hotels%3D426918%3Bhlrd%3Dwith_av%3Bitt%3D0%3Blabel_click%3Dundef%3Boffset%3D20%3Braw_dest_type%3Dcity%3Bredirected%3D1%3Broom1%3DA%252CA%3Brows%3D20%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsr_show_room%3D42691803_135071140_0_1_0%3Bsrpvid%3D7f6b670e3f050072%3Bssb%3Dempty%3Btrv_curr%3DVND%3Btrv_dp%3D591500%26%3B&highlighted_hotels=426918&ss=V%C5%A9ng+T%C3%A0u%2C+B%C3%A0+R%E1%BB%8Ba+-+V%C5%A9ng+T%C3%A0u%2C+Vi%E1%BB%87t+Nam&is_ski_area=&ssne=Ha%CC%80+N%C3%B4%CC%A3i&ssne_untouched=Ha%CC%80+N%C3%B4%CC%A3i&city=-3714993&checkin_year=2019&checkin_month=5&checkin_monthday=23&checkout_year=2019&checkout_month=5&checkout_monthday=24&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=v%C5%A9ng+t%C3%A0u&ac_position=0&ac_langcode=vi&ac_click_type=b&dest_id=-3733750&dest_type=city&place_id_lat=10.347682&place_id_lon=107.084427&search_pageview_id=7f6b670e3f050072&search_selected=true&search_pageview_id=7f6b670e3f050072&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                'https://www.booking.com/searchresults.vi.html?aid=398480&label=metatrivago-hotel-426918_xqdz-66a478a6363b883e5fe2a7108e907955_los-1_nrm-1_gstadt-2_gstkid-0_curr-vnd_lang-vi_itt-0_trvlp-a_losb-losb1_bw-17_bwb-bwb15_trvbm-a_split-00000a_defdate-0&lang=vi&sid=d329c175be2f8d73877c0ecc3395ca01&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D398480%3Blabel%3Dmetatrivago-hotel-426918_xqdz-66a478a6363b883e5fe2a7108e907955_los-1_nrm-1_gstadt-2_gstkid-0_curr-vnd_lang-vi_itt-0_trvlp-a_losb-losb1_bw-17_bwb-bwb15_trvbm-a_split-00000a_defdate-0%3Bsid%3Dd329c175be2f8d73877c0ecc3395ca01%3Btmpl%3Dsearchresults%3Bac_click_type%3Db%3Bac_position%3D0%3Bcheckin_month%3D5%3Bcheckin_monthday%3D23%3Bcheckin_year%3D2019%3Bcheckout_month%3D5%3Bcheckout_monthday%3D24%3Bcheckout_year%3D2019%3Bcity%3D-3714993%3Bclass_interval%3D1%3Bdest_id%3D-3733750%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Bhighlighted_hotels%3D426918%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bsrpvid%3D0ff56dd3212f023a%3Bss%3DV%25C5%25A9ng%2520T%25C3%25A0u%252C%2520B%25C3%25A0%2520R%25E1%25BB%258Ba%2520-%2520V%25C5%25A9ng%2520T%25C3%25A0u%252C%2520Vi%25E1%25BB%2587t%2520Nam%3Bss_all%3D0%3Bss_raw%3Dv%25C5%25A9ng%2520t%25C3%25A0u%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3DHa%25CC%2580%2520N%25C3%25B4%25CC%25A3i%3Bssne_untouched%3DHa%25CC%2580%2520N%25C3%25B4%25CC%25A3i%26%3B&highlighted_hotels=426918&ss=%C4%90%C3%A0+L%E1%BA%A1t%2C+L%C3%A2m+%C4%90%E1%BB%93ng%2C+Vi%E1%BB%87t+Nam&is_ski_area=&ssne=Vu%CC%83ng+Ta%CC%80u&ssne_untouched=Vu%CC%83ng+Ta%CC%80u&city=-3733750&checkin_year=2019&checkin_month=5&checkin_monthday=23&checkout_year=2019&checkout_month=5&checkout_monthday=24&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=%C4%90%C3%A0+l%E1%BA%A1t&ac_position=0&ac_langcode=vi&ac_click_type=b&dest_id=-3712045&dest_type=city&iata=DLI&place_id_lat=11.94266&place_id_lon=108.436908&search_pageview_id=0ff56dd3212f023a&search_selected=true&search_pageview_id=0ff56dd3212f023a&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0']

    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
     
    def parse(self, response):
        for row in response.css('div.sr_item.sr_item_new'):
            link = row.css('a.hotel_name_link.url::attr(href)').get().strip()
            if not row.css('div.sr--soldout-content'):    
                hotel = HotelItem()
                hotel['link'] = response.urljoin(link)
                hotel['destination'] = 'Booking.com'
                hotel['name'] = row.css('a.hotel_name_link span.sr-hotel__name::text').get(default='').strip()
                hotel['rating'] = row.css('div.bui-review-score__badge::text').get(default='').strip()
                #hotel['address'] = row.css('a.bui-link::text').getall()[0].strip()
                hotel['benefits'] = row.css('sup.sr_room_reinforcement::text').getall()
                image_url = row.css('img.hotel_image::attr(src)').get(default='')
                hotel['image_urls'] = [image_url]

                rooms = []
                roomitem = RoomItem()
                roomitem['room_type'] = row.css('span.room_link strong::text').get(default='')
                roomitem['price_per_night'] = row.css('div.bui-price-display__value::text').get(default='').strip()
                #roomitem['price_per_night'] = row.css('strong.price.availprice b::text').get(default='').strip()
                
                if roomitem is not None :
                    rooms.append(dict(roomitem))
                hotel['rooms'] = rooms
                #yield hotel
                request =  scrapy.Request(response.urljoin(link), callback=self.parse_detail)
                request.meta['hotel'] = hotel
                yield request

        NEXT_PAGE = response.css('a.bui-pagination__link.paging-next::attr(href)').get()
        NEXT_PAGE = response.urljoin(NEXT_PAGE)
        yield response.follow(NEXT_PAGE, callback=self.parse)
    def parse_detail(self, response):
        hotel = response.meta['hotel']
        hotel['address'] = response.css('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip::text').get().strip()
        hotel['star'] = response.css('i span.invisible_spoken::text').get()
        yield hotel