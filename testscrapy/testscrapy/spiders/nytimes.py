import logging

import scrapy
from scrapy.http import Response, TextResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from six import Iterator
from testscrapy.items import ArticleItem, TestscrapyItem


# this spider now finds every link on the cbc home page
class NyTimesSpider(CrawlSpider):
    name = 'nytimes'
    allowed_domains = ['www.nytimes.com', 'spiderbites.nytimes.com']

    start_url = 'https://spiderbites.nytimes.com'

    def start_requests(self):
        # start_url = 'https://www.nytimes.com/search?dropmab=true'
        # attrs = [
        #     'query=Climate%20Change%2CGlobal%20Warming',
        #     'sort=best',
        #     'types=article',
        #     'startDate=20000101',
        #     'endDate=20010101'
        # ]

        start_year = 2000
        end_year = 2001

        for i in range(start_year, end_year):
            url = self.start_url + '/' + str(i) + '/'
            yield scrapy.Request(url=url, callback=self.parse)

        

    def parse(self, response: TextResponse):
        hrefs = response.xpath('//div[@class="articlesMonth"]/ul/li/a/@href').getall()

        for page in hrefs:
            url =  self.start_url + page
            yield response.follow(url, self.parse_articles)

    
    def parse_articles(self, response: TextResponse):
        hrefs = response.xpath('//ul[@id="headlines"]/li/a/@href').getall()

        for article in hrefs:
            yield response.follow(article, self.parse_article)

    
    def parse_article(self, response: TextResponse):
        item = ArticleItem()

        item['headline'] = response.xpath('//hi[@itemprop="headline"]/text()').get()
        item['content'] = str.join('\n', response.xpath('//section[@itemprop="articleBody"]//p/text()').getall())

        yield item
                