# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DestinationPipeline(object):
    def process_item(self, item, spider):
        if item.get('destination'):
            item['destination'] = str(item['destination']).replace('/','')
        return item
            