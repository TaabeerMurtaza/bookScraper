# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['http://kitabosunnat.com']
    start_urls = ['http://http://kitabosunnat.com/']

    def parse(self, response):
        pass
