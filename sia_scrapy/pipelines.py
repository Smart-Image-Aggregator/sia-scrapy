# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.parse

from sia_scrapy.storage.dropbox import Dropbox
from datetime import datetime, timedelta


class SiaScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class StoragePipeline(object):
    storage = None

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        provider = item['provider']
        user = urllib.parse.quote(item['user'])
        name = urllib.parse.quote(item['name'])
        file_ending = item['file_ending']
        self.storage.upload(f'{user}@{provider}+{name}.{file_ending}', item['data'], item['time_created'])
