# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDbEnginesItem(scrapy.Item):
    # define the fields for your item here like:
    rank_href = scrapy.Field()
    rank_text = scrapy.Field()


class ScrapyDbEnginesDbmsItem(scrapy.Item):
    # define the fields for your item here like:
    rank_href = scrapy.Field()
    rank_text = scrapy.Field()
    rank = scrapy.Field()
    name_href = scrapy.Field()
    name_text = scrapy.Field()
    models = scrapy.Field()
