# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MegapolItem(scrapy.Item):
	url_abs = scrapy.Field()
	body = scrapy.Field()
	date = scrapy.Field()
	url_post = scrapy.Field()
