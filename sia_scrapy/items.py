# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SiaScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImageItem(scrapy.Item):
    data = scrapy.Field()
    name = scrapy.Field()
    time_created = scrapy.Field()
    provider = scrapy.Field()
    user = scrapy.Field()
    file_ending = scrapy.Field()
    is_video = scrapy.Field()
